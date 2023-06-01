import smtplib
from src import EMAIL, PASSWORD

class EmailNotifier:

    def __init__():
        pass
    
    @staticmethod
    def send_email(receiver_email, message, receiver_name):       
        # Set up the SMTP server details
        from_email = EMAIL
        password = PASSWORD
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection: 
            email_password = password
            connection.login(from_email, email_password )
            connection.sendmail(from_addr=from_email, to_addrs=receiver_email, 
            msg=f"subject:Onyumbani Web Message \n\n Hi, {receiver_name}\n\n{message}\n\n Kind regards, \n\n Onyumbani Team")

