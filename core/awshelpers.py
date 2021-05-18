import boto3
import base64
import re

#Get secrets from secrets manager
def get_secret_value(name, version=None):
    secrets_client = boto3.client("secretsmanager")
    kwargs = {'SecretId': name}
    if version is not None:
        kwargs['VersionStage'] = version
    response = secrets_client.get_secret_value(**kwargs)
    secret_string = response['SecretString']
    secret_value_unstripped = secret_string.split(':')[1]
    secret_value = re.sub('"|}','',secret_value_unstripped)

    return secret_value

def write_to_s3(s3_bucket, local_file_path, s3_file_path, file_name):
	s3 = boto3.resource('s3')   
	s3.Bucket(s3_bucket).upload_file(local_file_path,s3_file_path+file_name)
