##
## submit a structured prompt to Google AI Gemini
##
## Google AI Studio
## https://aistudio.google.com/app/prompts/18pzoRpKmAYXqp3OITa1r5GPPonGI5H02
## Trends-Gemini-X-Structured
##
## get Google API Key from Environment Variable
## GOOGLE_API_KEY = validateEnviron( 'GOOGLE_API_KEY', 1 )

import os
import google.generativeai as genai
import json


from decimal import Decimal
import logging

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
    
    



#
#
#
#
def handle_error( msg ):
  
    logger.error( msg )
    ret_obj = { "cd": 0,
                "err": msg
            }
    
    
    the_json = json.dumps(ret_obj, cls=DecimalEncoder)

    return the_json
    
    
    
    

#
#
#
#
def handle_success( msg ):
  
    ret_obj = { "cd": 1,
                "msg": msg
            }
    the_json = json.dumps(ret_obj, cls=DecimalEncoder)

    return the_json
    
    
    




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
    
    
    
    
    
    
# WORKS DIFFERENTLY than other lambdas
# not looking for queryStringParameters
# will throw ValueError
#
def validateParam( event, param, required ):
    
    value = ""
    
    if (param not in event):
            if required:
                raise ValueError("HTTP Request error.  No '" + param + "' event parameter")
    else:
        value = event[param] 
        
    return value


    
    
    
    
