import os
import json
import requests
import smtplib

url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=AIzaSyCtuXn9-2jp1bsO058Z3JGjvpwpBF5BDMI"
data = { "request": { "passengers": { "adultCount": 1 }, "slice": [{ "origin": "OAK", "destination": "HNL", "date": "2015-03-21" }, { "origin": "HNL", "destination": "OAK", "date": "2015-03-29" }]}} 
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(data), headers=headers)

resp = json.loads(r.text)
cost_set = set()
for el in resp['trips']['tripOption']:
    cost_set.add(float(el['saleTotal'][3:]))

min_cost = min(cost_set)

def notify(price):
    server = smtplib.SMTP( "smtp.gmail.com", 587 )
    server.starttls()
    server.login('rpflynn22@gmail.com', 'mybirthdayis222')
    server.sendmail('rpflynn22@gmail.com', '9252165538@txt.att.net', 'Price has dropped to $' + str(price))
    #server.sendmail('rpflynn22@gmail.com', '9258582952@txt.att.net', 'Price has dropped to $' + str(price))


######### CHECK IF PRICE IS LOWER HERE ##########

try:
    price = float(os.environ['PRICE_CHECKER'])
    print('no keyerr')
    if min_cost < price - 10:
        notify(min_cost)
except KeyError as e:
	print('keyerror')
	notify(min_cost)
	os.environ['PRICE_CHECKER'] = str(min_cost)