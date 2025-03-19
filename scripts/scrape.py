import csv
import datetime
import requests
from bs4 import BeautifulSoup

CSV_FILE = "./archive/data.original.csv"
URL = "https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp"

def get_latest_date(csv_file):
    """Extracts the latest date from the CSV file."""
    latest_date = None
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0]:  # Ensure year exists
                year = int(row[0])
                month = row[2].strip('"') if len(row) > 2 else "Jan"
                day = int(row[1]) if len(row) > 1 and row[1] else 1
                date = datetime.date(year, convert_month_to_int(month), day)
                if latest_date is None or date > latest_date:
                    latest_date = date
    return latest_date

def convert_month_to_int(month_str):
    """Converts month name to a number."""
    months = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "June": 6,
        "July": 7, "Aug": 8, "Sep": 9, "Sept": 9, "Oct": 10, "Nov": 11, "Dec": 12
    }
    return months.get(month_str, 1)

def scrape_interest_rates(start_date):
    """Scrapes Bank of England interest rate data from the given start date."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    new_data = []
    rows = soup.find_all("tr")[1:]  # Skip header row

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 2:
            continue

        date_str = cols[0].text.strip()
        rate_str = cols[1].text.strip()

        try:
            # Adjust date parsing for format: '05 Feb 09'
            date_obj = datetime.datetime.strptime(date_str, "%d %b %y").date()
            rate = float(rate_str.replace("%", ""))  # Convert to decimal

            if date_obj > start_date:
                new_data.append([date_obj.year, date_obj.day, date_obj.strftime("%b"), rate])
        except ValueError:
            continue  # Skip invalid rows

    print(new_data)
    # Sort data in ascending order before returning
    new_data.sort()
    
    return new_data

def append_to_csv(csv_file, data):
    """Appends new data to CSV file with correct formatting, avoiding triple quotes."""
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)  # Ensures correct quoting
        last_year = None

        for row in data:
            year, day, month, rate = row

            # If the year is the same as the previous row, leave it blank
            if last_year == year:
                writer.writerow(["", day, month, rate])
            else:
                writer.writerow([year, day, month, rate])
                last_year = year  # Update last known year



if __name__ == "__main__":
    latest_date = get_latest_date(CSV_FILE)
    print(f"Latest date in CSV: {latest_date}")

    new_rates = scrape_interest_rates(latest_date)
    
    if new_rates:
        append_to_csv(CSV_FILE, new_rates)
        print(f"Added {len(new_rates)} new entries to {CSV_FILE}.")
    else:
        print("No new data found.")