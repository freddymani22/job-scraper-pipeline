from bs4 import BeautifulSoup, NavigableString, Tag
import spacy
import re
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse, unquote
from supabase import create_client, Client
import random
import json
import openai
import chevron
from mistralai import Mistral
from time import sleep
import requests
import os
from dotenv import load_dotenv

load_dotenv()

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


def clean_jobs_json_string(result):
    result = result.replace('```json', '').replace('```', '')

    try:
        json_start = result.find('{')
        json_end = result.rfind('}') + 1

        if json_start == -1 or json_end == 0:
            raise ValueError("No JSON object found in the string")

        json_str = result[json_start:json_end]
        json_str = json_str.strip()

        return json_str

    except ValueError as e:
        print(f"Error cleaning JSON string: {e}")
        return None


def mistral_ai(user_message):
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)

    chat_response = client.agents.complete(
        agent_id="ag:7bcb4c28:20250214:untitled-agent:b02ab32e",
        messages=[
            {
                "role": "user",
                "content": user_message,
            },
        ]
    )

    response_json = json.dumps(chat_response, default=lambda o: o.__dict__, indent=4)

    response_dict = json.loads(response_json)

    result = response_dict.get('choices')[0].get('message').get('content')

    cleaned_json_str = clean_jobs_json_string(result)

    result_obj = json.loads(cleaned_json_str)

    return result_obj


def deepseek_ai(prompt):
    if prompt:
        completion = client_deep.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "system", "content": prompt}],
            response_format={"type": "json_object"},
        )

        res = json.loads(completion.choices[0].message.content)

        return res


def generalized_gpt_func(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        json_start = content.find('{')
        json_end = content.rfind('}') + 1
        if json_start >= 0 and json_end > json_start:
            json_str = content[json_start:json_end]
            json_str = json_str.replace("\n", "").strip()
            return json.loads(json_str)
        raise ValueError("Could not extract valid JSON from response")


def custom_strip(text):
    unwanted_chars = ['ÃÂÃÂ¢ÃÂ¢ÃÂÃÂ¬ÃÂÃÂ¢',': ','-', '.', '"', "~", '', "ÃÂÃÂ¢ÃÂÃÂÃÂÃÂ", '\u202f', '* ','* ', '1)', '2)', '3)', '4)', '5)', '6)', '7)', '8)', '9)', '10)']
    text = text.strip()

    text = text.replace('\u202f', ' ')
    text = text.replace("ÃÂÃÂ¯ÃÂÃÂ¿ÃÂÃÂ½", ' ')

    while text and text[0] in unwanted_chars:
        text = text[1:]

    text = text.strip()

    return text


def add_period_to_lines(text):
    lines = text.split('\n')
    lines_with_period = [line.strip() + '.' if line.strip() and not line.strip().endswith('.') else line.strip() for line in lines]
    return '\n'.join(lines_with_period)


def parse_exp(soup):
    jd_element = soup.find(class_="description__text description__text--rich")

    if not jd_element:
        return []
    jd_text = jd_element.get_text(separator='\n').strip()
    jd_text_with_period = add_period_to_lines(jd_text)

    nlp = spacy.blank("en")
    nlp.add_pipe("sentencizer")

    skill_pattern_path ="/home/kalibot-1/work/skills_pattern_for_jd.jsonl"
    ruler = nlp.add_pipe("entity_ruler", config={"overwrite_ents": True})
    ruler.from_disk(skill_pattern_path)

    doc = nlp(jd_text_with_period)

    experience_sentences = []

    for sent in doc.sents:
        sentence = sent.text.lower()

        if 'experience' in sentence:
            for _ in sent.ents:
                    number_pattern = r'\b(zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|1[0-4]|\d)\b'
                    experience_matches = re.findall(number_pattern, sentence)
                    if experience_matches and ('year' in sentence or 'years' in sentence):
                        experience_sentence = custom_strip(sent.text)
                        if not experience_sentence.endswith('.'):
                            experience_sentence += '.'
                        experience_sentences.append(experience_sentence)
                        break

    return experience_sentences


def parse_job_title(soup):
    job_title_tag = soup.find(class_='top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title')
    job_title = job_title_tag.get_text(strip=True)

    cleaned_title = job_title.strip()

    return cleaned_title


def parse_exp_level(soup):
    exp_level_tags = soup.find_all(class_="description__job-criteria-text description__job-criteria-text--criteria")

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
        span_elements = location_tag.find_all('span')

        if len(span_elements) >= 2:
            location_info= span_elements[1].text.strip()

            location_info = location_info.split(',')[0] if ',' in location_info else location_info

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
        }

        for city, standardized_city in city_mappings.items():
            if city.lower() in location_info.lower():
                return standardized_city

        top_it_hubs = ["Hyderabad", "Pune", "Chennai", "Noida", "Gurugram", "Gurgaon", "Mumbai", "Kolkata", "Visakhapatnam",  "Trivandrum", "Indore", "Delhi", "Coimbatore"]

        for hub in top_it_hubs:
            if hub.lower() in  location_info.lower():
                return hub

        return location_info
    else:
        print("Location element not found.")
        return None


