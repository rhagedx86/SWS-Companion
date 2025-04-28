import logging
import os
import requests
import tkinter as tk
import myNotebook as nb
import json
from config import appname
from edmc_data import commodity_bracketmap as bracketmap
from typing import Optional
from companion import CAPIData, SERVER_LIVE, SERVER_LEGACY, SERVER_BETA

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

def cmdr_data(data, is_beta):
    if data.get('commander') is None or data['commander'].get('name') is None:
        raise ValueError("Commander name is missing")
    if data.source_host == SERVER_LIVE:
        control = data['lastStarport']['minorfaction']
        if control == "Sidewinder Syndicate":
            name = data['lastSystem']['name']
            data['lastStarport']['system'] = name
            send_data_to_api(data['lastStarport'])



last_sent_entry = None  
cmdr_name = None  

def journal_entry(cmdrname: str, is_beta: bool, system: str, station: str, entry: dict, state: dict) -> None:
    global cmdr_name, last_sent_entry  
    try:
        if cmdr_name is None and cmdrname is not None:
            cmdr_name = cmdrname

        event_type = entry.get('event')

        if event_type in ('Docked', 'ColonisationConstructionDepot', 'ColonisationContribution'):

            event_data = {
                'info': {
                    'commander': cmdr_name,
                    'system': entry.get('system', {}).get('name', system),
                    'station': entry.get('station', {}).get('name', station),
                    'market_id': entry.get('MarketID')
                },
                'event': event_type,
                'timestamp': entry.get('timestamp'),
                'full_entry': entry
            }
            
            
        #prevent api spam cause fDev is spaming ColonisationConstructionDepot events every couple seconds....
        if last_sent_entry is None or {k: v for k, v in entry.items() if k != 'timestamp'} != last_sent_entry:
            send_data_to_api(event_data)
            last_sent_entry = {k: v for k, v in entry.items() if k != 'timestamp'}  # Remove timestamp before saving


    except Exception as e:
        return
        



def send_data_to_api(data):        
    api_url = "https://sidewindersyndicate.site/api/data"
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, json=data, headers=headers)  # Pass the dictionary directly
        if response.status_code == 200 or response.status_code == 201:
            logger.info("Data successfully sent to API")
        else:
            return
    except Exception as e:
        logger.error(f"Error sending data to API: {str(e)}")

def plugin_start3(plugin_dir: str) -> str:
    logger.info('SWS-Companion-loaded-v3')
    return "SWS-Companion-v3"

def plugin_prefs(parent: nb.Notebook, cmdr: str, is_beta: bool) -> Optional[tk.Frame]:
    frame = nb.Frame(parent)
    nb.Label(frame, text="Hello").grid()
    nb.Label(frame, text="Commander").grid()
    nb.Label(frame, text="This plugin aids in the creation of DTR's-v3!").grid()
    nb.Label(frame, text="This also tracks Construction and Contribution to Colonisation!").grid()    
    return frame
