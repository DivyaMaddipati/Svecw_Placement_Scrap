from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import csv
import time

# Setup WebDriver (Make sure chromedriver is in PATH or specify its location)
driver = webdriver.Chrome()

# URL to scrape
url = "https://svecw.edu.in/placement-details/"

# Open the URL
driver.get(url)
time.sleep(5)  # Wait for the page to load completely

# Output file for the collected data
output_file = "placement_details_complete.csv"

# Extract dropdown options and scrape data
try:
    # Locate the dropdown element
    dropdown = Select(driver.find_element(By.TAG_NAME, 'select'))  # Assuming dropdown uses <select> tag
    
    # Prepare to store table data
    all_table_data = []

    # Iterate through all options in the dropdown
    for option in dropdown.options:
        # Select the current option
        dropdown.select_by_visible_text(option.text)
        print(f"Scraping data for dropdown option: {option.text}")
        time.sleep(3)  # Allow time for table data to load

        # Locate the table
        table = driver.find_element(By.TAG_NAME, 'table')  # Assuming only one table on the page

        # Extract all rows from the table
        rows = table.find_elements(By.TAG_NAME, 'tr')

        # Extract headers for the first dropdown option
        if not all_table_data:
            header_row = rows[0].find_elements(By.TAG_NAME, 'th')
            headers = [header.text.strip() for header in header_row]
            headers.insert(0, 'Category')  # Adding a column for dropdown category
            all_table_data.append(headers)

        # Extract table rows
        for row in rows[1:]:  # Skip header row
            cells = row.find_elements(By.TAG_NAME, 'td')
            row_data = [cell.text.strip() for cell in cells]
            if row_data:  # Ensure non-empty rows
                row_data.insert(0, option.text)  # Add the dropdown category
                all_table_data.append(row_data)

    # Write to CSV file
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(all_table_data)

    print(f"Data successfully scraped and saved to '{output_file}'.")

except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()  # Close the browser
