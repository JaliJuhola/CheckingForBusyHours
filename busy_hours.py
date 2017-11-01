#!/usr/bin/env python3
import sys
import requests
import pandas as pd
import json
import string

def getDailyStats(startDate, endDate, accessToken):
    """
    Returns json type daily statistics
    """
    queryStrings = {'start_date': startDate, 'end_date': endDate}
    headers = {'Authorization': 'Token ' + accessToken, 'Accept': 'application/json'}
    r = requests.get('https://api.giosg.com/api/reporting/v1/rooms/84e0fefa-5675-11e7-a349-00163efdd8db/chat-stats/daily/', params=queryStrings, headers=headers)
    return r.json()

def getHourlyStats(date, accessToken):
    """
    Returns json type hourly statistics
    """
    queryStrings = {'start_date': date, 'end_date': date}
    headers = {'Authorization': 'Token ' + accessToken, 'Accept': 'application/json'}
    r = requests.get('https://api.giosg.com/api/reporting/v1/rooms/84e0fefa-5675-11e7-a349-00163efdd8db/user-presence-counts', params=queryStrings, headers=headers)
    return r.json()

def getThreeLargest(dailyStats):
    """
    Returns three greatest conversation_count rows
    """
    dailyStatsStr = json.dumps(dailyStats['by_date'])
    pdDailyStats = pd.read_json(dailyStatsStr)
    result = pdDailyStats.sort_values(by='conversation_count', ascending=False).head(3)
    return result.to_json(orient="index")


#running program

#Default values (access token hidden)
start_date = "2017-05-01"
end_date = "2017-06-15"
access_token = ""

if len(sys.argv) == 4:  # Reading arguments if exists
    start_date = sys.argv[1]
    end_date = sys.argv[2]
    access_token = sys.argv[3]

#Reads daily statistics and finds three greatest conversation_count rows
dailyStats = getDailyStats(start_date, end_date, access_token) 
threeLargest = getThreeLargest(dailyStats) 
threeLargest = json.loads(threeLargest) 

#Printing results
for identifier in threeLargest:

    #Printing daily information
    print('On: {date} there were {chat_count} chats'.format(date=dailyStats['by_date'][(int)(identifier)]['date'], chat_count=threeLargest[identifier]['conversation_count']))
    print("-----------------")

    #getting and printing hourly stats
    hourlyStats = getHourlyStats(str(dailyStats['by_date'][(int)(identifier)]['date']), access_token)
    for hour in hourlyStats['hourly']:
       print('{hour}:00 there was  there were {user_count} users present'.format(hour=hour['hour_of_day'], user_count=hour['user_count']))

    #Two empty rows for esthetics
    print()
    print()

