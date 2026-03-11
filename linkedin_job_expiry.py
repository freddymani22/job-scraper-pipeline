
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.common.exceptions import TimeoutException
from supabase import create_client, Client
from datetime import datetime, timezone, timedelta
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import random
import os
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse, unquote
from dotenv import load_dotenv

# Constants
SYSTEM_ID = 3
is_master_sys = True
IS_RASPBERRY_PI = False  # True = Raspberry Pi, False = Linux laptop
limit_per_req = 10

#Either choose random or order
is_random_job = False
has_order = True
order_by = 'job_posted_on'
order_by_desc = True


# choose any one location
is_global = False
is_india = True
is_us = False

if is_global:
    location_filter = ["neq.India", "neq.United States"]
    CYCLE_TYPE = 'expiry_global'
    country = 'Global'
    filter_type = 'is_expiry_checked'

elif is_india:
    location_filter = ["eq.India"]
    CYCLE_TYPE = 'expiry_india_linkedin'
    country = 'India'
    filter_type = 'is_skipped'

elif is_us:
    location_filter = ["eq.United States"]
    CYCLE_TYPE = 'expiry_us_linkedin'
    country = 'United States'
    filter_type = 'is_skipped'


# Set up local variables for Supabase
load_dotenv()
url = os.environ["SUPABASE_URL"]
key = os.environ["SUPABASE_KEY"]
dynamic_url = f'{url}/rest/v1/rpc/dynamic_query'
supabase: Client = create_client(url, key)

job_table_name = "jobs"
base_url = f"{url}/rest/v1/"
endpoint_url = f"{base_url}jobs"


def job_expired_flag(job_id):
    fixed_date = '1970-01-01'
    current_timestamp = datetime.now(timezone.utc).isoformat()

    supabase.table('jobs').update(
        {'application_closes_on': fixed_date, 'updated_on': current_timestamp}).eq('id', job_id).execute()


def get_final_url_or_original(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
                  "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }

    try:
        res = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        return res.url
    except Exception as e:
        print(e)
        return url

def clean_job_url(job_url, linkedin_id):
    """
    Clean and transform job URLs, with special handling for LinkedIn URLs
    and removal of LinkedIn-related parameters
    """
    # Handle 'Easy apply' case
    if job_url == 'Easy apply':
        return f'https://linkedin.com/jobs/view/{linkedin_id}'

    # Handle LinkedIn authwall URLs
    if job_url.startswith('https://www.linkedin.com/authwall') or \
       job_url.startswith('http://www.linkedin.com/authwall'):
        return f'https://linkedin.com/jobs/view/{linkedin_id}'

    # Parse the URL
    parsed_url = urlparse(job_url)

    # Special handling for LinkedIn URLs
    if 'linkedin.com' in parsed_url.netloc:
        # Get query parameters
        query_params = parse_qs(parsed_url.query)

        # Define terms to remove
        linkedin_terms = ['linkedin']

        # Check for redirect URL
        if 'url' in query_params:
            # Decode the redirect URL
            redirect_url = unquote(query_params['url'][0])

            # Parse the redirect URL
            parsed_redirect_url = urlparse(redirect_url)
            redirect_query_params = parse_qs(parsed_redirect_url.query)

            # Filter out LinkedIn-related parameters from redirect URL
            filtered_redirect_params = {}
            for key, values in redirect_query_params.items():
                # Check if the key contains any LinkedIn-related terms
                if not any(term in key.lower() for term in linkedin_terms):
                    # Check if any value contains LinkedIn-related terms
                    filtered_values = [
                        value for value in values
                        if not any(term in str(value).lower() for term in linkedin_terms)
                    ]

                    # Add to filtered params if values remain
                    if filtered_values:
                        filtered_redirect_params[key] = filtered_values
            print(urlunparse(parsed_redirect_url))
            parsed_redirect_url = get_final_url_or_original((urlunparse(parsed_redirect_url)))
            print('---------------------cleaned_url', parsed_redirect_url)
            parsed_redirect_url = urlparse(parsed_redirect_url)
            # Reconstruct the redirect URL without LinkedIn-related parameters
            cleaned_redirect_url = urlunparse((
                parsed_redirect_url.scheme,
                parsed_redirect_url.netloc,
                parsed_redirect_url.path,
                parsed_redirect_url.params,
                urlencode(filtered_redirect_params, doseq=True),
                parsed_redirect_url.fragment
            ))

            return cleaned_redirect_url

        # If no redirect URL, extract LinkedIn job ID
        path_parts = parsed_url.path.split('/')
        for part in path_parts:
            if part.isdigit():
                return f'https://linkedin.com/jobs/view/{part}'

    # Remove LinkedIn-related query parameters
    query_params = parse_qs(parsed_url.query)

    # Define terms to remove
    linkedin_terms = ['linkedin']

    # Filter out parameters containing LinkedIn-related terms
    updated_query_params = {}
    for key, values in query_params.items():
        # Check if the key contains any LinkedIn-related terms
        if not any(term in key.lower() for term in linkedin_terms):
            # Check if any value contains LinkedIn-related terms
            filtered_values = [
                value for value in values
                if not any(term in str(value).lower() for term in linkedin_terms)
            ]

            # Add to updated params if values remain
            if filtered_values:
                updated_query_params[key] = filtered_values

    # Construct the updated query string
    updated_query_string = urlencode(updated_query_params, doseq=True)

    # Reconstruct the URL with the updated components
    new_url = urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        updated_query_string,
        parsed_url.fragment
    ))

    return new_url


