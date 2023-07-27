from google.cloud import dialogflow_v2
from google.api_core.exceptions import InvalidArgument
import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
import os
from datetime import datetime
import csv
import random
from fuzzywuzzy import fuzz
import re

# Dialogflow Code
# """
# Returns intent, entity, confidence and reply
# """
def ca_bot(text):
  DIALOG_FLOW_PROJECT_ID = "tribal-archery-386911"
  DIALOGFLOW_LANGUAGE_CODE = "en"
  os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'

  text_input = dialogflow_v2.TextInput(text=text, language_code=DIALOGFLOW_LANGUAGE_CODE)
  SESSION_ID = 'me'
  session_client = dialogflow_v2.SessionsClient()
  session = session_client.session_path(DIALOG_FLOW_PROJECT_ID, SESSION_ID)
  query_input = dialogflow_v2.QueryInput(text=text_input)

  try:
      response = session_client.detect_intent(request={"session": session, "query_input": query_input})
  except InvalidArgument:
      raise

#   print("Query text: {}".format(response.query_result.query_text))
  intent = response.query_result.intent.display_name
  confidence = response.query_result.intent_detection_confidence
#   print("Detected intent: {} (confidence: {})\n".format(intent, confidence))

  entities = {}
  for entity in response.query_result.parameters:
      value = response.query_result.parameters[entity]
      if value:
          # Check if the value is a list and convert it to a string
          if isinstance(value, list):
              value = value[0] if len(value) > 0 else None  # Get the first element if it exists
          # Convert value to a string if it is not already
          if not isinstance(value, str):
              value = str(value)
          # Remove brackets using regular expressions
          value = re.sub(r'\[|\]', '', value)
          # Remove extra space and single quotation marks
          value = value.strip().strip("'")
          entities[entity] = value

