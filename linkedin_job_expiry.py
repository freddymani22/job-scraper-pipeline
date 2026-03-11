
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException,ElementNotInteractableException,ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import requests
import logging
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import json
from dateutil.parser import isoparse
import random
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import time
import re
from supabase import create_client, Client
from webdriver_manager.chrome import ChromeDriverManager


#CONSTANTS
SYSTEM_ID = 21
is_master_sys = False

#ordering values
has_order = True
is_desc = True
order_by = 'updated_on'  # id, 'created_at',

is_us = False
is_india = True

if is_us:
    country = 'United States'
    country_filter='united_states'
    CYCLE_TYPE = 'scrape_us'
    filter_type = 'is_us_scraped'
elif is_india:
    country = 'India'
    country_filter='india'
    CYCLE_TYPE = 'scrape_india'
    filter_type = 'is_linkedin_scraped'





load_dotenv()
url = os.environ["SUPABASE_URL"]
key = os.environ["SUPABASE_KEY"]


supabase: Client = create_client(url, key)



"""
Setup browser to open the necessary webpage.
Configure so the browser runs in background without interrupting other operations
"""
# def setup_browser_1():


#     # create Chrome options object
#     chrome_options = Options()
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     # set headless option to run Chrome in the background
#     chrome_options.add_argument('--headless')
#     # Set Chrome options
#     chrome_options = webdriver.ChromeOptions()
#     # chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")

#     driver = webdriver.Chrome( options=chrome_options)#executable_path="/usr/local/bin/chromedriver",
#     driver.maximize_window()
#     return driver

def setup_browser(user_data_dir=None):
    """
    Setup Chrome with persistent user data directory to maintain login sessions
    """
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    selected_user_agent = random.choice(user_agents)

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={selected_user_agent}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Use persistent user data directory to maintain sessions
    if user_data_dir:
        options.add_argument(f"--user-data-dir={user_data_dir}")
        options.add_argument("--profile-directory=Default")

    # service = Service(ChromeDriverManager().install())
    service = Service(executable_path='/usr/bin/chromedriver')

    driver = webdriver.Chrome(service=service, options=options)

    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": selected_user_agent
    })
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.maximize_window()
    logging.info("Chrome driver initialized successfully")
    return driver




# def setup_browser():
#     driver_path = '/usr/bin/chromedriver'
#     options = Options()

#     # Randomly choose User-Agent
#     user_agents = [
#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
#         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
#         "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
#     ]
#     options.add_argument(f"user-agent={random.choice(user_agents)}")

#     # Set headless mode if needed (uncomment if you want a visual check)
#     # options.add_argument('--headless')

#     # Initialize WebDriver with Service
#     service = Service(executable_path=driver_path)
#     driver = webdriver.Chrome(service=service, options=options)
    
    
#     driver.maximize_window()

#     # Wait for a random time to simulate human delay
#     time.sleep(random.uniform(1, 3))

#     # Clear cookies to simulate a fresh start
#     driver.delete_all_cookies()

#     # Return the driver
#     return driver
    




"""
Open the requested web page and wait to load the content
"""
def open_webpage(driver, url, country):


    print(country, 'country')

    # Parse the URL into components
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    # Remove unwanted parameters
    query_params.pop('geoId', None)
    query_params.pop('currentJobId', None)

    # Add new parameter
    query_params['location'] = country

    # Reconstruct the URL with the updated query parameters
    new_query = urlencode(query_params, doseq=True)
    new_url = urlunparse(parsed_url._replace(query=new_query))


    # Open the URL from the browser
    driver.get(new_url)





"""
Filter based on the past week,past 24 hours, past month
"""


