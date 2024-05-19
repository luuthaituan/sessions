import mysql.connector

def connect_to_database(config):
    try:
        # Establish a database connection
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        return cnx, cursor
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None, None

def execute_query(cursor, query):
    try:
        # Execute the SQL query
        cursor.execute(query)
        # Fetch all the records
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def print_results(results):
    # Print the results
    print("User | Host | DB | Command | Time Connected")
    print("-" * 50)
    for (user, host, db, command, time) in results:
        print(f"{user} | {host} | {db} | {command} | {time}")

def close_connection(cnx, cursor):
    # Close the cursor and the connection
    cursor.close()
    cnx.close()

if __name__ == "__main__":
    # Replace 'your_username' and 'your_password' with your database username and password
    config = {
        'user': 'thaituan',
        'password': 'tuan89',
        'host': 'localhost',
        'database': 'performance_schema',  # Changed to performance_schema
        'raise_on_warnings': True,
    }

    cnx, cursor = connect_to_database(config)
    if cnx and cursor:
        query = ("SELECT USER, HOST, DB, COMMAND, TIME FROM processlist;")  # Changed to processlist
        results = execute_query(cursor, query)
        if results:
            print_results(results)
        close_connection(cnx, cursor)