#   print("Detected entities:", entities)
  entity=entities

  # Load dataset from CSV file
  def load_dataset(file_path):
      with open(file_path, 'r', encoding="utf8") as csv_file:
          reader = csv.DictReader(csv_file)
          dataset = list(reader)
      for entry in dataset:
        skills = entry['SKILLS']
        if skills:
            entry['SKILLS'] = re.findall(r"'(.*?)'", skills)
        else:
            entry['SKILLS'] = []
      return dataset


  # Match intent and entity to display relevant information
  def match_intent_entity(user_intent, user_entity, dataset):
    matched_entries = []
    for entry in dataset:
        company_name = entry['COMPANY_NAME'].lower()
        jobtitle = entry['TITLE'].lower()
        location = entry['LOCATION'].lower()
        skills = [skill.lower() for skill in entry['SKILLS']]
        if  user_intent=='Default Welcome Intent':
          
          if fuzz.ratio(text.lower(), 'thank you') >= 75:
            matched_entries.append('Have a good day')
          elif fuzz.ratio(text.lower(), 'how are you') >= 75:
            matched_entries.append('I\'m good')
          elif fuzz.ratio(text.lower(), 'what is your name') >= 50: 
             matched_entries.append('My name is CABOT') 
          else:
            matched_entries.append('Hey! How can I help you today?')
        elif  user_intent=='Default Fallback Intent':
           matched_entries.append('Apologies for the inconvenience. My memory is currently limited.')
        elif user_intent == 'job_prospects':
            # Check if the user entity matches the entry
            if not user_entity or (len(user_entity) == 1 and 'number' in user_entity and isinstance(user_entity['number'], str) and user_entity['number'].isdigit()):
                matched_entries.append(f"{entry['TITLE']} - {entry['COMPANY_NAME']}")
            elif 'jobtitle' in user_entity and 'location' in user_entity:
                if re.search(fr"\b({user_entity['jobtitle'].replace('/', '|').lower()})\b", jobtitle) and \
                        re.search(fr"\b({user_entity['location'].lower()})\b", location):
                    matched_entries.append(f"{entry['TITLE']} - {entry['COMPANY_NAME']}")
            elif 'company_name' in user_entity and 'location' in user_entity:
                if re.search(fr"\b({user_entity['company_name'].replace('/', '|').lower()})\b", jobtitle) and \
                        re.search(fr"\b({user_entity['location'].lower()})\b", location):
                    matched_entries.append(entry['TITLE'])        
            elif 'company_name' in user_entity and re.search(fr"\b({user_entity['company_name'].replace('/', '|').lower()})\b", jobtitle):
                matched_entries.append(entry['TITLE'])
            elif 'jobtitle' in user_entity and re.search(fr"\b({user_entity['jobtitle'].replace('/', '|').lower()})\b", jobtitle):
                matched_entries.append(f"{entry['TITLE']} - {entry['COMPANY_NAME']}")
            elif 'location' in user_entity and re.search(fr"\b({user_entity['location'].lower()})\b", location):
                matched_entries.append(entry['TITLE'])
            elif 'skills' in user_entity and (user_entity['skills'].lower() in skills):
                matched_entries.append(entry['TITLE'])
            elif 'job_type' in user_entity and user_entity['job_type'].lower() == entry['JOBTYPE'].lower():
                matched_entries.append(entry['TITLE'])

        elif user_intent == 'list_of_companies':
            # Check if the user entity matches the entry
            if not user_entity or (len(user_entity) == 1 and 'number' in user_entity and isinstance(user_entity['number'], str) and user_entity['number'].isdigit()):
                matched_entries.append(entry['COMPANY_NAME'])
                
            elif 'jobtitle' in user_entity and 'location' in user_entity:
                if re.search(fr"\b({user_entity['jobtitle'].replace('/', '|').lower()})\b", jobtitle) and \
                        re.search(fr"\b({user_entity['location'].lower()})\b", location):
                   
                    matched_entries.append(f"{entry['TITLE']} - {entry['COMPANY_NAME']}")
                    
            elif 'company_name' in user_entity and 'location' in user_entity:
                if re.search(fr"\b({user_entity['company_name'].replace('/', '|').lower()})\b", jobtitle) and \
                        re.search(fr"\b({user_entity['location'].lower()})\b", location):
                    matched_entries.append(entry['COMPANY_NAME'])    
            elif 'company_name' in user_entity and re.search(fr"\b({user_entity['company_name'].replace('/', '|').lower()})\b", jobtitle):
                matched_entries.append(entry['COMPANY_NAME'])
            elif 'jobtitle' in user_entity and re.search(fr"\b({user_entity['jobtitle'].replace('/', '|').lower()})\b", jobtitle):
                matched_entries.append(f"{entry['TITLE']} - {entry['COMPANY_NAME']}")
            elif 'location' in user_entity and re.search(fr"\b({user_entity['location'].lower()})\b", location):
                matched_entries.append(entry['COMPANY_NAME'])
            elif 'skills' in user_entity and (user_entity['skills'].lower() in skills):
                matched_entries.append(entry['COMPANY_NAME'])
            elif 'job_type' in user_entity and user_entity['job_type'].lower() == entry['JOBTYPE'].lower():
                matched_entries.append(entry['COMPANY_NAME'])
        elif user_intent == 'skills_required':
            # Check if the user entity matches the entry
            if not user_entity or (len(user_entity) == 1 and 'number' in user_entity and isinstance(user_entity['number'], str) and user_entity['number'].isdigit()):
                matched_entries.extend(entry['SKILLS'])
            elif 'jobtitle' in user_entity and 'location' in user_entity:
                if re.search(fr"\b({user_entity['jobtitle'].replace('/', '|').lower()})\b", jobtitle) and \
                        re.search(fr"\b({user_entity['location'].lower()})\b", location):
                   
                    matched_entries.extend(entry['SKILLS'])
            elif 'company_name' in user_entity and 'location' in user_entity:
                if re.search(fr"\b({user_entity['company_name'].replace('/', '|').lower()})\b", jobtitle) and \
                        re.search(fr"\b({user_entity['location'].lower()})\b", location):
                    matched_entries.extend(entry['SKILLS'])    
            elif 'company_name' in user_entity and re.search(fr"\b({user_entity['company_name'].replace('/', '|').lower()})\b", jobtitle):
                matched_entries.extend(entry['SKILLS'])
            elif 'jobtitle' in user_entity and re.search(fr"\b({user_entity['jobtitle'].replace('/', '|').lower()})\b", jobtitle):
                matched_entries.extend(entry['SKILLS'])
            elif 'location' in user_entity and re.search(fr"\b({user_entity['location'].lower()})\b", location):
                matched_entries.extend(entry['SKILLS'])
            elif 'skills' in user_entity and (user_entity['skills'].lower() in skills):
                matched_entries.extend(entry['SKILLS'])
            elif 'job_type' in user_entity and user_entity['job_type'].lower() == entry['JOBTYPE'].lower():
                matched_entries.extend(entry['SKILLS'])                
        elif user_intent == 'qualifications_required':
            if not user_entity or (len(user_entity) == 1 and 'number' in user_entity and isinstance(user_entity['number'], str) and user_entity['number'].isdigit()):
              if 'qualification' in text.lower() or 'qualifications' in text.lower():
                 matched_entries.append(entry['QUALIFICATIONS'])
            # Check if the user entity matches the entry
            if 'jobtitle' in user_entity and 'location' in user_entity:
                if re.search(fr"\b({user_entity['jobtitle'].replace('/', '|').lower()})\b", jobtitle) and \
                        re.search(fr"\b({user_entity['location'].lower()})\b", location):
                   
                    matched_entries.append(entry['QUALIFICATIONS'])
            elif 'company_name' in user_entity and 'location' in user_entity:
                if re.search(fr"\b({user_entity['company_name'].replace('/', '|').lower()})\b", jobtitle) and \
                        re.search(fr"\b({user_entity['location'].lower()})\b", location):
                    matched_entries.append(entry['QUALIFICATIONS'])    
            elif 'company_name' in user_entity and re.search(fr"\b({user_entity['company_name'].replace('/', '|').lower()})\b", jobtitle):
                matched_entries.append(entry['QUALIFICATIONS'])
            elif 'jobtitle' in user_entity and re.search(fr"\b({user_entity['jobtitle'].replace('/', '|').lower()})\b", jobtitle):
                matched_entries.append(entry['QUALIFICATIONS'])
            else:
                matched_entries.append('Apologies, but I don\'t have the information you\'re seeking. Could you please retry your query using specific job titles or a company name?')
        elif user_intent == 'salary_info':   
            random_number = random.randrange(250000, 1500000, 10000)
            entry['random_number'] = random_number
            if not user_entity or (len(user_entity) == 1 and 'number' in user_entity and isinstance(user_entity['number'], str) and user_entity['number'].isdigit()):
                matched_entries.append(entry['random_number'])
            elif 'jobtitle' in user_entity and 'location' in user_entity:
                if re.search(fr"\b({user_entity['jobtitle'].replace('/', '|').lower()})\b", jobtitle) and \
                        re.search(fr"\b({user_entity['location'].lower()})\b", location):
                   
                    matched_entries.append(f"{entry['TITLE']} - {entry['random_number']}")
            elif 'company_name' in user_entity and 'location' in user_entity:
                if re.search(fr"\b({user_entity['company_name'].replace('/', '|').lower()})\b", jobtitle) and \
                        re.search(fr"\b({user_entity['location'].lower()})\b", location):
                    matched_entries.append(f"{entry['COMPANY_NAME']} - {entry['random_number']}")    
            elif 'company_name' in user_entity and re.search(fr"\b({user_entity['company_name'].replace('/', '|').lower()})\b", jobtitle):
                matched_entries.append(f"{entry['COMPANY_NAME']} - {entry['random_number']}")
            elif 'jobtitle' in user_entity and re.search(fr"\b({user_entity['jobtitle'].replace('/', '|').lower()})\b", jobtitle):
                matched_entries.append(f"{entry['TITLE']} - {entry['random_number']}")
            elif 'location' in user_entity and re.search(fr"\b({user_entity['location'].lower()})\b", location):
                matched_entries.append(entry['random_number'])
            elif 'skills' in user_entity and (user_entity['skills'].lower() in skills):
                matched_entries.append(entry['random_number'])
            elif 'job_type' in user_entity and user_entity['job_type'].lower() == entry['JOBTYPE'].lower():
                matched_entries.append(entry['random_number'])          
    matched_entries=list(set(matched_entries))
    
    if 'number' in user_entity:
        number = str(user_entity['number'])
        matched_entries = random.sample(list(set(matched_entries)), int(number))
    
    return matched_entries

  # Example usage
  def query_dataset(user_intent, user_entity):
      dataset = load_dataset('final_df.csv')  # Replace 'your_dataset.csv' with the actual file path

      # Match intent and entity to display relevant information
      
      matched_entries =(match_intent_entity(user_intent, user_entity, dataset))
      
    #   print(matched_entries)
      filtered_entries =set(list([str(entry) for entry in matched_entries for entry_part in str(entry).split(',') if entry_part.replace(' ', '').isalnum()]))
        
      if 'number' in user_entity:
        value=matched_entries
      elif user_intent=='Default Fallback Intent' or user_intent=='Default Welcome Intent':
        value= matched_entries 
      elif re.search(r'\baverage\b', text, re.IGNORECASE):
        numbers = [int(entry) for entry in matched_entries]
        if numbers:
          average = sum(numbers) / len(numbers) 
          value=int(average)
      elif re.search(r'\b(how\s+many|count)\b', text, re.IGNORECASE):
        value = len(filtered_entries)
      elif len(filtered_entries) > 10:
        matched_entries = random.sample(list(set(filtered_entries)), 10)
        value = matched_entries
      elif len(filtered_entries)>=1 and len(filtered_entries)< 10:
        matched_entries = set(filtered_entries)
        value =matched_entries
        
      elif matched_entries==[]:
          value="At the moment, my memory capabilities are restricted." 
      return list(value)

  reply=query_dataset(intent,entity)
  return intent,entity,confidence,reply