def filter_by_timeframe(driver, timeframe, USER_DELAY=2, CONTENT_LOAD=2):
    try:
        # Wait for filter button to be present
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'filter-button.pill.flex.items-center'))
        )
        elements = driver.find_elements(By.CLASS_NAME, 'filter-button.pill.flex.items-center')

        if len(elements) >= 2:
            second_element = elements[1]
            time.sleep(2)
            second_element.click()

            filter_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "collapsible-dropdown__list"))
            )[1]
            
            time.sleep(4)

            def handle_429_error():
                if 'HTTP ERROR 429' in driver.page_source:
                    for attempt in range(5):
                        try:
                            reload_button = driver.find_element(By.XPATH, "//*[text()='Reload']")
                            reload_button.click()
                            time.sleep(5)
                            
                            if 'HTTP ERROR 429' not in driver.page_source:
                                if 'https://www.linkedin.com/authwall?' in driver.current_url:
                                    return False
                                print('Page reloaded successfully.')
                                return True
                            else:
                                print(f"Still seeing 429 error after reload attempt {attempt + 1}.")
                        except Exception as e:
                            print(f"Error occurred during attempt {attempt + 1}: {e}")
                    return False
                return True

            def click_timeframe_and_check(element, retry_count=0):
                try:
                    element.click()
                    time.sleep(2)
                    
                    if not handle_429_error():
                        if retry_count < 3:
                            time.sleep(5)
                            return click_timeframe_and_check(element, retry_count + 1)
                        return False
                    return True
                except Exception as e:
                    print(f"Error clicking timeframe: {e}")
                    return False

            # Try different timeframes
            try:
                timeframe_element = filter_dropdown.find_element(
                    By.XPATH, f".//label[contains(text(), 'Past 24 hours')]")
                if not click_timeframe_and_check(timeframe_element):
                    raise Exception("Failed to apply Past 24 hours filter")
            except Exception:
                try:
                    timeframe_element = filter_dropdown.find_element(
                        By.XPATH, f".//label[contains(text(), 'Past week')]")
                    if not click_timeframe_and_check(timeframe_element):
                        raise Exception("Failed to apply Past week filter")
                except Exception:
                    try:
                        timeframe_element = filter_dropdown.find_element(
                            By.XPATH, f".//label[contains(text(), 'Past month')]")
                        if not click_timeframe_and_check(timeframe_element):
                            raise Exception("Failed to apply Past month filter")
                    except Exception:
                        print("None of the timeframe options are found or failed to apply.")

            # Click Done button with 429 handling
            try:
                done_button = filter_dropdown.find_element(By.CLASS_NAME, "filter__submit-button")
                if not click_timeframe_and_check(done_button):
                    raise Exception("Failed to click Done button")
            except Exception as e:
                print(f"Error clicking Done button: {e}")

            print(second_element.text)
        else:
            print("There are fewer than 2 elements with the specified class name.")

    except Exception as e:
        print(f"Exception while waiting for filter button: {e}")
        return

    # Handle old filter UI if present
    try:
        date_filter_button = driver.find_element(By.ID, "searchFilter_timePostedRange")    
        date_filter_button.click()
        time.sleep(USER_DELAY)

        options = driver.find_elements_by_xpath("//label[contains(@for, 'timePostedRange')]")
        
        for option in options:
            if timeframe in option.text:
                if not click_timeframe_and_check(option):
                    continue
                time.sleep(CONTENT_LOAD)
                break

        show = driver.find_element(
            By.XPATH,'//button[contains(.//span, "result") and contains(.//span, "Show")]')
        if not click_timeframe_and_check(show):
            raise Exception("Failed to click Show button")
        time.sleep(CONTENT_LOAD)
        print("Applied filters.")
    except Exception as e:
        print(f"Exception @filter_past_24hr_posts: {e}")

    # Handle filter pills if present
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'search-reusables__filter-pill-button'))
        )
        
        filter_buttons = driver.find_elements(By.CLASS_NAME, "search-reusables__filter-pill-button")
        for button in filter_buttons:
            if button.text == "Date posted":
                if not click_timeframe_and_check(button):
                    continue
                time.sleep(USER_DELAY)
                break

        options = driver.find_elements_by_xpath(f"//label[contains(@for, 'timePostedRange')]")
        for option in options:
            if "Past week" in option.text:
                if not click_timeframe_and_check(option):
                    continue
                time.sleep(CONTENT_LOAD)
                break

        show = driver.find_element(
            By.XPATH,'//button[contains(.//span, "result") and contains(.//span, "Show")]')
        if not click_timeframe_and_check(show):
            raise Exception("Failed to click Show button")
        time.sleep(CONTENT_LOAD)
    except Exception as e:
        print(f"Exception @filter_past_24hr_posts: {e}")

    print("Applied filters.")


def get_job_id_1(href):
        # Extract the job ID from the URL using regular expressions
        match = re.search(r"currentJobId=(\d+)", href)
        if match:
            job_id = match.group(1)
            return job_id
        

def is_page_loaded(driver):

        if driver.current_url == 'https://www.linkedin.com/':
            return False
        elif 'https://www.linkedin.com/authwall?' in driver.current_url:
            return False
        elif 'https://www.linkedin.com/?original_referer' in driver.current_url:
                return False
        elif 'HTTP ERROR 429' in driver.page_source:

            # Try to reload up to 3 times
            for attempt in range(5):
                try:
                    # Locate the button with inner text 'Reload'
                    reload_button = driver.find_element(By.XPATH, "//*[text()='Reload']")
                    
                    # Click the reload button
                    reload_button.click()
                    
                    # Wait for the page to reload (adjust the wait time as needed)
                    time.sleep(5)
                    
                    # Optionally, check if the page has been successfully reloaded
                    if 'HTTP ERROR 429' not in driver.page_source:
                        if 'https://www.linkedin.com/authwall?' in driver.current_url:
                            return False
                        else:
                            print('Page reloaded successfully.')
                            break  # Exit the loop if the reload was successful
                    else:
                        print(f"Still seeing 429 error after reload attempt {attempt + 1}.")
                
                except Exception as e:
                    print(f"Error occurred during attempt {attempt + 1}: {e}")

            # After 3 attempts, you can decide what to do
            if 'HTTP ERROR 429' in driver.page_source:
                return False
            elif ( driver.current_url == 'https://www.linkedin.com/') or ('https://www.linkedin.com/authwall?' in driver.current_url) or ('https://www.linkedin.com/?original_referer' in driver.current_url):
                return False
        return True

        
def get_job_id(href):
    print(href)
    
    # Find the position of the '?'
    position = href.rfind('?')
 
    
    # Go backward from the '?' to find the first '-'
    start = href.rfind('-', 0, position)
   
    
    # Extract the substring between the '?' and the first '-'
    job_id = href[start+1:position]
    print(job_id)
    return job_id


def get_new_job_items(job_items):
    all_job_ids = []
    job_id_to_item = {}
    
    for job_item in job_items:
        link = job_item.find_element(By.TAG_NAME, 'a')
        href = link.get_attribute('href')
        job_id = get_job_id(href)
        print(job_id,'iiiiiiiiiiiiiiii')
        if job_id:
            all_job_ids.append(job_id)
            job_id_to_item[job_id] = job_item
    

    print(all_job_ids, 'all jobs..')

    # Get all job IDs that are already in the database
    existing_jobs = supabase.table('scraping_raw_html').select('linkedin_job_id').in_('linkedin_job_id', all_job_ids).execute()
    existing_job_ids = set(job['linkedin_job_id'] for job in existing_jobs.data)

    print(existing_job_ids, 'existing job idss')

    print('Total jobs to scrape: ', len(all_job_ids)-len(existing_job_ids))
    
    # Return only the job items that are not in the database

    return [job_id_to_item[job_id] for job_id in all_job_ids if job_id not in existing_job_ids]




