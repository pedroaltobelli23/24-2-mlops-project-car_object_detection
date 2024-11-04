# What github actions have to do?

1. Create ECR:

2. build, tag and push docker image to ECR:

in github actions
```Bash
- name: Build Docker Image
      run: docker build -t my-lambda .

- name: Tag Docker Image
    run: docker tag my-lambda:latest ${{ steps.login-ecr.outputs.registry }}/my-lambda:latest

- name: Push Docker Image to ECR
    run: docker push ${{ steps.login-ecr.outputs.registry }}/my-lambda:latest

```