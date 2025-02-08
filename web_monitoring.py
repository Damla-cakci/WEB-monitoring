import time
import requests
import csv
from datetime import datetime

def check_website(url):
    try:
        start_time = time.time()
        response = requests.get(url, timeout=5)
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        if response.status_code == 200:
            return "UP", response_time
        else:
            return "DOWN", None
    except requests.exceptions.RequestException:
        return "DOWN", None

def log_data(url, status, response_time):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("website_log.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, url, status, response_time])

def monitor_website(url, interval=60):
    while True:
        status, response_time = check_website(url)
        log_data(url, status, response_time)
        print(f"{url} is {status}, response time: {response_time if response_time else 'N/A'} ms")
        time.sleep(interval)

def filter_logs_by_website(website_url):
    print(f"Logs for {website_url}:")
    with open("website_log.csv", "r") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if row[1] == website_url:
                print(row)

if __name__ == "__main__":
    while True:
        print("1. Monitor a website")
        print("2. Filter logs by website")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            url = input("Enter the website URL (e.g., https://google.com): ")
            try:
                monitor_website(url, interval=60)
            except KeyboardInterrupt:
                print("\nStopping monitoring.")
        elif choice == "2":
            website_url = input("Enter the website URL to filter logs (e.g., https://google.com): ")
            filter_logs_by_website(website_url)
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please try again.")