def extract_linkedin_id(link="http://www.linkedin.com/in/rishab-srivastava-63a6a3170/"):
    if not link.startswith("https://") and not link.startswith("http://"):
        link = "https://" + link

    parsed_url = urlparse(link)

    if parsed_url.path and parsed_url.path.startswith("/in/"):
        linkedin_id = parsed_url.path[4:]

        if linkedin_id.endswith("/"):
            linkedin_id = linkedin_id[:-1]

        if linkedin_id.startswith("/"):
            linkedin_id = linkedin_id[1:]

        return linkedin_id
    else:
        return None


def data_base_upsert(data,company,name):
    sleep(0.3)
    res = supabase.table("linkedin_connection_data").select('*').eq('company',company).eq('name',name).execute()

    response = res.data
    if response:
        if response[0]['id']:
            data['id'] = response[0]['id']

    try:
        supabase.table("linkedin_connection_data").upsert(data).execute()
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
    combined_text = "\n".join(text_blocks) + "\n"
    return combined_text


def remove_company_name(text, company_name):
    company_name_pattern = re.compile(re.escape(company_name), re.IGNORECASE)

    lines = text.split('\n')

    cleaned_lines = []

    for line in lines:
        if company_name_pattern.search(line):
            continue
        else:
            cleaned_lines.append(line)

    cleaned_text = '\n'.join(cleaned_lines)

    return cleaned_text


def print_text_between_ids(soup, id_list, company_name):
    if not id_list:
        print("The id_list is empty.")
        return ""

    combined_text = ""

    if len(id_list) < 2:
        last_element = soup.find(id=id_list[-1])
        if last_element:
            current_tag = soup.find()
            while current_tag and current_tag != last_element:
                combined_text += current_tag.get_text(separator=' ', strip=True) + ' '
                current_tag = current_tag.find_next_sibling()

            combined_text += last_element.get_text(separator=' ', strip=True) + ' '
            current_tag = last_element.find_next_sibling()
            while current_tag:
                combined_text += current_tag.get_text(separator=' ', strip=True) + ' '
                current_tag = current_tag.find_next_sibling()

        cleaned_text = remove_company_name(combined_text.strip(), company_name)
        return cleaned_text

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

    positive_regex = '|'.join([re.escape(pattern) for pattern in positive_words_patterns])
    positive_regex_pattern = re.compile(positive_regex, re.IGNORECASE)

    counter = 0
    id_list = []

    for tag in soup.find_all(True):
        tag_text = tag.get_text(separator=' ').strip()
        if len(tag_text.split()) <= 8:
            if positive_regex_pattern.search(tag_text):
                unique_id = generate_unique_id('tag', counter)
                tag['id'] = unique_id
                id_list.append(unique_id)
                counter += 1

    return soup, id_list


