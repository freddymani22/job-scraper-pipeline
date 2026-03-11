from bs4 import BeautifulSoup, NavigableString, Tag
import spacy
import re
from datetime import datetime, timedelta
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from supabase import create_client, Client
import random
# from configs import *
import json
import openai
import chevron
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse, unquote
from mistralai import Mistral
from time import sleep
import requests
import os
from dotenv import load_dotenv

load_dotenv()

#set up local variables for supabase using ENV

url = os.environ["SUPABASE_URL"]
key = os.environ["SUPABASE_KEY"]
supabase: Client = create_client(url, key)




client_deep = openai.OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")

client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])




countries_map = {
    "India": "in",
    "United Kingdom": "uk",
    "Netherlands": "nl",
    "Germany": "de",
    "Canada": "ca",
    "Singapore": "sg",
    "France": "fr",
    "Japan": "jp",
    "Australia": "au",
    "United States": "us"
}




roles = [
    {
        "name": "Ruby on Rails Backend Developer",
        "id": "6c7bf76d-cb84-48ab-882f-2885f0d6d30f",
        "category": "C1",
        "ordering": "42"
    },
    {
        "name": "SAP Developer",
        "id": "38f69e5a-3253-4838-981a-ad975054fe3b",
        "category": "C2",
        "ordering": "76"
    },
    {
        "name": "Technical Writer",
        "id": "6d354fcd-5be2-4a45-b05d-1afe2e062c1e",
        "category": "C3",
        "ordering": "1"
    },
    {
        "name": "Director",
        "id": "183f50fa-47a8-4ffa-970f-593cb5422a22",
        "category": "C3",
        "ordering": "17"
    },
    {
        "name": "Golang Backend Developer",
        "id": "13cdc59c-d9cb-4aa5-a550-7d6e524e34d0",
        "category": "C1",
        "ordering": "43"
    },
    {
        "name": "Database Developer",
        "id": "7ead99d7-87c0-4986-84bf-2f904cfa1d77",
        "category": "C2",
        "ordering": "69"
    },
    {
        "name": "Security Engineer",
        "id": "55497847-1eea-4947-bfb6-ec167923d902",
        "category": "C2",
        "ordering": "66"
    },
    {
        "name": "React Native Developer",
        "id": "3777b684-d848-4483-909d-d84b10544834",
        "category": "C1",
        "ordering": "46"
    },
    {
        "name": "Cloud Developer",
        "id": "1eb5bff7-efc0-4985-98eb-5676b35762eb",
        "category": "C2",
        "ordering": "62"
    },
    {
        "name": "DevOps Engineer",
        "id": "ca617812-a940-4409-9cfd-4b959899f149",
        "category": "C1",
        "ordering": "50"
    },
    {
        "name": "Business Analyst",
        "id": "9e924378-a124-442b-ac0a-7bab87a74198",
        "category": "C2",
        "ordering": "13"
    },
    {
        "name": "Admin",
        "id": "2daf4dc5-70ce-46d1-8b7d-436a99f31f43",
        "category": "C3",
        "ordering": "7"
    },
    {
        "name": "Oracle Consultant",
        "id": "2e4aebe1-fe39-4130-a95c-fa7e1476cdff",
        "category": "C3",
        "ordering": "77"
    },
    {
        "name": "Talent Acquisition",
        "id": "21da94f8-b485-4e94-a02e-f22cd68ca143",
        "category": "C3",
        "ordering": "8"
    },
    {
        "name": "VueJS Developer",
        "id": "c293c8ff-6d28-4535-bdb9-457626a5353f",
        "category": "C1",
        "ordering": "35"
    },
    {
        "name": "ASP.NET Backend Developer",
        "id": "94f225cf-8e54-438e-b83c-02d99b0a0df6",
        "category": "C1",
        "ordering": "40"
    },
    {
        "name": "PHP Backend Developer",
        "id": "8ae5394c-f09a-42f2-9c65-27dd82c2f94c",
        "category": "C1",
        "ordering": "41"
    },
    {
        "name": "Fullstack Developer",
        "id": "3abfa819-a382-4660-afe0-9c405ade2f22",
        "category": "C1",
        "ordering": "32"
    },
    {
        "name": "UI/UX Designer",
        "id": "29503dc7-1240-42c1-b4d4-2f4f8dcaeab6",
        "category": "C2",
        "ordering": "71"
    },
    {
        "name": "Google Cloud Platform Developer",
        "id": "4d7e7313-bc5c-4313-8a34-2501451fc342",
        "category": "C2",
        "ordering": "58"
    },
    {
        "name": "Product Manager",
        "id": "3260841e-d763-4eab-ad61-3f8c9a64d7c5",
        "category": "C3",
        "ordering": "14"
    },
    {
        "name": "SQL Database Developer",
        "id": "b8e08361-524a-4e3a-9313-3ebcd0f3776d",
        "category": "C2",
        "ordering": "57"
    },
    {
        "name": "Embedded Developer",
        "id": "8403c7dc-732f-418b-b153-efcebb592ac7",
        "category": "C2",
        "ordering": "65"
    },
    {
        "name": "Backend Developer",
        "id": "5dad4984-90b1-447c-b5f6-26c12d9cee16",
        "category": "C1",
        "ordering": "44"
    },
    {
        "name": "Project Manager",
        "id": "cdf900c7-8567-4ee0-b023-c395fd01d5a8",
        "category": "C3",
        "ordering": "12"
    },
    {
        "name": "AngularJS Developer",
        "id": "eae910e1-0bb7-4e3f-905f-e6bf2c4d4f32",
        "category": "C1",
        "ordering": "34"
    },
    {
        "name": "Network Engineer",
        "id": "e1dd9b18-620e-4c37-afe7-922085e48d64",
        "category": "C2",
        "ordering": "67"
    },
    {
        "name": "Product Designer",
        "id": "d000b2ed-967f-4f46-b663-986448ec4487",
        "category": "C3",
        "ordering": "15"
    },
    {
        "name": "Ruby on Rails Fullstack Developer",
        "id": "2c4c7d33-f335-4cdb-b974-f0559aa60790",
        "category": "C1",
        "ordering": "31"
    },
    {
        "name": "Java Fullstack Developer",
        "id": "123aff4a-a23e-44fd-b65f-2673c8917792",
        "category": "C1",
        "ordering": "29"
    },
    {
        "name": "Java Backend Developer",
        "id": "e12c32a3-d6e0-4e1f-a892-fd7591923b7a",
        "category": "C1",
        "ordering": "37"
    },
    {
        "name": "Automation Test Engineer",
        "id": "0114e2d5-a71a-431d-9696-1a07d315464e",
        "category": "C2",
        "ordering": "23"
    },
    {
        "name": "Azure Developer",
        "id": "e1ef21b4-c335-416a-a445-8918281f6e10",
        "category": "C2",
        "ordering": "59"
    },
    {
        "name": "Data Scientist",
        "id": "b149edfc-b704-4187-87bc-88e8ad39454a",
        "category": "C1",
        "ordering": "55"
    },
    {
        "name": "Supply Chain Roles",
        "id": "200b66a5-c887-43ff-a490-a776ec170159",
        "category": "C3",
        "ordering": "6"
    },
    {
        "name": "Physical Design Engineer",
        "id": "0cbe0e1d-9bee-43bf-b103-35601afc94f7",
        "category": "C2",
        "ordering": "63"
    },
    {
        "name": "System Engineer",
        "id": "f8654be9-ac42-4a8b-a765-773c02a948ac",
        "category": "C2",
        "ordering": "68"
    },
    {
        "name": "Salesforce Developer",
        "id": "e16f07a9-6295-444b-9663-b7c92b519803",
        "category": "C3",
        "ordering": "78"
    },
    {
        "name": "AI Developer",
        "id": "c2a4062a-76c3-4517-836b-471c0731ebf2",
        "category": "C1",
        "ordering": "53"
    },
    {
        "name": "Mobile Developer",
        "id": "554999ac-ae71-4081-bfcb-90ca09ce579c",
        "category": "C1",
        "ordering": "49"
    },
    {
        "name": "Business Development Specialist",
        "id": "91af04b9-9a5c-40c2-9bd1-6dda470a13d0",
        "category": "C3",
        "ordering": "-1"
    },
    {
        "name": "Finance",
        "id": "5528c31a-8cc5-4f00-9a67-251d50ca384d",
        "category": "C3",
        "ordering": "4"
    },
    {
        "name": "Analog Engineer",
        "id": "4e581d4a-36e6-43fa-91ca-0df8d5d97d46",
        "category": "C3",
        "ordering": "64"
    },
    {
        "name": "Game Developer",
        "id": "34c8a763-138f-4cc5-9c6c-43d822102b9e",
        "category": "C2",
        "ordering": "75"
    },
    {
        "name": "IOS Developer",
        "id": "68c24321-3e79-4704-bb3f-c5057fef1fd4",
        "category": "C1",
        "ordering": "47"
    },
    {
        "name": "Frontend Developer",
        "id": "301676de-3cc5-4455-8947-082f11cf85da",
        "category": "C1",
        "ordering": "36"
    },
    {
        "name": "Graphic Designer",
        "id": "1343eaef-4b13-4166-a1b0-df172555db49",
        "category": "C3",
        "ordering": "27"
    },
    {
        "name": "Vice President",
        "id": "10bccf75-5826-4821-8819-359d2aa19f40",
        "category": "C3",
        "ordering": "18"
    },
    {
        "name": "MERN Stack Developer",
        "id": "abd2fd71-5947-4658-b1b5-8ca42a49d1d8",
        "category": "C1",
        "ordering": "28"
    },
    {
        "name": "Silicon Design Engineer",
        "id": "0daf14df-2af9-4a4c-9fa0-62c74dc99f4c",
        "category": "C2",
        "ordering": "61"
    },
    {
        "name": "AWS Developer",
        "id": "0882fb58-58ee-4601-9a48-9546c0143e2d",
        "category": "C2",
        "ordering": "60"
    },
    {
        "name": "Data Engineer",
        "id": "05b60acf-4f73-4713-afc7-a0edc5ee153b",
        "category": "C1",
        "ordering": "70"
    },
    {
        "name": "Digital Marketing",
        "id": "7aceeb0f-86e5-4ace-969a-5b2fa6730eb1",
        "category": "C3",
        "ordering": "9"
    },
    {
        "name": "Engineering Manager",
        "id": "ac3342dc-cd43-4738-8480-7ac6ad59ba64",
        "category": "C3",
        "ordering": "16"
    },
    {
        "name": "ReactJS Developer",
        "id": "4dae1194-8b6e-484a-b078-29660a0e80db",
        "category": "C1",
        "ordering": "33"
    },
    {
        "name": "Reliability Engineer",
        "id": "2058dd20-2f36-48da-8de4-d9a54c46494b",
        "category": "C1",
        "ordering": "51"
    },
    {
        "name": "Human Resources",
        "id": "d7cd627d-b9f7-4945-b582-0e3f13a35cb7",
        "category": "C3",
        "ordering": "5"
    },
    {
        "name": "Python Fullstack Developer",
        "id": "ab822802-4934-462e-843b-adf940afa3a6",
        "category": "C1",
        "ordering": "30"
    },
    {
        "name": "Hardware Engineer",
        "id": "9874657c-44d5-4421-bddf-69ea88e398ba",
        "category": "C2",
        "ordering": "26"
    },
    {
        "name": "Java Developer",
        "id": "9d3a6983-5049-41d7-a180-12cf0db4e95b",
        "category": "C1",
        "ordering": "72"
    },
    {
        "name": "ASIC Engineer",
        "id": "76a2c818-7a86-454e-b9ed-6e1e341dc77a",
        "category": "C2",
        "ordering": "25"
    },
    {
        "name": "Big Data Engineer",
        "id": "abc4286e-8dea-4ab7-a158-750643b2a456",
        "category": "C1",
        "ordering": "52"
    },
    {
        "name": "Program Manager",
        "id": "a8e0c390-2aaf-45cd-ac38-9d9cd87a2bb9",
        "category": "C3",
        "ordering": "10"
    },
    {
        "name": "Python Developer",
        "id": "253d789b-460f-40d6-a39d-845ee98024d5",
        "category": "C1",
        "ordering": "73"
    },
    {
        "name": "NodeJS Developer",
        "id": "f305a78f-0af6-4cdd-ab76-d21a93f2ddc5",
        "category": "C1",
        "ordering": "39"
    },
    {
        "name": "Marketing",
        "id": "d2bfa23a-4d4b-44b5-ae4d-34d1acf5dee2",
        "category": "C3",
        "ordering": "3"
    },
    {
        "name": "Django Backend Developer",
        "id": "6e05f14a-5a2b-4b77-a192-f34bb6d854bc",
        "category": "C1",
        "ordering": "38"
    },
    {
        "name": "Recruiter",
        "id": "8cc7091b-2573-470c-be92-f310aecb3b96",
        "category": "C3",
        "ordering": "21"
    },
    {
        "name": "QA Engineer",
        "id": "8517975f-9d5e-4b40-ae29-2e3b02e64daf",
        "category": "C2",
        "ordering": "24"
    },
    {
        "name": "Flutter Developer",
        "id": "03007f41-3189-436c-a82c-c65241bb51f2",
        "category": "C1",
        "ordering": "45"
    },
    {
        "name": "Android Developer",
        "id": "f945cfd6-bb7d-45c2-be48-11cfdad52d17",
        "category": "C1",
        "ordering": "48"
    },
    {
        "name": "Machine Learning Developer",
        "id": "33d99058-65c0-4dd1-80f4-99485eac2c6e",
        "category": "C1",
        "ordering": "53"
    },
    {
        "name": "Sales",
        "id": "c7d51e4e-366b-4b8c-9a3f-02c4a6d491bc",
        "category": "C3",
        "ordering": "2"
    },
    {
        "name": "Data Analyst",
        "id": "ed4fa7cf-f622-4f9e-8039-fff3fba31f04",
        "category": "C1",
        "ordering": "56"
    }
]









#clean ai response
def clean_jobs_json_string(result):
    """
    Cleans a JSON string that may contain explanatory text, backticks, and other content.
    Returns a clean JSON string ready for parsing.
    """
    # Remove ```json and ``` if present
    result = result.replace('```json', '').replace('```', '')
    
    # Find the JSON object boundaries
    try:
        json_start = result.find('{')
        json_end = result.rfind('}') + 1
        
        if json_start == -1 or json_end == 0:
            raise ValueError("No JSON object found in the string")
            
        # Extract just the JSON part
        json_str = result[json_start:json_end]
        
        # Strip any leading/trailing whitespace
        json_str = json_str.strip()
        
        return json_str
        
    except ValueError as e:
        print(f"Error cleaning JSON string: {e}")
        return None