def convert_time_period(text):
    # Define regular expression patterns for days, weeks, hours, months, and years
    days_pattern = r'(\d+)\s+days?'
    weeks_pattern = r'(\d+)\s+weeks?'
    hours_pattern = r'(\d+)\s+hours?\s+ago'
    months_pattern = r'(\d+)\s+months?\s+ago'
    years_pattern = r'(\d+)\s+years?\s+ago'

    print(text, '-----')

    # Check for days pattern in the text
    days_match = re.search(days_pattern, text)
    if days_match:
        return int(days_match.group(1))  # Return the number of days as an integer

    # Check for weeks pattern in the text
    weeks_match = re.search(weeks_pattern, text)
    if weeks_match:
        weeks = int(weeks_match.group(1))
        return weeks * 7  # Convert weeks to days (1 week = 7 days)

    # Check for hours pattern in the text
    hours_match = re.search(hours_pattern, text)
    if hours_match:
        hours = int(hours_match.group(1))
        return hours / 24  # Convert hours to days (1 day = 24 hours)

    # Check for months pattern in the text
    months_match = re.search(months_pattern, text)
    if months_match:
        months = int(months_match.group(1))
        return months * 30  # Convert months to days (assuming average 30 days per month)

    # Check for years pattern in the text
    years_match = re.search(years_pattern, text)
    if years_match:
        years = int(years_match.group(1))
        return years * 365  # Convert years to days (assuming 365 days per year)

    # No recognized time pattern found
    return None


def parse_date_posted(reposted_ago, scraped_on=None):
    scraped_on = scraped_on or datetime.now()
    days_ago = convert_time_period(reposted_ago)

    if days_ago is not None:
        date_posted = scraped_on - timedelta(days=days_ago)
        return date_posted.date().isoformat()


