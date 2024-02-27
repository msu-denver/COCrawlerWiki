import csv
import os
import psycopg2

# Function to convert coordinates to PostGIS POINT format
def convert_coordinates(coord_str):
    try:
        lat, lon = coord_str.replace('°N', '').replace('°W', '').split()
        lat, lon = float(lat), -float(lon)  # Assuming all longitudes are west (negative)
        return f'SRID=4326;POINT({lon} {lat})'
    except ValueError:
        # Return None if coordinates cannot be parsed
        return None

# Establish database connection details
conn_details = {
    'dbname': 'xxxx',  # Your database name
    'user': 'xxxx',  # Your database user
    'password': 'xxx',  # Your database password
    'host': 'xxxx'  # Your database host
}

insert_query = """
INSERT INTO wiki_articles (summary, coordinates)
VALUES (%s, ST_GeomFromEWKT(%s));
"""

# Directory containing your CSV files
csv_directory_path = 's:\\Web_Crawler\\CSVData'  # Update this path to where your CSV files are located

def process_csv_file(csv_file_path):
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Check if any row in the file has invalid coordinates
        for row in reader:
            if row['Coordinates'].lower() == 'coordinates not found':
                print(f"Skipping {csv_file_path} due to invalid coordinates.")
                return  # Skip this file

        # If all rows have valid coordinates, reset reader and proceed with insertion
        csvfile.seek(0)
        next(reader)  # Skip header

        with psycopg2.connect(**conn_details) as conn:
            with conn.cursor() as cursor:
                for row in reader:
                    coordinates = convert_coordinates(row['Coordinates'])
                    if coordinates is None:  # Double-check for any parsing issues
                        continue
                    cursor.execute(insert_query, (row['Summary'], coordinates))

for filename in os.listdir(csv_directory_path):
    if filename.endswith(".csv"):
        csv_file_path = os.path.join(csv_directory_path, filename)
        process_csv_file(csv_file_path)

print("All valid files processed.")
