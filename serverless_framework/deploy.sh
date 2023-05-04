#!/bin/bash

# dicフォルダ配下をS3にアップロード
echo "dicフォルダ配下をS3にアップロード"
cd /home/user/project1-back-deploy/project1-back/serverless_framework/tools/dic_s3_uploader/
python dic_s3_uploader.py

# lambda layer作成
echo "lambda layer作成"
cd /home/user/project1-back-deploy/project1-back/serverless_framework/tools/layer_zip_creator
python layer_zip_creator.py

# serverless deploy
echo "serverless deploy"
cd /home/user/project1-back-deploy/project1-back/serverless_framework
sls deploy --stage dev
