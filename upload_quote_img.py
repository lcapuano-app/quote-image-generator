import base64
import os
from pickletools import optimize
from urllib import response
import requests
import http.client
import json
from io import BytesIO
from config import CFG
from PIL.Image import Image as ImageType
from error_log import ErrLog

def upload_image( final_img: ImageType, file_name: str ):

  key = os.environ['API_SECRET_KEY']
  value = os.environ['API_SECRET_VAL']
  url = CFG.API_UPLOAD_URL + '?' + key + '=' + value
  final_img_64 = __get_img_base64( final_img=final_img )

  headers = { 'Content-Type': 'application/json' }
  payload = json.dumps({ 'name': file_name, 'image': final_img_64 })

  try:
    conn = http.client.HTTPSConnection(CFG.API_HOST)
    conn.request("POST", f"{CFG.API_UPLOAD_URL}?{key}={value}", headers=headers, body=payload)
    res = conn.getresponse()
    code = res.getcode()

    if code != 200:
      raise Exception( f"File upload failed with a status {response.status_code}. File: {file_name}" )

    return CFG.API_OUTPUT_DIR + file_name

  except Exception as err:
    ErrLog.log(err)
    return CFG.API_OUTPU_DFLT_IMG

def __get_img_base64( final_img: ImageType ) -> str:
  output = BytesIO()
  final_img.save( fp=output, format='PNG', quality=70, optimize=True )
  img_data = output.getvalue()

  img_data = base64.b64encode(img_data)

  if not isinstance(img_data, str):
    # Python 3, decode from bytes to string
    img_data = img_data.decode()

  data_url = 'data:image/png;base64,' + img_data
  return data_url
