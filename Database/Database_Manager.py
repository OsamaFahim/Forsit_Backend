import mysql.connector
import os
from dotenv import load_dotenv
from pathlib import Path

#This singelton class would be used to create tables, execute queries 
class Database_Manager(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database_Manager, cls).__new__(cls)
            
            # I have created the .env.example file so that user can set up his enviroment variables
            # from his SQL connection and reuse the same logic
            # Note: the code first finds the enviroment folder which is already created and contains .env.example file which needs to be 
            # renamed to .env first

            # This line will get the path to /enviroment/.env (after renaiming and setting up your own
            # variables), basically constructing the absolute path to .env file
            env_path = Path(__file__).resolve().parent.parent / "environment" / ".env"
        
            #Loading the enviroment files to use its variables
            load_dotenv(dotenv_path = env_path)

            #setting up the configurations from the .env
            cls.DB_HOST = os.getenv("HOST")
            cls.DB_PASSWORD = os.getenv("PASSWORD")
            cls.DB_USER = os.getenv("USER")
            cls.DB_NAME = os.getenv("NAME")

            # Connecting with MYSQL, I am specifically not mentioning the Database, so that if the database does not exsist we create it first for
            # convenience of the user
            cls.connection = mysql.connector.connect(host = cls.DB_HOST, user = cls.DB_USER, password = cls.DB_PASSWORD)     
            cls.connection.autocommit = True
            cls.cursor = cls.connection.cursor()

            #firstly checking that if the DB named "DB_NAME" is already created or not
            cls.execute_query("SHOW DATABASES")
            databases = [db[0] for db in cls.cursor.fetchall()]
            if cls.DB_NAME not in databases:
                cls.execute_query(f"CREATE DATABASE {cls.DB_NAME}")
                print(f"New databases has been created with name{cls.DB_NAME}")
            else:
                print(f"The Databased named {cls.DB_NAME} was already created")

            #Now we are reconnecting, as the "DB_NAME" has been specified now and not previosuly
            cls.connection = mysql.connector.connect(host = cls.DB_HOST, user = cls.DB_USER,password = cls.DB_PASSWORD,database = cls.DB_NAME)
            cls.cursor = cls.connection.cursor()

                   
        return cls.instance
    
    #Making it class method 
    @classmethod
    def execute_query(cls, query_string):
        cls.cursor.execute(query_string)


#Checking if the singelton class is even working or not
#db = Database_Manager()
    
    
