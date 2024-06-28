import logging
import os
import json
import requests
import tkinter as tk
import myNotebook as nb
from config import appname
from edmc_data import commodity_bracketmap as bracketmap
from typing import Optional
from companion import CAPIData, SERVER_LIVE, SERVER_LEGACY, SERVER_BETA

plugin_name = os.path.basename(os.path.dirname(__file__))
logger = logging.getLogger(f'{appname}.{plugin_name}')

# Start logging
if not logger.hasHandlers():
    level = logging.INFO
    logger.setLevel(level)
    logger_channel = logging.StreamHandler()
    logger_formatter = logging.Formatter(f'%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d:%(funcName)s: %(message)s')
    logger_formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
    logger_formatter.default_msec_format = '%s.%03d'
    logger_channel.setFormatter(logger_formatter)
    logger.addHandler(logger_channel)

# Listen to EDMC trasmit function. 
def cmdr_data(data, is_beta):
    if data.get('commander') is None or data['commander'].get('name') is None:
        raise ValueError("Commander name is missing")
        
    # Determining source galaxy for the data
    if data.source_host == SERVER_LIVE:
        control = data['lastStarport']['minorfaction']
        if control == "Sidewinder Syndicate":
            # Extracting the file name from the lastStarport data
            name = data['lastSystem']['name']
            # This data is ONLY station market info!
            data['lastStarport']['system'] = name

            # Send data['lastStarport'] directly to the API
            send_data_to_api(data['lastStarport'])

# Send market data to database, just how Inara handles it.
def send_data_to_api(json_data):
    api_url = "http://sidewindersyndicate.site/api/data"
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, json=json_data, headers=headers)
        
        if response.status_code == 200:
            logger.info("Data successfully sent to API")
        else:
            logger.error(f"Failed to send data to API. Status code: {response.status_code}")
    
    except Exception as e:
        logger.error(f"Error sending data to API: {str(e)}")
        
# Startup
def plugin_start3(plugin_dir: str) -> str:
    logger.info('SWS-Companion-loaded')
    return "SWS-Companion"

# Info
def plugin_prefs(parent: nb.Notebook, cmdr: str, is_beta: bool) -> Optional[tk.Frame]:
   frame = nb.Frame(parent)
   nb.Label(frame, text="Hello").grid()
   nb.Label(frame, text="Commander").grid()
   nb.Label(frame, text="This plugin aids in the creation of DTR's!").grid()  
   return frame
