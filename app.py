from flask import Flask, redirect, url_for,render_template,request,session
from flask_mysqldb import MySQL
import tweepy
import json
app=Flask(__name__)
app.config['SECRET_KEY']='thisisme'

#################################
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'twitter_user'
app.config['MYSQL_PASSWORD']='_Twit@user1#'
app.config['MYSQL_DB']='last'
###################################

mysql=MySQL(app)

@app.route('/')




@app.route('/login', methods=["GET","POST"])
def First_page():
    cur=mysql.connection.cursor()
    if request.method =='POST':
        username=str(request.form['email_me']).encode('ascii', 'ignore')
        password=str(request.form['Password']).encode('ascii', 'ignore')
        print(username)

        # cur.execute('SELECT * FROM users')
        # data = cur.fetchall()
        # print(username)
        cur.execute("SELECT * FROM users WHERE username=% s AND password= % s", (username, password))
        account=cur.fetchone()
        if account: 
            session['loggedin'] = True
            session['username'] = username
            session['user_id'] = account[0]



            return redirect('/home')
        else:
            cur.execute("INSERT INTO users(username,password) VALUES (%s,%s)",[username,password])
            mysql.connection.commit()

            cur.execute("SELECT * FROM users WHERE username=% s AND password = % s", (username, password))
            account=cur.fetchone()
            session['username'] = username
            session['user_id'] = account[0]

            return redirect(url_for('home'))



        # if username==str:
        #     redirect(url_for('Home'))

        



    return render_template("home.html")

@app.route('/home')
def home():

    return render_template('home.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/home')



@app.route('/api/callback')
def api_callback():
    cur=mysql.connection.cursor()
    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')
    print("oauth_token: ", oauth_token)
    print("oauth_verifier: ", oauth_verifier)

    auth = tweepy.OAuthHandler("VXPUp8XJrpPWthVATRWiqGUvl","dKDZvazvzsNHDGHipaUbTfOTYDLCNBXUSTm8GjWIO4qJIGAQ8j")
    auth.request_token = { "oauth_token": oauth_token, "oauth_token_secret": oauth_verifier }
    auth.get_access_token(oauth_verifier)
    
    # print(auth.access_token)
    # print(auth.access_token_secret)
    # user_id = session['user_id']
    # print(user_id)


    api = tweepy.API(auth, wait_on_rate_limit=True,
            wait_on_rate_limit_notify=True)
    user = api.me()
    
    cur.execute("SELECT * FROM users WHERE token_access=% s AND token_secret= % s", (auth.access_token, auth.access_token_secret))
    account=cur.fetchone()
    if account: 
        session['loggedin'] = True
        session['username'] = user.screen_name
        session['user_id'] = account[0]
        session['profile'] = user.profile_image_url_https.replace("normal", "bigger")



        return redirect('/dashboard')
    else:
        cur.execute("INSERT INTO users(username,token_access,token_secret) VALUES (%s,%s,%s)",[user.screen_name,auth.access_token,auth.access_token_secret])
        mysql.connection.commit()

        cur.execute("SELECT * FROM users WHERE token_access=% s AND token_secret = % s", (auth.access_token, auth.access_token_secret))
        account=cur.fetchone()
        session['loggedin'] = True
        session['username'] = user.screen_name
        session['user_id'] = account[0]
        session['profile'] = user.profile_image_url_https.replace("normal", "bigger")



    return redirect('/dashboard')





@app.route('/api/authorize_twitter')
def authorize_twitter():

    auth = tweepy.OAuthHandler("VXPUp8XJrpPWthVATRWiqGUvl","dKDZvazvzsNHDGHipaUbTfOTYDLCNBXUSTm8GjWIO4qJIGAQ8j","https://twitterautoreply.com/api/callback")

    try:
        redirect_url = auth.get_authorization_url()
        print("REDIRECT: ", redirect_url)
        # session.set('request_token', auth.request_token['oauth_token'])
        return redirect(redirect_url)
    except tweepy.TweepError:
        print('Error! Failed to get request token.')
        return json.dumps({"message":"Failed to get request token"})




@app.route('/dashboard',methods=["GET","POST"])
def dashboard():
    cur=mysql.connection.cursor()
    if request.method =='POST':
        message=request.form['messages'].encode('ascii')


        # cur.execute("INSERT INTO messages(message) VALUES (%s)",[message])
        # mysql.connection.commit()

        user_id = session['user_id']

        cur.execute("""
            UPDATE users
            SET messages=%s
            WHERE id=%s
        """, (message,user_id))
        mysql.connection.commit()

    user_id = session['user_id']
    

    cur.execute("SELECT * FROM users WHERE id=%s",(user_id,))
    data=cur.fetchall()

    # print_me=data[0][5]
    # print(print_me)

        # print(type(message))
    
    username = session['username']
    user_image = session['profile']
    # data_us=data
    return render_template('dashboard.html',username=username,user_image=user_image,message=data)







    

if __name__=='__main__':
    app.run(debug=True)
