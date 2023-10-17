import sqlite3
import csv

# Connect to the SQLite database
conn = sqlite3.connect('pdf_data.db')
cursor = conn.cursor()

# Execute a query to fetch all data from the table (assuming the table name is 'pdf_data')
cursor.execute('SELECT * FROM pdf_data')

# Fetch all rows from the executed query
rows = cursor.fetchall()

# Define the path to the CSV file
csv_file_path = 'pdf_data.csv'

# Open the CSV file for writing
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write the header row based on your table structure (e.g., id, title, pdf_link)
    csv_writer.writerow(['id', 'title', 'pdf_link'])

    # Write data rows
    csv_writer.writerows(rows)

print(f'Data has been exported to {csv_file_path}')

# Close the database connection when you're done
conn.close()

