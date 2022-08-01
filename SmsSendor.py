# importing the requests library
import json
import requests
import html

def sendSms(number, token):
    # The api url
    url = "https://www.egosms.co/api/v1/plain/"

    # Fetching credentials
    f = open("credentials.txt", "r")

    # The parameters to be sent to the ego sms api
    username = f.readline()
    sender = f.readline()
    password = f.readline()
    message = "SWAMP here, this is your token: "+token

    # Close 
    f.close()
    print(message)
    
    parameters = {
        'username': html.escape(username),
        'password': html.escape(password),
        'number': html.escape(number),
        'message': html.escape(message),
        'sender': html.escape(sender)
    }

    timeout = 5

    # Check for the internet connection and make the request
    try:
        # sending post request and saving response as response object
        r = requests.get(url=url, params=parameters, timeout=timeout)

        # extracting response text
        response = r.text

        print(response)

    except(requests.ConnectionError, requests.Timeout) as exception:
        print("Check your internet connection")