# def scrape_job_data(driver,job_items, comp_name, comp_id, country):
#     count = 0
#     new_jobs = get_new_job_items(job_items)

 

#     for job_item in new_jobs:
#         count += 1
#         time.sleep(5)
        
#         try:
#             link = job_item.find_element(By.TAG_NAME, 'a')  
#             current_jobs_id = get_job_id_1(driver.current_url)
#             print(current_jobs_id)
#             print('link', link)    
#             link.click()
            



#             # Modified retry logic for loading detail view
#             max_retries = 2
#             retry_count = 0
#             detail_loaded = True
            
#             while retry_count < max_retries and not detail_loaded:
#                 try:
#                     wait = WebDriverWait(driver, 7)
#                     jd_detail_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "details-pane__content.details-pane__content--show")))
#                     detail_loaded = True  # Successfully loaded
#                 except Exception as e:
#                     retry_count += 1
#                     print(f'Detail view not loaded, attempt {retry_count} of {max_retries}')
                    
#                     if retry_count < max_retries:  # Don't sleep on last attempt
#                         time.sleep(4)
#                         link.click()
                        
#                         if count > 1:
#                             prev_job_item = job_items[count - 2]
#                             prev_link = prev_job_item.find_element(By.TAG_NAME, 'a')
#                             prev_link.click()
#                             time.sleep(3)
#                             link.click()
            



#             if not detail_loaded:

#                 print(f"Detail view failed to load, opening job URL in a new tab")
#                 new_url = f"https://www.linkedin.com/jobs/view/{current_jobs_id}"
                
#                 # Open the URL in a new tab
#                 driver.execute_script(f"window.open('{new_url}', '_blank');")



#                 # Get all window handles (tabs)
#                 window_handles = driver.window_handles
                
#                 # Optionally, switch to the new tab
#                 driver.switch_to.window(driver.window_handles[-1])


#                 is_success = is_page_loaded(driver)


#                 if is_success:
#                     print('job page loaded')

#                      # Find the element with class name 'details'
#                     details_element = driver.find_element(By.CLASS_NAME, 'details')

#                     # Get the HTML content of the element
#                     details_html = details_element.get_attribute('outerHTML')

#                     try:
#                         signup_buttons = driver.find_elements(By.CLASS_NAME, 'sign-up-modal__outlet')
#                         if len(signup_buttons) > 1:
#                             apply_button = signup_buttons[1]
#                             time.sleep(2)
#                             apply_button.click()

#                             company_apply_buttons = driver.find_elements(By.CLASS_NAME, 'sign-up-modal__company_webiste')
#                             if len(company_apply_buttons) > 1:
#                                 company_apply_button = company_apply_buttons[0]
#                                 time.sleep(2)
#                                 # company_apply_button.click()
#                                 # Get the href attribute of the button (if the button is a link)
#                                 job_apply_link = company_apply_button.get_attribute('href')
                                
#                                 # Print or use the href
#                                 print(f"Found href: {job_apply_link}")


#                         else:
#                             job_apply_link = new_url
#                             print('easy apply')

#                         post_data_to_db(
#                             raw_jd_html=details_html,
#                             job_url = job_apply_link, 
#                             linkedin_job_id=current_jobs_id, 
#                             company_name=comp_name,
#                             company_fk= comp_id ,
#                             country= country,
#                             has_detail_page = True
#                             )






                    
#                     except Exception as e:
#                             print(e)

                

#                 else:
#                     print(f"Failed to load detail view after {max_retries} attempts")

#                     job_apply_link = 'Easy apply'


#                     post_data_to_db(job_url= job_apply_link, linkedin_job_id= current_jobs_id, company_name= comp_name, company_fk=comp_id ,country= country, has_detail_page =None)


#                 driver.close()

#                 driver.switch_to.window(window_handles[0])
#                 continue


#             raw_jd_html = jd_detail_element.get_attribute('innerHTML')
#             orginal_window = driver.current_window_handle
#             job_url = driver.current_url
#             linkedin_id = get_job_id_1(job_url)

#             try:
#                 wait = WebDriverWait(driver, 10)
#                 time.sleep(5)
#                 apply_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-tracking-control-name="public_jobs_apply-link-offsite_sign-up-modal"]')))

#                 """APPLY LINK PART"""
#                 apply_button.click()

#                 wait = WebDriverWait(driver, 30)
#                 apply_on_company_website_link = wait.until(
#                     EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-tracking-control-name="public_jobs_apply-link-offsite_sign-up-modal-sign-up-later"]'))
#                 )

#                 time.sleep(5)
#                 apply_on_company_website_link.click()

#                 new_window = [window for window in driver.window_handles if window != orginal_window][0]
#                 driver.switch_to.window(new_window)
#                 time.sleep(5)

#                 job_company_url = driver.current_url
#                 print("New Tab URL:", job_company_url)

#                 driver.close()
#                 time.sleep(3)
                
#                 driver.switch_to.window(orginal_window)
#                 time.sleep(4)
                
#                 print('JOBS COUNT', count)

#                 post_data_to_db(raw_jd_html = raw_jd_html,job_url=job_company_url,linkedin_job_id= linkedin_id,company_name= comp_name, company_fk=comp_id ,country= country)




#             except TimeoutException:
#                 try:
#                     time.sleep(2)
#                     wait = WebDriverWait(driver, 10)
#                     apply_button = driver.find_element(By.CLASS_NAME, "apply-button")
#                     print('easy apply')
#                     job_company_url = 'Easy apply'
#                     post_data_to_db(raw_jd_html= raw_jd_html,job_url= job_company_url,linkedin_job_id= linkedin_id,company_name= comp_name,company_fk= comp_id ,country= country)

                          