def parse_skillset(soup, company_name):
    jd_element = soup.find(class_="description__text description__text--rich")

    new_soup, ids_list = find_two_word_tags(jd_element)

    parsed_skills = set()

    text = print_text_between_ids(new_soup, ids_list, company_name)

    text += '\n'

    text +=  combine_text_blocks(jd_element,company_name)

    nlp = spacy.blank("en")
    nlp.add_pipe("sentencizer")

    skill_pattern_path ="/home/kalibot-1/work/merged_unique.jsonl"
    ruler = nlp.add_pipe("entity_ruler", config={"overwrite_ents": True})
    ruler.from_disk(skill_pattern_path)
    skills = set()
    parsed_skills = set()

    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ == 'SKILL':
            skill = ent.text
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
    days_pattern = r'(\d+)\s+days?'
    weeks_pattern = r'(\d+)\s+weeks?'
    hours_pattern = r'(\d+)\s+hours?\s+ago'
    months_pattern = r'(\d+)\s+months?\s+ago'
    years_pattern = r'(\d+)\s+years?\s+ago'

    days_match = re.search(days_pattern, text)
    if days_match:
        return int(days_match.group(1))

    weeks_match = re.search(weeks_pattern, text)
    if weeks_match:
        weeks = int(weeks_match.group(1))
        return weeks * 7

    hours_match = re.search(hours_pattern, text)
    if hours_match:
        hours = int(hours_match.group(1))
        return hours / 24

    months_match = re.search(months_pattern, text)
    if months_match:
        months = int(months_match.group(1))
        return months * 30

    years_match = re.search(years_pattern, text)
    if years_match:
        years = int(years_match.group(1))
        return years * 365

    return None


def parse_date_posted(soup, scraped_on):
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

    date_element = soup.find(class_="tvm__text tvm__text--neutral") or soup.find(class_="tvm__text tvm__text--positive")
    if date_element:
        reposted_ago = date_element.get_text(strip=True)
        days_ago = convert_time_period(reposted_ago)

        if days_ago is not None:
            date_posted = scraped_on_datetime - timedelta(days=days_ago)
            return date_posted.date().isoformat()

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
    if job_url == 'Easy apply':
        return f'https://linkedin.com/jobs/view/{linkedin_id}'

    if job_url.startswith('https://www.linkedin.com/authwall') or \
       job_url.startswith('http://www.linkedin.com/authwall'):
        return f'https://linkedin.com/jobs/view/{linkedin_id}'

    parsed_url = urlparse(job_url)

    if 'linkedin.com' in parsed_url.netloc:
        query_params = parse_qs(parsed_url.query)

        linkedin_terms = ['linkedin']

        if 'url' in query_params:
            redirect_url = unquote(query_params['url'][0])

            parsed_redirect_url = urlparse(redirect_url)
            redirect_query_params = parse_qs(parsed_redirect_url.query)

            filtered_redirect_params = {}
            for key, values in redirect_query_params.items():
                if not any(term in key.lower() for term in linkedin_terms):
                    filtered_values = [
                        value for value in values
                        if not any(term in str(value).lower() for term in linkedin_terms)
                    ]

                    if filtered_values:
                        filtered_redirect_params[key] = filtered_values
            print(urlunparse(parsed_redirect_url))
            parsed_redirect_url=get_final_url_or_original((urlunparse(parsed_redirect_url)))
            print('---------------------cleaned_url',parsed_redirect_url)
            parsed_redirect_url = urlparse(parsed_redirect_url)
            cleaned_redirect_url = urlunparse((
                parsed_redirect_url.scheme,
                parsed_redirect_url.netloc,
                parsed_redirect_url.path,
                parsed_redirect_url.params,
                urlencode(filtered_redirect_params, doseq=True),
                parsed_redirect_url.fragment
            ))

            return cleaned_redirect_url

        path_parts = parsed_url.path.split('/')
        for part in path_parts:
            if part.isdigit():
                return f'https://linkedin.com/jobs/view/{part}'

    query_params = parse_qs(parsed_url.query)

    linkedin_terms = ['linkedin']

    updated_query_params = {}
    for key, values in query_params.items():
        if not any(term in key.lower() for term in linkedin_terms):
            filtered_values = [
                value for value in values
                if not any(term in str(value).lower() for term in linkedin_terms)
            ]

            if filtered_values:
                updated_query_params[key] = filtered_values

    updated_query_string = urlencode(updated_query_params, doseq=True)

    new_url = urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        updated_query_string,
        parsed_url.fragment
    ))

    return new_url