def mistral_ai(user_message):
    api_key = os.environ["MISTRAL_API_KEY"]
    model_name = "mistral-small-latest"


    # Initialize the Mistral client
    client = Mistral(api_key=api_key)

    # Make a chat request
    chat_response = client.agents.complete(
         agent_id="ag:7bcb4c28:20250214:untitled-agent:b02ab32e",
        messages=[
            {
                "role": "user",
                "content": user_message,
       

            },
        ]
    )

    # Convert the response to JSON format
    response_json = json.dumps(chat_response, default=lambda o: o.__dict__, indent=4)



    response_dict = json.loads(response_json)

    result = response_dict.get('choices')[0].get('message').get('content')


    cleaned_json_str = clean_jobs_json_string(result)


    result_obj = json.loads(cleaned_json_str)
    


    #         # Convert JSON string to Python object (dictionary)
    # python_obj = json.loads(self.clean_json_string(result))

    return result_obj





def deepseek_ai(prompt):
    if prompt:
        # Create the chat completion
        completion = client_deep.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "system", "content": prompt}],
            response_format={"type": "json_object"},
        
        )
        
    
        # Parse the response
        res = json.loads(completion.choices[0].message.content)
        
        return res
    

def generalized_gpt_func(prompt):

      # Send a request to the API
     # Send request to the API with correct parameter structure
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Keeping your original model choice
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}  # This should be outside messages
        )
        
        # Get the response content directly
        content = response.choices[0].message.content
        
        # Parse the JSON content
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Fallback parsing for malformed JSON
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                json_str = json_str.replace("\n", "").strip()
                return json.loads(json_str)
            raise ValueError("Could not extract valid JSON from response")




def custom_strip(text):
    """
    Remove unwanted characters from the beginning and end of the text.
    """
    unwanted_chars = ['ÃÂÃÂ¢ÃÂ¢ÃÂÃÂ¬ÃÂÃÂ¢',': ','-', '.', '"', "~", '', "ÃÂÃÂ¢ÃÂÃÂÃÂÃÂ", '\u202f', '* ','* ', '1)', '2)', '3)', '4)', '5)', '6)', '7)', '8)', '9)', '10)']  # Include the non-breaking space character and numbered list items
    text = text.strip()  # Remove leading and trailing whitespaces first

    # Replace non-breaking space character with a regular space
    text = text.replace('\u202f', ' ')
    text = text.replace("ÃÂÃÂ¯ÃÂÃÂ¿ÃÂÃÂ½", ' ')

    # Remove leading unwanted characters
    while text and text[0] in unwanted_chars:
        text = text[1:]

    # Remove trailing whitespaces
    text = text.strip()

    return text


def add_period_to_lines(text):
    lines = text.split('\n')  # Split the text into lines
    lines_with_period = [line.strip() + '.' if line.strip() and not line.strip().endswith('.') else line.strip() for line in lines]
    return '\n'.join(lines_with_period)



def parse_exp(soup):
    # Get the complete text from the soup
    jd_element = soup.find(class_="description__text description__text--rich")

    if not jd_element:
        return []
    jd_text = jd_element.get_text(separator='\n').strip()
    jd_text_with_period = add_period_to_lines(jd_text)

    # Load the spaCy NLP model with the sentencizer component
    nlp = spacy.blank("en")
    nlp.add_pipe("sentencizer")

    # Load the custom skill patterns
    skill_pattern_path ="/home/kalibot-1/work/skills_pattern_for_jd.jsonl"
    ruler = nlp.add_pipe("entity_ruler", config={"overwrite_ents": True})
    ruler.from_disk(skill_pattern_path)

    # Process the text with the NLP pipeline
    doc = nlp(jd_text_with_period)

    # List to store sentences mentioning experience and skills
    experience_sentences = []

    # Iterate through the sentences in the document
    for sent in doc.sents:
        # Convert the sentence to lowercase
        sentence = sent.text.lower()

        # Check if the sentence contains the 'experience' keyword
        if 'experience' in sentence:
            # Check if the sentence also contains any skills
            for ent in sent.ents:
                # if ent.label_ == 'SKILL':
                    # Check if the sentence also contains a number of years
                    number_pattern = r'\b(zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|1[0-4]|\d)\b'
                    experience_matches = re.findall(number_pattern, sentence)
                    if experience_matches and ('year' in sentence or 'years' in sentence):
                        # Add the sentence to the list
                        experience_sentence = custom_strip(sent.text)
                        if not experience_sentence.endswith('.'):
                            experience_sentence += '.'
                        experience_sentences.append(experience_sentence)
                        break  # Move on to the next sentence

    return experience_sentences







def parse_job_title(soup):


    job_title_tag = soup.find(class_='top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title')
    job_title = job_title_tag.get_text(strip=True)

    
    cleaned_title = job_title.strip()

    return cleaned_title




def parse_exp_level(soup):
    # Assuming 'soup' is your BeautifulSoup object
    exp_level_tags = soup.find_all(class_="description__job-criteria-text description__job-criteria-text--criteria")

    # Ensure that there are at least two tags found

    job_type = None
    if len(exp_level_tags) < 2:
        exp_level = None
        job_type = None

    experience_level = exp_level_tags[0]
    work_type = exp_level_tags[1]

   
    if work_type is not None:
        job_type = work_type.get_text().strip()

    exp_level = experience_level.text.strip()

    if exp_level == 'Not Applicable':
        exp_level= None

    return exp_level, job_type
    




def parse_job_location(soup):

    location_tag = soup.find(class_="topcard__flavor-row")

    if location_tag:
        # Find all <span> elements within the location_tag
        span_elements = location_tag.find_all('span')
        
        # Check if there is a second span element
        if len(span_elements) >= 2:
            # Get the second span element and return its text content after stripping any leading or trailing whitespace
            location_info= span_elements[1].text.strip()


           

            location_info = location_info.split(',')[0] if ',' in location_info else location_info






        



        # Define a dictionary to map city names to standardized forms
        city_mappings = {
            "bengaluru": "Bengaluru",
            "bangalore": "Bengaluru",
            "Gurugram": "Gurgaon",  
            "Thiruvananthapuram Taluk":"Trivandrum",
            "Tondiarpet":"Chennai",
            "Mundgod":"Bengaluru",
            "Vishakhapatnam":"Visakhapatnam",
            "Greater Visakhapatnam Area":"Visakhapatnam",
            
            "Bagalur" :"Bengaluru",
            "Kanayannur":"Ernakulam",
            "Anekal":"Bengaluru",
            'Worli' :'Mumbai',
            "Greater Lucknow Area":"Lucknow",
            "Pimpri Chinchwad" :"Pune",
            "Kurla" :"Mumbai",
            "Bhiwandi" :"Mumbai",
            "Bhubaneshwar":"Bhubaneswar"
            
            # Add more city name mappings as needed
        }

        # Check if the location_info contains any of the mapped city names
        for city, standardized_city in city_mappings.items():
            if city.lower() in location_info.lower():
                return standardized_city

        # Define a list of the top 10 IT hubs in India
        top_it_hubs = ["Hyderabad", "Pune", "Chennai", "Noida", "Gurugram", "Gurgaon", "Mumbai", "Kolkata", "Visakhapatnam",  "Trivandrum", "Indore", "Delhi", "Coimbatore"]

        # Check if the location_info contains any other top IT hub
        for hub in top_it_hubs:
            if hub.lower() in  location_info.lower():
                return hub

        # If no match is found, return the original location_info
        return location_info
    else:
        print("Location element not found.")
        return None
        


def extract_linkedin_id(link="http://www.linkedin.com/in/rishab-srivastava-63a6a3170/"):
  """Extracts the LinkedIn ID from a given profile URL.

  Args:
      link (str, optional): The LinkedIn profile URL. Defaults to "http://www.linkedin.com/in/rishab-srivastava-63a6a3170/".

  Returns:
      str: The extracted LinkedIn ID, or None if the URL is invalid or doesn't follow the expected format.
  """

  # Prepend "https://" if necessary
  if not link.startswith("https://") and not link.startswith("http://"):
    link = "https://" + link

  # Parse the URL using urllib.parse.urlparse
  parsed_url = urlparse(link)

  # Check if the path starts with "/in/"
  if parsed_url.path and parsed_url.path.startswith("/in/"):
    # Extract the LinkedIn ID from the path
    linkedin_id = parsed_url.path[4:]  # Remove "/in/"

    # Handle potential trailing slash
    if linkedin_id.endswith("/"):
      linkedin_id = linkedin_id[:-1]

    # Handle leading slash (shouldn't occur in valid URLs)
    if linkedin_id.startswith("/"):
      linkedin_id = linkedin_id[1:]

    return linkedin_id
  else:
    return None  # URL is invalid or doesn't follow the expected format




def data_base_upsert(data,company,name):
    sleep(0.3)
    res = supabase.table("linkedin_connection_data").select('*').eq('company',company).eq('name',name).execute()
    
    response = res.data
    if response:
        if response[0]['id']:
            data['id'] = response[0]['id']
            
    try:
      update_response = supabase.table("linkedin_connection_data").upsert(data).execute()
    except Exception as e:
        print(e)



def scrape_hr_data(html_content, company):
    soup = BeautifulSoup(html_content, 'html.parser')
    link_element = soup.find('a', class_='base-card__full-link')

    if link_element:
        name = link_element.find('span', class_='sr-only').text.strip()
        
        
        linkedin_url = link_element['href'].split("?")[0]
        
        
        linkedin_unique_id =extract_linkedin_id(linkedin_url)
        
  

        return {
            'name': name,
            'linkedin_url': linkedin_url,
            'company': company,
            'job_posting_status': True,
            'linkedin_unique_id':linkedin_unique_id
        }
        
        
        
    else:
        return None
    



def extract_text_blocks(soup, company_name):
    blocks = []
    current_block = ""
    found_first_br = False
    company_name_pattern = re.compile(re.escape(company_name), re.IGNORECASE)

    for element in soup.descendants:
        if isinstance(element, NavigableString):
            if not found_first_br:
                current_block += element.strip() + " "
            else:
                current_block += element.strip() + " "
        elif isinstance(element, Tag) and element.name == 'br':
            found_first_br = True
            if current_block.strip() and not any(re.search(re.escape(part), current_block, re.IGNORECASE) for part in company_name.split()):
                blocks.append(current_block.strip())
            current_block = ""

    if current_block.strip() and not any(re.search(re.escape(part), current_block, re.IGNORECASE) for part in company_name.split()):
        blocks.append(current_block.strip())

    if found_first_br:
        last_br_tag = soup.find_all('br')[-1]
        for tag in last_br_tag.find_all_next():
            if tag.name == 'br':
                break
            if isinstance(tag, NavigableString):
                text = tag.strip()
                if text and not any(re.search(re.escape(part), text, re.IGNORECASE) for part in company_name.split()):
                    blocks.append(text)

    return blocks

def extract_text(elements):
    text = ""
    for element in elements:
        if isinstance(element, NavigableString):
            text += element.strip() + " "
        else:
            text += extract_text(element.contents)
    return text.strip()



def combine_text_blocks(soup, company_name):
    text_blocks = extract_text_blocks(soup, company_name)
    # last_br_tag = soup.find_all('br')[-1]
    # remaining_text = extract_text(last_br_tag.find_all_next())
    combined_text = "\n".join(text_blocks) + "\n" 
    return combined_text





def remove_company_name(text, company_name):
    
    
    # Create a case-insensitive regex pattern for the company name
    company_name_pattern = re.compile(re.escape(company_name), re.IGNORECASE)

    # Split the text into lines
    lines = text.split('\n')

    # Create a list to store the lines without the company name block
    cleaned_lines = []

    # Iterate through the lines
    for line in lines:
        # Check if the line contains the company name
        if company_name_pattern.search(line):
            # If the line contains the company name, skip it
            continue
        else:
            # If the line doesn't contain the company name, add it to the cleaned_lines list
            cleaned_lines.append(line)

    # Join the cleaned lines back into a single string
    cleaned_text = '\n'.join(cleaned_lines)

    return cleaned_text





def print_text_between_ids(soup, id_list, company_name):
    if not id_list:
        print("The id_list is empty.")
        return ""

    combined_text = ""

    if len(id_list) < 2:
        # Take the entire text from start until the last tagged element
        last_element = soup.find(id=id_list[-1])
        if last_element:
            current_tag = soup.find()
            while current_tag and current_tag != last_element:
                combined_text += current_tag.get_text(separator=' ', strip=True) + ' '
                current_tag = current_tag.find_next_sibling()

            # Include the text of the last tagged element and the remaining text
            combined_text += last_element.get_text(separator=' ', strip=True) + ' '
            current_tag = last_element.find_next_sibling()
            while current_tag:
                combined_text += current_tag.get_text(separator=' ', strip=True) + ' '
                current_tag = current_tag.find_next_sibling()

        cleaned_text = remove_company_name(combined_text.strip(), company_name)
        return cleaned_text

    # Add text from the beginning until the first tagged element
    first_element = soup.find(id=id_list[0])
    if first_element:
        previous_tag = first_element.find_previous_sibling()
        while previous_tag:
            combined_text = previous_tag.get_text(separator=' ', strip=True) + ' ' + combined_text
            previous_tag = previous_tag.find_previous_sibling()

    for i in range(len(id_list) - 1):
        id1 = id_list[i]
        id2 = id_list[i + 1]
        element1 = soup.find(id=id1)
        element2 = soup.find(id=id2)

        if element1 is None or element2 is None:
            combined_text += f"One of the elements with ids '{id1}' or '{id2}' was not found.\n"
            continue

        text_between = element1.get_text(separator=' ', strip=True) + ' '
        current_tag = element1.find_next_sibling()
        while current_tag and current_tag != element2:
            text_between += current_tag.get_text(separator=' ', strip=True) + ' '
            current_tag = current_tag.find_next_sibling()

        cleaned_text = remove_company_name(text_between.strip(), company_name)

        combined_text += cleaned_text + "\n---\n"

    # Add text after the last tagged element
    last_element = soup.find(id=id_list[-1])
    if last_element:
        remaining_text = ''
        current_tag = last_element.find_next_sibling()
        while current_tag:
            remaining_text += current_tag.get_text(separator=' ', strip=True) + ' '
            current_tag = current_tag.find_next_sibling()

        cleaned_remaining_text = remove_company_name(remaining_text.strip(), company_name)
        combined_text += cleaned_remaining_text

    return combined_text
 
 
 
def generate_unique_id(base, counter):
    return f"{base}_{counter}"
   


