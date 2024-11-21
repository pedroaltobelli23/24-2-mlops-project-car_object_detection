.. Car Detection Mlops documentation master file, created by
   sphinx-quickstart on Wed Nov  6 20:46:05 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Car Detection Mlops's documentation!
===============================================

Deploy a full Mlops Object detection Web application that detects cars and motobikes!

Features:

- Download and preprocess the `Stanford Cars Dataset`_.
- Data versioning with `DVC`_.
- Train model with `YOLO`_ and export in `ONNX`_ format.
- `AWS API Gateway`_ is created using an `AWS Lambda function`_ inside an `AWS ECR`_ that make predictions using the trained model.
- AWS S3 Bucket used for storing Dataset versions and the model that will be used by the Lambda function.
- Documentation created using `Sphinx`_ and deployed using `Github Pages`_.
- Web Application deployed using `Heroku`_.
- Automated pipeline to deploy all the infrastructure to production using `Github Actions`_.
- Local logging and also `CloudWatch`_ logging (for the lambda function).

.. _Stanford Cars Dataset: https://universe.roboflow.com/openglpro/stanford_car/dataset/10
.. _Heroku: https://www.heroku.com/platform
.. _AWS ECR: https://aws.amazon.com/en/ecr/
.. _AWS API Gateway: https://aws.amazon.com/en/api-gateway/
.. _AWS Lambda function: https://docs.aws.amazon.com/lambda/latest/dg/welcome.html
.. _YOLO: https://docs.ultralytics.com/
.. _DVC: https://dvc.org/
.. _Sphinx: https://www.sphinx-doc.org/en/master/ 
.. _CloudWatch: https://aws.amazon.com/pt/cloudwatch/
.. _Github Actions: https://github.com/features/actions
.. _Github Pages: https://pages.github.com/
.. _ONNX: https://onnx.ai/
.. _Onnxruntime: https://onnxruntime.ai/

.. toctree::
   :maxdepth: 4
   :caption: Tutorial:

   tutorial_startup

   tutorial_data_versioning

   tutorial_training
   
   tutorial_deploy

.. toctree::
   :maxdepth: 4
   :caption: Modules:

   train.rst

   predict.rst

   dataset.rst

   s3_bucket.rst

   lambda_function.rst

   deploy_API.rst

   see_logs_lambda.rst

.. toctree::
   :maxdepth: 4
   :caption: Scripts:

   scripts
   
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
