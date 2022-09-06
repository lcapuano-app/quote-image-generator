import os
import json
import requests
from .quote_default import dflt_response
from .quote_type import QuoteType
from error_log import ErrLog

class Quote():

  def get_quote( quote_id: str ) -> QuoteType:
    base_url = os.environ['API_URL']
    api_key = os.environ['API_KEY']
    url = base_url + quote_id + '?$simple=true'
    headers = { 'x-api-key': api_key }
    payload={}

    try:
      response = requests.request("GET", url, headers=headers, data=payload)

      if response.status_code != 200:
        raise Exception( response.text )

      data = json.loads(response.text)

      return data

    except Exception as err:
      ErrLog.log( err )
      return json.loads(dflt_response)

  def update_quote( quote_id: str, img_url: str ) -> int:
    base_url = os.environ['API_URL']
    api_key = os.environ['API_KEY']
    url = base_url + quote_id
    headers = {
      'x-api-key': api_key,
      'Content-Type': 'application/json'
    }

    try:
      payload = json.dumps({ "imgs.qt": img_url })
      print(payload)
      response = requests.request("PATCH", url, headers=headers, data=payload)

      if response.status_code != 200:
        raise Exception( response.text )

      return response.status_code

    except Exception as err:
      ErrLog.log( err )
      return 500