#                     continue
#                 except NoSuchElementException:
#                     print("Apply button or link not found.")
                    
#         except Exception as e:
#             print("An error occurred:", str(e))
#             continue


def scrape_job_data(driver, job_items, comp_name, comp_id, country):
    count = 0
    new_jobs = get_new_job_items(job_items)

    for job_item in new_jobs:
        count += 1
        time.sleep(2)  # Reduced from 5 to 2 seconds
        
        try:
            link = job_item.find_element(By.TAG_NAME, 'a')
            job_url = link.get_attribute('href')
            current_jobs_id = get_job_id(job_url)  # Use the href to get job ID
            print('Current job ID:', current_jobs_id)
            
            # Skip the click attempt and go directly to opening in new tab
            print(f"Opening job URL in a new tab for job ID: {current_jobs_id}")
            new_url = f"https://www.linkedin.com/jobs/view/{current_jobs_id}"
            
            # Open the URL in a new tab
            driver.execute_script(f"window.open('{new_url}', '_blank');")
            
            # Switch to the new tab
            window_handles = driver.window_handles
            driver.switch_to.window(driver.window_handles[-1])
            
            is_success = is_page_loaded(driver)
            
            if is_success:
                print('Job page loaded successfully')
                
                try:
                    # Find the element with class name 'details'
                    details_element = driver.find_element(By.CLASS_NAME, 'details')
                    details_html = details_element.get_attribute('outerHTML')
                    time.sleep(1)
                    hide_modal(driver)
                    try:
                        signup_buttons = driver.find_elements(By.CLASS_NAME, 'sign-up-modal__outlet')
                        if len(signup_buttons) > 1:
                            apply_button = signup_buttons[1]
                            time.sleep(2)
                            apply_button.click()
                      
                            company_apply_buttons = driver.find_elements(By.CLASS_NAME, 'sign-up-modal__company_webiste')
                            if len(company_apply_buttons) > 1:
                                company_apply_button = company_apply_buttons[0]
                                time.sleep(2)
                                job_apply_link = company_apply_button.get_attribute('href')
                                print(f"Found href: {job_apply_link}")
                        else:
                            job_apply_link = new_url
                            print('Easy apply')
                            
                        post_data_to_db(
                            raw_jd_html=details_html,
                            job_url=job_apply_link, 
                            linkedin_job_id=current_jobs_id, 
                            company_name=comp_name,
                            company_fk=comp_id,
                            country=country,
                            has_detail_page=True
                        )
                    
                    except Exception as e:
                        print(f"Error processing apply buttons: {str(e)}")
                        job_apply_link = 'Easy apply'
                        post_data_to_db(
                            raw_jd_html=details_html,
                            job_url=job_apply_link,
                            linkedin_job_id=current_jobs_id,
                            company_name=comp_name,
                            company_fk=comp_id,
                            country=country,
                            has_detail_page=True
                        )
                
                except NoSuchElementException:
                    print("Could not find details element")
                    job_apply_link = 'Easy apply'
                    post_data_to_db(
                        job_url=job_apply_link,
                        linkedin_job_id=current_jobs_id,
                        company_name=comp_name,
                        company_fk=comp_id,
                        country=country,
                        has_detail_page=False
                    )
            
            else:
                print("Failed to load job page")
                job_apply_link = 'Easy apply'
                post_data_to_db(
                    job_url=job_apply_link,
                    linkedin_job_id=current_jobs_id,
                    company_name=comp_name,
                    company_fk=comp_id,
                    country=country,
                    has_detail_page=False
                )
            
            # Close the tab and switch back to main window
            driver.close()
            driver.switch_to.window(window_handles[0])
            
        except Exception as e:
            print(f"An error occurred processing job {count}: {str(e)}")
            continue


"""
Scroll through all the jobs to load complete jobs search list
"""
# def load_all_jobs(driver, comp_name, comp_id, country):
#     # Wait for the jobs list to load
#     jobs_list = WebDriverWait(driver, 5).until(
#         EC.presence_of_element_located((By.CLASS_NAME, 'jobs-search__results-list'))
#     )


#     try: 
#         while True:

#             # Find all child li elements of the jobs list
#             job_items = jobs_list.find_elements(By.TAG_NAME, 'li')
#             print(len(job_items))

#             scrape_job_data(driver, job_items, comp_name, comp_id, country)
            
#             time.sleep(5)
            
#             try:
#                 # Wait for the "See more jobs" button to be clickable
#                 wait = WebDriverWait(driver, 10)
#                 see_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'See more jobs')]")))

#                 # Get the button coordinates
            

#                 if see_more_button.is_displayed():
#                     # Click the button if it's in the viewport and visible
#                     see_more_button.click()
                
                    
                
#                 time.sleep(5)
                

                    
#                 if see_more_button.is_displayed():
#                     # Click the button if it's in the viewport and visible
#                     see_more_button.click()
                
                    
                
#                 time.sleep(5)
                
#                 new_job_items = jobs_list.find_elements(By.TAG_NAME, 'li')
#                 new_job_items = [item for item in new_job_items if item not in job_items]
                
                
                
#                 scrape_job_data(driver, new_job_items, comp_name,comp_id, country)

#                 job_items = jobs_list.find_elements(By.TAG_NAME, 'li')

                
#             except:
#                 # If the button is not found, break the loop
#                 print("No more jobs to load")
#                 break
            
#     finally:
#         print()


