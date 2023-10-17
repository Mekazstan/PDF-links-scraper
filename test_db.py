import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('pdf_data.db')
cursor = conn.cursor()

# Execute a query to fetch all data from the table (assuming the table name is 'pdf_data')
cursor.execute('SELECT * FROM pdf_data')

# Fetch all rows from the executed query
rows = cursor.fetchall()

# You can iterate through the rows to access the data
for row in rows:
    # The row variable contains the data from each row
    print(row)

# Close the database connection when you're done
conn.close()