def find_two_word_tags(soup):
    positive_words_patterns = [
        'response', 'preferred', 'qualification', 'experience', 'skills',
        'require', 'role', 'must have', 'description', 'education', 'degree',
        'nice to have', 'job summary', 'requirements'
    ]

    # Escape special characters for regex
    positive_regex = '|'.join([re.escape(pattern) for pattern in positive_words_patterns])
    positive_regex_pattern = re.compile(positive_regex, re.IGNORECASE)

    counter = 0  # Initialize a counter for unique IDs
    id_list = []  # List to store generated IDs

    for tag in soup.find_all(True):  # Find all tags
        tag_text = tag.get_text(separator=' ').strip()
        if len(tag_text.split()) <= 8:  # Check if the tag contains six words or less
            if positive_regex_pattern.search(tag_text):
                unique_id = generate_unique_id('tag', counter)
                tag['id'] = unique_id  # Add unique ID to the tag
                id_list.append(unique_id)  # Store the generated ID
                counter += 1  # Increment the counter for the next unique ID

    return soup, id_list




   
def parse_skillset(soup, company_name):
    
    jd_element = soup.find(class_="description__text description__text--rich")
    
    new_soup, ids_list = find_two_word_tags(jd_element)
    
    parsed_skills = set() 
           
    text = print_text_between_ids(new_soup, ids_list, company_name)

    text += '\n'

    text +=  combine_text_blocks(jd_element,company_name)
    
    
    nlp = spacy.blank("en")
    # Add sentencizer component to the pipeline
    nlp.add_pipe("sentencizer")
    

    # Load your custom skill patterns
    skill_pattern_path ="/home/kalibot-1/work/merged_unique.jsonl"
    # Add the entity ruler with custom skill patterns
    ruler = nlp.add_pipe("entity_ruler", config={"overwrite_ents": True})
    ruler.from_disk(skill_pattern_path)
    skills = set()
    parsed_skills = set()  # Set to store lowercase normalized skills

    # Use a set to store unique skills
    doc = nlp(text)
    
    # for sentence in doc.text:
        # if 'experience' in sentence.lower():
            # print(sentence.text)
        
        
    for ent in doc.ents:
        if ent.label_ == 'SKILL':
            skill = ent.text
            # Split the skill at spaces (' ')
            skills.add(skill)
            
            
    standardized_skills = {
        'VueJS': ['vue.js', 'vuejs', 'vue', 'vue js'],
        'ReactJS': ['react', 'react js', 'react.js', 'reactjs'],
        'AngularJS': ['angular', 'angular js', 'angular.js', 'angularjs'],
        'NodeJS': ['node', 'node js', 'node.js', 'nodejs'],
        'BackboneJS': ['backbone', 'backbone js', 'backbone.js', 'backbonejs'],
        'ExpressJS': ['express', 'express js', 'express.js', 'expressjs'],
        'HandlebarsJS': ['handlebars', 'handlebars js', 'handlebars.js', 'handlebarsjs'],
        'NextJS': ['next', 'next js', 'next.js', 'nextjs'],
        'SvelteJS': ['svelte', 'svelte js', 'svelte.js', 'sveltejs'],
        'EmberJS': ['ember', 'ember js', 'ember.js', 'emberjs'],
        'RxJS': ['rx js', 'rx.js', 'rxjs'],
        
        'Web3JS' :['web3js'],
        
        'NightwatchJS': ['nightwatchjs'],
        'RequireJS':['requirejs'],
        'D3JS': ['d3.Js'],
        'Redux': ['redux', 'redux js', 'redux.js', 'reduxjs'],
        'NightwatchJS': ['nightwatch.js'],
        'D3JS': ['d3.Js'],
        'gRPC' :['grpc'],
        'ES6' :['es6'],
        'AI':['artificial intelligence'],
        'Database' :['databases'],
        'Azure Cosmos DB' :['cosmos db'],
        'PHP':['php framework'],
        'Embedded Systems':['embedded system'],
        'Azure Cosmos DB' :['cosmos db'],
        'Amazon DynamoDB' :['dynamodb'],
            'Power BI' :['powerbi'],
        "SQL" :['sql', 'mysql', 'sql databases', 'sqlite','sql db'],
        "REST API" : ['restful apis'],
        "Amazon EC2" :['ec2', 'aws ec2'],
        'Amazon S3' :['s3', 'aws s3'],
        
        'ML':['machine learning'], 
    
    
        
    }

    technologies =['DAC', 'TCP IP', 'SQL server', 'CDN', 'ETL', 'SQL DB', 'SOA', 'Tailwind CSS', 
                   'DBMS', 'CAP theorem', 'Microsoft SQL server', 'DFM', 'JTAG', 'SSIS', 'WIFI', 
                   '.NET Framework', 'ADO.NET', 'Azure Cosmos DB', 'RSpec', 'API gateway', 'REST API',
                   'IBM Db2', 'OAUTH', 'GitHub', 'LWC', 'SQLAlchemy', 'RDF', 'SPI', 'JUnit', 
                   'CouchDB', 'SMA*', 'MEAN', 'C/C++', 'Owasp ZAP', 'MariaDB', 'AWS Cloudformation', 
                   'GPS', 'MATLAB', 'Power BI', 'Chef', 'REST assured', 'ML', 'EKS', 'HTML5', 
                   'AWS Codebuild', 'IAM', 'ArangoDB', 'RTL design', 'JIRA', 'GDB', 'MVC Architecture', 
                   'API Gateway', 'BLE', 'SQLite', 'DevOps', 'DFA', 'UX Design', 'Microsoft SQL Server',
                   'OpenGL', 'Amazon S3', 'MySQL', 'UART', 'FPGA', 'SVN', 'ORM', 'NPM', 'UI Design',
                   '.NET Core', 'EHS', 'Amazon DynamoDB', 'LambdaTest', 'IOT', 'RxSwift', 'TimescaleDB', 
                   'CMOS', 'InfluxDB', 'Exploratory Data Analysis EDA', 'JSX', 'Django REST framework',
                   'SAP fiori', 'I2C', 'API design', 'RAML', 'RTL coding', 'SwiftUI', 'iOS SDK', 
                   'SonarQube', 'NoSQL', 'SignalR', 'API testing', 'GraphQL', 'I2S', 'ELK stack', 'OOP',
                   'SQLite DB', 'ASP.NET', 'IOS', 'Azure SDK', 'RESTful API', 'MQTT', 'API Testing', 'C',
                   'SQL databases', 'OWASP ZAP', 'Semantic HTML', 'SQL', 'API', 'Google Cloud SDK', 'CAN',
                   'JMeter', 'SoapUI', 'AWS', 'YII', 'DynamoDB', 'ELK Stack', 'SAS', 'JavaScript', 'LXD', 
                   'Cisco ASA', 'AWS IoT', 'DFD', 'TypeScript', 'JSON', 'SQL Server', 'NLTK', 'JQuery', 
                   'OpenCV', 'UI design', 'PWM', 'ES6+', 'ArgoCD', 'GitLab CI', 'AWS CloudFormation', 
                   'Synopsys ICC', 'NumPy', 'AWS CDK', 'Django ORM', 'CSS', 'PWA', 'Voice Over IP', 
                   'Amazon RDS', 'SAML', 'Django REST Framework', 'AWS IAM', 'ASP.NET MVC', 'SOQL', 
                   'Search Engine', 'VBA', 'ADC', 'S3', 'GCP', 'GSM', 'API Design', 'CISCO', 'EDA Tools', 
                   'ADC DAC', 'ChatOps', 'Voice And SMS', 'AWS RDS', 'ZeroMQ', 'HTML', 'Swagger UI', 
                   'ASIC design', 'RTOS', 'ASIC Design', 'VMware vSphere', 'Angular CLI', 'YARN', 'VCS', 
                   'Ki CAD', 'ETL Tools', 'Natural Language Processing NLP', 'Kendo UI', 'COBOL', 'VLSI', 
                   'REST', 'LTE', 'IBM DB2', 'AWS Codepipeline', 'CRM', 'R', 'SASS', 'Zephyr OS', 'ABAP', 
                   'SEO', '.NET framework', 'UX design', 'APEX', 'LXC', 'SPICE', 'Android SDK', 'SAP', 
                   'PostgreSQL', 'gRPC', 'C++', 'IBM cloud', 'AI', 'MERN', 'IntelliJ', 'UIKit', 'MobX', 
                   'PyTorch', 'ETL tools', 'TCL', 'EC2', 'CI CD', 'HANA', 'COSMOS DB', 'Single File Components SFC', 
                   'XML', 'AWS EC2', 'LINQ', '.NET', 'FPGA Design', 'Google Cloud Platform GCP', 'BERT',
                   'P2P', 'RabbitMQ', 'BSP', 'GitLab', 'Google cloud SQL', 'Amazon SNS', 'OWASP', 'NLP', 
                   'USB', 'SOLID principles', 'Gitlab CI', 'RxJava', 'WCF', 'PCB layout', 'Cosmos DB', 'ASIC', 
                   'API Automation', 'SOSL', 'MVC', 'Multi Layer PCB design', 'SFD', 'ASP.NET Core', 'Neo4j', 
                   'WPF', 'API automation', 'SOAP', 'ActiveMQ', 'STLC', 'CAD', 'HSPICE', 'SFDC', 'NATS', 'NLU',
                   'DSA', 'AVA', 'F#', 'ES6', 'LoadRunner', 'PPC', 'PCB design', 'FastAPI', 'Material UI', 
                   'MongoDB Atlas', 'YAML', 'Restful APIS', 'SDLC', 'PCB Layout', 'STL', 'SPECTRA', 'SEM', 
                   'MVC architecture', 'AWS Lambda', 'MongoDB', 'C#', 'EDA tools', 'DSP', 'DDD', 'CI CD pipelines',
                   'VHDL', 'FPGA design', 'PHP', 'Vue CLI', 'Google Cloud API', 'Amazon EC2', 'GIT', 'SQL Databases', 
                   'NoSQL Databases', 'UI UX design']



    for skill in skills:
        skill_found = False
        if skill.lower() == 'java':
            parsed_skills.add('Java')
            continue

        for pattern, technologies_list in standardized_skills.items():
            for tech in technologies_list:
                if skill.lower() == tech.lower():
                    parsed_skills.add(pattern)
                    skill_found = True
                    break
            if skill_found:
                break

        if not skill_found:
            for tech in technologies:
                if skill.lower() == tech.lower():
                    parsed_skills.add(tech)
                    skill_found = True
                    break

        if not skill_found:
            parsed_skills.add(skill.title())
    

    return list(parsed_skills)





def convert_time_period(text):
    # Define regular expression patterns for days, weeks, hours, months, and years
    days_pattern = r'(\d+)\s+days?'
    weeks_pattern = r'(\d+)\s+weeks?'
    hours_pattern = r'(\d+)\s+hours?\s+ago'
    months_pattern = r'(\d+)\s+months?\s+ago'
    years_pattern = r'(\d+)\s+years?\s+ago'
    
    # print(text, '-----')

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




def parse_date_posted(soup, scraped_on):


    date_tag = soup.find_all(class_="topcard__flavor-row")

    if date_tag:
        # Find all <span> elements within the date_tag
        span_elements = date_tag[1].find_all('span')
        
        # Check if there is a second span element
        if len(span_elements) >= 2:
            # Get the second span element and return its text content after stripping any leading or trailing whitespace
            date_element = span_elements[0]



    if date_element:
        # Extract the inner text of the element
        date_posted_text = date_element.get_text(strip=True)
        days_ago = convert_time_period(date_posted_text)

        if days_ago is not None:
             # Convert scraped_on to datetime object
            scraped_on_datetime = datetime.strptime(scraped_on, '%Y-%m-%dT%H:%M:%S.%f')
            # Calculate the posted date by subtracting days_ago from scraped_on_datetime
            date_posted = scraped_on_datetime - timedelta(days=days_ago)
            # Convert date_posted to ISO 8601 formatted string
            date_posted_str = date_posted.date().isoformat()
            return date_posted_str

    # If date element not found using the primary class, try alternative classes
    date_element = soup.find(class_="tvm__text tvm__text--neutral") or soup.find(class_="tvm__text tvm__text--positive")
    if date_element:
        reposted_ago = date_element.get_text()
        days_ago = convert_time_period(reposted_ago)

        if days_ago is not None:
            # Calculate the posted date by subtracting days_ago from the scraped_on datetime
            scraped_on_datetime = datetime.strptime(scraped_on, '%Y-%m-%d %H:%M:%S.%f')
            date_posted = scraped_on_datetime - timedelta(days=days_ago)
            # Convert date_posted to ISO 8601 formatted string
            date_posted_str = date_posted.date().isoformat()
            return date_posted_str

    # If date element not found using any class, return current date
    return datetime.now().date().isoformat()



def parse_date_posted(soup, scraped_on):
    # Convert scraped_on to datetime object
    scraped_on_datetime = datetime.strptime(scraped_on, '%Y-%m-%dT%H:%M:%S.%f')

    date_tag = soup.find_all(class_="topcard__flavor-row")
    if date_tag:
        span_elements = date_tag[1].find_all('span')
        if len(span_elements) >= 1:
            date_element = span_elements[0]
            if date_element:
                date_posted_text = date_element.get_text(strip=True)
                days_ago = convert_time_period(date_posted_text)
                
                if days_ago is not None:
                    date_posted = scraped_on_datetime - timedelta(days=days_ago)
                    return date_posted.date().isoformat()

    # If date element not found using the primary class, try alternative classes
    date_element = soup.find(class_="tvm__text tvm__text--neutral") or soup.find(class_="tvm__text tvm__text--positive")
    if date_element:
        reposted_ago = date_element.get_text(strip=True)
        days_ago = convert_time_period(reposted_ago)
        
        if days_ago is not None:
            date_posted = scraped_on_datetime - timedelta(days=days_ago)
            return date_posted.date().isoformat()

    # If date element not found using any class, return scraped_on date
    return scraped_on_datetime.date().isoformat()


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
            parsed_redirect_url=get_final_url_or_original((urlunparse(parsed_redirect_url)))
            print('---------------------cleaned_url',parsed_redirect_url)
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



# def clean_job_url(job_url, linkedin_id):
#     """
#     Clean and transform job URLs, with special handling for LinkedIn URLs
#     and removal of LinkedIn-related parameters
#     """
#     # Handle 'Easy apply' case
#     if job_url == 'Easy apply':
#         return f'https://linkedin.com/jobs/view/{linkedin_id}'
    
#     # Handle LinkedIn authwall URLs
#     if job_url.startswith('https://www.linkedin.com/authwall') or \
#        job_url.startswith('http://www.linkedin.com/authwall'):
#         return f'https://linkedin.com/jobs/view/{linkedin_id}'
    
#     # Parse the URL
#     parsed_url = urlparse(job_url)
    