def load_all_jobs(driver, comp_name, comp_id, country):
    print("Starting infinite scroll to load all jobs...")
    
    # Wait for job list to load initially
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'jobs-search__results-list'))
    )
    
    consecutive_no_change = 0
    max_consecutive = 3
    previous_job_count = 0
    
    while True:
        try:
            hide_modal(driver)
            
            # Scroll to bottom of page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Check for "You've viewed all jobs" message - this is our exit condition
            try:
                viewed_all_element = driver.find_element(By.CSS_SELECTOR, 
                    "div.see-more-jobs__viewed-all p.inline-notification__text")
                if "You've viewed all jobs for this search" in viewed_all_element.text:
                    print("✅ Found 'You've viewed all jobs for this search' message. All jobs loaded!")
                    break
            except NoSuchElementException:
                pass  # Message not found, continue scrolling
            
            # Try to click "See more jobs" button if it exists
            see_more_clicked = False
            try:
                see_more_btn = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'See more jobs')]"))
                )
                if see_more_btn.is_displayed():
                    print("Clicking 'See more jobs' button...")
                    see_more_btn.click()
                    see_more_clicked = True
                    time.sleep(3)  # Wait a bit longer after clicking
            except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
                pass  # Button may not exist
            
            # Get current job count
            job_list = driver.find_element(By.CLASS_NAME, 'jobs-search__results-list')
            job_items = job_list.find_elements(By.TAG_NAME, 'li')
            current_job_count = len(job_items)
            
            print(f"Current job count: {current_job_count}")
            
            # Check if new jobs were loaded
            if current_job_count > previous_job_count:
                print(f"New jobs loaded! Previous: {previous_job_count}, Current: {current_job_count}")
                consecutive_no_change = 0
                previous_job_count = current_job_count
            elif see_more_clicked:
                # If we clicked "See more jobs" but count didn't change, wait a bit more
                time.sleep(2)
                job_list = driver.find_element(By.CLASS_NAME, 'jobs-search__results-list')
                job_items = job_list.find_elements(By.TAG_NAME, 'li')
                current_job_count = len(job_items)
                
                if current_job_count > previous_job_count:
                    consecutive_no_change = 0
                    previous_job_count = current_job_count
                else:
                    consecutive_no_change += 1
            else:
                consecutive_no_change += 1
                print(f"No new jobs loaded. Consecutive attempts: {consecutive_no_change}/{max_consecutive}")
            
            # Safety exit if we've tried too many times without progress
            if consecutive_no_change >= max_consecutive:
                print("⚠️ No new jobs loaded after multiple attempts. Assuming all jobs are loaded.")
                break
                
            # Wait before next scroll
            time.sleep(2)
            
        except Exception as e:
            print(f"Error during infinite scroll: {e}")
            break
    
    # Now scrape all the jobs at once
    print("🔄 Starting to scrape all loaded jobs...")
    try:
        job_list = driver.find_element(By.CLASS_NAME, 'jobs-search__results-list')
        all_job_items = job_list.find_elements(By.TAG_NAME, 'li')
        print(f"Total jobs to scrape: {len(all_job_items)}")
        
        # Scrape all jobs
        scrape_job_data(driver, all_job_items, comp_name, comp_id, country)
        
    except Exception as e:
        print(f"Error scraping job data: {e}")
    
    print("✅ Finished loading and scraping all jobs.")


def try_click_see_more(driver):
    """Helper function to attempt clicking the See More button"""
    try:
        see_more_btn = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'See more jobs') or contains(., 'Show more jobs')]"))
        )
        # Scroll to the button first to ensure it's clickable
        driver.execute_script("arguments[0].scrollIntoView(true);", see_more_btn)
        time.sleep(0.5)
        see_more_btn.click()
        print("Clicked 'See more jobs' button")
        time.sleep(1.5)
        return True
    except Exception as e:
        return False
def post_data_to_synology(file_name,html_raw):
    supabase.storage.from_("jobs_scraping").upload(file=html_raw.encode('utf-8'),path=file_name, file_options={"content-type": "text/html"})





"""
Post the scraped data into supabase db
"""
def post_data_to_db( job_url, linkedin_job_id, company_name, company_fk, country, has_detail_page = False, raw_jd_html= None):


    print(job_url)
    print('EASY_APPLY', job_url=='Easy apply')


    linkedin_url = f'https://www.linkedin.com/jobs/view/{linkedin_job_id}'


    if job_url == 'Easy apply':
        job_url = linkedin_url


    # job_dump_url = f"https://amplify-testext-dev-c21d2-deployment.s3.ap-south-1.amazonaws.com/job_scraping_raw_html/{linkedin_job_id}"    

   
    print(linkedin_job_id)
    data = {
        # 'json_dump_url': job_dump_url,
        'job_url': job_url,
        'linkedin_job_id': linkedin_job_id,
        'linkedin_job_url': linkedin_url,
        'company': company_name,
        'company_id': company_fk,
        'country': country, 
        'system_no':SYSTEM_ID,
         'has_detail_page' :has_detail_page
         
          }

    
    if raw_jd_html is not None:
     post_data_to_synology(linkedin_job_id,raw_jd_html)


    print(data)



     # NEED TO LOG TO TRANSACTION TABLE HERE
     
    supabase.table('transaction_log').insert({"transaction_type":"job_added", 'system_id':SYSTEM_ID}).execute()
    response = supabase.table('scraping_raw_html').upsert(data).execute()
    print(response, 'response from supabase')





    


def get_page_content(driver):
    # Get the page content as a string
    return driver.find_element(By.TAG_NAME, 'body').text  
    



"""
Scrap posted jobs info from the linkedin jobs listing
"""

# def scrap_jobs_info(driver, comp_name, comp_id, country):
 

#     if driver.current_url == 'https://www.linkedin.com/':
#      return True
#     elif 'https://www.linkedin.com/authwall?' in driver.current_url:
#         return True
#     elif 'https://www.linkedin.com/?original_referer' in driver.current_url:
#         return True


    
#     try:
#         element = driver.find_element(By.XPATH, '//h1[contains(@class, "core-section-container__main-title") and contains(text(), "We couldnÃ¢Â€Ât find a match for")]')
#         return None  # Return None if the element is found
#     except NoSuchElementException:
#         print("jobs found")


        

    

