import datetime
from aws.CloudFront_Config import *

# The AWS region to connect to.
AWS_REGION = "us-east-2"
AWS_ACCESS_KEY_ID = 'AKIAINXOLWXQQ7J4WU6Q'
AWS_SECRET_ACCESS_KEY = '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'
AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = True


AWS_STORAGE_BUCKET_NAME = 'miso-smarttools'
S3DIRECT_REGION = 'us-east-2'
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
#MEDIA_ROOT = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL ='media/'
#STATIC_URL = S3_URL + 'static/'
#STATIC_ROOT = AWS_CLOUDFRONT_DOMAINNAME
STATIC_URL = 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

#AWS_S3_CUSTOM_DOMAIN = '%s.s3.us-east-2.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_CUSTOM_DOMAIN = AWS_CLOUDFRONT_DOMAINNAME

DEFAULT_FILE_STORAGE = 'smartTools.aws.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'smartTools.aws.utils.StaticRootS3BotoStorage'
#DEFAULT_FILE_STORAGE = AWS_CLOUDFRONT_DOMAINNAME + "/" + MEDIA_URL
#STATICFILES_STORAGE = AWS_CLOUDFRONT_DOMAINNAME + "/" + STATIC_URL

#AWS_S3_SECURE_URLS = False

# two_months = datetime.timedelta(days=61)
# date_two_months_later = datetime.date.today() + two_months
# expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")
#
# AWS_HEADERS = {
#      'Expires': expires,
#      'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
#  }