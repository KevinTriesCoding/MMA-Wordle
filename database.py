import psycopg2

def create_connection():
    # Connects me to my postgresql db
    connection = None
    try:
        connection = psycopg2.connect (
            host = "localhost",
            database = "ufc_fighters",
            user = "", #idk what my username is
            password = "" #idk what my password is
        )

        print ("Database connection established.")
    except psycopg2.Error as e:
        print(f"Error connection to the database: {str(e)}")
    return connection

def create_tables (connection):
    #Creates tables for the db
    try:
        cursor = connection.cursor()
        cursor.execute('''
 CREATE TABLE IF NOT EXISTS fighters (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                division VARCHAR(255),
                country VARCHAR(255),
                age INTEGER,
                height VARCHAR(255),
                nickname VARCHAR(255),
                mma_record VARCHAR(255)
                       ''')
        
        connection.commit()
        print ("Tables created successfully.")
    except psycopg2.Error as e:
        print(f"Error connection to the database: {str(e)}")
    
def insert_fighter (connection, fighter_data):
    # Inserts the fighter information into the db
    try:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO fighters (name, division, country, age, height, nickname, mma_record)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', fighter_data)
        connection.commit()
    except psycopg2.Error as e:
        print(f"Error inserting fighter record: {str(e)}")