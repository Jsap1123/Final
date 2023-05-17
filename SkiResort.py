import requests
import pprint
import csv
from twilio.rest import Client


resortsFile = open('resorts.csv')
resortsReader = csv.reader(resortsFile)
resortsData = list(resortsReader)

outputFile = open('out.csv', 'w', newline='')
outputWriter = csv.writer(outputFile)
body = ''

print('Enter the name of the file that contains the ski resorts:')
resorts = input()
print('What is your phone number?')
MaxSnow = 0
MaxResortName = ''
for row in resortsData:
    r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + str(row[1]) + str(row[2]), '+CA&key=AIzaSyCYIen_c3ag0CZix5eFcaiGNnm1gNspj7w')
    json = r.json()

    lat = json['results'][0]['geometry']['location']['lat']
    lng = json['results'][0]['geometry']['location']['lng']

    s = requests.get('https://api.darksky.net/forecast/4588b8443530f7c04ea4160a434520d3/' + str(lat) + ',' + str(lng))
    json1 = s.json()

    totalsnowfall = 0
    weather = json1['daily']['data']
    for day in weather:
        if 'precipAccumulation' in day:
            totalsnowfall = totalsnowfall + day['precipAccumulation']
    print('Fetching data for ' + row[0])
    print(totalsnowfall)
    if totalsnowfall > MaxSnow:
        MaxSnow = totalsnowfall
        MaxResortName = row[0]
    outputWriter.writerow([row[0], row[1], row[2], totalsnowfall])

outputFile.close()

account_sid = 'AC411c6a78f221cb517097cfdcca9a55db'
auth_token = '049894ce8526ba2ddb744794e193473c'
client = Client(account_sid, auth_token)

message = client.messages.create\
(
    from_='+19082743337',
    body= MaxResortName + ' has the most potential snow with ' + str(MaxSnow),
    to='+19084949958'
)