#     # Special handling for LinkedIn URLs
#     if 'linkedin.com' in parsed_url.netloc:
#         # Get query parameters
#         query_params = parse_qs(parsed_url.query)
        
#         # Define terms to remove
#         linkedin_terms = ['linkedin']
        
#         # Check for redirect URL
#         if 'url' in query_params:
#             # Decode the redirect URL
#             redirect_url = unquote(query_params['url'][0])
            
#             # Parse the redirect URL
#             parsed_redirect_url = urlparse(redirect_url)
#             redirect_query_params = parse_qs(parsed_redirect_url.query)
            
#             # Filter out LinkedIn-related parameters from redirect URL
#             filtered_redirect_params = {}
#             for key, values in redirect_query_params.items():
#                 # Check if the key contains any LinkedIn-related terms
#                 if not any(term in key.lower() for term in linkedin_terms):
#                     # Check if any value contains LinkedIn-related terms
#                     filtered_values = [
#                         value for value in values 
#                         if not any(term in str(value).lower() for term in linkedin_terms)
#                     ]
                    
#                     # Add to filtered params if values remain
#                     if filtered_values:
#                         filtered_redirect_params[key] = filtered_values
            
#             # Reconstruct the redirect URL without LinkedIn-related parameters
#             cleaned_redirect_url = urlunparse((
#                 parsed_redirect_url.scheme,
#                 parsed_redirect_url.netloc,
#                 parsed_redirect_url.path,
#                 parsed_redirect_url.params,
#                 urlencode(filtered_redirect_params, doseq=True),
#                 parsed_redirect_url.fragment
#             ))
            
#             return cleaned_redirect_url
        
#         # If no redirect URL, extract LinkedIn job ID
#         path_parts = parsed_url.path.split('/')
#         for part in path_parts:
#             if part.isdigit():
#                 return f'https://linkedin.com/jobs/view/{part}'
    
#     # Remove LinkedIn-related query parameters
#     query_params = parse_qs(parsed_url.query)
    
#     # Define terms to remove
#     linkedin_terms = ['linkedin']
    
#     # Filter out parameters containing LinkedIn-related terms
#     updated_query_params = {}
#     for key, values in query_params.items():
#         # Check if the key contains any LinkedIn-related terms
#         if not any(term in key.lower() for term in linkedin_terms):
#             # Check if any value contains LinkedIn-related terms
#             filtered_values = [
#                 value for value in values 
#                 if not any(term in str(value).lower() for term in linkedin_terms)
#             ]
            
#             # Add to updated params if values remain
#             if filtered_values:
#                 updated_query_params[key] = filtered_values
    
#     # Construct the updated query string
#     updated_query_string = urlencode(updated_query_params, doseq=True)
    
#     # Reconstruct the URL with the updated components
#     new_url = urlunparse((
#         parsed_url.scheme,
#         parsed_url.netloc,
#         parsed_url.path,
#         parsed_url.params,
#         updated_query_string,
#         parsed_url.fragment
#     ))
    
#     return new_url



