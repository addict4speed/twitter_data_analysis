import oauth2 as oauth
#This module provides a high-level interface for fetching data across the World Wide Web. 
import urllib2 as urllib    

"""
Q: how does oauth work?
A: The parameters and information for an HTTP request, suitable for
   authorizing with OAuth credentials.
   
   When a consumer wants to access a service's protected resources, it does
   so using a signed HTTP request identifying itself (the consumer) with its
   key, and providing an access token authorized by the end user to access
   those resources. 
"""
 
access_token_key = "303205747-PODLDdQsLZ4vMMBvKg3dS8hTU3uDOe0wlDVjwWmC"
access_token_secret = "k17KZaqFxiexEhQFKtunAN6gePcOqE9x9ph79i2VwwU"
 
consumer_key = "66tYwy2JzzsR5kSk9Rw0Q"
consumer_secret = "D6S4apHzJsUtEC961uxkAFbRdT9vb91fJc6Iwxloi0"

_debug = 0

# Set up instances of our Token and Consumer. 
oauth_token = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

# Sign the request using HMAC_SHA1
signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
 
http_method = "GET"

#Q: What is a handler:
#A: A handler is a routine/function/method which is specialized in a certain type of data or focused on 
#certain special tasks.

#Q: what does the HTTPHandler method do? Why does the code exist?
#A: HTTPHandler is a class to handle opening of HTTP URLs. Send an HTTP request, which can be either GET or POST, depending on req.has_data()  

#Q: what are debug levels? 
#A: 
# 0: no logging
# 
# 1: exception logging: log every thrown error. For example in c#: logging in catch blocks. When these log 
# operations are triggered, you know you have an error. You can also log in switch statements if there is a 
# case which should never be hit and the like.
# 
# 2: operation logging: logging operations, which are not in catch blocks (normal operations), should be set 
# to high debugging. This way you can see which method starts executing and then ends up in a catch block.
#
# in our case, we set the debug level to 0
http_handler = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)
 
# Construct, sign, and open a twitter request using the hard-coded credentials above.
def twitterreq(url, method, parameters):
    
    #create the request with the tokens, returns dict of class Request containing information of the Request
    #{u'oauth_version': u'1.0', u'oauth_consumer_key': u'66tYwy2JzzsR5kSk9Rw0Q', u'oauth_token': u'303205747-PODLDdQsLZ4vMMBvKg3dS8hTU3uDOe0wlDVjwWmC', u'oauth_nonce': u'10277585', u'oauth_timestamp': u'1373818844'}
    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                                token=oauth_token,
                                                http_method=http_method,
                                                http_url=url,
                                                parameters=parameters)
     
    # the sign_request method sets the signature parameter to the result of the sign for req.
    # {'oauth_body_hash': '2jmj7l5rSw0yVb/vlWAYkK/YBwk=', u'oauth_nonce': u'13115790', u'oauth_timestamp': u'1373819004', u'oauth_consumer_key': u'66tYwy2JzzsR5kSk9Rw0Q', 'oauth_signature_method': 'HMAC-SHA1', u'oauth_version': u'1.0', u'oauth_token': u'303205747-PODLDdQsLZ4vMMBvKg3dS8hTU3uDOe0wlDVjwWmC', 'oauth_signature': 'BnWb3wA5M43HL3Ut6rMBYNCNMTo='}
    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)
    
    #Q: what does the to_header() method do?
    #A: converts and return the req from type class Request to dict with the key "Authorization" and value being the info from req
    #Q: why do we need to execute to_header() command?
    headers = req.to_header()
    
    #Q: what does the postdata() method do? 
    if http_method == "POST":
        encoded_post_data = req.to_postdata()
        
    else:
        encoded_post_data = None
        url = req.to_url()
#   The OpenerDirector class opens URLs via BaseHandlers chained together. It manages the chaining of handlers, and recovery from errors.
#   The BaseHandlers is the base class for all registered handlers, and handles only the simple mechanics of registration.
    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)
     
    response = opener.open(url, encoded_post_data)
    return response
 
def fetchsamples():
    url = "https://stream.twitter.com/1.1/statuses/sample.json"
    parameters = []
    response = twitterreq(url, "GET", parameters)
    
    for line in response:
        #.strip() simply removes the whitespace and return the string. 
        #http://docs.python.org/2/library/stdtypes.html
        print line.strip()
    return response
     
if __name__ == '__main__':
     fetchsamples() 
    
    