def assign_role(job_title):
    if not job_title:
        return

    sleep(0.1)
    roles_res = supabase.table('roles').select('attributes', 'id').eq('is_deleted', False).execute()

    rules = []

    executive_roles = [
        'Vice President', 'Director', 'Sales', 'Finance', 'Product Manager',
        'Business Development Specialist', 'Technical Writer', 'Data Scientist',
        'Project Manager', 'Digital Marketing', 'Admin', 'Engineering Manager',
        'Human Resources', 'Program Manager', 'Business Analyst', 'Graphic Designer',
        'Marketing', 'Recruiter', 'Talent Acquisition', 'Supply Chain Roles',
        'UI/UX Designer'
    ]

    keywords = r"(engineer|developer|analyst|intern|architect|lead|scientist|specialist|designer|director|consultant)"

    for role in roles_res.data:
        attributes = role['attributes']
        rules.append((
            attributes.get('role_search_using_title_p1'),
            attributes.get('ordering'),
            role['id'],
            attributes.get('category'),
            attributes.get('name')
        ))

    rules.sort(key=lambda x: x[1])

    for pattern, ordering, role, category, _ in rules:
        if re.search(pattern, job_title, re.IGNORECASE):
            if any(exec_role in job_title for exec_role in executive_roles):
                return {
                    "roles": role,
                    "ordering": ordering,
                    "category": category,
                    'priority':1
                }

    for pattern, ordering, role, category, _ in rules:
        if re.search(pattern, job_title, re.IGNORECASE):
            if re.search(keywords, job_title, re.IGNORECASE):
                return {
                    "roles": role,
                    "ordering": ordering,
                    "category": category,
                    'priority':1
                }

    return None


def generate_uuid(JRole=None, Company=None, CompType=None, Domain=None, Location=None, Investor=None, WorkType=None):
    uuid_bytes = b"\x00\x00\x00\x00"

    uuid_bytes += (0 if JRole is None else JRole).to_bytes(2, byteorder="big")

    uuid_bytes += (0 if Company is None else Company).to_bytes(3, byteorder="big")

    uuid_bytes += (0 if CompType is None else CompType).to_bytes(1, byteorder="big")

    uuid_bytes += (0 if Domain is None else Domain).to_bytes(1, byteorder="big")

    uuid_bytes += (0 if Location is None else Location).to_bytes(2, byteorder="big")

    uuid_bytes += (0 if Investor is None else Investor).to_bytes(2, byteorder="big")

    uuid_bytes += (0 if WorkType is None else WorkType).to_bytes(1, byteorder="big")

    uuid_string = uuid_bytes.hex()

    return uuid_string


def clean_json_string(json_string):
    cleaned = ' '.join(json_string.split())

    return cleaned


def clean_string(s):
    s = s.lower()

    cleaned = []
    for c in s:
        code_point = ord(c)
        if 0x1D5D4 <= code_point <= 0x1D5ED:
            cleaned.append(chr(ord('a') + (code_point - 0x1D5D4)))
        elif 0x1D5EE <= code_point <= 0x1D607:
            cleaned.append(chr(ord('a') + (code_point - 0x1D5EE)))
        else:
            cleaned.append(c)
    s = ''.join(cleaned)

    new_s = []
    for c in s:
        if c.isalnum() or c == '-':
            new_s.append(c)
        else:
            new_s.append('-')
    s = ''.join(new_s)

    s = re.sub(r'-+', '-', s)
    s = s.replace('-startups', '-funded-startups')
    s = s.strip('-')

    return s