def assign_role(job_title,primary_skills):
    roles_with_priority ={}
    roles = []
    p1=False
    
    if not job_title:
        return
    
    # Fetch roles from database
    sleep(0.1)
    roles_res = supabase.table('roles').select('attributes', 'id').eq('is_deleted', False).execute()
    
    # Initialize rules list
    rules = []
    
    # Define executive level roles that should return immediately
    executive_roles = [
    'Vice President', 'Director', 'Sales', 'Finance', 'Product Manager',
    'Business Development Specialist', 'Technical Writer', 'Data Scientist',
    'Project Manager', 'Digital Marketing', 'Admin', 'Engineering Manager',
    'Human Resources', 'Program Manager', 'Business Analyst', 'Graphic Designer',
    'Marketing', 'Recruiter', 'Talent Acquisition', 'Supply Chain Roles',
    'UI/UX Designer'
]

    
    # Keywords to match in job title
    keywords = r"(engineer|developer|analyst|intern|architect|lead|scientist|specialist|designer|director|consultant)"
    
    
    # Populate rules list with tuple (pattern, ordering, role_id, category, role_name)
    for role in roles_res.data:
        attributes = role['attributes']
        rules.append((
            attributes.get('role_search_using_title_p1'),
            attributes.get('ordering'),
            role['id'],
            attributes.get('category'),
            attributes.get('name')
        ))
    
    # Sort rules by ordering in ascending order
    rules.sort(key=lambda x: x[1])
    
    # First check for executive roles
    for pattern, ordering, role, category, role_name in rules:
        if re.search(pattern, job_title, re.IGNORECASE):
            if any(exec_role in job_title for exec_role in executive_roles):
                return {
                    "roles": role,
                    "ordering": ordering,
                    "category": category,
                    'priority':1
                }
    
    # Then check for other roles that contain specified keywords
    for pattern, ordering, role, category, role_name in rules:
        if re.search(pattern, job_title, re.IGNORECASE):
            if re.search(keywords, job_title, re.IGNORECASE):
                return {
                    "roles": role,
                    "ordering": ordering,
                    "category": category,
                    'priority':1
                }
    
    return None
    
    
    if primary_skills:
 
        
        primary_skills = [skill.lower() for skill in primary_skills]
        
        
        role_skill_map = {'Business Development Specialist': {'skills': None, 'category': 4}, 'Engineering Manager': {'skills': None, 'category': 4}, 'React Native Developer': {'skills': ['TypeScript', 'JavaScript', 'Git', 'MVC', 'React', 'Gradle', 'REST API', 'SQL', 'React Native', 'Redux', 'NPM', 'Expo', 'CSS', 'UI/UX Design'], 'category': 4}, 'Network Engineer': {'skills': ['Networking', 'Testing', 'Network Management', 'Putty', 'Ethernet', 'Perl', 'Openstack', 'VMware', 'Terraform', 'Router', 'Python', 'Network Security', 'Wireshark', 'CISCO'], 'category': 4}, 'AI Developer': {'skills': ['Git', 'Statistics', 'Kafka', 'TensorFlow', 'R', 'Hadoop', 'Pandas', 'Scala', 'Python', 'spaCy', 'Keras', 'Tableau', 'NLTK', 'PyTorch'], 'category': 4}, 'Product Designer': {'skills': ['Localization', 'Testing', 'Sketch', 'Framer', 'Invision', 'Figma', 'DevOps', 'AI', 'Prototyping', 'Wireframing', 'Usability Testing', 'UX Design', 'User Interface', 'Design Patterns'], 'category': 4}, 'Vice President': {'skills': None, 'category': 4}, 'Product Manager': {'skills': ['Project Management', 'Market Research and Analysis', 'Roadmapping and Planning', 'HubSpot', 'Google Analytics', 'Asana', 'Salesforce', 'Jira', 'Excel'], 'category': 4}, 'SAP Developer': {'skills': ['Testing', 'SAP Fiori', 'ABAP', 'HANA', 'SAP'], 'category': 4}, 'Marketing': {'skills': None, 'category': 4}, 'Salesforce Developer': {'skills': ['LWC', 'Web Components', 'Salesforce', 'REST API', 'APEX', 'Jira', 'SOQL', 'CRM', 'Trailhead', 'SFD'], 'category': 4}, 'Talent Acquisition': {'skills': None, 'category': 4}, 'Android Developer': {'skills': ['Git', 'Android Studio', 'MVC', 'Firebase', 'DSA', 'Android SDK', 'XML', 'Gradle', 'ViewModel', 'LiveData', 'REST API', 'Java', 'SQL', 'Material Design', 'Kotlin', 'RecyclerView', 'Jetpack Components', 'Retrofit', 'Dagger', 'UI/UX Design'], 'category': 4}, 'Program Manager': {'skills': ['Confluence', 'HubSpot', 'Google Analytics', 'Strategy and Risk Management', 'Microsoft Excel', 'Agile Methodologies', 'Asana', 'Salesforce', 'Resource Management', 'Management', 'Jira', 'Trello', 'CRM', 'Team Leadership', 'Stakeholder Management', 'Power BI', 'Tableau'], 'category': 4}, 'Project Manager': {'skills': ['Confluence', 'HubSpot', 'Google Analytics', 'Strategy and Risk Management', 'Microsoft Excel', 'Agile Methodologies', 'Asana', 'Salesforce', 'Resource Management', 'Management', 'Jira', 'Trello', 'CRM', 'Team Leadership', 'Stakeholder Management', 'Power BI', 'Tableau'], 'category': 4}, 'Ruby on Rails Backend Developer': {'skills': ['Git', 'Ruby', 'RSpec', 'GraphQL', 'WebSockets', 'Authentication', 'Amazon Web Services', 'ActiveRecord', 'Azure', 'RESTful API', 'Ruby on Rails', 'SQL', 'MongoDB', 'PostgreSQL', 'Elastic Search', 'Sidekiq', 'Google Cloud Platform', 'Docker', 'NoSQL'], 'category': 4}, 'Reliability Engineer': {'skills': ['Git', 'Grafana', 'Linux', 'Amazon Web Services', 'Azure', 'Kubernetes', 'Puppet', 'Terraform', 'Ansible', 'Chef', 'Jenkins', 'Python', 'Automation', 'Bash', 'Prometheus', 'Google Cloud Platform', 'ELK Stack', 'DevOps', 'Orchestration', 'Docker'], 'category': 4}, 'Big Data Engineer': {'skills': ['Pig', 'Apache NiFi', 'Avro', 'Hive', 'YARN', 'Sqoop', 'Kafka', 'NoSQL Databases', 'Java', 'SQL', 'Apache Flink', 'Hadoop', 'Linux Shell Scripting', 'MapReduce', 'Python', 'Cloud Platforms', 'Impala', 'Spark', 'Docker', 'Power BI', 'Tableau'], 'category': 4}, 'Golang Backend Developer': {'skills': ['Golang', 'Git', 'Gin', 'microservices', 'Redis', 'RESTful API', 'Kubernetes', 'RabbitMQ', 'Go Web Framework', 'Concurrency', 'Goroutines', 'SQL', 'PostgreSQL', 'Message Queues', 'Echo', 'Docker', 'NoSQL'], 'category': 4}, 'Django Backend Developer': {'skills': ['Git', 'GraphQL', 'WebSockets', 'microservices', 'Authentication', 'Redis', 'Amazon Web Services', 'Azure', 'RESTful API', 'Kubernetes', 'Pytest', 'Django REST Framework', 'Django ORM', 'Asyncio', 'SQL', 'PostgreSQL', 'Python', 'MySQL', 'Elastic Search', 'Django', 'Celery', 'serverless', 'Google Cloud Platform', 'Docker'], 'category': 4}, 'Python Fullstack Developer': {'skills': ['JavaScript', 'Git', 'React', 'Amazon Web Services', 'Azure', 'RESTful API', 'Vue', 'CI/CD', 'SOAP', 'HTML', 'Pytest', 'SQL', 'Flask', 'ORM', 'Python', 'Django', 'MVC Architecture', 'Jinja', 'Google Cloud Platform', 'Angular', 'CSS', 'Web Services'], 'category': 4}, 'Human Resources': {'skills': None, 'category': 4}, 'Oracle Consultant': {'skills': ['Fusion', 'API', 'Amazon Web Services', 'Backup And Recovery', 'Oracle', 'SQL', 'PostgreSQL', 'Data Migration', 'Performance Tuning', 'Database Design'], 'category': 4}, 'Physical Design Engineer': {'skills': ['Power Integrity', 'PrimeTime', 'Synopsys ICC', 'Git', 'Cadence Innovus', 'Perl', 'Cadence Voltus', 'Python', 'Clock Tree Synthesis', 'Power Distribution Network', 'Tempus', 'TCL', 'RTL Design', 'Apache Redhawk', 'Signal Integrity'], 'category': 4}, 'Frontend Developer': {'skills': ['TypeScript', 'JavaScript', 'Git', 'GraphQL', 'React', 'DSA', 'RESTful API', 'Vue', 'Webpack', 'HTML', 'Component Libraries', 'Unit Testing', 'NPM', 'Angular', 'CSS'], 'category': 4}, 'ReactJS Developer': {'skills': ['TypeScript', 'JavaScript', 'Git', 'GraphQL', 'React', 'DSA', 'RESTful API', 'Webpack', 'Hooks', 'HTML', 'Component Libraries', 'State Management', 'Unit Testing', 'Redux', 'React Router', 'NPM', 'CSS'], 'category': 4}, 'Data Scientist': {'skills': ['Scikit-learn', 'numPy', 'Apache NiFi', 'Amazon Web Services', 'Azure', 'Google BigQuery', 'Snowflake', 'Plotly', 'TensorFlow', 'SQL', 'Matplotlib', 'Seaborn', 'Apache Hadoop', 'Google Cloud Platform', 'Amazon Redshift', 'Apache Spark', 'PyTorch'], 'category': 4}, 'Sales': {'skills': None, 'category': 4}, 'Supply Chain Roles': {'skills': None, 'category': 4}, 'Director': {'skills': None, 'category': 4}, 'NodeJS Developer': {'skills': ['JavaScript', 'Git', 'Mocha', 'Amazon Web Services', 'DSA', 'Azure', 'RESTful API', 'Kubernetes', 'Express.js', 'Jest', 'SQL', 'MongoDB', 'PostgreSQL', 'MySQL', 'Elastic Search', 'Unit Testing', 'NPM', 'Node.js', 'Google Cloud Platform', 'Docker', 'NoSQL'], 'category': 4}, 'DevOps Engineer': {'skills': ['Git', 'Grafana', 'Linux', 'Amazon Web Services', 'Azure', 'Kubernetes', 'Terraform', 'Ansible', 'Chef', 'Jenkins', 'Python', 'Automation', 'Prometheus', 'Google Cloud Platform', 'ELK Stack', 'DevOps', 'Orchestration', 'Docker'], 'category': 4}, 'VueJS Developer': {'skills': ['TypeScript', 'JavaScript', 'Git', 'GraphQL', 'Vue Router', 'DSA', 'RESTful API', 'Vue', 'Webpack', 'HTML', 'Vuex', 'Unit Testing', 'NPM', 'CSS', 'Single-File Components (SFC)', 'Vue CLI'], 'category': 4}, 'Google Cloud Platform Developer': {'skills': ['Google Cloud API', 'Python', 'Google Cloud SDK', 'Google Cloud Platform', 'IAM'], 'category': 4}, 'Azure Developer': {'skills': ['Azure SDK', 'Azure Virtual Machines', 'IaC', 'Azure Cosmos DB', 'Azure Functions', 'C#', 'CI/CD', 'SQL', 'Python'], 'category': 4}, 'Silicon Design Engineer': {'skills': ['HSPICE', 'Power Integrity', 'Git', 'DAC', 'Perl', 'Device Modeling', 'Layout Design', 'Python', 'ADC', 'RTL Coding', 'CMOS', 'SPICE', 'Xilynx Vivado', 'TCL', 'Signal Integrity'], 'category': 4}, 'Digital Marketing': {'skills': ['SEM', 'SEO', 'Search Engine', 'Landing Pages', 'Marketing Automation', 'Google Analytics', 'Content Management', 'Email Marketing'], 'category': 4}, 'ASP.NET Backend Developer': {'skills': ['Git', 'ASP.NET Core', 'microservices', 'Authentication', 'Amazon Web Services', 'Azure', 'RESTful API', 'RabbitMQ', 'C#', 'SQL', 'MongoDB', 'Elastic Search', 'Message Queues', '.NET Framework', 'Entity Framework', 'NUnit', 'Google Cloud Platform', 'Docker', 'ASP.NET'], 'category': 4}, 'SQL Database Developer': {'skills': ['Git', 'Amazon Web Services', 'Oracle', 'Azure', 'SQL', 'Python', 'ETL Tools', 'Performance Tuning', 'Database Design', 'NoSQL', 'Power BI', 'Tableau', 'Tableau'], 'category': 4}, 'Java Backend Developer': {'skills': ['Git', 'JUnit', 'microservices', 'Authentication', 'Spring Framework', 'Amazon Web Services', 'Azure', 'RESTful API', 'Kafka', 'Java', 'SQL', 'MongoDB', 'PostgreSQL', 'Spring Boot', 'Maven', 'MySQL', 'Elastic Search', 'Hibernate', 'Google Cloud Platform', 'Docker', 'NoSQL'], 'category': 4}, 'Recruiter': {'skills': None, 'category': 4}, 'Hardware Engineer': {'skills': ['DSP', 'DFD', 'Microcontroller', 'UART', 'I2C', 'Altium', 'Ki-CAD', 'Schematic design', 'Multi layer PCB Design', 'DFM', 'Analog Electronics', 'Ethernet', 'Signal Conditioning', 'Power Supply Design', 'Oscilloscopes', 'Logic Analyzers', 'SPICE', 'Microprocessor', 'Eagle', 'SPI', 'Amplifiers', 'Filters', 'USB'], 'category': 4}, 'Database Developer': {'skills': ['Replication', 'Database', 'Amazon Web Services', 'Backup And Recovery', 'Oracle', 'Azure', 'Cassandra', 'Kafka', 'SQL', 'MongoDB', 'PostgreSQL', 'Python', 'Performance Tuning', 'Database Design', 'Google Cloud Platform'], 'category': 4}, 'Mobile Developer': {'skills': ['Git', 'Core Data', 'SwiftUI', 'Alamofire', 'DSA', 'CocoaPods', 'Swift', 'UIKit', 'REST API', 'Objective C', 'SQL', 'iOS SDK', 'Auto Layout', 'MVC Architecture', 'Xcode', 'UI/UX Design'], 'category': 4}, 'Security Engineer': {'skills': ['Splunk', 'OpenVAS', 'Qualys', 'CrowdStrike', 'Snort', 'Metasploit', 'Nessus', 'Nmap', 'Kali Linux', 'Ansible', 'Python', 'Network Security', 'Cryptography', 'Bash', 'Penetration Testing', 'Cisco ASA', 'Wireshark'], 'category': 4}, 'Embedded Developer': {'skills': ['BLE', 'CAN', 'Git', 'Firmware Development', 'Networking', 'Wi-fi', 'GPS', 'Bootloader', 'Zephyr OS', 'ADC/DAC', 'PWM', 'Timers', 'JTAG', 'GDB', 'Microcontroller', 'RTOS', 'Linux', 'UART', 'BSP', 'I2C', 'Ethernet', 'TCP/IP', 'LTE', 'Lora', 'Python', 'Logic Analyzer', 'SPI', 'VxWorks', 'FreeRTOS', 'Bluetooth', 'Drivers', 'Modbus', 'ZigBee', 'Wireshark', 'IOT'], 'category': 4}, 'Data Engineer': {'skills': ['ETL', 'Data Engineering', 'Snowflake', 'Kafka', 'Java', 'SQL', 'Scala', 'Python', 'Cloud Platforms', 'Streaming Data Processing', 'Apache Hadoop', 'Amazon Redshift', 'Data Warehousing', 'Data Modelling', 'Apache Spark'], 'category': 4}, 'Admin': {'skills': None, 'category': 4}, 'MERN Stack Developer': {'skills': ['JavaScript', 'Git', 'MERN', 'GraphQL', 'Amazon Web Services', 'Azure', 'RESTful API', 'Webpack', 'CI/CD', 'HTML', 'Jest', 'Responsive Design', 'JSX', 'Mongoose', 'MVC Architecture', 'Redux', 'NPM', 'Google Cloud Platform', 'CSS', 'Docker'], 'category': 4}, 'Machine Learning Developer': {'skills': ['Data Preprocessing', 'Statistics', 'Applied Mathematics', 'Machine Learning Algorithms', 'Deep Learning', 'Natural Language Processing (NLP)', 'Computer Vision', 'Model Deployment', 'TensorFlow', 'Python', 'PyTorch'], 'category': 4}, 'Flutter Developer': {'skills': ['Git', 'Firebase', 'REST API', 'Bloc Pattern', 'SQL', 'Dart', 'Flutter', 'Material Design'], 'category': 4}, 'Fullstack Developer': {'skills': ['JavaScript', 'Git', 'Nginx', 'Ruby', 'API', 'Kubernetes', 'Webpack', 'Babel', 'HTML', 'SQL', 'PHP', 'Django', 'Node.js', 'Spring', 'CSS', 'Docker', 'NoSQL', 'Elasticsearch', 'UI/UX Design', 'ASP.NET'], 'category': 4}, 'Java Developer': {'skills': ['Git', 'JUnit', 'DSA', 'Gradle', 'Apache Maven', 'MySQL Spring', 'Java', 'Spring Boot', 'Mockito', 'Hibranate'], 'category': 4}, 'Business Analyst': {'skills': ['Confluence', 'Google Analytics', 'Microsoft Excel', 'SQL', 'Power BI', 'Tableau'], 'category': 4}, 'iOS Developer': {'skills': ['Git', 'Core Data', 'SwiftUI', 'Alamofire', 'DSA', 'CocoaPods', 'Swift', 'UIKit', 'REST API', 'Objective C', 'SQL', 'iOS SDK', 'Auto Layout', 'MVC Architecture', 'Xcode', 'UI/UX Design'], 'category': 4}, 'Automation Test Engineer': {'skills': ['JUnit', 'Appium', 'C#', 'Selenium', 'Java', 'Python'], 'category': 4}, 'Data Analyst': {'skills': ['Statistics', 'dplyr', 'SQL', 'R', 'Pandas', 'Data Analysis', 'Python', 'Matplotlib', 'Data Visualization', 'Data Cleaning', 'Seaborn', 'Excel', 'Data Warehousing', 'Exploratory Data Analysis (EDA)', 'Power BI', 'Tableau'], 'category': 4}, 'AngularJS Developer': {'skills': ['TypeScript', 'JavaScript', 'Git', 'GraphQL', 'DSA', 'Angular CLI', 'RESTful API', 'Webpack', 'HTML', 'Angular Material', 'Unit Testing', 'NPM', 'Angular', 'CSS'], 'category': 4}, 'Graphic Designer': {'skills': ['Sketch', 'Dash', 'Adobe Illustrator', 'Adobe Photoshop', 'Indesign', 'Figma', 'AI', 'Graphic Design', 'CSS', 'Prototyping'], 'category': 4}, 'Backend Developer': {'skills': ['Git', 'Redis', 'Amazon Web Services', 'RESTful API', 'RabbitMQ', 'Ruby on Rails', 'Java', 'SQL', 'MongoDB', 'PHP', 'Django', 'Node.js', 'Google Cloud Platform', 'Spring', 'Docker', 'Elasticsearch'], 'category': 4}, 'QA Engineer': {'skills': ['Git', 'JMeter', 'JUnit', 'Testing', 'Appium', 'CI/CD', 'Selenium', 'Java', 'SQL', 'Jenkins', 'Jira', 'Python', 'Automation', 'Postman'], 'category': 4}, 'ASIC Engineer': {'skills': ['Synopsys Design Compiler', 'Git', 'Cadence encounter', 'Static Timing Analysis', 'FPGA', 'ASIC', 'ModelSim', 'Perl', 'EDA Tools', 'verilog', 'Python', 'VCS', 'mentorgraphics calibre', 'Clock Gating', 'Voltage Scaling', 'RTL Design', 'ASIC Design', 'Power Gating'], 'category': 4}, 'Ruby on Rails Fullstack Developer': {'skills': ['JavaScript', 'Git', 'Ruby', 'RSpec', 'React', 'Amazon Web Services', 'ActiveRecord', 'Azure', 'RESTful API', 'Vue', 'Webpack', 'CI/CD', 'HTML', 'Ruby on Rails', 'Responsive Design', 'SQL', 'MVC Architecture', 'Google Cloud Platform', 'Angular', 'CSS', 'NoSQL'], 'category': 4}, 'AWS Developer': {'skills': ['Amazon Web Services', 'Lambda', 'Amazon EC2', 'Amazon S3', 'Python', 'Amazon DynamoDB', 'IAM'], 'category': 4}, 'Technical Writer': {'skills': ['Localization', 'Confluence', 'Zendesk', 'HTML', 'Swagger', 'CRM', 'Content Management', 'Markdown'], 'category': 4}, 'Analog Engineer': {'skills': ['Matlab', 'Analog Layout Design', 'SPECTRA', 'Power Management', 'Cadence Virtuso', 'Mentor Graphics Eldo', 'CAD', 'Noise Analysis and Reduction', 'Perl', 'Analog Circuit Design', 'Mixed Signal Design', 'EDA Tools', 'Python', 'SPICE', 'Synapsys Custom Compiler', 'Mentor Calibre', 'TCL', 'Signal Integrity'], 'category': 4}, 'Cloud Developer': {'skills': ['Golang', 'Amazon Web Services', 'Azure', 'Terraform', 'Amazon EC2', 'Amazon S3', 'Python', 'Prometheus', 'Google Cloud Platform', 'Amazon Lambda', 'EKS'], 'category': 4}, 'Game Developer': {'skills': ['Git', 'Game Engine', 'DSA', 'Unreal Engine', 'Game Development', 'Unit Testing', 'Unity'], 'category': 4}, 'Java Fullstack Developer': {'skills': ['JavaScript', 'Git', 'JUnit', 'Spring Framework', 'React', 'Amazon Web Services', 'Azure', 'RESTful API', 'Vue', 'Gradle', 'CI/CD', 'SOAP', 'HTML', 'Build Tools', 'Java', 'SQL', 'Spring Boot', 'Maven', 'ORM', 'MVC Architecture', 'Hibernate', 'Google Cloud Platform', 'Angular', 'CSS', 'NoSQL', 'Web Services'], 'category': 4}, 'System Engineer': {'skills': ['Git', 'Git', 'Networking', 'Linux', 'Amazon Web Services', 'Perl', 'VMware', 'Ansible', 'Python', 'Scripting', 'Automation', 'Bash', 'ELK Stack', 'Drivers', 'CISCO'], 'category': 4}, 'Finance': {'skills': None, 'category': 4}, 'UI/UX Designer': {'skills': ['User Acceptance', 'Invision', 'Figma', 'Material Design', 'Graphic Design', 'CSS', 'Prototyping', 'Wireframing', 'Usability Testing', 'UX Design', 'User Interface', 'Design Patterns'], 'category': 4}, 'Python Developer': {'skills': ['Git', 'Selenium', 'Pandas', 'Matplotlib', 'BeautifulSoup'], 'category': 4}, 'PHP Backend Developer': {'skills': ['PHPUnit', 'Git', 'Composer', 'microservices', 'Authentication', 'JQuery', 'RESTful API', 'RabbitMQ', 'Laravel', 'Symfony', 'SQL', 'PostgreSQL', 'SOLID Principles', 'MySQL', 'Message Queues', 'PHP', 'CodeIgniter', 'MVC Architecture', 'Magento', 'Docker', 'NoSQL'], 'category': 4}}
  
        # Define common skill sets
        mern_skills = ['mongodb', 'reactjs', 'nodejs', 'expressjs']
        front_end_skills = ['angularjs', 'reactjs', 'vuejs']



        # MERN Stack Developer
        if all(skill in primary_skills for skill in mern_skills):
            return {"roles": "abd2fd71-5947-4658-b1b5-8ca42a49d1d8", "priority": 2,"category":'C4'}

        # Java Fullstack Developer
        if any(skill in front_end_skills for skill in primary_skills) and any(skill in ['java', 'spring', 'spring boot'] for skill in primary_skills):
            return {"roles": "123aff4a-a23e-44fd-b65f-2673c8917792", "priority": 2,"category":'C4'}

        # Python Fullstack Developer
        if "python" in primary_skills and any(skill in front_end_skills for skill in primary_skills):
            return {"roles": "ab822802-4934-462e-843b-adf940afa3a6", "priority": 2,"category":'C4'}

        # Ruby on Rails Fullstack Developer
        if any(skill in ['ruby', 'rails'] for skill in primary_skills) and any(skill in front_end_skills for skill in primary_skills):
            return {"roles": "2c4c7d33-f335-4cdb-b974-f0559aa60790", "priority": 2,"category":'C4'}
        
        
        
        
        
        
        
        multiple_skill_roles = {
            
         '3777b684-d848-4483-909d-d84b10544834': ['react native'],
         'e1dd9b18-620e-4c37-afe7-922085e48d64': ['network performance', 'internet protocol suite', 'network architecture', 'ethernet'], 
         'c2a4062a-76c3-4517-836b-471c0731ebf2': ['artificial intelligence', 'pytorch'], 
         '38f69e5a-3253-4838-981a-ad975054fe3b': ['sap'], 
         'e16f07a9-6295-444b-9663-b7c92b519803': ['salesforce', 'salesforce sales cloud'],
         'f945cfd6-bb7d-45c2-be48-11cfdad52d17': ['android studio', 'android', 'android sdk', 'android jetpack'], 
         '6c7bf76d-cb84-48ab-882f-2885f0d6d30f': ['rails'], 
         '2058dd20-2f36-48da-8de4-d9a54c46494b': ['reliability engineering'], 
         'abc4286e-8dea-4ab7-a158-750643b2a456': ['big data'],
         '13cdc59c-d9cb-4aa5-a550-7d6e524e34d0': ['golang'], 
         '6e05f14a-5a2b-4b77-a192-f34bb6d854bc': ['django', 'django rest framework', 'django orm'], 
         '4dae1194-8b6e-484a-b078-29660a0e80db': ['reactjs'],
         'b149edfc-b704-4187-87bc-88e8ad39454a': ['data science', 'tensorflow', 'nlp', 'natural language processing'], 
         'f305a78f-0af6-4cdd-ab76-d21a93f2ddc5': ['expressjs'], 
         'ca617812-a940-4409-9cfd-4b959899f149': ['devops', 'kubernetes'], 
         'c293c8ff-6d28-4535-bdb9-457626a5353f': ['vuejs'],
         '94f225cf-8e54-438e-b83c-02d99b0a0df6': ['spring boot', 'spring framework'], 
         '9874657c-44d5-4421-bddf-69ea88e398ba': ['computer hardware', 'graphics', 'system on a chip', 'silicon', 'microprocessor', 'physical design'], 
         '55497847-1eea-4947-bfb6-ec167923d902': ['network security', 'computer security', 'database security'],
         '8403c7dc-732f-418b-b153-efcebb592ac7': ['embedded', 'firmware', 'iot', 'wireless', 'internet of things', 'microcontroller', 'embedded systems', 'embedded system', 'power management', 'microprocesser'],
         '05b60acf-4f73-4713-afc7-a0edc5ee153b': ['scala', 'snowflake', 'hadoop', 'kafka', 'airflow', 'apache spark', 'data warehouse', 'data mining'], 
         '33d99058-65c0-4dd1-80f4-99485eac2c6e': ['machine learning', 'deep learning', 'artificial intelligence', 'pattern recognition'], 
         '03007f41-3189-436c-a82c-c65241bb51f2': ['flutter'],
         '68c24321-3e79-4704-bb3f-c5057fef1fd4': ['xcode'], 
         'ed4fa7cf-f622-4f9e-8039-fff3fba31f04': ['pandas', 'tableau'], 
         'eae910e1-0bb7-4e3f-905f-e6bf2c4d4f32': ['angularjs'], 
         '1343eaef-4b13-4166-a1b0-df172555db49': ['graphic design'], 
         '34c8a763-138f-4cc5-9c6c-43d822102b9e': ['game development', 'game engine', 'unity'], 
         '29503dc7-1240-42c1-b4d4-2f4f8dcaeab6': ['wireframing', 'ux design', 'figma', 'user interface'], 
         '8ae5394c-f09a-42f2-9c65-27dd82c2f94c': ['php', 'php framework', 'laravel']
         
         }



        matching_roles = []

        # Check multiple skill roles
        for role_id, skills in multiple_skill_roles.items():
            # Find matching skills from the `multiple_skill_roles` for the primary skills
            matching_skills_from_multiple = [skill for skill in skills if skill in primary_skills]
            
            # Check if the role exists in role_skill_map
            if role_id in role_skill_map:
                # Lowercase all skills in role_skill_map for consistent matching
                role_specific_skills = [skill.lower() for skill in role_skill_map[role_id]['skills']]
                matching_skills_from_map = [skill for skill in role_specific_skills if skill in primary_skills]
                
                # Check if at least one skill from multiple_skill_roles and two from role_skill_map match
                if len(matching_skills_from_multiple) >= 1 and len(matching_skills_from_map) >= 2:
                    total_matching_skills = len(matching_skills_from_multiple) + len(matching_skills_from_map)
                    matching_roles.append({"roles": role_id, "priority": 2, "category": 'C4', "matching_skills": total_matching_skills})

        # If multiple roles match, return the one with the most matching skills
        if matching_roles:
            best_match = max(matching_roles, key=lambda x: x["matching_skills"])
            return {"roles": best_match["roles"], "priority": 2, "category": 'C4'}


    # if roles_with_priority=={}:
    #     roles_with_priority={"roles": "No Match", "priority": 1, 'category':'C6'}
        # roles = ["No Match"]


