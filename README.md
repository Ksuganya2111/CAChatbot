# CAChatbot
It is a chatbot that guides people in their career.
## 1. Data Collection
 - AI/ML related job details are scraped from Indeed using Selenium and BeautifulSoup.
 - The collected details are stored in text format.
## 2. Extract Information
 - Job_Title, Company_Name, Salary, Skills, and Qualifications are extracted from the text file using NER transformers.
## 3. Build a Knowledge Base
 - The extracted details are stored in a dataset.
## 4. Parse a User Request
 - Intent and entity are extracted from a user request. For example, when a user says, "I want to know about company X," the system understands the request and sends a request to the backend to get company information. Some possible approaches include noun phrase extraction, verb phrase extraction (for example, find all companies, find all jobs, what skills are needed for ML jobs at X).
 - To achieve this, Google Dialogflow is utilized to train the model to understand the intent and entity.
## 5. Display Response
 - Data is gathered from backend services to generate a text response message.
 - Regular Expression and Fuzzy matching techniques are used to match the extracted intent and entity with the dataset.
 - Streamlit is employed as the frontend to display the response.
