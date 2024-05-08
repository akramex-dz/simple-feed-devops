import os
from dotenv import load_dotenv
import pymongo
import mysql.connector
from datetime import datetime

# Load environment variables
load_dotenv()

# Connect to MongoDB
mongo_client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
mongo_db = mongo_client[os.getenv('MONGODB_DB')]

# Connect to MySQL
mysql_db = mysql.connector.connect(
  host=os.getenv('MYSQL_HOST'),
  user=os.getenv('MYSQL_USER'),
  password=os.getenv('MYSQL_PASSWORD'),
  database=os.getenv('MYSQL_DB')
)
mysql_cursor = mysql_db.cursor()

# Get current date and time
now = datetime.now().strftime('%Y%m%d%H%M%S')

# Create tables
mysql_cursor.execute(f'CREATE TABLE Post_{now} (id VARCHAR(255), userId VARCHAR(255), content TEXT, createdAt DATETIME, updatedAt DATETIME)')
mysql_cursor.execute(f'CREATE TABLE Comment_{now} (id VARCHAR(255), postId VARCHAR(255), userId VARCHAR(255), content TEXT, createdAt DATETIME, updatedAt DATETIME)')
mysql_cursor.execute(f'CREATE TABLE Like_{now} (id VARCHAR(255), likedId VARCHAR(255), onModel VARCHAR(255), userId VARCHAR(255))')

# Get data from MongoDB
posts = mongo_db['posts'].find({})
comments = mongo_db['comments'].find({})
likes = mongo_db['likes'].find({})

# Transform and insert data into MySQL
for post in posts:
  transformed_data = (
    str(post['_id']),
    post['userId'],
    post['content'],
    post['createdAt'],
    post['updatedAt']
  )
  mysql_cursor.execute(f'INSERT INTO Post_{now} (id, userId, content, createdAt, updatedAt) VALUES (%s, %s, %s, %s, %s)', transformed_data)

for comment in comments:
  transformed_data = (
    str(comment['_id']),
    str(comment['postId']),
    comment['userId'],
    comment['content'],
    comment['createdAt'],
    comment['updatedAt']
  )
  mysql_cursor.execute(f'INSERT INTO Comment_{now} (id, postId, userId, content, createdAt, updatedAt) VALUES (%s, %s, %s, %s, %s, %s)', transformed_data)

for like in likes:
  transformed_data = (
    str(like['_id']),
    str(like['likedId']),
    like['onModel'],
    like['userId'],
  )
  mysql_cursor.execute(f'INSERT INTO Like_{now} (id, likedId, onModel, userId) VALUES (%s, %s, %s, %s)', transformed_data)


# select the last version of post, comments and likes tables and duplicate each table into a new table calles Post, Comment and Like
mysql_cursor.execute('DROP TABLE IF EXISTS Post_latest')
mysql_cursor.execute('DROP TABLE IF EXISTS Comment_latest')
mysql_cursor.execute('DROP TABLE IF EXISTS Like_latest')

mysql_cursor.execute(f'CREATE TABLE Post_latest AS SELECT * FROM Post_{now}')
mysql_cursor.execute(f'CREATE TABLE Comment_latest AS SELECT * FROM Comment_{now}')
mysql_cursor.execute(f'CREATE TABLE Like_latest AS SELECT * FROM Like_{now}')

# Commit changes and close connections
mysql_db.commit()
mysql_cursor.close()
mysql_db.close()
mongo_client.close()