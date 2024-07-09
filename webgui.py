from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import tempfile
import shutil
import concurrent.futures
import os

# Function to create a temporary directory in the current project path
def create_temp_dir_in_project():
    project_path = os.path.dirname(os.path.abspath(__file__))  # Get current script's directory
    temp_dir_path = os.path.join(project_path, 'temp_user_data')  # Path for temporary directory
    os.makedirs(temp_dir_path, exist_ok=True)  # Create the directory if it doesn't exist
    return temp_dir_path

# Function to remove a temporary directory
def remove_temp_dir(path):
    try:
        shutil.rmtree(path)
    except OSError as e:
        print(f"Error: {path} : {e.strerror}")

# Function to locate Chrome WebDriver relative to script's directory
def get_chromedriver_path():
    project_path = os.path.dirname(os.path.abspath(__file__))  # Get current script's directory
    driver_filename = 'chromedriver'  # Adjust for your WebDriver filename
    driver_path = os.path.join(project_path, driver_filename)
    return driver_path

# Function to monitor a single URL
def monitor_url(url):
    # Get Chrome WebDriver path relative to the script's directory
    driver_path = get_chromedriver_path()
    
    # Create a temporary user data directory in the project path
    temp_user_data_dir = create_temp_dir_in_project()

    # Set up Chrome options to use the temporary user data directory
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"--user-data-dir={temp_user_data_dir}")

    # Initialize the WebDriver with the Chrome options
    driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)

    try:
        # Open the web page
        driver.get(url)
        
        # Wait for the page to load completely (adjust as necessary)
        time.sleep(5)
        
        # Find the console input element (replace with the actual element selector)
        console_input = driver.find_element(By.ID, 'console-input')  # Example selector
        
        # Record the start time
        start_time = time.time()
        
        # Send a command to the console
        console_input.send_keys('your-command-here')
        console_input.send_keys(Keys.RETURN)
        
        # Wait for the response (adjust as necessary)
        time.sleep(2)
        
        # Find the console output element (replace with the actual element selector)
        console_output = driver.find_element(By.ID, 'console-output')  # Example selector
        
        # Record the end time
        end_time = time.time()
        
        # Calculate the response time
        response_time = end_time - start_time
        print(f"Response time for {url}: {response_time} seconds")
        
    finally:
        # Close the WebDriver
        driver.quit()
        # Remove the temporary user data directory
        remove_temp_dir(temp_user_data_dir)

# List of URLs to monitor
urls = [
    'http://example.com/page1',
    'http://example.com/page2',
    'http://example.com/page3',
    # Add more URLs as needed
]

# Monitor each URL in parallel
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(monitor_url, urls)
