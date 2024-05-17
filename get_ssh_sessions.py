import subprocess

def get_ssh_sessions():
    try:
        # Run 'who' command to get current SSH sessions
        result = subprocess.run(['who'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        # Decode the output
        output = result.stdout.decode()

        # Split the output into lines
        lines = output.strip().split('\n')

        # Print each line
        for line in lines:
            print(line)

    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

# Call the function
get_ssh_sessions()