#     # Initial page content
#     prev_content = get_page_content(driver)




#     while True:

#         time.sleep(3)
#         driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    
#         # Wait for a short time for more content to load
#         time.sleep(5)


#         if "You've viewed all jobs for this search" in driver.page_source:
       
#             break




#         # Scroll up a bit to trigger more content loading
#         actions = ActionChains(driver)
#         actions.send_keys(Keys.PAGE_UP).perform()
        
#         # Wait for a short time after scrolling up
#         time.sleep(3)
        
#         # Scroll back to the bottom to continue loading
#         driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        
#         # Wait for a short time for more content to load
#         time.sleep(5)
            
#         try:
#             # Compare current page content with previous content

#             time.sleep(8)
#             current_content = get_page_content(driver)
#             if current_content == prev_content:
#                 print("No more new jobs to load. Exiting.")
#                 break
#             elif prev_content == current_content and driver.find_elements(By.CLASS_NAME, "inline-notification__text.text-sm.leading-regular"):
#                 print("All available jobs have been loaded.")
#                 break
#             else:
#                 prev_content = current_content
#         except StaleElementReferenceException:
#             # Handle StaleElementReferenceException if necessary
#             continue

#     print("Loading all jobs...")
 


#     load_all_jobs(driver, comp_name, comp_id, country)

#     print("Scraping jobs info...")
    
    
#     try:
#         if driver.find_element(By.CLASS_NAME,"jobs-search-no-results-banner__image"):
#             return 
#     except:
#         print("jobs found")   
        
 
 
def scrap_jobs_info(driver, comp_name, comp_id, country):
    # Skip invalid pages
    if driver.current_url in ['https://www.linkedin.com/', 
                              'https://www.linkedin.com/?original_referer'] or \
       'https://www.linkedin.com/authwall?' in driver.current_url:
        print("Invalid LinkedIn state, skipping.")
        return True

    try:
        # If "no jobs found" message is present
        driver.find_element(By.XPATH, '//h1[contains(text(), "We couldn’t find a match for")]')
        print("No jobs match the search criteria.")
        return None
    except NoSuchElementException:
        print("Jobs found, continuing...")

    # Load all jobs by scrolling and clicking buttons
    print("Loading all jobs...")
    load_all_jobs(driver, comp_name, comp_id, country)

    # Final check for no-results image
    try:
        driver.find_element(By.CLASS_NAME, "jobs-search-no-results-banner__image")
        print("No results banner found after load.")
        return
    except:
        print("Jobs found and processed.")
        
        

def check_if_jobs_available(driver):
    try:
        # Wait for up to 10 seconds for the element to be present
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "section.core-section-container.my-3.no-results"))
        )
        # If the element is found, it means no jobs are available
        return False
    except TimeoutException:
        # If the element is not found within the timeout period, it means jobs are available
        return True



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
        
        time.sleep(3)
        
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


def get_and_apply_filters(country_filter,res_main):

    filter_res_main=supabase.table('jobs_scraping_filters'
    ).select('country, bands, domains,employee_count_range, total_funding, roles'
    ).eq('country',country_filter
    ).limit(1
    ).execute()

    if filter_res_main:
        filter_res=filter_res_main.data
        print(filter_res)
        if filter_res and filter_res[0]:
            filter_data={
                'bands_filter':filter_res[0]['bands'],
                'domains_filter':filter_res[0]['domains'],
                'employee_count_filter':filter_res[0]['employee_count_range'],
                'funding_filter':filter_res[0]['total_funding'],
                'roles_filter':filter_res[0]['roles']
            }

            if(filter_data):
                if(filter_data['bands_filter']):
                    res_main.in_('attributes->>band',filter_data['bands_filter'])
                else:
                    res_main.in_('attributes->>band',["L1", 'L2','L3','L4','L5','L6'])
                if(filter_data['domains_filter']):
                    res_main.contains('company_verticals',filter_data['domains_filter'])
                if(filter_data['employee_count_filter']):
                    res_main.in_('employee_count_range',filter_data['employee_count_filter'])
                if(filter_data['funding_filter']):
                    res_main.gte('total_funding',filter_data['funding_filter'])
                
    
            return res_main
        
    return res_main

# def hide_modal(driver):
#     try:
#         # Wait for any visible modal overlay to appear
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CLASS_NAME, 'modal__overlay'))
#         )

#         print("Modal found. Forcing it to hide by injecting CSS using setAttribute.")

#         # Use JavaScript to forcibly override all styles via setAttribute
#         driver.execute_script("""
#             const modals = document.querySelectorAll('.modal__overlay');
#             modals.forEach(modal => {
#                 modal.setAttribute('style', 'display: none !important; visibility: hidden !important; opacity: 0 !important;');
#             });
#         """)

#         print("Modal successfully hidden using setAttribute and !important.")

#     except TimeoutException:
#         print("Modal not found or already hidden.")




def hide_modal(driver):
    try:
        # Wait for modal to appear
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'modal__overlay'))
        )
        print("Modal found.")

        # Step 1: Try to click the close ('X') button
        try:
            close_btn = driver.find_element(By.CLASS_NAME, 'modal__dismiss')
            close_btn.click()
            print("Modal closed via X button.")
            return
        except (TimeoutException, ElementNotInteractableException, Exception) as e:
            print("X button not clickable:", e)

        # Step 2: Try pressing Escape key
        try:
            actions = ActionChains(driver)
            actions.send_keys(Keys.ESCAPE).perform()
            print("Escape key sent to close modal.")
            return
        except Exception as e:
            print("Escape key failed:", e)

        # Step 3: Force hide via JS and CSS if above fails
        print("Trying to hide modal via JavaScript fallback.")
        driver.execute_script("""
            const modals = document.querySelectorAll('.modal__overlay');
            modals.forEach(modal => {
                modal.setAttribute('style', 'display: none !important; visibility: hidden !important; opacity: 0 !important;');
            });
        """)
        print("Modal forcefully hidden via JavaScript.")

    except TimeoutException:
        print("No modal found.")
