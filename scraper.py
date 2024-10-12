import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# Function to fetch the page content
def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        print("Page fetched successfully")
        return response.text
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

# Function to parse the HTML and extract data
def parse_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extracting rows from the table
    rows = soup.select('div#SpecialContentHolder table tr')
    print(f"Found {len(rows)} rows in the table.")
    
    data = {}
    if len(rows) == 0:
        print("No rows found in the table. Check the page structure or selector.")
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) == 2:  # Ensuring there are two columns
            label = cols[0].text.strip()
            value = cols[1].text.strip()
            print(f"Extracted label: '{label}' with value: '{value}'")

            if "zarejestrowanych" in label.lower():
                data['registered_businesses'] = value
            elif "wznowionych" in label.lower():
                data['resumed_businesses'] = value
            elif "zawieszonych" in label.lower():
                data['suspended_businesses'] = value
            elif "zamkniętych" in label.lower():
                data['closed_businesses'] = value

    # Check if all data points were collected
    if not data:
        print("No data extracted. Check the page structure or selectors.")
    
    # Adding the current date
    data['date'] = datetime.now().strftime('%Y-%m-%d')

    return data

# Function to save data to a CSV file
def save_to_csv(data, filename="business_data.csv"):
    file_exists = False
    try:
        with open(filename, 'r'):
            file_exists = True
    except FileNotFoundError:
        pass
    
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        
        # Write headers only if the file doesn't exist
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(data)
    print(f"Data saved to {filename}.")

# Main function to run the scraper
def run_scraper():
    url = "https://prod.ceidg.gov.pl/ceidg.cms.engine/Template/Includes/StatisticPage.aspx?Id=3814CF7F-246D-4CC3-8B89-88AA1395DF1D"
    html_content = fetch_data(url)
    if html_content:
        data = parse_data(html_content)
        print(f"Extracted data: {data}")
        save_to_csv(data)

if __name__ == "__main__":
    run_scraper()
