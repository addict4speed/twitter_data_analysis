import oauth2 as oauth
import urllib2 as urllib
 
 
access_token_key = "303205747-PODLDdQsLZ4vMMBvKg3dS8hTU3uDOe0wlDVjwWmC"
access_token_secret = "k17KZaqFxiexEhQFKtunAN6gePcOqE9x9ph79i2VwwU"
 
consumer_key = "66tYwy2JzzsR5kSk9Rw0Q"
consumer_secret = "D6S4apHzJsUtEC961uxkAFbRdT9vb91fJc6Iwxloi0"
 
_debug = 0
 
oauth_token = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
 
signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
 
http_method = "GET"
 
 
http_handler = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)
 
# '''
# Construct, sign, and open a twitter request
# using the hard-coded credentials above.
# '''

def twitterreq(url, method, parameters):
    #Q: how does oauth work?
    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                                token=oauth_token,
                                                http_method=http_method,
                                                http_url=url,
                                                parameters=parameters)
     
    #Q: where did the sign_request method come from? 
    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)
     
    headers = req.to_header()
     
    if http_method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
        url = req.to_url()
     
    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)
     
    response = opener.open(url, encoded_post_data)
     
    return response
 
def fetchsamples():
    url = "https://api.twitter.com/1.1/search/tweets.json?q=microsoft"
    parameters = []
    response = twitterreq(url, "GET", parameters)
#     print type(response)
#     for line in response:
#         print line.strip()
    return response
     
if __name__ == '__main__':
    response = fetchsamples()
    print response
