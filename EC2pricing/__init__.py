import requests, json

'''
 Get the user required AWS EC2 service along with few parameters

'''
# send the link request and parse them into the local JSON file
url_response = requests.get("https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/index.json")
print(url_response)

print(url_response.json())