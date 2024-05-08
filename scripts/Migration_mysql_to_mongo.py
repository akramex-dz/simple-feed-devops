import os
from dotenv import load_dotenv
import mysql.connector
import pymongo
from bson.objectid import ObjectId
from datetime import datetime

# Load environment variables
load_dotenv()

# Connect to MySQL
mysql_db = mysql.connector.connect(
  host=os.getenv('MYSQL_HOST'),
  user=os.getenv('MYSQL_USER'),
  password=os.getenv('MYSQL_PASSWORD'),
  database=os.getenv('MYSQL_DB')
)
mysql_cursor = mysql_db.cursor()

# Connect to MongoDB
mongo_client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
db = mongo_client['user-data-back-up']

now = datetime.now().strftime('%Y%m%d%H%M%S')

# Migrate data from MySQL to MongoDB
for table_name in ['User', 'Follows', 'RefreshToken', '_Follows']:
    # Fetch all rows from the MySQL table
    mysql_cursor.execute(f'SELECT * FROM {table_name}')
    rows = mysql_cursor.fetchall()

    # Get column names from the MySQL table
    column_names = [column[0] for column in mysql_cursor.description]

    # Insert each row into the MongoDB collection
    for row in rows:
        document = {column_names[i]: row[i] for i in range(len(column_names))}
        # Convert 'id' from string to ObjectId
        if 'id' in document:
          # Creating a new ObjectId because the MySQL ID is not a valid ObjectId on mongodb
          # another aproach would be converting te string to a valid ObjectId but it would be a different id and prone to errors 
          document['_id'] = ObjectId() 
          # Store the MySQL ID to not lose existing relationships
          document['mysql_id'] = document.pop('id')  
        db[f'{table_name}{now}'].insert_one(document)
    
    # Drop the old collection
    db[f'{table_name}'].drop()
    
    # Assign the new collection to the old one
    db[f'{table_name}{now}'].aggregate([
        {
            "$merge": {
                "into": f"{table_name}",
                "whenMatched": "replace"
            }
        }
    ])

# Close connections
mysql_cursor.close()
mysql_db.close()
mongo_client.close()