def get_social_channels(role_id):
    if not role_id:
        return None
    try:
        channels_data=supabase.table('channel_automation')\
            .select('social_media_type','channel_name','description', 'channel_url')\
            .contains('multiple_roles', [role_id]).execute()

        if not channels_data.data:
            return None

        channels = {'in': {}}

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

        attributes['query'] = parsed_template['query']
        attributes['seo_title']= parsed_template['seo_title']
        attributes['seo_description'] = parsed_template['seo_description']
        if country_code is not None:
            attributes['country_code']=country_code

    attributes['url_path'] = clean_string(f'{role_name}-{data_name}')
    if (attributes['url_path']):
        url_check_res=supabase.table('job_groups').select('id').eq('attributes->>url_path',attributes['url_path']).execute()
    if url_check_res.data:
        if 'company' in  combination_name:
            attributes['url_path']=clean_string(f'{role_name}-{linkedin_company_name}')
        if 'location' in combination_name:
            attributes['url_path']=clean_string(f'{role_name}-{data_name}-{country_code}')

    attributes['bg_color'] = random.choice(bgColor)

    channels=get_social_channels(role_id)
    if(channels):
        attributes['channels']=channels

    try:
        supabase.table('job_groups').insert({'attributes':attributes, 'criteria':criteria,'unique_hex':job_group_uuid, 'combination_name':combination_name}).execute()
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

    attributes['url_path'] = clean_string(f'{data_name}')
    if (attributes['url_path']):
        url_check_res=supabase.table('job_groups').select('id').eq('attributes->>url_path',attributes['url_path']).execute()
    if url_check_res.data:
        if 'company' in  combination_name:
            attributes['url_path']=clean_string(f'{linkedin_company_name}')
        if 'location' in combination_name:
            attributes['url_path']=clean_string(f'{data_name}-{country_code}')

    attributes['bg_color'] = random.choice(bgColor)

    if type_1=='roles':
        channels=get_social_channels(data_id)
        if(channels):
            attributes['channels']=channels

    try:
        supabase.table('job_groups').insert({'attributes':attributes, 'criteria':criteria,'unique_hex':job_group_uuid, 'combination_name':combination_name}).execute()
    except Exception:
        print(job_group_uuid,type_1)