def check_if_job_expired(job_id, linkedin_job_id, driver):

    new_updated_url = None
    posted_date = None

    is_expired = False  # Initialize is_expired here

    try:
        signup_buttons = driver.find_elements(By.CLASS_NAME, 'sign-up-modal__outlet')
        if len(signup_buttons) > 1:
            sleep(2)

            company_apply_buttons = driver.find_elements(By.CLASS_NAME, 'sign-up-modal__company_webiste')
            if len(company_apply_buttons) > 1:

                company_apply_button = company_apply_buttons[0]
                sleep(2)

                # Get the href attribute of the button (if the button is a link)
                href = company_apply_button.get_attribute('href')

                # Print or use the href
                print(f"Found href: {href}")

                new_updated_url = clean_job_url(href, linkedin_job_id)

                print(new_updated_url)

                is_expired = False
                job_posted_date = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, 'posted-time-ago__text'))
                )

                posted_date = parse_date_posted(job_posted_date.text)

                print(posted_date, 'job_posted_date----------------------------------')

        else:
            signup_buttons = driver.find_elements(By.CLASS_NAME, 'apply-button')
            if len(signup_buttons) > 1:
                is_expired = False
                job_posted_date = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, 'posted-time-ago__text'))
                )

                posted_date = parse_date_posted(job_posted_date.text)

                print(posted_date, 'job_posted_date----------------------------------')
            else:
                is_expired = True

    except Exception as ex:
        print("Exception occurred:", ex)
        is_expired = True

    finally:
        if is_expired:
            job_expired_flag(job_id)
            print('Job expired date updated in the database.')

    if not posted_date:
        posted_date = datetime.now(timezone.utc).isoformat()

    updated_on = datetime.now(timezone.utc).isoformat()

    if new_updated_url:
        supabase.table('jobs').update({'job_posted_on': posted_date, 'updated_on': updated_on, 'apply_link': new_updated_url, filter_type: not CURRENT_BOOL}).eq('id', job_id).execute()
    else:
        supabase.table('jobs').update({filter_type: not CURRENT_BOOL, 'job_posted_on': posted_date, 'updated_on': updated_on}).eq('id', job_id).execute()

    supabase.table('transaction_log').insert({'system_id': SYSTEM_ID, 'transaction_type': 'expiry', 'is_expired': is_expired, 'job_unique_id': job_id}).execute()
    print("Is expired:", is_expired)

    return is_expired


def set_up_browser():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")

    if IS_RASPBERRY_PI:
        # options.add_argument("--headless=new")
        driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)
    else:
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        ]
        options.add_argument(f"user-agent={random.choice(user_agents)}")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.maximize_window()

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.delete_all_cookies()
    return driver


def log_to_file(message):
    """Logs a message to a .txt file with a timestamp."""
    log_file_path = "cycle_logs.txt"  # Specify the name of your log file
    timestamp = datetime.now().isoformat()
    with open(log_file_path, "a") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")


def manage_cycles():
    """
    Manages the cycle system for checks.
    Handles cycle endings and new cycle starts with proper reset function handling.
    Rechecks job count after each reset attempt.
    """

    log_to_file(f"{CURRENT_BOOL} - Current BOOL value")

    # Get current cycle information
    current_cycle = supabase.table('cycles')\
        .select('cycle_type', 'cycle_count')\
        .eq('cycle_type', CYCLE_TYPE)\
        .limit(1)\
        .execute()

    if not current_cycle.data:
        log_to_file(f"No cycles found for {CYCLE_TYPE}")
        return

    current_cycle = current_cycle.data[0]
    cycle_key = f"{current_cycle['cycle_type']}_{current_cycle['cycle_count']}"

    # Check if there's an active cycle
    active_cycle = supabase.table('cycle_transaction_logs')\
        .select('*')\
        .eq('unique_key', cycle_key)\
        .execute()

    current_time = datetime.now(timezone.utc).isoformat()
    res_cycle_update = supabase.table('cycles').update({'check_status': not CURRENT_BOOL}).eq('cycle_type', CYCLE_TYPE).execute()

    log_to_file(f"Cycle update response: {res_cycle_update}")

    if active_cycle.data:
        log_to_file(f"Attempting to end cycle for {CYCLE_TYPE}")

        # After breaking from loop (no more jobs), end the current cycle
        log_data = {'end_time': datetime.now(timezone.utc).isoformat()}
        supabase.table('cycle_transaction_logs')\
            .update(log_data)\
            .eq('unique_key', cycle_key)\
            .execute()

        log_to_file(f"Ended cycle for {CYCLE_TYPE}, cycle count: {current_cycle['cycle_count']}")

        sleep(3)

        # Get the updated cycle count after trigger
        updated_cycle = supabase.table('cycles')\
            .select('cycle_type', 'cycle_count')\
            .eq('cycle_type', CYCLE_TYPE)\
            .limit(1)\
            .execute()

        if not updated_cycle.data:
            log_to_file(f"Could not fetch updated cycle information for {CYCLE_TYPE}")
            return

        updated_cycle = updated_cycle.data[0]
        new_cycle_key = f"{CYCLE_TYPE}_{updated_cycle['cycle_count']}"

        # Start new cycle with updated count
        new_cycle_data = {
            'cycle_type': CYCLE_TYPE,
            'cycle_count': updated_cycle['cycle_count'],
            'system_id': SYSTEM_ID,
            'start_time': datetime.now(timezone.utc).isoformat(),
            'unique_key': new_cycle_key
        }

        supabase.table('cycle_transaction_logs')\
            .upsert(new_cycle_data)\
            .execute()

        log_to_file(f"Started next cycle for {CYCLE_TYPE}: {updated_cycle['cycle_count']}")

    else:
        # Start first cycle
        log_to_file(f"Starting new cycle for {CYCLE_TYPE}")
        log_data = {
            'cycle_type': CYCLE_TYPE,
            'system_id': SYSTEM_ID,
            'start_time': current_time,
            'cycle_count': current_cycle['cycle_count'],
            'unique_key': cycle_key
        }

        supabase.table('cycle_transaction_logs')\
            .upsert(log_data)\
            .execute()

        log_to_file(f"Started first cycle for {CYCLE_TYPE}, cycle count: {current_cycle['cycle_count']}")


