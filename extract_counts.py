# Import the re module for regular expressions
import re
from datetime import datetime


# Define a function to extract counts from a chat file
def extract_counts(chat_file):
    # Create an empty list to store the dates and counts
    data = []

    # Open the chat file in read mode
    with open(chat_file, 'r', encoding='utf-8') as chat:
        # Loop through each line in the chat file
        for line in chat:
            # Check if the line contains a date and a count
            if re.search(r'\d{1,2}\.\d{1,2}\.\d{4} \d{2}\.\d{2} - .*:\s*(\d+)', line):
                # Extract the date and the count from the line
                date = re.search(r'\d{1,2}\.\d{1,2}\.\d{4}', line).group()
                count = re.search(r':\s*(\d+)', line).group(1)
                # Parse the date string
                date_obj = datetime.strptime(date, '%d.%m.%Y')
                # Check if it's a Wednesday between 20:00 and 21:30
                if date_obj.year == 2023 and date_obj.weekday() == 2 and (20 <= date_obj.hour < 22 or (date_obj.hour == 21 and date_obj.minute == 30)):
                    # Append the date and the count as a tuple to the data list
                    data.append((date, count))

    # Print a table header with column names
    print(f"{'Pvm':<15}{'Lkm':<5}")

    # Loop through each tuple in the data list
    for date, count in data:
        # Print the date and the count in a table row
        print(f"{date:<15}{count:<5}")
    
# Call the function with the name of your chat file
extract_counts('keskiviikot.txt')
