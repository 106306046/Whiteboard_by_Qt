from pathlib import Path
import os
from PIL import Image
import io
from io import BytesIO
import base64
import requests

# --- path ---

path = Path('./P2_20231117')

OBSERVE_FOLDER_PATH = path / 'saveimg'
OUTPUT_FOLDER_PATH = path / 'outputimg'

OBSERVE_FOLDER_STATUS = os.listdir( OBSERVE_FOLDER_PATH )

# --- api ---

DOMAIN = 'http://127.0.0.1:8001'+'/upload'

def return_img_base64(img):
    # 將圖片轉換為 Base64 字串
    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format='JPEG')
    img_base64 = base64.b64encode(img_byte_array.getvalue()).decode('utf-8')
    return img_base64

while True:

    current_folder_status = os.listdir( OBSERVE_FOLDER_PATH )

    if len(current_folder_status) != len(OBSERVE_FOLDER_STATUS):

        # get diff in folder
        current_folder_status_set = set(current_folder_status)
        diff_list = [ file for file in OBSERVE_FOLDER_STATUS if  file not in current_folder_status_set ]
        
        # call api
        for file in diff_list:
            image = Image.open(str( OBSERVE_FOLDER_PATH / file ))
            base64_img = return_img_base64(image.convert('RGB'))

            payload_dct = {
                "image": base64_img 
            }
            
            request = requests.post( DOMAIN, json = payload_dct )

            request_image = Image.open(BytesIO(base64.b64decode(request['base64_image'])))
            request.save(str(OUTPUT_FOLDER_PATH / file ))

        # update OBSERVE_FOLDER_STATUS
        OBSERVE_FOLDER_STATUS = current_folder_status