def generate_uuid(JRole=None, Company=None, CompType=None, Domain=None, Location=None, Investor=None, WorkType=None):
    # Step 1: Initialize the UUID bytes with 4 bytes of 0's
    uuid_bytes = b"\x00\x00\x00\x00"
    
    # Step 2: Convert JRole to 2 bytes and append it
    # uuid_bytes += JRole.to_bytes(2, byteorder="big")
    uuid_bytes += (0 if JRole is None else JRole).to_bytes(2, byteorder="big")

    
    # Step 3: Convert Company to 3 bytes and append it
    uuid_bytes += (0 if Company is None else Company).to_bytes(3, byteorder="big")
    
    # Step 4: Convert CompType to 1 byte and append it
    uuid_bytes += (0 if CompType is None else CompType).to_bytes(1, byteorder="big")
    
    # Step 5: Convert Domain to 1 byte and append it
    uuid_bytes += (0 if Domain is None else Domain).to_bytes(1, byteorder="big")
    
    # Step 6: Convert Location to 2 bytes and append it
    uuid_bytes += (0 if Location is None else Location).to_bytes(2, byteorder="big")
    
    # Step 7: Convert Investor to 2 bytes and append it
    uuid_bytes += (0 if Investor is None else Investor).to_bytes(2, byteorder="big")
    
    # Step 8: Convert WorkType to 1 byte and append it
    uuid_bytes += (0 if WorkType is None else WorkType).to_bytes(1, byteorder="big")
    

    # Convert the UUID bytes to a hex string
    uuid_string = uuid_bytes.hex()
    
    return uuid_string

def clean_json_string(json_string):
    
    # Replace newline characters within string values with space
    cleaned = ' '.join(json_string.split())

    return cleaned


def clean_string(s):
    # Step 1: Convert to lowercase
    s = s.lower()
    
    # Step 2: Convert mathematical bold characters to ASCII equivalents
    cleaned = []
    for c in s:
        code_point = ord(c)
        # Check for Mathematical Bold uppercase (?-? ? a-z)
        if 0x1D5D4 <= code_point <= 0x1D5ED:
            cleaned.append(chr(ord('a') + (code_point - 0x1D5D4)))
        # Check for Mathematical Bold lowercase (?-? ? a-z)
        elif 0x1D5EE <= code_point <= 0x1D607:
            cleaned.append(chr(ord('a') + (code_point - 0x1D5EE)))
        else:
            cleaned.append(c)
    s = ''.join(cleaned)
    
    # Step 3: Replace non-alphanumeric/non-hyphen characters with hyphens
    new_s = []
    for c in s:
        if c.isalnum() or c == '-':
            new_s.append(c)
        else:
            new_s.append('-')
    s = ''.join(new_s)
    
    # Step 4: Collapse multiple hyphens into one and handle edge cases
    s = re.sub(r'-+', '-', s)  # Replace multiple hyphens with a single hyphen
    s = s.replace('-startups', '-funded-startups')  # Specific replacement
    s = s.strip('-')  # Remove leading/trailing hyphens
    
    return s



# only for india
def get_social_channels(role_id):
    """
    Get social media channels data for a given role ID.
    
    Args:
        role_id: ID of the role to fetch channels for
        
    Returns:
        dict: Object with format {
            'in': {
                'whatsapp': {
                    'name': str,
                    'description': str,
                    'url': str
                },
                'telegram': {
                    'name': str,
                    'description': str,
                    'url': str
                }
            }
        } or None if no data
        
    Example:
        >>> get_social_channels("123")
        {
            'in': {
                'whatsapp': {
                    'name': 'Group Name',
                    'description': 'Group Description',
                    'url': 'https://whatsapp.group/123'
                }
            }
        }
    """
    if not role_id:
        return None
    try:
        # Fetch channels data from Supabase
        # channels_url = f'{url}channel_automation?select=social_media_type,channel_url,channel_name,description&role_id=eq.{role_id}'
        # channels_data = requests.get(url=channels_url,headers=headers).json()
        channels_data=supabase.table('channel_automation')\
            .select('social_media_type','channel_name','description', 'channel_url')\
            .contains('multiple_roles', [role_id]).execute()
            
        # If no data returned, return None
        if not channels_data.data:
            return None


        # Initialize channels dictionary
        channels = {'in': {}}
        
        # Process each channel
        for channel in channels_data.data:
            social_type = channel['social_media_type']
            channel_url = channel['channel_url']
            name = channel['channel_name']
            description = channel['description']
            
            if social_type in ['whatsapp', 'telegram']:
                channels['in'][social_type] = {
                    'name': name,
                    'description': description,
                    'url': channel_url if channel_url else None
                }
                
        # Return None if no valid channels were found
            # print('chanels',channels)
        return channels if channels['in'] else None
        
    except Exception as e:
        print(f"Error fetching channel data: {str(e)}")
        return None

def job_group_create(type_1,data_id,data_name,role_id,role_name,category,job_group_uuid,gte=None,lte=None,bands=None, country=None,country_code=None,linkedin_company_name=None):
    bgColor = [
    "#f1f8e8",
    "#fff0f0",
    "#fff8dc",
    "#e4fcfc",
    "#f1eaff",
    "#ede5e8",
  ]
    criteria = []
    attributes = {}
    query_template=supabase.table('percolate_query_template').select('template').eq('type',type_1).execute()
    
    
    # print(query_template.data)
    temp_data={
        "data_id": data_id,
        "role_id": role_id,
        "data_name":data_name,
        "role_name":role_name,
        "country": country,
        "country_code": country_code,
         'gte':gte,
        'lte':lte,
        'bands':bands.replace('L','') if bands else None
    }

    criteria.extend([
    {"category": category, "id": data_id, "show": 1},
    {"category": "Role", "id": role_id, "show": 0}
])


    combination_name= "-".join([item["category"].lower() for item in criteria]) if len(criteria) > 1 else criteria[0]["category"].lower()

    
    template_raw = query_template.data[0].get('template')
    if template_raw:
        template = json.dumps(template_raw)
        query = chevron.render(template, temp_data)
       
        

      
        cleaned_query = clean_json_string(query)
        parsed_template = json.loads(cleaned_query)

        
        # print(type_1)
        attributes['query'] = parsed_template['query']
        attributes['seo_title']= parsed_template['seo_title']
        attributes['seo_description'] = parsed_template['seo_description']
        if country_code is not None:
            attributes['country_code']=country_code
        
        
# Convert name to a URL-friendly path
    attributes['url_path'] = clean_string(f'{role_name}-{data_name}')
    if (attributes['url_path']):
        url_check_res=supabase.table('job_groups').select('id').eq('attributes->>url_path',attributes['url_path']).execute()
    if url_check_res.data:
        if 'company' in  combination_name:
            attributes['url_path']=clean_string(f'{role_name}-{linkedin_company_name}')
        if 'location' in combination_name:
            attributes['url_path']=clean_string(f'{role_name}-{data_name}-{country_code}')

    # Randomly select a background color
    attributes['bg_color'] = random.choice(bgColor)

    channels=get_social_channels(role_id)
    if(channels):
        attributes['channels']=channels

    try:
        supabase.table('job_groups').insert({'attributes':attributes, 'criteria':criteria,'unique_hex':job_group_uuid, 'combination_name':combination_name}).execute()
        # print('job group created combo', job_group_uuid,type_1)

    except Exception as e:
        print(e)
        print('multiple')



def individual_group(type_1,data_id,data_name,category,job_group_uuid,gte=None,lte=None,bands=None, country=None,country_code=None,linkedin_company_name=None):
    bgColor = [
    "#f1f8e8",
    "#fff0f0",
    "#fff8dc",
    "#e4fcfc",
    "#f1eaff",
    "#ede5e8",
  ]
    criteria = []
    attributes = {}
    query_template=supabase.table('percolate_query_template').select('template').eq('type',f'individual_{type_1}').execute()
    
    
    # print(query_template.data)
    temp_data={
        "data_id": data_id,
        "data_name":data_name,
        "country": country,
        "country_code": country_code,
        'gte':gte,
        'lte':lte,
        'bands': bands.replace('L','') if bands else None
    }
    criteria.extend([
    {"category": category, "id": data_id, "show": 1},
])


    combination_name= "-".join([item["category"].lower() for item in criteria]) if len(criteria) > 1 else criteria[0]["category"].lower()
    
    template_raw = query_template.data[0].get('template')
    if template_raw:
        template = json.dumps(template_raw)
        query = chevron.render(template, temp_data)
       
        

      
        cleaned_query = clean_json_string(query)
        parsed_template = json.loads(cleaned_query)

        
  
        attributes['query'] = parsed_template['query']
        attributes['seo_title']= parsed_template['seo_title']
        attributes['seo_description'] = parsed_template['seo_description']
        if country_code is not None:
            attributes['country_code']=country_code
        
        
# Convert name to a URL-friendly path
    attributes['url_path'] = clean_string(f'{data_name}')
    if (attributes['url_path']):
        url_check_res=supabase.table('job_groups').select('id').eq('attributes->>url_path',attributes['url_path']).execute()
    if url_check_res.data:
        if 'company' in  combination_name:
            attributes['url_path']=clean_string(f'{linkedin_company_name}')
        if 'location' in combination_name:
            attributes['url_path']=clean_string(f'{data_name}-{country_code}')


    # Randomly select a background color
    attributes['bg_color'] = random.choice(bgColor)

    if type_1=='roles':
        channels=get_social_channels(data_id)           
        if(channels):
            # print('chanels',channels)
            attributes['channels']=channels



    

    # print(attributes)
    x={"criteria":criteria,"attributes":attributes}
    # print(x)

    try:
        supabase.table('job_groups').insert({'attributes':attributes, 'criteria':criteria,'unique_hex':job_group_uuid, 'combination_name':combination_name}).execute()
        # print('job group created', job_group_uuid,type_1)
    except Exception as e:
 
        print(job_group_uuid,type_1)

        

