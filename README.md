"# simple-feed-devops" 

Here you'll find some usefull script I realised under my simple-feed project, I'll add intresting stuff now and then.

# Running MongoDb to MySQL Migration Script

Follow these steps to run the migration script:

1. **Install the necessary libraries**:
   If you haven't already, install the required Python libraries with pip:
   ```bash
   pip install pymongo mysql-connector-python
   ```

2. **Set up your environment variables:**:
   The script uses environment variables for the MongoDB and MySQL connection details. Set these in your terminal before running the script:
   ```bash
   export MONGODB_DB=your_mongodb_database
   export MYSQL_HOST=localhost
   export MYSQL_USER=your_mysql_user
   export MYSQL_PASSWORD=your_mysql_password
   export MYSQL_DB=your_mysql_database
   ```

3. **Run the script**:
   Navigate to the directory containing the script and run it with Python:
   ```bash
   python migration_script.py
   ```

Remember to replace the placeholders with your actual data.

