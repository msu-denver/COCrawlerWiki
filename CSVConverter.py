import csv
import os
import re

# Directory containing your text files
directory_path = 'C:\\Users\\lukef\\Desktop\\EXAMPLES'

# Specify the output directory for CSV files
output_directory_path = 'C:\\Users\\lukef\\Desktop\\EXAMPLES\\CSV_OUTPUT'  # Change this path to your desired output directory

# Ensure the output directory exists, create it if it does not
if not os.path.exists(output_directory_path):
    os.makedirs(output_directory_path)

def extract_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Initialize default values for URL, summary, and coordinates
    url = 'N/A'
    summary = 'N/A'
    coordinates = 'N/A'
    
    # Extract URL
    url_match = re.search(r'URL: (.+)', content)
    if url_match:
        url = url_match.group(1).strip()
    
    # Extract Coordinates
    coordinates_match = re.search(r'==Coordinates ==\s*(.+)', content)
    if coordinates_match:
        coordinates = coordinates_match.group(1).strip().split('\n')[0]  # Get the first line after "==Coordinates =="
    
    # Extract Summary
    summary_match = re.search(r'\sSummary: “(.+?)”', content, re.DOTALL)
    if summary_match:
        summary = summary_match.group(1).strip().replace('\n', ' ')

    return url, summary, coordinates

# Iterate over each file in the directory and create a corresponding CSV file
for filename in os.listdir(directory_path):
    if filename.endswith(".txt"):  # Consider only text files
        file_path = os.path.join(directory_path, filename)
        
        # Modify here to save CSVs to the specified output directory
        output_csv_path = os.path.join(output_directory_path, filename.replace('.txt', '.csv'))
        
        # Extract information from the text file
        url, summary, coordinates = extract_info(file_path)
        
        # Open the CSV file for writing in the output directory
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['URL', 'Summary', 'Coordinates'])
            writer.writerow([url, summary, coordinates])

print('All files processed and saved as individual CSV files in the specified directory.')
