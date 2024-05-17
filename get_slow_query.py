import csv
import mysql.connector

# Function to connect to the MySQL database
def connect_to_database(host, user, password, database):
    try:
        return mysql.connector.connect(host=host, user=user, password=password, database=database)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Function to fetch slow queries from the slow_log table
def fetch_slow_queries(cursor):
    cursor.execute("SELECT * FROM mysql.slow_log")
    return cursor.fetchall()

# Function to write slow queries to a CSV file
def write_to_csv(file_name, data, headers):
    with open(file_name, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)

# Main function
def main():
    db_connection = connect_to_database(host="localhost", user="thaituan", password="tuan89", database="mysql")
    if db_connection is not None:
        cursor = db_connection.cursor()
        slow_queries = fetch_slow_queries(cursor)
        if slow_queries:
            headers = [i[0] for i in cursor.description]  # Get the headers from the cursor description
            write_to_csv('slow_queries.csv', slow_queries, headers)
            print("Slow queries have been written to 'slow_queries.csv'.")
        else:
            print("Không có truy vấn chậm.")
        cursor.close()
        db_connection.close()

if __name__ == "__main__":
    main()
