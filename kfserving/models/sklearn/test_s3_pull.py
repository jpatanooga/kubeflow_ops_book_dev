#from google.api_core.protobuf_helpers import get_messages
#from google.cloud
import glob
import logging
import tempfile
import os
import re
from urllib.parse import urlparse

from minio import Minio
from minio.error import ResponseError


_GCS_PREFIX = "gs://"
_S3_PREFIX = "s3://"
_BLOB_RE = "https://(.+?).blob.core.windows.net/(.+)"
_LOCAL_PREFIX = "file://"


#from minio import Minio

"""
download_s3(uri, temp_dir: str):
        client = Storage._create_minio_client()
        bucket_args = uri.replace(_S3_PREFIX, "", 1).split("/", 1)
        bucket_name = bucket_args[0]
        bucket_path = bucket_args[1] if len(bucket_args) > 1 else ""
        objects = client.list_objects(bucket_name, prefix=bucket_path, recursive=True)
        count = 0
        for obj in objects:
            # Replace any prefix from the object key with temp_dir
            subdir_object_key = obj.object_name.replace(bucket_path, "", 1).strip("/")
            # fget_object handles directory creation if does not exist
            if not obj.is_dir:
                if subdir_object_key == "":
                    subdir_object_key = obj.object_name
                client.fget_object(bucket_name, obj.object_name,
                                   os.path.join(temp_dir, subdir_object_key))
            count = count + 1
        if count == 0:
            raise RuntimeError("Failed to fetch model. \
The path or model %s does not exist." % (uri))
"""

client = Minio('s3.amazonaws.com', access_key='AKIAJFFDI3UU6OO6SH2A', secret_key='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', secure=False)

strs3URI = "s3://mnist/v1/export" #"s3://pattersonconsulting/kubeflow/kfserving/models/sklearn" #"s3://mnist/v1/export"
bucket_args = strs3URI.replace(_S3_PREFIX, "", 1).split("/", 1)

temp_dir = "/tmp/"

print( bucket_args)

bucket_name = bucket_args[0]
bucket_path = bucket_args[1] if len(bucket_args) > 1 else ""

print( bucket_name )
print( bucket_path )


objects = client.list_objects(bucket_name, prefix=bucket_path, recursive=True)
count = 0
for obj in objects:
	print( obj )

	subdir_object_key = obj.object_name.replace(bucket_path, "", 1).strip("/")
	# fget_object handles directory creation if does not exist
	if not obj.is_dir:
		if subdir_object_key == "":
			subdir_object_key = obj.object_name
		client.fget_object(bucket_name, obj.object_name, os.path.join(temp_dir, subdir_object_key))
	count = count + 1
if count == 0:
	raise RuntimeError("Failed to fetch model. The path or model %s does not exist." % (uri))

"""
bucket_name = bucket_args[0]


print('test')

s3_uri = "s3://pattersonconsulting/"

#Storage._download_s3(s3_url, "/tmp/s3_test/")


minioClient_private = Minio('s3.amazonaws.com', access_key='AKIAJFFDI3UU6OO6SH2A', secret_key='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', secure=False)
minioClient_public = Minio('s3.amazonaws.com', access_key='', secret_key='', secure=False)


print( minioClient_public.bucket_exists("pattersonconsulting") )

objects = minioClient_public.list_objects('pattersonconsulting', recursive=True)

	  



for obj in objects:
	print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified, obj.etag, obj.size, obj.content_type)
"""
