import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="tweets_db"
)
mycursor = mydb.cursor()


def save_tweets(data):
    data_to_insert = []
    sql = "INSERT INTO tweets_db.tweets(tweet_id, user_id, retweets, favorites, text, user_screen_name, user_name, created_at, sentiment, group_key) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    for x in data:
        data_to_insert.append((x['tweet_id'], x['user_id'], x['retweets'], x['favorites'], x['text'],
                               x['user_screen_name'], x['user_name'], x['created_at'], x['sentiment'], x['group_key']))
    mycursor.executemany(sql, data_to_insert)
    mydb.commit()
    print(mycursor.rowcount, "was inserted.")