def create_job_group(job_data):
    job_data = job_data[0]
    company_id = job_data.get('company')
    location = job_data['job_locations'][0]['label'].split(', ')[0]
    job_role = job_data.get('job_role', None)

    sleep(0.2)
    company_res = supabase.table('companies').select('incre_id','linkedin_unique_key','attributes->>band', 'company_verticals', 'brand_name').eq('id', company_id).execute()

    if job_role:
        job_role_res = supabase.table('roles').select('incre_id', 'id', 'attributes->>name').eq('id', job_role).execute()
        job_role_incre_id = job_role_res.data[0]['incre_id']
        job_role_name = job_role_res.data[0]['name']
        role_id = job_role_res.data[0]['id']

        job_role_uuid = generate_uuid(JRole=job_role_incre_id)
        individual_group(type_1='roles', data_id=role_id, data_name=job_role_name,
                        category='Role', job_group_uuid=job_role_uuid)
    for company in company_res.data:
        comp_incre_id = company['incre_id']
        comp_types = company['company_verticals']
        company_name = company['brand_name']
        comp_band = company['band']
        linkedin_company_name=company['linkedin_unique_key']

        ind_comp_uuid = generate_uuid(Company=comp_incre_id)
        individual_group(type_1='companies', data_id=company_id, data_name=company_name,
                       category='Company', job_group_uuid=ind_comp_uuid,linkedin_company_name=linkedin_company_name)

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
                if comp_att_funding is None:
                    template_type = 'company_type'
                elif '-' in comp_att_funding:
                    lte = comp_att_funding.split('-')[1]
                    gte = comp_att_funding.split('-')[0]
                    template_type = 'company_type_funding_range'
                else:
                    gte = int(comp_att_funding.rstrip('+'))
                    template_type = 'company_type_gte'

                ind_comp_att_uuid = generate_uuid(CompType=comp_att_incre_id)
                individual_group(type_1=template_type, data_id=comp_att_id, data_name=comp_att_name,
                               category='Company_Attribute', job_group_uuid=ind_comp_att_uuid,
                               lte=lte, gte=gte, bands=comp_band)

                if job_role:
                    comp_att_role_uuid = generate_uuid(CompType=comp_att_incre_id, JRole=job_role_incre_id)
                    job_group_create(type_1=template_type, data_id=comp_att_id, data_name=comp_att_name,
                                   role_id=role_id, bands=comp_band, role_name=job_role_name,
                                   category='Company_Attribute', lte=lte, gte=gte,
                                   job_group_uuid=comp_att_role_uuid)

        if comp_types:
            for comp_type in comp_types:
                domain_res = supabase.table('domains').select('incre_id','id','name').eq('id', comp_type).execute()

                domain_incre_id = domain_res.data[0]['incre_id']
                domain_res_id = domain_res.data[0]['id']
                domain_name = domain_res.data[0]['name']

                ind_domain_uuid = generate_uuid(Domain=domain_incre_id)
                individual_group(type_1='domains', data_id=domain_res_id, data_name=domain_name,
                            category='Domain', job_group_uuid=ind_domain_uuid)

                if job_role:
                    job_role_domain_uuid = generate_uuid(JRole=job_role_incre_id, Domain=domain_incre_id)
                    job_group_create(type_1='domains', data_id=domain_res_id, data_name=domain_name,
                                role_id=role_id, role_name=job_role_name, category='Domain',
                                job_group_uuid=job_role_domain_uuid)

    location_res = supabase.table('locations').select('incre_id','id','city', 'attributes').eq('attributes->>is_top_city', 'true').or_(f'city.ilike.%{location}%,attributes->aliases->>0.ilike.%{location}%').execute()

    if location_res.data:
        location_incre_id = location_res.data[0]['incre_id']
        location_name = location_res.data[0]['city']
        location_id = location_res.data[0]['id']
        location_country = location_res.data[0]['attributes']['country']
        location_country_code = location_res.data[0]['attributes']['country_code']

        ind_loc_uuid = generate_uuid(Location=location_incre_id)
        individual_group(type_1='locations', data_id=location_id, data_name=location_name,
                       category='Location', country=location_country,
                       country_code=location_country_code, job_group_uuid=ind_loc_uuid)

        if job_role:
            job_location_uuid = generate_uuid(JRole=job_role_incre_id, Location=location_incre_id)
            job_group_create(type_1='locations', data_id=location_id, data_name=location_name,
                           role_id=role_id, role_name=job_role_name, category='Location',
                           country=location_country, country_code=location_country_code,
                           job_group_uuid=job_location_uuid)


def assign_secondary_role(job_title: str) -> str:
    job_title_lower = job_title.lower()

    developer_pattern = r'\b(sde|developer|dev)\b'
    engineer_pattern = r'\b(engineer)\b'

    if re.search(developer_pattern, job_title_lower):
        return 'Developer'
    elif re.search(engineer_pattern, job_title_lower):
        return 'Engineer'

    return None


def clean_job_data(soup, job_title):
    jd_element = soup.find(class_="description__text description__text--rich")

    if jd_element:
        jd_text = jd_element.get_text().lower()
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

    role = None
    job_role = None
    role_meta_data = {}

    if role_name_llm:
        matched_role = next(role for role in roles if role["name"] == role_name_llm)

        job_role = matched_role["id"]

        role_meta_data = {
            "category": matched_role["category"],
            "priority": 1
        }

    if role:
        job_role = role.get('roles', None)

        role_meta_data = {key: role.get(key) for key in ['priority', 'category'] if role.get(key) is not None}

    exp_range = None
    if job_title:
        exp_range = job_role_assign_unmatched(job_title,exp)

    experience_level = 'Internship' if exp_level == 'Internship' else (job_type_llm or exp_level)

    secondary_role =None

    if  not role:
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

        return True
    else:
        return False


