# -*- coding: utf-8 -*-
from storages.backends.s3boto3 import S3Boto3Storage
from botocore.client import Config
from aws import S3_Config, CloudFront_Config
import boto3

StaticRootS3BotoStorage = lambda: S3Boto3Storage(location='static') #TODO Funciona para S3
MediaRootS3BotoStorage = lambda: S3Boto3Storage(location='media') #TODO Funciona para S3


#Conexión S3 - Boto3
s3 = boto3.resource(
    's3',
    aws_access_key_id = S3_Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key = S3_Config.AWS_SECRET_ACCESS_KEY,
    config = Config(signature_version='s3v4')
)
#Obteniendo bucket.
bucket = s3.Bucket(S3_Config.AWS_STORAGE_BUCKET_NAME)

#Conexión Cloud Front
#clientCloudFront = boto3.client('cloudfront')

#Metodo encargado de subir archivos al bucket.
def upload_file(pathFile, data):
    bucket.put_object(
        ACL='public-read', #TODO Revisar
        Key=pathFile,
        Body=data
    )


#Metodo encargado de eliminar un archivo en el bucket.
def delete_file(pathFile):
    s3.Object(S3_Config.AWS_STORAGE_BUCKET_NAME, pathFile).delete()


#Metodo encargado de crear una copia del archivo con el nuevo nombre.
def update_name_file(pathOld, newName):
    _, oldFileName = pathOld.rsplit("https://" + S3_Config.AWS_S3_CUSTOM_DOMAIN + "/", 1);
    original_path, old_name = oldFileName.rsplit('/', 1)
    _, original_extension = oldFileName.rsplit('.', 1)
    newName = (newName + "." + original_extension)
    s3.Object(S3_Config.AWS_STORAGE_BUCKET_NAME, original_path + "/" + newName).copy_from(CopySource= S3_Config.AWS_STORAGE_BUCKET_NAME + "/" + oldFileName, ACL='public-read')
    delete_file(oldFileName)

    return "https://" + S3_Config.AWS_S3_CUSTOM_DOMAIN + "/" + original_path + "/" + newName