import sys
import requests
import pandas as pd
import json


#Returns json type daily statistics
def getDailyStats(startDate, endDate, accessToken):
    queryStrings = {'start_date': startDate, 'end_date': endDate}
    headers = {'Authorization': 'Token ' + accessToken, 'Accept': 'application/json'}
    r = requests.get('https://api.giosg.com/api/reporting/v1/rooms/84e0fefa-5675-11e7-a349-00163efdd8db/chat-stats/daily/', params=queryStrings, headers=headers)
    return r.json()

#Returns json type hourly statistics
def getHourlyStats(date, accessToken):
    queryStrings = {'start_date': date, 'end_date': date}
    headers = {'Authorization': 'Token ' + accessToken, 'Accept': 'application/json'}
    r = requests.get('https://api.giosg.com/api/reporting/v1/rooms/84e0fefa-5675-11e7-a349-00163efdd8db/user-presence-counts', params=queryStrings, headers=headers)
    return r.json()

#Returns three greatest conversation_count rows
def getThreeLargest(dailyStats):
    dailyStatsStr = json.dumps(dailyStats['by_date'])
    pdDailyStats = pd.read_json(dailyStatsStr)
    result = pdDailyStats.sort_values(by='conversation_count', ascending=True).tail(3)
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
    print("On " + str(dailyStats['by_date'][(int)(identifier)]['date'])  + " there were "+ str(threeLargest[identifier]['chats_from_visitor_count']) +" chats")
    print("-----------------")

    #getting and printing hourly stats
    hourlyStats = getHourlyStats(str(dailyStats['by_date'][(int)(identifier)]['date']), access_token)
    for hour in hourlyStats['hourly']:
        print(str(hour['hour_of_day']) +":00 there was " + str(hour['user_count']) +" users present")
    
    #Two empty rows for esthetics
    print()
    print()
    