# Create a csv file which contains the intent, confidence, entities, reply
if not os.path.exists("logs"):  # Creating a new directory to store the logs
    os.makedirs("logs")

# Streamlit app
st.set_page_config(page_title="CABOT", initial_sidebar_state="collapsed")
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stActionButton {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
if "rerun" not in st.session_state:
    # pth = dict()
    # pth["path"] = ""
    now = datetime.now()  # Get the current date and time
    now = re.sub(r'[^\w_. -]', '_', now.strftime("%d/%m/%Y %H:%M:%S"))  # Replacing _ with - as filenames do not support these 
    path = os.path.join("logs", f"{now}.csv")
    with open(path, 'a') as csvfile: 
        csvfile.write("Date,Question,Response,Entities,Confidence,Intent" + "\n")
    st.session_state.rerun = path


st.title("🤖CABOT")
if "generated" not in st.session_state:
    st.session_state["generated"] = ["Hello! Welcome"]

if "past" not in st.session_state:
    st.session_state["past"] = ["Hi!"]

response_container = st.container()
colored_header(label='', description='', color_name='blue-30')
input_container = st.container()

def get_text():
    if "input_text" not in st.session_state:
        st.session_state.input_text = ""

    def clear_text():
        st.session_state.input_text = st.session_state.input
        st.session_state.input = ""
    input_text = st.text_input("You: ", "", key="input", on_change=clear_text)

    return st.session_state.input_text

with input_container:
    user_input = get_text()

def generate_response(prompt):
    intent,entity,confidence,reply = ca_bot(prompt)
    with open(st.session_state.rerun, "a") as f:
        r = "["
        if type(reply) == type([]):
            r = f"'{reply}'"
            r = re.sub(r",", "\t", r)
            f.write(f"{datetime.now()},{prompt},{r},{entity},{confidence},{intent}\n")
        else:
            f.write(f"{datetime.now()},{prompt},{reply},{entity},{confidence},{intent}\n")
    sam = ""
    if type(reply) == type([]):
            for msg in reply:
                sam = sam + msg + "\n"
            reply = sam
    return reply



with response_container:
    if user_input:
        response = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)
        
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state['generated'][i], key=str(i))
with st.sidebar:
    st.sidebar.title("Logs")
    try:
        with open(st.session_state.rerun, "r") as f:
            st.download_button("Download Logs", f, file_name=st.session_state.rerun, mime="text/csv")
    except:
        st.info("Start Chatting to get the logs")