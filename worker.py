print "Responde"
import boto3
from botocore.client import Config
import aws.QSQConfig
import aws.S3_Config
#from aws.CloudFront_Config import *
#from aws.QSQConfig import *
import os
from email.mime.text import MIMEText
from smtplib import SMTP
import smtplib
from time import time

sqs = boto3.resource(
    aws.QSQConfig.QUEUE,
    aws_access_key_id=aws.QSQConfig.QUEUE_ACCESS_KEY,
    aws_secret_access_key=aws.QSQConfig.QUEUE_SECRET_ACCESS,
    region_name=aws.QSQConfig.QUEUE_REGION_NAME
)

s3 = boto3.resource(
    's3',
    aws_access_key_id = aws.S3_Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key = aws.S3_Config.AWS_SECRET_ACCESS_KEY,
    config = Config(signature_version='s3v4')
)
dynamodb = boto3.resource('dynamodb', region_name='us-east-2', aws_access_key_id='AKIAIGNQ6QGQCSAOMINA',
                          aws_secret_access_key='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')
videos_table = dynamodb.Table('videos')
bucket = s3.Bucket(aws.S3_Config.AWS_STORAGE_BUCKET_NAME)
##print aws.S3_Config.AWS_S3_CUSTOM_DOMAIN
##for obj in bucket.objects.all():
##    print(obj)

EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_HOST_USER = 'AKIAIQZGD2J6YKE5DJ6A'
EMAIL_HOST_PASSWORD = 'Arq0NZ8C2aJ+3CG/M5JsAJucxLrQs+jtpssH2gOrB2By'
EMAIL_PORT = 587

#Usando cola existente
tiempo_inicial = time()
contador = 0

queue = sqs.get_queue_by_name(QueueName='QueueVideo.fifo')
for message in queue.receive_messages(MessageAttributeNames=[
        'All',
    ]):
    path = message.message_attributes.get('path').get('StringValue')
    idVideo = message.message_attributes.get('idVideo').get('StringValue')
    idCompetition= message.message_attributes.get('idCompetition').get('StringValue')
    email = message.message_attributes.get('email').get('StringValue')
    nameFile =path[23:]
    name,extension = nameFile.split('.')
    pathFile = 'media/videos/converted/'+name+'.mp4'
    print  "name  "+name+" namefile "+nameFile+"\n"
    print "  path "+path+" idVideo  "+idVideo+" idCompetition "+idCompetition+" email "+email+"\n"
    print " cuepo "+message.body
    bucket.download_file(path, './tmp/'+nameFile) ;
    os.system("ffmpeg -i " + './tmp/'+nameFile+ " " +'./conv/'+name+'.mp4')
    bucket.put_object(
       ACL='public-read',  # TODO Revisar
       Key=pathFile,
       Body='./conv/'+name+'.mp4'
    )

    response = videos_table.update_item(
        Key={
            'guidCompetition': idCompetition,
            'guidVideo': idVideo
        },
        UpdateExpression='SET pathConverted = :pc, videoState = :st',
        ExpressionAttributeValues={
            ':pc': pathFile,
            ':st': '1'
        }
    )

    ######ENVIO MENSAJE #################
    destinatarios = ["Usuario  <" + email + ">"]
    emisor = "grupo2cloud@gmail.com"
    receptor = destinatarios

    # Configuracion del mail
    html = "<th>Estado Publicacion Video </th>"
    html += "<table>"
    html += "<tr><td><font color='red'> Apreciado usuario " + email + " :</font> </td></tr>"
    html += "<tr><td><font color='blue'> El video Ya se encuentra publicado <br></font></td></tr>"
    html += "<tr><td><b><font color='red'>Grupo 2 Cloud Computer 201702 </font><b></td></tr>"
    html += "</table>"
    mensaje = MIMEText(html, 'html')
    mensaje['From'] = emisor
    mensaje['To'] = ', '.join(receptor)
    mensaje['Subject'] = "Notificacion Publicacion  Video " + email
    # Nos conectamos al servidor SMTP de Gmail
    serverSMTP = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    # serverSMTP.ehlo()
    serverSMTP.starttls()
    # serverSMTP.ehlo()
    serverSMTP.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    serverSMTP.sendmail(emisor, receptor, mensaje.as_string())

    ## boorro temporales :
    os.system("rm " + './tmp/' + nameFile)
    os.system("rm "+ './conv/' + name + '.mp4')
    contador = contador + 1
    message.delete()
    print ("********** video" + str(contador) + "**********")

tiempo_final = time()
tiempo_ejecucion = tiempo_final - tiempo_inicial
print ("**********   numero de videos "+str(contador)+" tiempo "+str(tiempo_ejecucion))
