##
## theLeedz_on_X
##
## for more on LeedzAi visit theleedz.com
##
## Controller for Gemini-Powered X Poster  
##
## coordinates three modules:
##
##   1. trends_hander -- calls 3rd party HTTP API to get list of trending topcs
##   2. gemini_handler -- call Google Gemini HTTP API to turn list into statements about the Leedz
##   3. async_x_handler -- async call to post messages to X  
##

import boto3
import json
from decimal import Decimal


import logging


# import trends from LAMBDA LAYER .zip file
# because no external libraries required -- just uses http.client.HTTPSConnection
from trends_handler import get_trends_string




logger = logging.getLogger()
logger.setLevel(logging.INFO)




#
# Use this to JSON encode the DYNAMODB output
#
#
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            long_str = str(obj)
            short_str = long_str.strip("Decimal()")
            return short_str
        return json.JSONEncoder.default(self, obj)
    
    



    
    
##
## get the trending keywords
## gemini AI converts them to statements about the Leedz
## post statements to X async
##
def lambda_handler(event, context):
    
    json_data = None
    try:
        
        ## TRENDS API
        ##
        trends_string = get_trends_string()
        logger.info(trends_string)
    
    
        ## GOOGLE GEMINI 
        ##
        payload = {
            'function':'trends_to_x',
            'trends_string': trends_string
        }
        
        lambda_function = boto3.client('lambda')
        
        response = lambda_function.invoke(FunctionName='gemini_handler',
                                        InvocationType='RequestResponse',
                                        Payload= json.dumps( payload ))

        #
        # big process to extract the actual msg String from gemini_handler
        #
        payload = json.loads( response['Payload'].read() )
        body = json.loads( payload['body'] )

        # contains 1 or 0
        # Look for ERROR and terminate
        cd = body['cd']  
        if (int(cd) == 0):
            err = body['err']  
            raise Exception(err)  


        ## GOT GEMINI RESPONSES !!
        gemini_responses = body['msg']
        # logger.info("GEMINI: " + gemini_responses)
        sentences = gemini_responses.split('\n')
       
        ## 
        ## asynchronous X handler
        ##
        # AWS lambda function call API
        #
        lambda_function = boto3.client('lambda')

        # an array of sentences to send to X_handler
        post_counter = 0
        for x_post in sentences:

            post_len = len(x_post)

            # omit any linebreaks and any nonsense that might get through
            if ( post_len <= 10 ):
                continue
            
            # Check if the tweet text exceeds the character limit
            # Truncate the tweet text to 280 characters
            elif post_len > 200:
                x_post = x_post[:200]
    

            # arg to function call
            payload = {
                'function':'post_text',
                'x_post': x_post
            }
        
            lambda_function.invoke(FunctionName='async_x_handler',
                                    InvocationType='Event',
                                    Payload= json.dumps( payload, cls=DecimalEncoder ))
            
            logger.info("POSTED: " + x_post)
            post_counter = post_counter + 1
                    


        return {
            'statusCode': 200,
            'body': 'Success!  X posts generated: ' + str(post_counter)
        }


        
        
    except Exception as err:
        
        str_err = str(err)
        logger.error(str_err)
        json_data = json.dumps({ "cd": 0, "er" : str_err })
        