def main():


    global CURRENT_BOOL
    last_24_hours = datetime.now() -timedelta(days=3)

    last_24_hours = last_24_hours.isoformat()
 
    
    try:

        
        
        count = 1
        while count >0:



            cycles_res = supabase.table('cycles').select('*').eq('cycle_type', CYCLE_TYPE).execute()

            cycles_res = cycles_res.data


            CURRENT_BOOL = cycles_res[0].get('check_status')



            print(CURRENT_BOOL, 'CURRENT_BOOL')



            # res_main = supabase.table('company_scrape_data'
            # ).select('company_id,  companies(id, brand_name,verified, is_deleted, attributes ,updated_on, is_to_be_deleted, created_on,scraping_data->>company_job_url)', 'created_at', 'new_countries', count = 'exact'
            # ).not_.is_('companies', 'null'
            # ).not_.is_('companies.scraping_data->>company_job_url','null'
            # ).eq('companies.verified', True
            # ).eq('companies.is_deleted', False
            # ).eq('companies.is_to_be_deleted',False
            # ).in_('companies.attributes->>band',["L1", 'L2','L3','L4']
            # ).not_.is_(f'new_countries->>{country}', 'null'
            # ).or_(f'{filter_type}.eq.{CURRENT_BOOL},{filter_type}.is.null'
            # )

            res_main = supabase.table('companies'
            ).select('id, brand_name,verified, is_deleted, attributes ,updated_on,jobs_last_scraped_date, is_to_be_deleted, created_on,scraping_data->>company_job_url', 'country_job_scrape_map', count = 'exact'
            ).not_.is_('scraping_data->>company_job_url','null'
            ).eq('verified', True
            ).eq('is_deleted', False
            ).eq('is_to_be_deleted',False            
            ).in_('attributes->>band',["L1", 'L2','L3','L4']
            ).not_.is_(f'country_job_scrape_map->>{country_filter}', 'null'
            ).eq(f'country_job_scrape_map->>{country_filter}',str(CURRENT_BOOL).lower()
            )



            res_main=get_and_apply_filters(country_filter,res_main)

                
                



            if has_order:
                if is_desc:
                  res_main.order(order_by, desc = True)
                else:
                 res_main.order(order_by)




            res = res_main.limit(1).execute()
        
            print(res.count)


            count = res.count
             
            if is_master_sys:
                # total_job_count_res =supabase.table('company_scrape_data'
                # ).select('company_id,  companies(id, brand_name,verified, is_deleted, attributes ,updated_on, is_to_be_deleted, created_on,scraping_data->>company_job_url)', 'created_at', 'new_countries', count = 'exact'
                # ).not_.is_('companies', 'null'
                # ).not_.is_('companies.scraping_data->>company_job_url','null'
                # ).eq('companies.verified', True
                # ).eq('companies.is_deleted', False
                # ).eq('companies.is_to_be_deleted',False
                # ).in_('companies.attributes->>band',["L1", 'L2','L3','L4']
                # ).not_.is_(f'new_countries->>{country}', 'null'
                # ).limit(1).execute()

                total_job_count_res = supabase.table('companies'
                ).select(' id, brand_name,verified, is_deleted, attributes ,updated_on, is_to_be_deleted, created_on,scraping_data->>company_job_url', 'country_job_scrape_map', count = 'exact'
                ).not_.is_('scraping_data->>company_job_url','null'
                ).eq('verified', True
                ).eq('is_deleted', False
                ).eq('is_to_be_deleted',False
                # ).in_('attributes->>band',["L1", 'L2','L3','L4']
                ).not_.is_(f'country_job_scrape_map->>{country_filter}', 'null'
                )

                total_job_count_res=get_and_apply_filters(country_filter,total_job_count_res)
                total_job_count_response= total_job_count_res.limit(1).execute()

                total_job_count= total_job_count_response.count
                
                
                print(total_job_count)
                
                
                
                supabase.table('cycles').update({'remaining_row_count':res.count,'total_count':total_job_count}).eq('cycle_type', CYCLE_TYPE).execute()
            
            
            
            if count == 0 and is_master_sys:
                print('insdde reset')
                manage_cycles()
       


            for r in res.data:
                # company_job_url= r['companies']['company_job_url']
                # scapre_data_table_id = r['company_id']
                # comp_name = r['companies']['brand_name']
                
                # comp_id = r['companies']['id']
                # updated_on = r['companies']['updated_on']

                # countrywise_data = r['new_countries']
                company_job_url= r['company_job_url']
                scapre_data_table_id = r['id']
                comp_name = r['brand_name']
                
                comp_id = r['id']
                updated_on = r['updated_on']

                countrywise_data = r['country_job_scrape_map']
                jobs_last_scraped=r.get('jobs_last_scraped_date') if r.get('jobs_last_scraped_date') else {}

                


                if 'f_C' not in company_job_url:

                            countrywise_data[country_filter]=not CURRENT_BOOL
                            jobs_last_scraped[country_filter]=scraped_on
                            

                            print(company_job_url)                            
                            scraped_on = datetime.now(timezone.utc).isoformat()
                            supabase.table('companies').update({'country_job_scrape_map': countrywise_data, 'jobs_last_scraped_date':jobs_last_scraped}, ).eq('id',scapre_data_table_id).execute()

                            # supabase.table('companies').update({filter_type: not CURRENT_BOOL, 'linkedin_last_scraped_at':scraped_on}, ).eq('company_id',scapre_data_table_id).execute()
                            continue


                print(company_job_url)
                
                if country_filter in countrywise_data.keys():
                        url = company_job_url
                        driver = setup_browser()
                        
                    
                        open_webpage(driver, url, country)

                        time.sleep(5)

                        page_loaded = is_page_loaded(driver)

                        if not page_loaded:
                            driver.quit()
                            continue


                        # try:
                        #     # Wait for the modal to be present
                        #     modal = WebDriverWait(driver, 10).until(
                        #         EC.presence_of_element_located((By.CLASS_NAME, 'contextual-sign-in-modal__screen'))
                        #     )
                            
                        #     print("Modal found. Attempting to dismiss with Escape key.")
                            
                        #     # Send Escape key to the body of the page
                        #     body = driver.find_element(By.TAG_NAME, 'body')
                        #     body.send_keys(Keys.ESCAPE)
                            
                        #     # Wait for the modal to disappear
                        #     WebDriverWait(driver, 10).until(
                        #         EC.invisibility_of_element_located((By.CLASS_NAME, 'contextual-sign-in-modal__screen'))
                        #     )
                            
                        #     print("Modal successfully dismissed.")

                        # except TimeoutException:
                        #     print("Modal with class 'contextual-sign-in-modal__screen' not found or didn't disappear after Escape key.")
                        # try:
                        #     # Wait for any visible modal overlay to appear
                        #     WebDriverWait(driver, 10).until(
                        #         EC.presence_of_element_located((By.CLASS_NAME, 'modal__overlay'))
                        #     )

                        #     print("Modal found. Forcing it to hide by injecting CSS using setAttribute.")

                        #     # Use JavaScript to forcibly override all styles via setAttribute
                        #     driver.execute_script("""
                        #         const modals = document.querySelectorAll('.modal__overlay');
                        #         modals.forEach(modal => {
                        #             modal.setAttribute('style', 'display: none !important; visibility: hidden !important; opacity: 0 !important;');
                        #         });
                        #     """)

                        #     print("Modal successfully hidden using setAttribute and !important.")

                        # except TimeoutException:
                        #     print("Modal not found or already hidden.")

                        hide_modal(driver)
                        is_jobs_avail = check_if_jobs_available(driver)


                        if not is_jobs_avail:
                            scraped_on = datetime.now(timezone.utc).isoformat()
                            countrywise_data[country_filter]=not CURRENT_BOOL
                            jobs_last_scraped[country_filter]=scraped_on
                            supabase.table('companies').update({'country_job_scrape_map': countrywise_data, 'jobs_last_scraped_date':jobs_last_scraped}, ).eq('id',scapre_data_table_id).execute()


                            # supabase.table('company_scrape_data').update({filter_type: not CURRENT_BOOL}, ).eq('company_id',scapre_data_table_id).execute()
                            driver.delete_all_cookies()

                            # NEED TO LOG TO TRANSACTION TABLE HERE
                            supabase.table('transaction_log').insert({"transaction_type":"com_scraped", 'system_id':SYSTEM_ID}).execute()
                            driver.quit()
                            continue
                    


                      

                        # filter_by_timeframe(driver, timeframe = 'Past 24 hours')


                        if ( driver.current_url == 'https://www.linkedin.com/') or ('https://www.linkedin.com/authwall?' in driver.current_url) or ('https://www.linkedin.com/?original_referer' in driver.current_url):
                            driver.quit()
                            continue
                        


                        is_jobs_avail = check_if_jobs_available(driver)





                        if not is_jobs_avail:
                            scraped_on = datetime.now(timezone.utc).isoformat()
                            countrywise_data[country_filter]=not CURRENT_BOOL
                            jobs_last_scraped[country_filter]=scraped_on
                            supabase.table('companies').update({'country_job_scrape_map': countrywise_data, 'jobs_last_scraped_date':jobs_last_scraped}, ).eq('id',scapre_data_table_id).execute()


                            # supabase.table('company_scrape_data').update({filter_type: not CURRENT_BOOL}, ).eq('company_id',scapre_data_table_id).execute()
                            driver.delete_all_cookies()

                            # LOG TO TRANSACTION LOG
                            supabase.table('transaction_log').insert({"transaction_type":"com_scraped", 'system_id':SYSTEM_ID}).execute()
                            driver.quit()
                            continue


                        #scrap data from company_job_url
                        is_login = scrap_jobs_info(driver, comp_name, comp_id, country)
                        
                        if is_login:
                            driver.delete_all_cookies()
                            
                           

                            driver.quit()
                            continue
                        



                        print(countrywise_data)
                        
                        # driver.close()
                        driver.quit()
                        
                        
                 
                        
                scraped_on = datetime.now(timezone.utc).isoformat()
                countrywise_data[country_filter]=not CURRENT_BOOL
                jobs_last_scraped[country_filter]=scraped_on            
                supabase.table('companies').update({'country_job_scrape_map': countrywise_data, 'jobs_last_scraped_date':jobs_last_scraped}, ).eq('id',scapre_data_table_id).execute()


                # supabase.table('company_scrape_data').update({filter_type: not CURRENT_BOOL, 'linkedin_last_scraped_at':scraped_on, }, ).eq('company_id',scapre_data_table_id).execute()
                supabase.table('transaction_log').insert({"transaction_type":"com_scraped", 'system_id':SYSTEM_ID}).execute()




                time.sleep(2)
                    
                
    except Exception as e:
        print("error", e)
        # driver.quit()
                

if __name__ == "__main__":
    main()
