import tweepy
import time
import MySQLdb
import mysql.connector

db_connection = mysql.connector.connect(
host="",
user="",
passwd="",
database ='',
auth_plugin = 'mysql_native_password',
)

cur=db_connection.cursor()
cur.execute("SELECT * FROM users")
data = cur.fetchall()

# while True:
try:
    for new_data_me in data:
        # time.sleep(2)
        # print(new_data_me)
        token=new_data_me[2]
        token_secret=new_data_me[3]
        message=new_data_me[5]



        API_KEY="VXPUp8XJrpPWthVATRWiqGUvl"
        API_SECRET="dKDZvazvzsNHDGHipaUbTfOTYDLCNBXUSTm8GjWIO4qJIGAQ8j"
        ACCESS_TOKEN = token
        ACCESS_SECRET =token_secret



        auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

        api = tweepy.API(auth, wait_on_rate_limit=True,
            wait_on_rate_limit_notify=True)

        time.sleep(2)

        while True:

            last_dms = api.list_direct_messages(1)
            sender=last_dms[0].message_create['sender_id']
            print(last_dms)
            api.send_direct_message(sender,message)
            break



        print('done')
        time.sleep(300)

except:
    print("it didn't work ")






