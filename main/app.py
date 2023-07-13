import boto3
import json
import logging

iam_client = boto3.client('iam')
user_name = 'DevMauricio' #OS.ENVIRON
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    iam_access_keys = iam_client.list_access_keys(UserName=user_name)
    metadata_iam = iam_access_keys["AccessKeyMetadata"]
    if not metadata_iam:
        msg = "%s does not have Access Keys and Secret Access keys created"
        logger.error(msg % user_name)
        raise ValueError(msg % user_name)
    if len(metadata_iam) != 2:
        msg = "%s does not have two Access Keys and Secret Access keys created"
        logger.error(msg % user_name)
        raise ValueError(msg % user_name)  
    print(metadata_iam)

    for item in metadata_iam:
        if item["Status"] == "Inactive":
            iam_client.delete_access_key(UserName=user_name,AccessKeyId=item["AccessKeyId"])
            print("entró a inactive")

    create_access_key = iam_client.create_access_key(UserName=user_name)
    credentials = {
        'AccessKeyId': create_access_key['AccessKey']['AccessKeyId'],
        'SecretAccessKey': create_access_key['AccessKey']['SecretAccessKey']
    }
    
    iam_access_keys = iam_client.list_access_keys(UserName=user_name)
    metadata_iam = iam_access_keys["AccessKeyMetadata"]
    
    if metadata_iam[0]["CreateDate"] > metadata_iam[1]["CreateDate"]:
        iam_client.update_access_key(UserName=user_name, AccessKeyId=metadata_iam[1]["AccessKeyId"], Status='Inactive')
    else:
        iam_client.update_access_key(UserName=user_name, AccessKeyId=metadata_iam[0]["AccessKeyId"], Status='Inactive')
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
        }),
    }