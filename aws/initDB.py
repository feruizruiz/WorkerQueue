import dynamodbConfig
import boto3

dynamodb=boto3.resource(dynamodbConfig.DYNAMO_RESOURCE,
                          region_name=dynamodbConfig.REGION_NAME,
                          aws_access_key_id=dynamodbConfig.USER_ID_DYNAMODB,
                          aws_secret_access_key=dynamodbConfig.SECRET_ACCESS_KEY_DYNAMODB)


table = dynamodb.create_table(
    TableName=dynamodbConfig.COMPETITIONS,
   KeySchema=[
       {
           'AttributeName': dynamodbConfig.ADMIN_USER_ATTR,
           'KeyType': 'HASH'  #Partition key
       },
       {
           'AttributeName': dynamodbConfig.GUID_COMPETITION_ATTR,
           'KeyType': 'RANGE'  #Sort key
       }
   ],
   AttributeDefinitions=[
       {
           'AttributeName': dynamodbConfig.ADMIN_USER_ATTR,
           'AttributeType': 'S' #string
      },
        {
           'AttributeName': dynamodbConfig.GUID_COMPETITION_ATTR,
           'AttributeType': 'S' #string
       }
   ],
   ProvisionedThroughput={
       'ReadCapacityUnits': 10,
       'WriteCapacityUnits': 10
   }
)

table = dynamodb.create_table(
    TableName=dynamodbConfig.VIDEOS,
    KeySchema=[
        {
            'AttributeName': dynamodbConfig.GUID_COMPETITION_ATTR,
            'KeyType': 'HASH'  # Partition key
        },
        {
            'AttributeName': dynamodbConfig.GUID_VIDEO_ATTR,
            'KeyType': 'RANGE'  # Sort key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': dynamodbConfig.GUID_COMPETITION_ATTR,
            'AttributeType': 'S'  # string
        },
        {
            'AttributeName': dynamodbConfig.GUID_VIDEO_ATTR,
            'AttributeType': 'S'  # string
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)
