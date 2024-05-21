##
## Make a request to trends API for the current trending topics on X
## results updated every 30 min
## https://rapidapi.com/brkygt88/api/twitter-trends5
##
## API key in Environment Variable
##
## 3rd party Twitter Trends API -- PRO plan $3/month x 3000 posts
## https://rapidapi.com/brkygt88/api/twitter-trends5/
## 
##
## Environment Variables
##  
##   TRENDS_API = validateEnviron("TRENDS_API", 1)
##   WOEID = validateEnviron("WOEID",1)
##   X_KEY = validateEnviron("X_KEY",1)
##   NUM_TRENDS = int( validateEnviron("NUM_TRENDS", 1) )
##

import os
import http.client
import json

import random



import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)
  



#
#
def validateEnviron( var, required ):
    
    the_val = ""
    try:
        the_val = os.environ[var]
    except KeyError:
        if required:
            raise ValueError("Environment Variable not found: " + var)
        the_val = ""
        
    return the_val
    
    


## 3rd party Twitter Trends API -- free plan
## https://rapidapi.com/brkygt88/api/twitter-trends5/pricing
## 100 requests a month
##
def get_trends_string() :
    
    X_KEY = ""
    TRENDS_API = ""
    WOEID = ""

    try :
        
        TRENDS_API = validateEnviron("TRENDS_API", 1)
    
        conn = http.client.HTTPSConnection( TRENDS_API )
        
        WOEID = validateEnviron("WOEID",1)
        
        X_KEY = validateEnviron("X_KEY",1)
        
        
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'X-RapidAPI-Key': X_KEY,
            'X-RapidAPI-Host': TRENDS_API
        }
        
        conn.request("POST", "/twitter/request.php", WOEID, headers)
        
        res = conn.getresponse()
        data = res.read()
        
        trends_data = data.decode("utf-8")
        
        trends_string = trends_to_string( trends_data )
    
        # numbered list of NUM_POSTS Strings
        #
        return trends_string
    
    
    except Exception as e:
        logger.error("X_KEY: " + X_KEY)
        logger.error("TRENDS_API: " + TRENDS_API)
        logger.error("WOEID: " + WOEID)
        logger.error("ERROR getting trends data: " + str(e))
        raise




  
##
## Parse the trends data into a string for input to Gemini
## 
## returns NUM_POSTS number of results randomly selected from total list (50?)
##
## throws Exception if no trends returned
def trends_to_string( trends_data ):

    NUM_TRENDS = int( validateEnviron("NUM_TRENDS", 1) )

    # Parse the JSON data
    data = json.loads( trends_data )

    if (not data['trends']):
        raise Exception("No trends data returned from API")

    # generate a string representing a numbered list of NUM_TRENDS items long, 
    # randomly selected from the input data, and ensures that each item is unique in the list.
    trends_string = ""
    trends_keys = list(data['trends'].keys())
    selected_keys = random.sample(trends_keys, NUM_TRENDS)

    for index, key in enumerate(selected_keys, start=1):
        value = data['trends'][key]
        name = value['name'].lstrip('#')
        domain_context = value.get('domainContext', '')
        context_string = f" ({domain_context})" if domain_context else ''
        trends_string += f"{index}. {name}{context_string}\n"

    return trends_string
        
  
  

  
  
  
  

