import sqlite3
from bs4 import BeautifulSoup
import requests

# Define your SQLite database connection parameters
db_path = "pdf_data.db"  # SQLite database file path

# Establish a connection to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Select data from the SQLite database
select_query = "SELECT id, pdf_link FROM pdf_data"
cursor.execute(select_query)
rows = cursor.fetchall()

for row in rows:
    pdf_id, link = row
    # Skip the request if pdf_url already ends with ".pdf"
    if link.endswith(".pdf"):
        print(f"PDF link for id {pdf_id} already ends with '.pdf'. Skipping.")
        continue

    try:
        response = requests.get(link)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            download_div = soup.find("div", id="download")
            if download_div:
                h2_element = download_div.find("h2")
                link_tag = h2_element.find("a")
                href = link_tag.get("href")

                # Update the database with the new PDF link
                update_query = "UPDATE pdf_data SET pdf_link = ? WHERE id = ?;"
                cursor.execute(update_query, (href, pdf_id))
                conn.commit()
                print(f"Updated PDF link for id {pdf_id}: {href}")
            else:
                print(f"No download link found for id {pdf_id}")
        else:
            print(f"Failed to fetch HTML content for id {pdf_id}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request for id {pdf_id}: {e}")

# Close the SQLite connection
conn.close()

print("Done updating PDF links in the database.")
