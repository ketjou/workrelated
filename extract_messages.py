import re
import argparse
from datetime import datetime

def filter_chat(input_file, output_file):
    # Regular expression to match your date-time pattern (D.M.YYYY HH.mm)
    date_time_pattern = re.compile(r'\d{1,2}\.\d{1,2}\.\d{4} \d{2}\.\d{2}')

    # Open the input and output files
    with open(input_file, 'r', encoding='utf-8') as input_chat, open(output_file, 'w', encoding='utf-8') as output_chat:
        for line in input_chat:
            # Check if the line contains a date-time pattern
            match = date_time_pattern.search(line)
            if match:
                # Extract the date-time from the line
                date_time_str = match.group()
                # Parse the date-time string
                date_time = datetime.strptime(date_time_str, '%d.%m.%Y %H.%M')
                # Check if it's a Wednesday between 20:00 and 21:30
                #if date_time.weekday() == 2 and date_time.year == 2023:  # Check for Wednesdays in 2023 (0=Monday, 1=Tuesday, 2=Wednesday)
                 #   if 20 <= date_time.hour <= 21 and date_time.minute <= 30:
                #        output_chat.write(line)
                if date_time.year == 2023 and date_time.weekday() == 2 and 
                    (20 <= date_time.hour < 22 or (date_time.hour == 21 and 
                    date_time.minute == 30)):
                        output_chat.write(line)
                
    print(f"Filtered chat messages have been saved to '{output_file}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter chat messages sent on Wednesdays in 2023 between 20:00 and 21:30.")
    parser.add_argument("input_file", help="Input chat text file")
    parser.add_argument("output_file", help="Output filtered chat text file")
    args = parser.parse_args()

    filter_chat(args.input_file, args.output_file)
