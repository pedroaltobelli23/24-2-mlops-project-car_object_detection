# Bash scripts

In this project, three bash scripts were used to automate processes:

### configure_dvc.sh

```{code} bash
#!/bin/bash

# Remove DVC files
rm -rf .dvc/ data/data.zip.dvc .dvcignore

BUCKET_NAME=$1

if [ -z "$BUCKET_NAME" ]; then
    echo "Error: BUCKET_NAME parameter is missing."
    echo "Usage: $0 <bucket_name>"
    exit 1
fi

# Init dvc versioning
dvc init

dvc add data/data.zip

git add data/data.zip.dvc 

git commit -m "Add data to project"

git push

# Add connection to the S3 bucket
dvc remote add -f myremote s3://"$BUCKET_NAME"

dvc remote default myremote

dvc push

git add .

git commit -m "version 0"

git push

# Create first tag and send it to remote
git tag -a v0.0.0 -m "Release version 0.0.0"

git push origin tag v0.0.0
```

### data.sh

```{code} Bash
#!/bin/bash

set -e

DROP=$1

if [ -z "$DROP" ]; then
    echo "Error: DROP parameter is missing. See data/preprocess.py for more."
    echo "Usage: $0 <drop_value>"
    exit 1
fi

# Download data and Drop images and respective labels of the full folder
python3 data/dataset.py --drop $DROP --download_data

zip -r data/data.zip data/data/

rm -r data/data/
```

### new_dataset_version.sh

```{code} Bash
#!/bin/bash

set -e 

VERSION=$1

echo "Commit data/data.zip and push to the bucket"
dvc commit data/data.zip
dvc push

echo "commit to github"
git add .
git commit -m "version $VERSION"
git push

git tag -a $VERSION -m "Release version $VERSION"
echo "Tag created"

echo "pushing to github..."
git push origin tag $VERSION
echo "Push complete!"
```

# YML script

### workflow.yml
```{code} yaml
name: API Endpoint deploy with AWS lambda function inside ECR
on:
  push:
    branches:
      - main
jobs:
    Amazon-ECR-Image:
        runs-on: ubuntu-latest
        env:
            AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
            AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
            AWS_REGION: ${{ secrets.AWS_REGION }}
        steps:
            - name: Checkout code
              uses: actions/checkout@v4

            - name: Configure AWS credentials
              uses: aws-actions/configure-aws-credentials@v4
              with:
                aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
                aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
                aws-region: ${{ secrets.AWS_REGION }}
            
            - name: Create ECR repository
              run: |
                aws ecr describe-repositories --repository-names "${{ secrets.ECR_NAME }}" > /dev/null 2>&1 || \
                aws ecr create-repository --repository-name "${{ secrets.ECR_NAME }}" --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE --query 'repository.{repositoryArn:repositoryArn, repositoryUri:repositoryUri}'
              
            - name: Login to Amazon ECR
              id: login-ecr
              uses: aws-actions/amazon-ecr-login@v2
              with:
                mask-password: 'true'

            - name: Build, tag, and push image to Amazon ECR
              env:
                ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
                ECR_REPOSITORY: ${{ secrets.ECR_NAME }}
                IMAGE_TAG: latest
              run: |
                docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG --platform linux/amd64 -f deploy/Dockerfile .
                docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG  
    Create-API-Endpoint:
        runs-on: ubuntu-latest
        needs: Amazon-ECR-Image
        env:
            AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
            AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
            AWS_REGION: ${{ secrets.AWS_REGION }}
            AWS_LAMBDA_ROLE_ARN: ${{ secrets.AWS_LAMBDA_ROLE_ARN }}
            BUCKET_MODEL: ${{secrets.BUCKET_MODEL}}
        outputs:
          api_endpoint: ${{steps.create_endpoint.outputs.api_endpoint}}
        steps:
          - name: Checkout code
            uses: actions/checkout@v4

          - name: Set up Python
            uses: actions/setup-python@v5
            with:
              python-version: '3.12'

          - name: Install dependencies
            run: pip install -r deploy/requirements/create_lambda_requirements.txt

          - name: Create Endpoint
            id: create_endpoint
            run: |
              endpoint=$(python deploy/deploy_API.py --image_uri ${{secrets.AWS_ACCOUNT_ID}}.dkr.ecr.${{secrets.AWS_REGION}}.amazonaws.com/${{secrets.ECR_NAME}}:latest --api_gateway demo_project_pedroatp)
              echo "api_endpoint=$endpoint" >> "$GITHUB_OUTPUT"
          
          - name: Sleep for 30 seconds
            run: sleep 30s
            shell: bash
    Run-Tests:
      runs-on: ubuntu-latest
      needs: Create-API-Endpoint
      env:
            ENDPOINT: ${{needs.Create-API-Endpoint.outputs.api_endpoint}}
            AWS_REGION: ${{ secrets.AWS_REGION }}
      steps:
        - name: Checkout code
          uses: actions/checkout@v4

        - name: Set up Python
          uses: actions/setup-python@v5
          with:
            python-version: '3.12'

        - name: Install dependencies
          run: pip install -r tests/requirements.txt

        - name: Run pytest
          run: pytest tests/test_predict.py
    Deploy-Heroku-Webpage:
      runs-on: ubuntu-22.04
      needs: [Create-API-Endpoint, Run-Tests]
      steps:
        - uses: actions/checkout@v4
        - uses: akhileshns/heroku-deploy@v3.13.15
          with:
            heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
            heroku_app_name: ${{ vars.HEROKU_APP_NAME }}
            heroku_email: ${{ vars.HEROKU_EMAIL }}
            appdir: "app"
          env:
            HD_ENDPOINT: ${{ needs.Create-API-Endpoint.outputs.api_endpoint }}
            HD_AWS_REGION: ${{ secrets.AWS_REGION }}
    deploy-docs:
      runs-on: ubuntu-latest
      permissions:
        contents: write
      steps:
        - uses: actions/checkout@v4

        - name: Setup Python
          uses: actions/setup-python@v5
          with:
            python-version: '3.12'

        - name: Upgrade pip
          run: python -m pip install --upgrade pip

        - name: Get pip cache dir
          id: pip-cache
          run: echo "dir=$(pip cache dir)" >> $GITHUB_OUTPUT

        - name: Cache dependencies
          uses: actions/cache@v4
          with:
            path: ${{ steps.pip-cache.outputs.dir }}
            key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
            restore-keys: |
              ${{ runner.os }}-pip-

        - name: Install dependencies
          run: python -m pip install -r ./requirements.txt

        - name: Build documentation
          working-directory: ./docs
          run: make html

        - name: Deploy
          uses: peaceiris/actions-gh-pages@v4
          if: github.ref == 'refs/heads/main'
          with:
            github_token: ${{ secrets.GITHUB_TOKEN }}
            publish_dir: ./docs/_build/html
```