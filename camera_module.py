import subprocess

# Specify the command to be executed
def capture():
    command = "libcamera-still -o /home/r2dc/watersense/paperstrip.jpg"

# Run the command
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Print the command output
    print("Command Output:")
    print(result.stdout)

    # Print the return code
    print("\nReturn Code:", result.returncode)