def create_job_group(job_data):
    job_data = job_data[0]
    company_id = job_data.get('company')
    location = job_data['job_locations'][0]['label'].split(', ')[0]
    job_id = job_data['id']
    job_role = job_data.get('job_role', None)

    # Process company data
    sleep(0.2)
    company_res = supabase.table('companies').select('incre_id','linkedin_unique_key','attributes->>band', 'company_verticals', 'brand_name').eq('id', company_id).execute()
    
    # If job_role exists, create job-company relationship
    if job_role:
        job_role_res = supabase.table('roles').select('incre_id', 'id', 'attributes->>name').eq('id', job_role).execute()
        job_role_incre_id = job_role_res.data[0]['incre_id']
        job_role_name = job_role_res.data[0]['name']
        role_id = job_role_res.data[0]['id']

        # Create individual role group
        job_role_uuid = generate_uuid(JRole=job_role_incre_id)
        individual_group(type_1='roles', data_id=role_id, data_name=job_role_name,
                        category='Role', job_group_uuid=job_role_uuid)
    for company in company_res.data:
        comp_incre_id = company['incre_id']
        comp_types = company['company_verticals'] 
        company_name = company['brand_name']
        comp_band = company['band']
        linkedin_company_name=company['linkedin_unique_key']
                        
        # Create individual company group
        ind_comp_uuid = generate_uuid(Company=comp_incre_id)
        individual_group(type_1='companies', data_id=company_id, data_name=company_name, 
                       category='Company', job_group_uuid=ind_comp_uuid,linkedin_company_name=linkedin_company_name)


        if job_role:
        # Create job-company relationship
            job_comp_uuid = generate_uuid(JRole=job_role_incre_id, Company=comp_incre_id)
            # job_group_create(type_1='companies', data_id=company_id, data_name=company_name,
            #                 role_id=role_id, role_name=job_role_name, category='Company', 
            #                 job_group_uuid=job_comp_uuid)

        # Process company attributes (band)
        if comp_band:
            company_attributes = supabase.table('company_attributes').select('incre_id','id','attributes').eq('attributes->>type', 'company_type').eq('attributes->criteria->bands->>0', comp_band).execute()
            
            for comp_att in company_attributes.data:
                comp_att_incre_id = comp_att['incre_id']
                comp_att_id = comp_att['id']
                comp_att_name = comp_att['attributes']['name']
                comp_att_funding = comp_att['attributes']['criteria'].get('funding')

                template_type = None
                lte = None
                gte = None
                # print(comp_att_funding,'checkingggggg')
                if comp_att_funding is None:
                    template_type = 'company_type'
                elif '-' in comp_att_funding:
                    lte = comp_att_funding.split('-')[1]
                    gte = comp_att_funding.split('-')[0]
                    template_type = 'company_type_funding_range'
                else:
                    gte = int(comp_att_funding.rstrip('+'))
                    template_type = 'company_type_gte'

                # Create individual company attribute group
                ind_comp_att_uuid = generate_uuid(CompType=comp_att_incre_id)
                individual_group(type_1=template_type, data_id=comp_att_id, data_name=comp_att_name,
                               category='Company_Attribute', job_group_uuid=ind_comp_att_uuid,
                               lte=lte, gte=gte, bands=comp_band)

                # If job_role exists, create job-company attribute relationship
                if job_role:
                    comp_att_role_uuid = generate_uuid(CompType=comp_att_incre_id, JRole=job_role_incre_id)
                    job_group_create(type_1=template_type, data_id=comp_att_id, data_name=comp_att_name,
                                   role_id=role_id, bands=comp_band, role_name=job_role_name,
                                   category='Company_Attribute', lte=lte, gte=gte,
                                   job_group_uuid=comp_att_role_uuid)

        # Process domains

        if comp_types:
            for comp_type in comp_types:
                domain_res = supabase.table('domains').select('incre_id','id','name').eq('id', comp_type).execute()
                
                domain_incre_id = domain_res.data[0]['incre_id']
                domain_res_id = domain_res.data[0]['id']
                domain_name = domain_res.data[0]['name']

                # Create individual domain group
                ind_domain_uuid = generate_uuid(Domain=domain_incre_id)
                individual_group(type_1='domains', data_id=domain_res_id, data_name=domain_name,
                            category='Domain', job_group_uuid=ind_domain_uuid)

                # If job_role exists, create job-domain relationship
                if job_role:
                    job_role_domain_uuid = generate_uuid(JRole=job_role_incre_id, Domain=domain_incre_id)
                    job_group_create(type_1='domains', data_id=domain_res_id, data_name=domain_name,
                                role_id=role_id, role_name=job_role_name, category='Domain',
                                job_group_uuid=job_role_domain_uuid)

    # Process location
    location_res = supabase.table('locations').select('incre_id','id','city', 'attributes').eq('attributes->>is_top_city', 'true').or_(f'city.ilike.%{location}%,attributes->aliases->>0.ilike.%{location}%').execute()

    if location_res.data:
        location_incre_id = location_res.data[0]['incre_id']
        location_name = location_res.data[0]['city']
        location_id = location_res.data[0]['id']
        location_country = location_res.data[0]['attributes']['country']
        location_country_code = location_res.data[0]['attributes']['country_code']

        # Create individual location group
        ind_loc_uuid = generate_uuid(Location=location_incre_id)
        individual_group(type_1='locations', data_id=location_id, data_name=location_name,
                       category='Location', country=location_country, 
                       country_code=location_country_code, job_group_uuid=ind_loc_uuid)

        # If job_role exists, create job-location relationship
        if job_role:
            job_location_uuid = generate_uuid(JRole=job_role_incre_id, Location=location_incre_id)
            job_group_create(type_1='locations', data_id=location_id, data_name=location_name,
                           role_id=role_id, role_name=job_role_name, category='Location',
                           country=location_country, country_code=location_country_code,
                           job_group_uuid=job_location_uuid)




def assign_secondary_role(job_title: str) -> str:
    """
    Assigns a job role based on job title using regex patterns.
    Returns 'Developer' for SDE/developer matches or 'Engineer' for engineer matches.
    
    Args:
        job_title (str): The job title to analyze
        skillsets (list): List of skills associated with the role
    
    Returns:
        str: 'Developer', 'Engineer', or None if no match
    """
    # Normalize job title for consistent matching
    job_title_lower = job_title.lower()
    
    # Regex job_locationpatterns for specific role matching
    developer_pattern = r'\b(sde|developer|dev)\b'
    engineer_pattern = r'\b(engineer)\b'
    
    # Check for developer/SDE pattern first
    if re.search(developer_pattern, job_title_lower):
        return 'Developer'
    # Then check for engineer pattern
    elif re.search(engineer_pattern, job_title_lower):
        return 'Engineer'
    
    return None





def clean_job_data(soup, job_title):
    
    
        jd_element = soup.find(class_="description__text description__text--rich")
            
        if jd_element:
            jd_text = jd_element.get_text().lower()  # Extract text from the element 
        else:
            jd_text = None



        roles_name = [
    "Ruby on Rails Backend Developer", "SAP Developer", "Technical Writer", 
    "Director", "Golang Backend Developer", "Database Developer", 
    "Security Engineer", "React Native Developer", "Cloud Developer", 
    "DevOps Engineer", "Business Analyst", "Admin", "Oracle Consultant", 
    "Talent Acquisition", "VueJS Developer", "ASP.NET Backend Developer", 
    "PHP Backend Developer", "Fullstack Developer", "UI/UX Designer", 
    "Google Cloud Platform Developer", "Product Manager", 
    "SQL Database Developer", "Embedded Developer", "Backend Developer", 
    "Project Manager", "AngularJS Developer", "Network Engineer", 
    "Product Designer", "Ruby on Rails Fullstack Developer", 
    "Java Fullstack Developer", "Java Backend Developer", 
    "Automation Test Engineer", "Azure Developer", "Data Scientist", 
    "Supply Chain Roles", "Physical Design Engineer", "System Engineer", 
    "Salesforce Developer", "AI Developer", "Mobile Developer", 
    "Business Development Specialist", "Finance", "Analog Engineer", 
    "Game Developer", "IOS Developer", "Frontend Developer", 
    "Graphic Designer", "Vice President", "MERN Stack Developer", 
    "Silicon Design Engineer", "AWS Developer", "Data Engineer", 
    "Digital Marketing", "Engineering Manager", "ReactJS Developer", 
    "Reliability Engineer", "Human Resources", "Python Fullstack Developer", 
    "Hardware Engineer", "Java Developer", "ASIC Engineer", 
    "Big Data Engineer", "Program Manager", "Python Developer", 
    "NodeJS Developer", "Marketing", "Django Backend Developer", 
    "Recruiter", "QA Engineer", "Flutter Developer", "Android Developer", 
    "Machine Learning Developer", "Sales", "Data Analyst"
]

        
        prompt = f"""
    Analyze the following job description and extract key information in JSON format. Follow these requirements:

    Here is the Job Description:- {jd_text}
    Here is the Job Title:- {job_title}
    Here is the Roles List:- {roles_name}

    1. **CRITICAL: Role Classification Requirements**
    - The role MUST be selected ONLY from the exact roles provided in the {roles_name} list
    - DO NOT modify, adapt, or create variations of the role names
    - Role selection process:
        * Read and analyze the ENTIRE job description thoroughly
        * Consider all responsibilities, requirements, and technical skills mentioned
        * Compare against each role in the provided roles list
        * Identify the closest matching role based on overall description alignment
        * Must have 90% or higher confidence in the match
        * If multiple roles seem close but none reaches 90% confidence, return null
        * Do not force-fit a role just because some keywords match
    - Return null for role_name if:
        * No role matches with 90%+ confidence after full description analysis
        * Multiple roles seem equally applicable
        * You're unsure about the exact match
        * The position is a support role (e.g., "Security Support Engineer", "Technical Support Engineer")
        * The job title or description contains "support" as a key responsibility
        * The role is primarily focused on supporting existing systems/users rather than development/creation
        * The  roles like System Engineer, Security Engineer should be IT based role.
    - Example cases where role should be null:
        * "Sales Support" even if "Sales" is in roles list
        * "Security Support Engineer" even if "Security Engineer" is in roles list
        * "Technical Support Developer" even if "Developer" roles exist in list
        * Any role where "support" is a primary function
        * Roles that seem similar but don't fully align with any option in the roles list
    - The role matching must:
        * Be based on comprehensive analysis of the entire job description
        * Consider all aspects of the role, not just the title or key technologies
        * Reach 90% confidence through detailed comparison with roles list
        * Default to null if any doubt exists about the match accuracy


    2. **Experience Requirements:**
    - Extract all experience requirements, including:
        - Specific years mentioned (e.g., "X years", "X+ years", "X-Y years").
        - Do not average ranges; include them as-is (e.g., "2-5 years" remains "2-5 years").
        - Include all instances of "X years", "X+ years", or "X-Y years" experience.
        - Include specific technical skills (e.g., "experience in Docker") even if years are not mentioned.
    - Simplify and merge related requirements while maintaining essential context.
    - Focus on technical and role-specific experience, excluding generic skills (e.g., "communication skills").
    - Ensure all experience formats are captured (e.g., "2 years", "3+ years", "4-6 years").
    - Reframe and simplify sentences to make them concise and easy to understand.
    - Capitalize the required word like CRM should be CRM not crm like HR should HR not hr.

    3. **Job Type Classification:**
    - Identify the job type as "Internship", "Fresher", or `null`.
    - Look for keywords such as "internship", "fresher", "entry-level position", or similar phrases.
    - Return `null` if the job type is not clearly specified.

    4. **Work Type Detection:**
    - Identify if the role is "Remote", "Hybrid", or "Office".
    - Look for keywords indicating work arrangement (e.g., "work from home", "remote position", "hybrid schedule", "in-office").
    - Return `null` if work type is not clearly specified.
    - For hybrid roles, ensure explicit mention of hybrid or a mix of remote/office work.

   5. **Role-Specific Skills:**
    - Extract a list of skills that are ONLY directly relevant to the identified role.
    - Focus on specific technologies, frameworks, libraries, and tools that distinguish this role from others.
    - Exclude generic programming concepts (like algorithms, version control, APIs) unless they are specifically emphasized as core requirements for this particular role.
    - Use official, standardized names for all technologies and skills (e.g., "React.js" not "React", "Node.js" not "Node").
    - if somthing like 'ai agents or ai tools' you need to covert into 'AI'.
    - The skills should be presented as individual terms or short phrases, not in sentence form.
    - Return the results as a simple array of strings.
    i If the skillsets are not you can always return empty array
    - Examples:
    - For a React Developer: ["React.js", "Redux", "Next.js", "React Hooks", "React Router"]
    - For a Data Scientist: ["Python", "pandas", "scikit-learn", "TensorFlow", "PostgreSQL"]
    - For a DevOps Engineer: ["Kubernetes", "Docker", "Terraform", "Jenkins", "Amazon Web Services"]

    
    6. **Total Experience Selection:**
    - From the extracted experience requirements, identify and return a **single most relevant value** for `total_experience`.
    - Prioritize ranges (e.g., "2-5 years") if explicitly mentioned, otherwise choose the highest explicitly stated value (e.g., "5+ years" over "3 years").
    - If the experience is in the Expericence List says something like 2 to 3 years of experience, it should return "2-3 years" and if it says 2 plus of experience it should  return "2+ years".
    - If no explicit experience is mentioned, return `null`.
    
    
    THE DATA SHOULD RETURN IN JSON SUCH THAT WHEN I RUN json.loads() it should be converted into python dict type.

    Return the data in this exact JSON format:
    {{
        "role_name": string or null,  // Matched role from roles list or null
        "experience": [               // Array of simplified experience requirements
            string,                  // Format: "X years in [skill/domain]" or "X+ years in [skill/domain]" or "X-Y years in [skill/domain]" or "Experience in [skill]"
            ...
        ],
        "total_experience": string or null,  // Single most relevant experience value
        "job_type": string or null,         // "Internship", "Fresher", or null
        "work_type": string or null,        // "Remote", "Hybrid", "Office", or null
        "skills": [                        // Array of role-specific skills
            string,                        // Each skill relevant to the identified role
            ...
        ]
    }}

    Example outputs:

    For remote roles:
    {{
        "role_name": "Frontend Developer", #role_name should be strictly from the list provided.
        "experience": [
            "2 years in JavaScript.",
            "3+ years in React.",
            "2-5 years in building/designing automation framework & testing tools.",
            "Experience in Docker."
        ],
        "total_experience": "2-5 years",
        "job_type": "Internship",
        "work_type": "Remote",
        "skills": ["JavaScript", "React.js", "CSS", "HTML"]
    }}

    For hybrid roles:
    {{
        "role_name": "Fullstack Developer",  #role_name should be strictly from the list provided.
        "experience": [
            "8 years in software development.",
            "5+ years in cloud platforms.",
            "Experience in Kubernetes."
        ],
        "total_experience": "8 years",
        "job_type": null,
        "work_type": "Hybrid",
        "skills": ["Java", "AWS", "Kubernetes", "Spring Boot", "React.JS"]
    }}
    
    
     For hybrid roles:
    {{
        "role_name": "DevOps Engineer",  #role_name should be strictly from the list provided.
        "experience": [
            "8 to 10 years in software development.",
            "5+ years in cloud platforms.",
            "Experience in Kubernetes."
        ],
        "total_experience": "8-10 years",
        "job_type": null,
        "work_type": "Hybrid",
        "skills": ["Terraform", "Kubernetes","Jenkins", "GitHub Actions", "Prometheus"]
    }}
"""





        res = mistral_ai(prompt)


        # res = deepseek_ai(prompt)
        return res
   



