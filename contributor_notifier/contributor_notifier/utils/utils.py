########################################################################
#                    Prurpose of the Package                           #
########################################################################

# Check if there is a change in the GitHub repo. 
# Detect the contributors.
# Check of the contributor wants to be notified. 
# Extract the subject and the datamodel that has been change.  
# Send them customized emails depending on the change. 

########################################################################
#                                 Imports                              #
########################################################################
import os
import json
import requests
#import ruamel.yaml as yaml
import yaml
import time

from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

########################################################################
#                               URL                                    #
########################################################################

# Detect the contributors:  
# Construct from the Github url the url to the contributors.yaml. 
# Extract the subject and the datamodel that has been change.


# There is a challenge which is that the "https://github.com/smart-data-models" on GitHub has so many other repositories. 
# other than the data models, therefore it is not possible to use this approach.
# Option 1: Use the official list of SDMs and construct all the possible subject that need to be watched.  
# Always check the change in these repos. 
# Option 2: Construct a database of contribotors 

datamodels_list = []

def detect_contributors(github_url: str) -> str:
    contributors_urls = []

########################################################################
#                                json                                  #
########################################################################

def open_json(file_url):
    """
    Opens a JSON file or URL.

    Args:
        file_url (str): The file path or URL to the JSON file.

    Returns:
        dict: The JSON data as a dictionary, or None if the file could not be opened.
    """
    if file_url.startswith("http"):
        # is a URL
        try:
            pointer = requests.get(file_url)
            return json.loads(pointer.content.decode('utf-8'))
        except:
            return None

    else:
        # is a file
        try:
            file = open(file_url, "r")
            return json.loads(file.read())
        except:
            return None
        
########################################################################
#                                yaml                                  #
########################################################################

def open_yaml(file_url):
    """
    Opens a YAML file from the given file path or URL.

    Args:
        file_url (str): The file path or URL to the YAML file.

    Returns:
        dict: The YAML data as a dictionary, or None if the file could not be opened.
    """
    if file_url.startswith("http"):
        # es URL
        pointer = requests.get(file_url)
        return yaml.safe_load(pointer.content.decode('utf-8'))
    else:
        # es file
        file = open(file_url, "r")
        return yaml.safe_load(file.read())

