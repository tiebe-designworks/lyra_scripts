### download_from_domain_b2_priv.py: Allows you to download files from a private Backblaze B2 bucket over a URL. Useful if you're using Cloudflare.
### Created by Cam Cuozzo (@camcuozzo on Github)
### This script is used as one of the functions in the back-end script for Lyra.

from b2sdk.v1 import * # https://pypi.org/project/b2sdk/
import base64
import json
import requests
import urllib.request

# All of the variables B2 needs to authenticate a private bucket
info = InMemoryAccountInfo()
b2_api = B2Api(info)
application_key = 'YOUR_KEY'
application_key_id = 'YOUR_KEY_ID'
b2_api.authorize_account("production", application_key_id, application_key)

# Gets an auth token from B2 API so we can download from a private bucket via URL
def get_b2_auth():
    flag_debug = False 
    b2_app_key = bytes(application_key, encoding='utf-8')
    b2_app_key_id = bytes(application_key_id, encoding='utf-8')
    base_authorization_url = 'https://api.backblazeb2.com/b2api/v2/b2_authorize_account'
    b2_get_download_auth_api = '/b2api/v2/b2_get_download_authorization'

    id_and_key = b2_app_key_id + b':' + b2_app_key
    b2_auth_key_and_id = base64.b64encode(id_and_key)
    basic_auth_string = 'Basic ' + b2_auth_key_and_id.decode('UTF-8')
    authorization_headers = {'Authorization' : basic_auth_string}

    resp = requests.get(base_authorization_url, headers=authorization_headers)

    # If you need to see the below for debugging purposes, set flag_debug to True
    if flag_debug:
        print (resp.status_code)
        print (resp.headers)
        print (resp.content)

    resp_data = json.loads(resp.content)
    auth_token = resp_data["authorizationToken"]

    return auth_token

# Downloading the target file with the auth token generated
def download_from_b2():
    token = get_b2_auth()
    file_name = "the file path and name you want to save to"
    file_url = "url where you're hosting files" + string_of_the_file_name_you_need + "?Authorization=" + token
    
    # B2 would act up if we didn't add a Firefox user agent for whatever reason
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')] 
    urllib.request.install_opener(opener)
    
    # Download the file from the specified URL to the specified file name and path
    urllib.request.urlretrieve(file_url, file_name)
