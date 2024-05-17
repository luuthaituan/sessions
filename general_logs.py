import mysql.connector
from binascii import unhexlify
from tabulate import tabulate

# Function to convert hexadecimal to plaintext
def hex_to_plaintext(hex_string):
    try:
        # Convert the hexadecimal string to bytes and then decode to a string
        return unhexlify(hex_string).decode('utf-8')
    except Exception as e:
        # Print an error message if conversion fails
        print(f"Error converting hex: {e}")
        return hex_string  # Return the original hex string if conversion fails

# Establish a database connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="thaituan",  # Replace with your actual username
    password="tuan89",  # Replace with your actual password
    database="testdb"
)

# Create a cursor object
cursor = db_connection.cursor()

# Execute the query to fetch the general log
cursor.execute("SELECT event_time, user_host, thread_id, server_id, command_type, argument FROM mysql.general_log")

# Fetch all the rows
rows = cursor.fetchall()

# Check if rows are fetched
if not rows:
    print("No data found in mysql.general_log.")
else:
    # Prepare the data for tabulate
    table_data = []
    for row in rows:
        event_time, user_host, thread_id, server_id, command_type, argument = row
        # Decode argument to a string if it is bytes
        if isinstance(argument, bytes):
            argument = argument.decode('utf-8')
        # Check if the argument is a hex value
        if argument.startswith('0x'):
            plaintext_argument = hex_to_plaintext(argument[2:])  # Remove the '0x' prefix
        else:
            plaintext_argument = argument  # Assume argument is already plaintext
        table_data.append([event_time, user_host, thread_id, server_id, command_type, plaintext_argument])
    
    # Define the headers
    headers = ["Time", "User", "Thread ID", "Server ID", "Command", "Argument"]
    
    # Print the table using tabulate
    print(tabulate(table_data, headers=headers, tablefmt="pretty"))

# Close the cursor and connection
cursor.close()
db_connection.close()
