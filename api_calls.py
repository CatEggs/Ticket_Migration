import json
import requests
from requests.auth import HTTPBasicAuth
#import boto3
#import botocore
import wget

def get_request(url,auth_data,payload):
    r = requests.get(url, params=payload, auth = auth_data)

    if r.status_code == 200:
        #print("Request completed successfully")
        response = json.loads(r.content)
        return response
    else:
        #print("Failed to create ticket, errors are displayed below,")
        #response = json.loads(r.content)
        #errors = response["errors"]
        #print(errors +"\n"+ "Status Code : " + str(r.status_code) )
        return None

def create_ticket(yrl, auth_data, payload):
    #url = 
    headers = { 'Content-Type' : 'application/json' }

    r = requests.post(url, auth = auth_data , headers = headers, data = json.dumps(payload))

    if r.status_code == 201:
        return r.content
        #print("Location Header : " + r.headers['Location'])
    else:
        #print "Failed to create ticket, errors are displayed below,"
        response = json.loads(r.content)
        print(response["errors"])

        #print "x-request-id : " + r.headers['x-request-id']
        return("Status Code : " + str(r.status_code)) 

def download_attachment(file_url):
    
    folder_path = r'C:\Users\Cathy\Desktop\PythonProjects\Import_to_Jitbit\fd_attachments'
    for url in file_url:
        wget.download(url, folder_path)
    # BUCKET_NAME = 'my-bucket' # replace with your bucket name
    # KEY = 'my_image_in_s3.jpg' # replace with your object key

    # s3 = boto3.resource('s3')

    # try:
    #     s3.Bucket(BUCKET_NAME).download_file(KEY, 'my_local_image.jpg')
    # except botocore.exceptions.ClientError as e:
    #     if e.response['Error']['Code'] == "404":
    #         print("The object does not exist.")
    #     else:
    #         raise

#def update_ticket()
            