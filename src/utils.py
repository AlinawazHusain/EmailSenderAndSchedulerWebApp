import re
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from groq import Groq
from config import GROQ_API_KEY


def GenerateResponse(prompt):
    '''
    Generates Response Fron Given Prompt Using GROQ API

    __-================================================-__
    ||    UPDATAE yout GROQ API KEY in config.py file   ||
    __-================================================-__

    '''
    client = Groq(
        api_key= GROQ_API_KEY,
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content






def readFile(file, filename):
    '''

    Reads Uploaded excel files and Return pandas DataFrame

    '''
    extension = 'csv'
    if(filename[-4:] == 'xlsx'):
        extension = 'xlsx'
    df = pd.read_csv(file) if extension == 'csv' else pd.read_excel(file)

    return df







def readGoogleSheet(jsoncredential , sheetName):
    '''

    Takes JSon credentials and sheet name as input and return Pandas DataFrame

    '''
    scope = ["https://www.googleapis.com/auth/spreadsheets.readonly", 
            "https://www.googleapis.com/auth/drive.readonly"]

    creds = ServiceAccountCredentials.from_json_keyfile_name(jsoncredential, scope)
    
    client = gspread.authorize(creds)
    sheet = client.open(sheetName).sheet1
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df






def formatEmailBody(raw_body):
    '''
    This function formats a raw email body to ensure proper structure with:
    - Paragraph breaks
    - Properly formatted list items
    - Removes excessive whitespace and structures the email properly
    '''
    # Step 1: Normalize white spaces - Replace multiple spaces with a single space
    body = re.sub(r'\s+', ' ', raw_body).strip()
    
    # Step 2: Separate sections of email with paragraph breaks
    # We want to keep meaningful breaks (i.e., double newlines or big gaps)
    body = re.sub(r'\n{2,}', '\n\n', body)  # Ensures double newline as paragraph breaks
    
    # Step 3: Identify bullet points and format them into proper list items
    body = re.sub(r'\*\s*', '\n* ', body)  # Any line starting with '*' should be on a new line
    
    # Step 4: Add breaks around certain keywords for better structure (e.g., "Dear [Name],")
    body = re.sub(r'(Dear \S+)', r'\n\1', body)  # Ensure a newline before "Dear"
    body = re.sub(r'(Best regards,)', r'\n\1', body)  # Ensure a newline before "Best regards"
    
    # Optional: Remove any other extra spaces after paragraph formatting
    body = re.sub(r'(\s{2,})', ' ', body)  # Remove any excessive spaces between words
    
    # Step 5: Clean up extra spaces around paragraph breaks
    body = re.sub(r'\n\s*\n', '\n\n', body)  # Remove unwanted newlines

    return body

def getMailSubjectAndBody(email_text):
    '''
    Extracts and formats the subject and body from a generated response.
    Cleans up the body with paragraph breaks and list formatting.
    '''
    # Extracting the subject part
    email_text = email_text.split("Subject:")[1]
    subject = email_text.split('\n')[0].strip()

    # Extracting the raw body (the rest of the text)
    body = '\n'.join(email_text.split('\n')[1:]).strip()

    # Clean and structure the body with our formatting function
    cleaned_body = formatEmailBody(body)
    seperated_content = []

    first_comma_position = cleaned_body.find(',')
    seperated_content.append(cleaned_body[:first_comma_position+1])
    best_regards_position = cleaned_body.lower().find("best regards")
    seperated_content.append(cleaned_body[first_comma_position+1 : best_regards_position])
    lastpos = best_regards_position
    if best_regards_position != -1:
        post_best_regards = cleaned_body[best_regards_position + len("Best regards"):]
        # Find all commas in the substring
        comma_positions_after_best_regards = [i + best_regards_position + len("Best regards") for i in range(len(post_best_regards)) if post_best_regards[i] == ',']
        for  i in comma_positions_after_best_regards:
            seperated_content.append(cleaned_body[lastpos:i+1])
            lastpos = i+1
    seperated_content.append(cleaned_body[lastpos:])
    
    mailbodycontent = "\n".join(seperated_content) + "\n"
    
    return [subject, mailbodycontent]