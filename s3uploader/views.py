# myapp/views.py

import uuid
import boto3
from botocore.exceptions import NoCredentialsError
from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
from django.http import JsonResponse
import mimetypes
from datetime import datetime, timedelta
import time

def welcome(request):
   return HttpResponse("Hello world")


def my_view(request):
    remote_url = str(request.GET.get("remote_url"))
    bucket = 'textract-dataholder'
    file_name = str(uuid.uuid4())
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID , aws_secret_access_key=SECRET_ACCESS_KEY)
    try:
        imageResponse = requests.get(remote_url, stream=True).raw
        content_type = imageResponse.headers['content-type']
        extension = mimetypes.guess_extension(content_type)
        s3.upload_fileobj(imageResponse, bucket, file_name + extension)
        return HttpResponse(my_results(request))
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


def my_results(request):

    client = boto3.client('logs', aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    region_name='us-east-1')

    log_query = "fields @timestamp, @message | sort @timestamp desc| filter @type != 'START'| filter @type != 'END'| filter @type != 'REPORT'| filter Blocks.0.BlockType != 'PAGE'| limit 10"

    log_group = '/aws/lambda/textract-lambda'
    start_query_response = client.start_query(
        logGroupName=log_group,
        startTime=int((datetime.today() - timedelta(hours=24)).timestamp()),
        endTime=int(datetime.now().timestamp()),
        queryString=log_query,
    )

    query_id = start_query_response['queryId']

    response = None

    while response == None or response['status'] == 'Running':
        time.sleep(1)
        response = client.get_query_results(
            queryId=query_id
        )
    result_text = ""
    events = response['results']  # ['events']
    with open('logs.json', 'w') as file:
        for obj in events[0]:
            if obj["field"] == "@message":
                file.write(obj["value"])
                result_text += obj["value"]

    return HttpResponse(result_text)