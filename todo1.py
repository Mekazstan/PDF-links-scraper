import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os
import re

# Set the path to the ChromeDriver executable
chrome_driver_path = Service(r"/home/chukwuemeka/Downloads/selenium-setup/chromedriver")
options = webdriver.ChromeOptions()
# options.add_argument('--headless')

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=chrome_driver_path, options=options)

# Define your SQLite database connection
db_path = "pdf_data.db"  # SQLite database file path

# Establish a connection to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
# Create a table to store the scraped data
create_table_query = """
CREATE TABLE IF NOT EXISTS pdf_data (
    id INTEGER PRIMARY KEY,
    title TEXT,
    pdf_link TEXT
);
"""
cursor.execute(create_table_query)
conn.commit()
        
base_url = "https://libgen.is/search.php?"

list_of_topics = ["codebase"]

def handle_table_body(table_body_element):
    table_rows = table_body_element.find_elements(By.TAG_NAME, "tr")
    return table_rows

def handle_table_data(table_data):
    is_english = table_data[6]
    if is_english.text.lower() == "english":
        # print "is english"
        pdf_column = table_data[8]
        if pdf_column.text == "pdf":
            # print "is pdf"
            book_tag = table_data[2]
            title_tag = book_tag.text.strip().replace('\n', ' ').replace(',', '')
            book_title = re.sub(r'\d', '', title_tag)
            link_element = table_data[9].find_element(By.TAG_NAME, "a")
            book_link = link_element.get_attribute("href")
            return book_title, book_link
    return None, None

def scrape_links(driver, conn, cursor):
    pdfs_div = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))

    if pdfs_div:
        tbody_elements = driver.find_elements(By.TAG_NAME, "tbody")
        if len(tbody_elements) >= 4:
            try:
                # For single page
                table_body_element = tbody_elements[2]
                table_rows = handle_table_body(table_body_element)
                if len(table_rows) <= 1:
                    raise Exception("No data found in the table for a single page")
                print(f"The total items on this page = {len(table_rows)}")
            except:
                # For multiple pages
                table_body_element = tbody_elements[3]
                table_rows = handle_table_body(table_body_element)
                print(f"The total items on this page = {len(table_rows)}")

            for row in table_rows:
                table_data = row.find_elements(By.TAG_NAME, "td")
                book_title, book_link = handle_table_data(table_data)
                if book_title and book_link:
                    ####### VALIDATION TEST ###########
                    # Check if the PDF link already exists in the SQLite database
                    select_query = "SELECT id FROM pdf_data WHERE pdf_link = ?;"
                    cursor.execute(select_query, (book_link,))
                    existing_data = cursor.fetchone()
                    if not existing_data:
                        # PDF link doesn't exist, insert the data into the SQLite database
                        insert_query = "INSERT INTO pdf_data (title, pdf_link) VALUES (?, ?);"
                        cursor.execute(insert_query, (book_title, book_link))
                    else:
                        print(f"PDF link already exists: {book_link}")
            conn.commit()
        else:
            print("Not OK")

def run():
    for topic in list_of_topics:        
        scraped_pages = 1
        while scraped_pages <= 100:
            url = f"{base_url}&req={topic}&res=100&page={scraped_pages}"
            driver.get(url)
            print(f"Query successfully submitted for {topic}")

            print("\n")
            print(f"Topic: {topic}")

            time.sleep(2)
            # scraping function [Should take the number of links to be scraped]
            scrape_links(driver, conn, cursor)
            scraped_pages += 1

            table_tags = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            table_elements = driver.find_elements(By.TAG_NAME, "table")
            if len(table_elements) < 6:
                break
            else:
                continue

        # Close the SQLite connection
        conn.close()
        
    # Close the WebDriver
    driver.quit()
    print("Scraper ran successfully.")
   
   
if __name__ == "__main__":
    run()
