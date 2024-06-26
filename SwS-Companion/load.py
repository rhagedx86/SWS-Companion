import logging
import os
import json
import requests
import tkinter as tk
import myNotebook as nb
from config import appname
from edmc_data import commodity_bracketmap as bracketmap
from typing import Optional

# This could also be returned from plugin_start3()
plugin_name = os.path.basename(os.path.dirname(__file__))

logger = logging.getLogger(f'{appname}.{plugin_name}')
if not logger.hasHandlers():
    level = logging.INFO
    logger.setLevel(level)
    logger_channel = logging.StreamHandler()
    logger_formatter = logging.Formatter(f'%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d:%(funcName)s: %(message)s')
    logger_formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
    logger_formatter.default_msec_format = '%s.%03d'
    logger_channel.setFormatter(logger_formatter)
    logger.addHandler(logger_channel)

from companion import CAPIData, SERVER_LIVE, SERVER_LEGACY, SERVER_BETA

folder_path = os.path.expanduser("~/Documents/sws")
os.makedirs(folder_path, exist_ok=True)

def cmdr_data(data, is_beta):
    if data.get('commander') is None or data['commander'].get('name') is None:
        raise ValueError("Commander name is missing")

    logger.info(data['commander']['name'])

    # Determining source galaxy for the data
    if data.source_host == SERVER_LIVE:
        control = data['lastStarport']['minorfaction']
        if control == "Sidewinder Syndicate":
            # Extracting the file name from the lastStarport data
            file_name = f"{data['lastStarport']['name'].replace(' ', '_')}_data.json"
            file_path = os.path.join(folder_path, file_name)
            name = data['lastSystem']['name']
            data['lastStarport']['system'] = name
            logger.info(data['lastStarport']['system'])
            
            # Saving the lastStarport data to the file
            with open(file_path, 'w') as file:
                json.dump(data['lastStarport'], file)
            
            logger.info(f"Data saved to {file_path}")
            
            # Send data['lastStarport'] directly to the API
            send_data_to_api(data['lastStarport'])


def send_data_to_api(json_data):
    api_url = "http://15.204.67.28:80/api/data"  # Replace with your API endpoint URL
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, json=json_data, headers=headers)
        
        if response.status_code == 200:
            logger.info("Data successfully sent to API")
        else:
            logger.error(f"Failed to send data to API. Status code: {response.status_code}")
    
    except Exception as e:
        logger.error(f"Error sending data to API: {str(e)}")
        
        
def plugin_start3(plugin_dir: str) -> str:
    logger.info('SWS-EDMC-loaded')
    return "SWS-Companion"

def plugin_prefs(parent: nb.Notebook, cmdr: str, is_beta: bool) -> Optional[tk.Frame]:
   frame = nb.Frame(parent)
   nb.Label(frame, text="Hello").grid()
   nb.Label(frame, text="Commander").grid()
   nb.Label(frame, text="This plugin aids in the creation of DTR's!").grid()  
   return frame