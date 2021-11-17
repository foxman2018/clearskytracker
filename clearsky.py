#!/usr/bin/env python3

import requests
import json
import smtplib
import datetime

apiKey = 'a8ae93f6bb409f9812eoiqjld'
date = datetime.datetime.today().strftime('%Y%m%d')

def getWeatherData(lon, lat, email):
    url = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}&units=metric'.format(lon, lat, apiKey)
    r = requests.get(url)
    response = json.loads(r.text)
    if response['cod'] == '200':
        parseData(response, email, lon, lat)
    else:
        logText = 'Error retrieving weather data from API - ({}) {}'.format(response['cod'], response['message'])
        writeLog(logText)
        exit()

def getLunarData(lon, lat, date):
    url = 'https://api.solunar.org/solunar/{},{},{},0'.format(lat, lon, date)
    r = requests.get(url)
    response = json.loads(r.text)
    return response

def parseData(data, email, lon, lat):
    list = data['list']
    i = 0
    j = 0
    details = ''

    for l in list:
        i = i + 1
        desc = l['weather'][0]['main']
        time = l['dt_txt']
        messageLine = '{} - {}'.format(time, desc)
        details = '{}\r{}'.format(details, messageLine)
        if desc == 'Clear':
            j = j + 1
        if i == 4:
            break

    lunarData = getLunarData(lon, lat, date)

    message = 'The weather outlook for the next few hours is: \r{}\r\r\rMoon/Sun details:\r\rMoonrise - {}\rMoonset - {}\rMoon Illumination - {}\rMoon Phase - {}\r\rSunrise - {}\rSunset - {}'.format(details, lunarData['moonRise'], lunarData['moonSet'], str(round(lunarData['moonIllumination'], 4)), lunarData['moonPhase'], lunarData['sunRise'], lunarData['sunSet'])
    if j > 2:
        sendEmail(message, email)

def sendEmail(details, email):
    try:
        sendTo = email
        sentBy = 'Clear Sky Checker <clearskychecker@gmail.com>'
        subject = 'Looks like the sky is clear tonight!'
        message = 'Subject: {}\n\n{}'.format(subject, details)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login('clearskychecker@gmail.com', 'abc123')
        server.sendmail(sentBy, sendTo, message)
        server.quit()
        print('Email sent...')
        logText = 'Clear Sky reminder sent to {}'.format(email)
        writeLog(logText)
    except Exception as e:
        logText = 'Error sending email to {} - {}'.format(email, e)
        writeLog(logText)

def writeLog (logText):
    now = datetime.datetime.now() 
    logText = '{} : {}\r'.format(now, logText)
    text_file = open('sendlog.txt', 'a')
    text_file.write(logText)
    text_file.close()

getWeatherData('-6.031830', '48.9872913', 'email@email.com')

exit()