def get_total_job_counts():
    # Query parameters
    params = {
        "select": "id,apply_link,company,attributes, companies(id,attributes,brand_name)",
        "application_closes_on": "is.null",
        "job_locations->0->>country": location_filter,
        'is_deleted': 'eq.false',
        'limit': 1
    }

    if not is_global:
        params[filter_type] = 'not.is.null'

    headers = {'apikey': key, 'Authorization': f"Bearer {key}", 'Prefer': 'count=exact'}
    response = requests.get(endpoint_url, params=params, headers=headers)
    print(response.headers)

    content_range = response.headers.get("content-range")
    count = int(content_range.split("/")[1]) if content_range else None

    return count


# Function to load job page and process job IDs
def load_job_page(driver):

    global CURRENT_BOOL

    count = 1
    while count > 0:

        # call the cycle_table to get the reset flag here

        cycles_res = supabase.table('cycles').select('*').eq('cycle_type', CYCLE_TYPE).execute()
        cycles_res = cycles_res.data
        CURRENT_BOOL = cycles_res[0].get('check_status')

        # Query parameters
        params = {
            "select": "id,apply_link,company,attributes",
            "application_closes_on": "is.null",
            "or": f"({filter_type}.eq.{CURRENT_BOOL},{filter_type}.is.null)",
            "limit": limit_per_req,
            'is_deleted': 'eq.false',
            "job_locations->0->>country": location_filter,
        }

        dynamic_query_obj = {
            'p_table_name': 'jobs',
            'p_columns': ['id', 'attributes', 'apply_link', 'company'],
            'p_limit_value': limit_per_req,
            'p_order_by': 'random()',
            'p_where_clause': f"application_closes_on is null  and is_deleted = false and job_locations->0->>'country' = '{country}' and ({filter_type} = {CURRENT_BOOL} or {filter_type} is null)",
        }

        if is_global:
            dynamic_query_obj['p_where_clause'] = f"application_closes_on is null and is_deleted = false and job_locations->0->>'country' <> 'United States' and job_locations->0->>'country'<>'India' and is_expiry_checked = {CURRENT_BOOL}"

        if has_order and order_by_desc:
            params['order'] = f'{order_by}.desc'
        elif has_order:
            params['order'] = order_by

        headers = {'apikey': key, 'Authorization': f"Bearer {key}", 'Prefer': 'count=exact'}

        response = requests.post(base_url, params=params, headers=headers)

        if is_random_job:
            response = requests.post(dynamic_url, json=dynamic_query_obj, headers=headers)
            jobs_json = response.json().get('data')

        else:
            response = requests.get(endpoint_url, params=params, headers=headers)
            jobs_json = response.json()

        print(len(jobs_json), 'checkeddddddddddd')

        jobs = jobs_json

        count = len(jobs)

        if response.status_code >= 200 and response.status_code < 300 and is_master_sys:
            print("Request was successful!")
            if is_random_job:
                response = requests.get(endpoint_url, params=params, headers=headers)

            # Get total count from content-range header
            content_range = response.headers.get("content-range")
            count = int(content_range.split("/")[1]) if content_range else None

            total_job_count = get_total_job_counts()
            supabase.table('cycles').update({'remaining_row_count': count, 'total_count': total_job_count}).eq('cycle_type', CYCLE_TYPE).execute()

        if count == 0 and is_master_sys:
            manage_cycles()

        print("count of jobs..", count)

        for job in jobs:

            linkedin_job_id = job['attributes'].get('linkedin_job_id')

            id = job['id']

            if linkedin_job_id is None:

                supabase.table(job_table_name).update({filter_type: not CURRENT_BOOL}).eq('id', id).execute()

                continue

            print('Job Id', id)
            sleep(5)

            print(linkedin_job_id)

            job_url = f'https://www.linkedin.com/jobs/view/{linkedin_job_id}/'

            print(job_url)

            driver.get(job_url)

            sleep(2)

            #check if page is avaiable, if not mark expired and continue the loop
            if 'expired_jd_redirect' in driver.current_url or "Page not found" in driver.page_source:
                print("Job not found or expired. expired_jd_redirect")
                job_expired_flag(id)
                supabase.table('transaction_log').insert({'system_id': SYSTEM_ID, 'transaction_type': 'expiry', 'is_expired': True, 'job_unique_id': id}).execute()
                print("Is expired:", True)
                sleep(2)
                continue

            if not 'jobs/view' in driver.current_url:
                print("Job Checking Skipped")
                sleep(2)
                continue

            #check for 429 error
            if 'HTTP ERROR 429' in driver.page_source:
                print('429 error')

                for attempt in range(5):
                    try:
                        # Locate the button with inner text 'Reload'
                        reload_button = driver.find_element(By.XPATH, "//*[text()='Reload']")

                        # Click the reload button
                        reload_button.click()

                        # Wait for the page to reload (adjust the wait time as needed)
                        sleep(5)

                        # Optionally, check if the page has been successfully reloaded
                        if 'HTTP ERROR 429' not in driver.page_source:
                            if 'https://www.linkedin.com/authwall?' in driver.current_url:
                                break
                            else:
                                print('Page reloaded successfully.')
                                break  # Exit the loop if the reload was successful
                        else:
                            print(f"Still seeing 429 error after reload attempt {attempt + 1}.")

                    except Exception as e:
                        print(f"Error occurred during attempt {attempt + 1}: {e}")

                # After 3 attempts, you can decide what to do
                if 'HTTP ERROR 429' in driver.page_source:
                    print("Failed to resolve the error after 3 attempts.")

            try:
                # Wait for the modal to be present
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'contextual-sign-in-modal__screen'))
                )

                print("Modal found. Attempting to dismiss with Escape key.")

                # Send Escape key to the body of the page
                body = driver.find_element(By.TAG_NAME, 'body')
                body.send_keys(Keys.ESCAPE)

                # Wait for the modal to disappear
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, 'contextual-sign-in-modal__screen'))
                )

                print("Modal successfully dismissed.")

            except TimeoutException:
                print("Modal with class 'contextual-sign-in-modal__screen' not found or didn't disappear after Escape key.")

            except Exception as e:
                print(f"An error occurred: {e}")

            #check if page is avaiable, if not mark expired and continue the loop
            if 'expired_jd_redirect' in driver.current_url or "Page not found" in driver.page_source:
                print("Job not found or expired. expired_jd_redirect")
                job_expired_flag(id)
                supabase.table('transaction_log').insert({'system_id': SYSTEM_ID, 'transaction_type': 'expiry', 'is_expired': True, 'job_unique_id': id}).execute()
                print("Is expired:", True)
                sleep(2)
                continue

            if not 'jobs/view' in driver.current_url:
                print("Job Checking Skipped")
                sleep(2)
                continue

            try:
                #check for job expiry key word
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'top-card-layout__card')))
                check_if_job_expired(id, linkedin_job_id, driver)

            except Exception as e:
                print("Timeout occurred while waiting for element to be present on the page. Retrying...")


if __name__ == "__main__":
    while True:  # This outer loop ensures the script runs indefinitely
        driver = set_up_browser()
        try:
            load_job_page(driver)
            sleep(5)
        finally:
            driver.quit()
            print("Driver has been quit. Restarting the loop.")