def parse_job_data(html_text,job_url, job_id, comp_id, company_name, country,scraped_date =datetime.now().isoformat()):

    soup = BeautifulSoup(html_text,'html.parser')
    cleaned_url = clean_job_url(job_url, job_id)
    job_title = parse_job_title(soup)
    exp_level, job_type = parse_exp_level(soup)
    job_location = parse_job_location(soup)
    exp = parse_exp(soup)
    skillsets = parse_skillset(soup, company_name)
    date_posted = parse_date_posted(soup, scraped_date)
  
    if country == 'India':
        partition_category = 'India'
    elif country == 'United States':
        partition_category = 'United States'
    else:
        partition_category = 'Rest of the World'
        
    
    clean_data =  clean_job_data(soup, job_title)
    
    
    
    print(clean_data)
    
    
    
    role_name_llm = clean_data['role_name']
    exp_lst_llm = clean_data['experience']
    total_exp_llm  = clean_data['total_experience']
    work_type_llm = clean_data['work_type']
    job_type_llm = clean_data['job_type']
    # clean_location_llm = clean_data.get('location', {}).get('mapped_city')
    
    
    role = None
    job_role = None
    role_meta_data = {}
    
    if role_name_llm:

        # Find the role that matches the provided role name
        matched_role = next(role for role in roles if role["name"] == role_name_llm)

        # Extract the job role ID
        job_role = matched_role["id"]

        # Construct the role_meta_data dictionary with category and priority
        role_meta_data = {
            "category": matched_role["category"],
            "priority": 1  # Set the priority as required
        }
                
    # else:
    #     role = assign_role(job_title, skillsets)
        
        
              
    if role:
        job_role = role.get('roles', None)
        
        role_meta_data = {key: role.get(key) for key in ['priority', 'category'] if role.get(key) is not None}

    # print(job_title)



    exp_range = None
    if job_title:
        exp_range = job_role_assign_unmatched(job_title,exp)
        

    # fresher_or_intern = check_fresher( soup, exp_range, job_title)
    
    
    experience_level = 'Internship' if exp_level == 'Internship' else (job_type_llm or exp_level)
    
    
    secondary_role =None
        
    if  not role:
        
        #check if the job_title has engineer, developer
        secondary_role = assign_secondary_role(job_title)
    

    is_deleted = False if (job_role  or secondary_role) else True
    

    
    parsed_data = {
                
                    'job_title' :job_title,
                    'relevant_exp' :{'role':None, 'list':exp_lst_llm if exp_lst_llm else exp, 'experience_level':experience_level},
                    'job_posted_on':date_posted,
                    'primary_skills':skillsets,
                    'apply_link': cleaned_url, 
                    'job_posted_on':date_posted,
                    
                    'attributes':{
                    'linkedin_job_id' :job_id,
                    'role_meta_data':role_meta_data,
                    },
                    'job_locations':[{ 'work_arrangements': [work_type_llm] if work_type_llm else [],
                                    'label':job_location,
                                    'country':country,
                                    'country_code':countries_map.get(country)
                                    }],
                    'job_source': 'ext-linkedin',
                    'job_type': job_type, 
                    'company':comp_id,
                    'partition_category':partition_category,
                    'job_role' :job_role,
                    'total_exp' :exp_range, 
                    'job_role_type':secondary_role,
                    'is_deleted': is_deleted,
                    'total_experience_raw': total_exp_llm,
                    'raw_skills':clean_data['skills']
            }
    
    

    if job_title is not None  and cleaned_url is not None and comp_id is not None and (exp_lst_llm or exp):

        
        
        print(parsed_data)
        
        insert_response = supabase.table('jobs').insert(parsed_data).execute()
        sleep(0.2)
        if insert_response.data:
            r=supabase.table('transaction_log').insert({'transaction_type':'job_parsed','system_id':26}).execute()
            print('clrrrrrrrr')
            print(r)
        
        new_job_data = insert_response.data
        
        # if parsed_data['job_role'] or  parsed_data['relevant_exp']['experience_level'] in ['Fresher','Internship']  or  parsed_data['job_role_type']:
        #     create_job_group(new_job_data)
        
    
  

        return True
    else:
        return False
        


def get_page_from_synology(linkedin_in):

    try:
      sleep(0.5)
      res = supabase.storage.from_('jobs_scraping').download(linkedin_in)
      return res
    except Exception as e :
        supabase.table('scraping_raw_html').update({'is_deleted':True}).eq('linkedin_job_id',linkedin_in).execute()
        return None
    
  



def job_role_assign_unmatched(job_title,exp):
    matched_count_exp = 0
    matched_from_title_count = 0
    unmatched_titles = []  # List to keep track of unmatched titles
    timestamp = datetime.now(timezone.utc) - timedelta(days=1)
    timestamp = timestamp.isoformat()

    # Define role patterns
    levels = {
        "Technical Architect": r"(?i)\b(?:Architect|Head of)\b",
        "Principal Engineer": r"(?i)\b(?:Principal)\b",
        "Senior Staff Engineer": r"(?i)\b(?:Senior|Sr\.)\b.*?\b(?:Staff|Manager)\b",
        "Staff Engineer": r"(?i)\b(?:Staff|Specialist|SDE[ _-]?4|Engineer[ _-]?4|L4|IV|SDET[ _-]?4|analyst[ _-]?4|manager)\b",
        "Senior Lead Engineer": r"(?i)\b(?:Senior|Sr\.)\b.*?\bLead\b",
        "Lead Engineer": r"(?i)\b(?:Lead|SDE[ _-]?3|Engineer[ _-]?3|leader|L3|III|SDE[ _-]?3|analyst[ _-]?3)\b",
        "Senior Engineer": r"(?i)\b(?:Senior|sr\.?|SDE[ _-]?2|Engineer[ _-]?2|L2|II|SDE[ _-]?2|analyst[ _-]?2)\b",
        "Engineer": r"(?i)\b(?:Associate|SDE[ _-]?1|Engineer[ _-]?1|L1|I|SDE[ _-]?1|tester|analyst|Engineer|Developer)\b",
        "Intern": r"(?i)\b(?:Intern|Trainee|Internship)\b"
    }

    # Mapping roles to experience years
    experience_mapping = {
        "Technical Architect": [15,17],
        "Principal Engineer": [13,15],
        "Senior Staff Engineer": [11,13],
        "Staff Engineer": [9,11],
        "Senior Lead Engineer": [7,9],
        "Lead Engineer": [5,7],
        "Senior Engineer": [3,5],
        "Engineer": [1,3],
        "Intern": [0,1]
    }


 

    # Initialize matched role and highest experience years
    matched_level = None
    highest_experience_years = 0

    # Extract experience years from relevant_exp
    if exp:
        exp_text = ' '.join(exp)
        years = extract_years_of_experience(exp_text)
        if years:
            highest_experience_years = max(years)  # Get the highest number of experience years
            # print(f"Job Title: {job_title}")
            # print(f"Extracted Highest Experience Years: {highest_experience_years}")
            
            
            print()
            matched_count_exp += 1
            return highest_experience_years # Skip title matching if experience is found
    
    # Check job title against levels if no experience years found
    for level, pattern in levels.items():
        if re.search(pattern, job_title, re.IGNORECASE):
            matched_level = level
            break

    # Determine the mapped experience years from the job title
    if matched_level:
        mapped_experience_years = experience_mapping.get(matched_level, 0)
        # print(f"Job Title: {job_title}")
        # print(f"Job Level from Title: {matched_level}")
        # print(f"Mapped Experience Years: {mapped_experience_years}")
        matched_from_title_count += 1
        
        return mapped_experience_years
        print()
    else:
        # Add unmatched titles to the list
        unmatched_titles.append({'Job Title': job_title})

 

# Example function to extract years of experience from text
def extract_years_of_experience(exp_text):
    

    years = re.findall(r'\b(\d+)\s*year', exp_text)
    years = list(map(int, years))
    
    # Define the ranges based on the extracted years
    ranges = []
    for year in years:
        if year >= 15:
            ranges.append([15, 17])
        elif year >= 13:
            ranges.append([13, 15])
        elif year >= 11:
            ranges.append([11, 13])
        elif year >= 9:
            ranges.append([9, 11])
        elif year >= 5:
            ranges.append([5, 7])
        elif year >= 3:
            ranges.append([3, 5])
        elif year >= 1:
            ranges.append([1, 3])
        else:
            ranges.append([0, 1])
    
    return ranges  
    




def check_fresher(soup, total_exp,job_title):
            """
            Check if job posting contains fresher keywords in the job description or job title,
            or intern keywords in the job title, or if total experience is within the range [0, 1].
            Returns 'Internship' or 'Fresher' based on the match.

            Args:
                soup (BeautifulSoup): Parsed HTML content.
                total_exp (list or int or float): Experience range or single experience value.
                linkedin_id (str): LinkedIn job ID.
                job_title (str): Job title.

            Returns:
                str or None: 'Internship' if intern-related keywords found in the title,
                'Fresher' if fresher-related keywords found, or None if no match.
            """
            # Locate the specific job description element
            jd_element = soup.find(class_="description__text description__text--rich")
            if jd_element:
                text = jd_element.get_text().lower()  # Extract text from the element
            else:
                text = ""  # Default to empty string if the element is not found

            # Patterns to match fresher-related keywords
            fresher_pattern = r'\b(fresher|freshers|trainee|trainees|apprentice|apprentices)\b'
            # Pattern to match intern-related keywords
            intern_pattern = r'\b(intern|interns|apprentice|apprentices|internship)\b'

            # Check for fresher-related keywords in job description text
            match_description_fresher = re.search(fresher_pattern, text)
            contains_fresher_keywords_desc = bool(match_description_fresher)

            # Check for fresher-related keywords in job title
            job_title = job_title.lower()  # Convert title to lowercase for case-insensitive matching
            match_title_fresher = re.search(fresher_pattern, job_title)
            contains_fresher_keywords_title = bool(match_title_fresher)

            # Check for intern-related keywords in job title only
            match_title_intern = re.search(intern_pattern, job_title)
            contains_intern_keywords_title = bool(match_title_intern)

            # Print the matched keyword(s)
            # if match_description_fresher:
            #     print(f"Matched fresher keyword in description: {match_description_fresher.group()}")
            # if match_title_fresher:
            #     print(f"Matched fresher keyword in title: {match_title_fresher.group()}")
            # if match_title_intern:
            #     print(f"Matched intern keyword in title: {match_title_intern.group()}")
                
                

            # Determine the match type
            if contains_intern_keywords_title:
                return 'Internship'  # Return 'Internship' if intern keywords are found in the title
            elif contains_fresher_keywords_desc or contains_fresher_keywords_title:
                return 'Fresher'  # Return 'Fresher' if fresher keywords are found



            # Check total experience range and return 'Fresher' if within [0, 1]
            if total_exp and len(total_exp) == 2:  # List case
                total_exp = sorted(total_exp)
                is_fresher_experience = 0 <= total_exp[0] <= 1 and 0 <= total_exp[1] <= 1
                if is_fresher_experience:
                    return 'Fresher'  # Return 'Fresher' if experience is in the fresher range

            return None  # Return None if no match is found


def main():

    total_jobs_parsed = 0
    count = 1
    while count>0:

        sleep(1.5)
        # res = supabase.table('Jobs').select('id', 'job_title', 'primary_skills', 'job_locations', 'Companies(id,company_verticals, attributes)').eq('is_priority_updated', False).limit(1).execute()

        res = supabase.table("scraping_raw_html"
                            ).select('job_url','company_id','companies!inner(id,is_jobs_to_be_parsed)', 'linkedin_job_id', 'linkedin_job_url', 'created_on', 'company', 'country', count = 'exact'
                            ).eq('is_parsed', False
                            ).eq('flag', False
                            ).eq('is_deleted', False
                            ).eq('companies.is_jobs_to_be_parsed',True  
                            ).not_.is_('has_detail_page', 'null'
                            ).eq('country','India'
                            # ).in_('country', ('India')
                            ).order('created_on', desc = True
                            # ).or_('country.not.eq.India,country.not.eq.United States'
                            ).limit(1
                            ).execute()


        count = res.count



        print('total remaining...',count)
        
        
        
   
        for raw_data in res.data:
       
            job_url = raw_data['job_url']

            job_id = raw_data['linkedin_job_id']

            com_id = raw_data['company_id']

            scraped_date = raw_data['created_on']
            
            company_name = raw_data['company']
            
            
            country = raw_data['country']
            
  
     
            print('------linkedin_id',job_id)


            sleep(0.33)


            job_exists_response = supabase.table('jobs').select('id', count = 'exact').eq('attributes->>linkedin_job_id', job_id).is_('application_closes_on', 'null').eq('is_deleted', False).execute()
    
            if job_exists_response.count:

                supabase.table('scraping_raw_html').update({"is_deleted":True}).eq('linkedin_job_id', job_id).execute()
                continue

            
            html_text =get_page_from_synology(job_id)

            if  html_text ==None:
                print('xxxxx', html_text )
                supabase.table('scraping_raw_html').update({'has_detail_page': None}).eq('linkedin_job_id',job_id).execute()
                continue


     

            html_text = html_text.decode('utf-8')



            # file_name = f"job_{job_id}_checkkkkkkkkk.html"

            # # Open a file in write mode and save the HTML content
            # with open(file_name, 'w', encoding='utf-8') as file:
            #     file.write(html_text)



            
            print('------',scraped_date)
            
            try:
             res = parse_job_data(html_text,job_url,job_id , com_id, company_name, country, scraped_date)
            except Exception as e:
                print('job_detail_page is not found',e )
                supabase.table('scraping_raw_html').update({"flag":True}).eq('linkedin_job_id', job_id).execute()
                sleep(0.1)
                # supabase.table('scraping_raw_html').update({'is_deleted': True}).eq('linkedin_job_id',job_id).execute()
                continue
           
           
            
            if country == 'India':

                hr_data = scrape_hr_data(html_text, company_name )
                if hr_data is not None:
                    print('===========')
                    data_base_upsert(hr_data,company_name,hr_data['name'])
                    # print('success')
                    # print(hr_data,company_name,hr_data['name'])
                    print('===========')
                    # break

            

            if res:
                update_data_after_parse = {
                'is_parsed': True,
                'is_deleted':True
                }

                job_created_res = supabase.table("scraping_raw_html").update(update_data_after_parse).eq('linkedin_job_id', job_id).execute()
                
                
                total_jobs_parsed += 1
            else:

                supabase.table("scraping_raw_html").update({'is_deleted':True}).eq('linkedin_job_id', job_id).execute()

    print(total_jobs_parsed)

                

if __name__ == "__main__":

    
    main()
