import utils
import requests
from datetime import datetime, timedelta
import time
import config


class SendMails:
    def __init__(self , data , prompt , sender_email):
        self.data = data
        self.prompt = prompt
        self.sender_email = sender_email
        self.datalen = len(self.data)
    
    def GetCustomizeMail(self):
        for i in range(self.datalen):
            customisation_text = f"I want to send this mail to someone with name = {self.data.iloc[i]['name']} and company name = {self.data.iloc[i]['company_name']} and dont give any extra placeholder too "
            response = utils.getMailSubjectAndBody(utils.GenerateResponse(self.prompt+customisation_text))
            custom_mail_data = {
                'subject': response[0],
                'body' :response[1],
                'receiver': self.data.iloc[i]['email']
            }
            yield custom_mail_data
    
    def sender(self , counts):
        dataloader = self.GetCustomizeMail()
        counts[0] = "SENDING MAILS"
        for i in range(self.datalen):
            mail_data = next(dataloader)
            subject = mail_data['subject']
            body = mail_data['body']
            receiver = mail_data['receiver']

            data = {
                'from': self.sender_email,
                'to': receiver,
                'subject': subject,
                'text': body,
            }
            response = requests.post(config.MAILGUN_API_URL, auth=('api', config.MAILGUN_API_KEY), data=data)
            if response.status_code == 200:
                counts[1]+=1
            else:
                counts[2]+=1

            time.sleep(1)
        counts[0] = "IDOL"
        
    
    def schedule_email(self , delay_minutes , counts):
        dataloader = self.GetCustomizeMail()
        counts[0] = "SCHEDULING MALES"
        curr_time = datetime.now()
        timelapse = delay_minutes
        for i in range(self.datalen):
            mail_data = next(dataloader)
            subject = mail_data['subject']
            body = mail_data['body']
            receiver = mail_data['receiver']

            send_at = (curr_time + timedelta(minutes=timelapse)).strftime('%Y-%m-%d %H:%M:%S')
            data = {
                'from': self.sender_email,
                'to': receiver,
                'subject': subject,
                'text': body,
                'o:deliverytime': send_at
            }
        
            response = requests.post(config.MAILGUN_API_URL, auth=('api', config.MAILGUN_API_KEY), data=data)
            
            if response.status_code == 200:
                counts[3]+=1
            else:
                counts[2]+=1

            timelapse += delay_minutes
            time.sleep(1)
        counts[0] = "IDOL"
    

