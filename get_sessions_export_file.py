import csv
import mysql.connector
from binascii import unhexlify
from tabulate import tabulate

# Function to convert hexadecimal to plaintext
def hex_to_plaintext(hex_string):
    try:
        return unhexlify(hex_string).decode('utf-8')
    except Exception as e:
        print(f"Error converting hex: {e}")
        return hex_string

db_connection = mysql.connector.connect(
    host="localhost",
    user="thaituan",
    password="tuan89",
    database="testdb"
)

cursor = db_connection.cursor()

cursor.execute("SELECT event_time, user_host, thread_id, server_id, command_type, argument FROM mysql.general_log")

rows = cursor.fetchall()

if not rows:
    print("No data found in mysql.general_log.")
else:
    table_data = []
    for row in rows:
        event_time, user_host, thread_id, server_id, command_type, argument = row
        if isinstance(argument, bytes):
            argument = argument.decode('utf-8')
        if argument.startswith('0x'):
            plaintext_argument = hex_to_plaintext(argument[2:])
        else:
            plaintext_argument = argument
        table_data.append([event_time, user_host, thread_id, server_id, command_type, plaintext_argument])

    headers = ["Time", "User", "Thread ID", "Server ID", "Command", "Argument"]

    print(tabulate(table_data, headers=headers, tablefmt='simple'))

    # Filter by user
    user = 'root'
    filtered_data = [row for row in table_data if user in row[1]]

    # Write to CSV
    with open(f'{user}_query-list.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(filtered_data)
