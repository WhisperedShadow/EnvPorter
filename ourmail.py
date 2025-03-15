import os
from dotenv import load_dotenv
from mailjet_rest import Client

load_dotenv()

api_key = os.getenv("MAIL_API_KEY")
api_secret = os.getenv("MAIL_SECRET_KEY")

mailjet = Client(auth=(api_key, api_secret), version='v3.1')

from_mail = os.getenv("FROM_MAIL")
to_email = os.getenv("TO_MAIL")

def send_mail(name, email, phNo, subject, sMessage):
    text_content = f"""\  
    Hello,  

    A new issue has been reported on EnvPorter. Below are the details:  

    **User Name:** {name}  
    **Email:** {email}  
    **Phone Number:** {phNo}  

    **Issue Subject:** {subject}  

    **Message:**  
    {sMessage}  

    Please review the issue and take the necessary action.  

    Regards,  
    EnvPorter Support Team  
    """

    message = {
        'Messages': [
            {
                "From": {
                    "Email": from_mail,  
                    "Name": "EnvPorter Support"
                },
                "To": [
                    {
                        "Email": to_email
                    }
                ],
                "Subject": subject,
                "TextPart": text_content
            }
        ]
    }

    result = mailjet.send.create(data=message)

    if result.status_code == 200:
        print("Mail sent successfully!")
    else:
        print(f"Failed to send email. Status code: {result.status_code}, Response: {result.json()}")