def get_page_from_synology(linkedin_in):
    try:
        sleep(0.5)
        res = supabase.storage.from_('jobs_scraping').download(linkedin_in)
        return res
    except Exception:
        supabase.table('scraping_raw_html').update({'is_deleted':True}).eq('linkedin_job_id',linkedin_in).execute()
        return None


def job_role_assign_unmatched(job_title,exp):
    timestamp = datetime.now(timezone.utc) - timedelta(days=1)
    timestamp = timestamp.isoformat()

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

    matched_level = None
    highest_experience_years = 0

    if exp:
        exp_text = ' '.join(exp)
        years = extract_years_of_experience(exp_text)
        if years:
            highest_experience_years = max(years)
            print()
            return highest_experience_years

    for level, pattern in levels.items():
        if re.search(pattern, job_title, re.IGNORECASE):
            matched_level = level
            break

    if matched_level:
        mapped_experience_years = experience_mapping.get(matched_level, 0)
        return mapped_experience_years
    else:
        pass


def extract_years_of_experience(exp_text):
    years = re.findall(r'\b(\d+)\s*year', exp_text)
    years = list(map(int, years))

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
    jd_element = soup.find(class_="description__text description__text--rich")
    if jd_element:
        text = jd_element.get_text().lower()
    else:
        text = ""

    fresher_pattern = r'\b(fresher|freshers|trainee|trainees|apprentice|apprentices)\b'
    intern_pattern = r'\b(intern|interns|apprentice|apprentices|internship)\b'

    match_description_fresher = re.search(fresher_pattern, text)
    contains_fresher_keywords_desc = bool(match_description_fresher)

    job_title = job_title.lower()
    match_title_fresher = re.search(fresher_pattern, job_title)
    contains_fresher_keywords_title = bool(match_title_fresher)

    match_title_intern = re.search(intern_pattern, job_title)
    contains_intern_keywords_title = bool(match_title_intern)

    if contains_intern_keywords_title:
        return 'Internship'
    elif contains_fresher_keywords_desc or contains_fresher_keywords_title:
        return 'Fresher'

    if total_exp and len(total_exp) == 2:
        total_exp = sorted(total_exp)
        is_fresher_experience = 0 <= total_exp[0] <= 1 and 0 <= total_exp[1] <= 1
        if is_fresher_experience:
            return 'Fresher'

    return None


def main():
    total_jobs_parsed = 0
    count = 1
    while count>0:
        sleep(1.5)

        res = supabase.table("scraping_raw_html"
                            ).select('job_url','company_id','companies!inner(id,is_jobs_to_be_parsed)', 'linkedin_job_id', 'linkedin_job_url', 'created_on', 'company', 'country', count = 'exact'
                            ).eq('is_parsed', False
                            ).eq('flag', False
                            ).eq('is_deleted', False
                            ).eq('companies.is_jobs_to_be_parsed',True
                            ).not_.is_('has_detail_page', 'null'
                            ).eq('country','India'
                            ).order('created_on', desc = True
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

            print('------',scraped_date)

            try:
                res = parse_job_data(html_text,job_url,job_id , com_id, company_name, country, scraped_date)
            except Exception as e:
                print('job_detail_page is not found',e )
                supabase.table('scraping_raw_html').update({"flag":True}).eq('linkedin_job_id', job_id).execute()
                sleep(0.1)
                continue

            if country == 'India':
                hr_data = scrape_hr_data(html_text, company_name )
                if hr_data is not None:
                    print('===========')
                    data_base_upsert(hr_data,company_name,hr_data['name'])
                    print('===========')

            if res:
                update_data_after_parse = {
                    'is_parsed': True,
                    'is_deleted':True
                }

                supabase.table("scraping_raw_html").update(update_data_after_parse).eq('linkedin_job_id', job_id).execute()

                total_jobs_parsed += 1
            else:
                supabase.table("scraping_raw_html").update({'is_deleted':True}).eq('linkedin_job_id', job_id).execute()

    print(total_jobs_parsed)


if __name__ == "__main__":
    main()