##
## create structured text query 
## Trends-Gemini-X-Structured in Google AI Studio
##
## throws Exception 
def trends_to_x( trends_string ) :

    try :        

        GOOGLE_API_KEY = validateEnviron( 'GOOGLE_API_KEY', 1 )

        ## CONNECT TO GOOGLE GEMINI 
        ##
        genai.configure(api_key=GOOGLE_API_KEY)
        
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
        }

        safety_settings = [
        {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_ONLY_HIGH"
        },
        {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_ONLY_HIGH"
        },
        {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_ONLY_HIGH"
        },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest",
                                        generation_config=generation_config,
                                        safety_settings=safety_settings)

            
     
        prompt_parts = [
        "You are an AI bot who creates posts on X to advertise a business called The Leedz.\nYour input is a list of keywords.\nYou will generate a list of sentences advertising the business containing the keywords.\nEach sentence must be less than 201 characters long.\n\nEach sentence must contain one keyword. \nOnce a keyword has been used, remove it from the list and do not re-use it in another sentence.\nThe first time a keyword is used, preface it with a '#'.\nIf a keyword contains a term in parentheses, use the term for context to clarify the meaning of the keyword. \nFor example,  'Smith (NBA)' indicates that Smith is the name of an NBA player.\nDO NOT include parentheses in the sentence you generate.\n\nTo craft each sentence, use one or more or parts of phrases from About:\nIf a hashtag appears in the About, continue to use it in the output sentence.  \n\nGoals:\n1. Each output sentence should assume that the keyword is true, trending, and important to the reader right now.\n2. Each sentence should promote the Leedz as a business solution to the situation the keyword describes or problem created by the keyword trending now.\n\n\nAbout:\n\n1. theleedz.com is a web app users can access from any browser\n2. The Leedz is a marketplace for #smallbiz vendors to make more money from their booking calendars.\n3. The Leedz solves a problem that every vendor has.  You book a date on your calendar, and afterwards someone else requests your service for the same date. \nThe request has value to another vendor who can take the booking.  Now you can sell it, on the Leedz.\n4. The Leedz enables #smallbusiness owners to make back their advertising money, and grow a network of trusted vendors with whom to trade booking info\n5. The business model of the Leedz is the inverse of #GigSalad, #Thumbtack, #Yelp and other booking providers.  They sell you five gigs for the same date, knowing you can only work one.  Make that money back by selling the other four, on the Leedz.  \n6. #Partyvendors like #inflatables and #facepainters make excellent money on weekends with very low overhead.  These are popular second-jobs, or #sidehustles.\n7. Every day more people are adopting #sidehustles and second jobs to make ends meet in what is called the exploding #gigeconomy\n8. There are over 50 trades on the Leedz from #photobooth vendors, to #caterers, to hair #braiding and #personaltrainers.\n9. The Leedz is built on #serverless #AWS technology and uses #Square to process all payments.  Most #small-business vendors ALREADY use Square to charge sales .  When you sell a leed the money goes directly into your Square account.\n10. The Leedz incorporates industry-standard encryption technology and security protocols to keep your personal and payment data private.",
        "Keywords: 1. Fooball\n2. Ubisoft (software)",
        "Sentences: Spend more time watching #football this season and less time managing your calendar with the Leedz, a web app that helps vendors find new clients and make more money from their existing bookings.\n\nAs #Ubisoft and other software companies announce layoffs and the 'gig economy' grows faster than ever,  the Leedz can help anyone with a side-hustle find work and build a market for their services.",
        "Keywords: 1. Tacos",
        "Sentences: Book the perfect food vendor for your next party, from #tacos to churros, you can find them on the Leedz.",
        "Keywords: 1. dogs\n2. WWE\n3. NBA Playoffs\n4. Dembele (Champions League)\n5. Ethe\n6. Apple (stock market)\n7. Boeing Whistleblower Dead (corporate politics)\n8. earthquake (Tokyo)\n9. layoffs (business)\n10. Mother's Day",
        "Sentences: walking #dogs is a popular #sidehustle.  Use the Leedz to find your next client and network with other vendors with whom you can trade booking info in the future.\n\nAre you hosting a #WWE watch party?  The Leedz can help you find the perfect mix of food and entertainment vendors to make it a true Royal Rumble!\n\nThe #NBA Playoffs is a perfect time for a house party with #catering #balloonart and #caricatures.  Find all those vendors and more on the Leedz.\n\nWhile you're watching the #Dembele score a goal in the Champions League, the Leedz is working to sell the bookings you can't work to vendors who can.\n\nTrading #Ethe is a great way to finance your next small-business #sidehustle.  When you are ready to find your first bookings, join the Leedz.\n\nThe stock market is volatile, but #Apple is a safe bet, and so is The Leedz. \n\nWith news of the #Boeing Whistleblower Death and other corporate politics, people are turning to more secure, reliable home businesses.  Build yours on the Leedz. \n\nDon't let an #earthquake  in Tokyo stop you from running your business.  Grow it on the Leedz.\n\n#Layoffs happen in every industry. The Leedz can help you find new gigs and earn extra income from your #sidehustle.\n\nFind a #florist and #balloonart for #MothersDay on the Leedz, a marketplace for small-business vendors.",
        "Keywords: 1. Sukuna\n2. Yuji\n3. Hardaway (NBA)\n4. Yasuke (Gaming)\n5. Chargers\n6. Darby (Wrestling)\n7. Hannity\n8. Nitro (Technology)\n9. Kenjaku",
        "Sentences: The Leedz can help you maximize your time and resources so you can focus on what matters most: your passion for #Sukuna and the world of Jujutsu Kaisen.  \n\nWith all the excitement surrounding #Yuji, the Leedz helps you book more gigs so you can spend more time enjoying your favorite anime.  \n\nOn the Leedz you can sell your unused dates and make more money from your #sidehustle than #Hardaway or any other player in the NBA.\n\nThe Leedz is the perfect platform for anyone with a #sidehustle in the #gaming industry, like those who love Yasuke, to manage their calendars more efficiently.\n\nThe Leedz is a great way to connect with other party vendors in the #Chargers tailgate community and grow the network for your unique product or service.  \n\nThe Leedz helps you manage your time more efficiently so you can spend more time watching #Darby in the wrestling ring and less time searching for new clients.  \n\nThe Leedz is a great way to make money from your existing bookings, even if you're busy watching #Hannity like millions of others. \n\n#Nitro is the latest technology craze, but the Leedz is the platform that will help you grow your small business. \n\nDon't let #Kenjaku get in the way of your business goals.  The Leedz is a marketplace for party vendors and entertainers to make more money from their booking calendars.",
        "Keywords:" + trends_string,
        "Sentences: ",
]

        response = model.generate_content(prompt_parts)        
        return response.text
    
    
    except Exception as e:
        logger.error("Error making Gemini AI request with trends: " + trends_string)
        logger.error( str( e ) )        
        raise





 
#
# this helper function contains code serving several different callers
# the function name is in the event request object
# other params will vary accordingly
#
#
def lambda_handler(event, context):
    
    function_name = ""
    try:
        # which function to call
        function_name = validateParam(event, "function", 1)
        match function_name:
        
            # post a single text String to X
            # 
            case "trends_to_x":
                
                the_trends = validateParam(event, "trends_string", 1)
                result = trends_to_x( the_trends )

                # SUCCESS
                return createHttpResponse( handle_success( result ))


            # ERROR condition
            #
            case _:
                raise Exception("Unknown function request: " + function_name)
        
        
    except Exception as e:
        return createHttpResponse( handle_error( str(e )))
    




        
#
# Create the HTTP response object
#
#
def createHttpResponse( json_result ):
   
    response = {
            'statusCode': 200,
            'body': json_result,
            'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            },
    }

    # logger.info("RETURNING RESPONSE")
    # logger.info(response)
    
    
    return response

 