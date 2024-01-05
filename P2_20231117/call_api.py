from pathlib import Path
import os
from PIL import Image
import io
import re
from io import BytesIO
import base64
import requests

def main():
    
    # --- path ---

    path = Path('./P2_20231117')

    OBSERVE_FOLDER_PATH = path / 'saveimg'
    OUTPUT_FOLDER_PATH = path / 'outputimg'

    OBSERVE_FOLDER_STATUS = os.listdir( OBSERVE_FOLDER_PATH )
    print(OBSERVE_FOLDER_STATUS)

    # --- api ---

    DOMAIN = 'http://127.0.0.1:8001'+'/upload'

    def return_img_base64(img):
        # 將圖片轉換為 Base64 字串
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='JPEG')
        img_base64 = base64.b64encode(img_byte_array.getvalue()).decode('utf-8')
        return img_base64

    def base64_to_image(base64_str):
        base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
        byte_data = base64.b64decode(base64_data)
        image_data = BytesIO(byte_data)
        img = Image.open(image_data)
        return img

    while True:

        current_folder_status = os.listdir( OBSERVE_FOLDER_PATH )

        if len(current_folder_status) != len(OBSERVE_FOLDER_STATUS):
            print('dif')
            # get diff in folder
            diff_list = list(set(current_folder_status) - set(OBSERVE_FOLDER_STATUS))
            
            # call api
            for file in diff_list:
                image = Image.open( OBSERVE_FOLDER_PATH / file )
                if(image):
                    print(image)
                else:
                    break
                base64_img = return_img_base64(image.convert('RGB'))

                payload_dct = {
                    "image": base64_img 
                }
                
                request = requests.post( DOMAIN, json = payload_dct ).json()
                base64_img = request['base64_image']
                output_img = base64_to_image(base64_img)

                output_img.save(str(OUTPUT_FOLDER_PATH / file ))

            # update OBSERVE_FOLDER_STATUS
            OBSERVE_FOLDER_STATUS = current_folder_status


# main()