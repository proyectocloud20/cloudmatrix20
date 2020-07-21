#!/usr/bin/env python
# coding: utf-8
"""
Author: Ammar Okran
Date  : 03/10/2019
Email : ammar.okran@gmail.com

Description:
Classify the outlier points as noise, so it is easier to ignore them in subsequent processes.
Execute it in the IBM cloud Function.
You have to substitute "XXXXXX" with your own details.

The documentation of the pdal libery can be found in the following
address: https://pdal.io/index.html
"""

import pywren_ibm_cloud as pywren 
from pywren_ibm_cloud.utils import get_current_memory_usage
import pdal
import pandas as pd
import json
import os
import ibm_boto3
import ibm_botocore 
from ibm_botocore.client import Config
import time



# Constants for IBM COS values
cos_config = { 'bucket_name' : 'XXXXXXX',
              'api_key' : 'XXXXXXX',
              'service_endpoint' : 'XXXXXXXX'
             }



api_key = cos_config.get('api_key')
print(api_key)
auth_endpoint = cos_config.get('auth_endpoint')
service_endpoint = cos_config.get('service_endpoint')
print(service_endpoint)
cos_client = ibm_boto3.client('s3',
                              ibm_api_key_id=api_key,
                              ibm_auth_endpoint=auth_endpoint,
                              config=Config(signature_version='oauth'),
                              endpoint_url=service_endpoint)



def remove_noise(obj, ibm_cos):
    
    print("Remove noise is starting ...")
    key = obj.key
    print('I am processing the object {}'.format(key))
    print("The utilized memory befor doing anything is: {}".format(get_current_memory_usage()))
    workdir = "/tmp" 
    bucket_name = 'XXXXXX'
    path_folder = workdir + "/lidar_files/"
    res_folder = workdir + "/res_files/"
    
    #-----------------------------------------------------------------------------------

    # Create folders for files
    
    if not os.path.exists(path_folder):
        try:
            os.mkdir(path_folder)
            print("Directory " , path_folder ,  " Created ")
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        
        
    if not os.path.exists(res_folder):
        try:
            os.mkdir(res_folder)
            print("Directory " , res_folder ,  " Created ")
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    
    try:
        files = os.listdir(path_folder)
        if len(files) > 0:
            for file in files:
                if '.laz' in file or '.LAZ' in file:
                    file_path = os.path.join(path_folder, file)
                    print(file_path)
                    os.unlink(file_path)
                    print("Folder has cleaned")
        else:
            print("Folder is empty")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
            
    
    try:
        files = os.listdir(res_folder)
        if len(files) > 0:
            for file in files:
                if '.laz' in file or '.LAZ' in file:
                    file_path = os.path.join(res_folder, file)
                    print(file_path)
                    os.unlink(file_path)
                    print("Folder has cleaned")
        else:
            print("Folder is empty")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    # -----------------------------------------------------------------------------------      
    
    # Read data stream of object
    print("#------------ Starting download data -----------#")
    st_download_time = time.time()
    data = obj.data_stream.read()    
    print("The utilized memory after reading data stream is: {}".format(get_current_memory_usage()))
     

    # Save data into file in order to free the memory
    s_file = path_folder + key
    print(s_file)
    with open(s_file, 'wb') as fname:
        fname.write(data)
        print(fname.name)
    
    elap_download_time = time.time() - st_download_time
    print("Downloading data has taken {} seconds".format(elap_download_time))
    print("The utilized memory after downloaded the file is: {}".format(get_current_memory_usage()))
         
    # Delete the variable data to free spaces in the memory
    del data
    print("The utilized memory after deleted the data variable is: {}".format(get_current_memory_usage()))
    
    # ----------------------------------------------------------------------------------- 
    
    # Applying some filter for each file
  
    out_file = res_folder + fname.name.split("/")[3].split(".")[0] + '_denoise.laz'
    print(out_file)
    file_name = {"type":"readers.las", "filename": fname.name}
    cr_json = {
        "pipeline": [
            file_name, 
            {
                # Creates a window to find outliers. If they are found they are classified as noise (7).
                "type": "filters.outlier",
                "method": "statistical",
                "multiplier": 3,
                "mean_k": 8
            },
            {
                "type": "writers.las",
                "compression": "laszip",
                "filename": out_file
            }
        ]
    }
    
    pipeline = pdal.Pipeline(json.dumps(cr_json, indent=4))
    pipeline.validate()   # Check if json options are good
    pipeline.loglevel = 8
    count = pipeline.execute()
    print(count)
    
    print("The utilized memory after executing the pipeline is: {}".format(get_current_memory_usage()))
    del pipeline
    print("The utilized memory after deleting the pipeline variable is: {}".format(get_current_memory_usage()))
    
    
    #Upload files into COS
    
    files = []
    for r, d, f in os.walk(res_folder): # r=root, d=directories, f = files
        for file in f:
            print(file)
            try:
                print(key)
                ibm_cos.delete_object(Bucket=bucket_name, Key=key)
            except:
                print('File is not exist in the bucket {}'.format(bucket_name))
                              
            # Upload the file
            ibm_cos.upload_file(Filename = res_folder + file, Bucket = bucket_name, Key = file)
    
    return count
    



if __name__ == "__main__":
    # Name of the bucket
    bucket_name = 'XXXXX'
    
    # Get the contents of bucket
    list_obj = cos_client.list_objects(Bucket=bucket_name)['Contents']
    obj_key = []
    for obj in list_obj:
        obj_key.append(bucket_name + '/' + obj['Key'])
    print(len(obj_key))

    # Run pywren 
    pw = pywren.ibm_cf_executor(runtime='ammarokran/pywren-pdal:1.0.2',runtime_memory=1024, log_level='DEBUG')
    exec_time = {}
    iterdata = obj_key
    print(iterdata)
    st_process_time = time.time()
    pw.map(remove_noise, bucket_name, chunk_size=None)
    result = pw.get_result()
    print(result)




