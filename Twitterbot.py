import tweepy
import time
import MySQLdb
import mysql.connector

db_connection = mysql.connector.connect(
host="127.0.0.1",
user="twitter_user",
passwd="_Twit@user1#",
database ='last',
auth_plugin = 'mysql_native_password',
)

cur=db_connection.cursor()
cur.execute("SELECT * FROM users")
data = cur.fetchall()

# while True:
# try:
for new_data_me in data:
      # time.sleep(2)
      print(new_data_me)
      token=new_data_me[2]
      token_secret=new_data_me[3]
      message=new_data_me[5]
      last_id=new_data_me[6]



      API_KEY="VXPUp8XJrpPWthVATRWiqGUvl"
      API_SECRET="dKDZvazvzsNHDGHipaUbTfOTYDLCNBXUSTm8GjWIO4qJIGAQ8j"
      ACCESS_TOKEN = token
      ACCESS_SECRET =token_secret



      auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
      auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

      try:
        api = tweepy.API(auth, wait_on_rate_limit=True,
            wait_on_rate_limit_notify=True)

        time.sleep(2)

      except:
        print('couldnotauthenticate')

      while True:
          
          try:
            last_dms = api.list_direct_messages(1)
          
          except:
            print('coul not authenticate')

          if last_dms:
            sender=last_dms[0].message_create['sender_id']
            latest_id=last_dms[0].id
            print(last_dms)

            try:
                  
              if int(latest_id) > (last_id):
                api.send_direct_message(sender,message)
                print('sentmessage')
                cur.execute("""
                    UPDATE users
                    SET last_id=%s
                    WHERE token_secret=%s
                """, (latest_id,token_secret))
                db_connection.commit()
                print(cur.rowcount, "record(s) affected")

            except:
              print('couldnotsenddm')

          else:
            print('couldnotfetchlastdm')

          break



      print('done')
      time.sleep(10)

# except:
    # print('did not work')






