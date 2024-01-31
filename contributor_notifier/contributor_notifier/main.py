########################################################################
#                    Prurpose of the Package                           #
########################################################################

# Check if there is a change in the GitHub repo. 
# Detect the contributors.
# Check of the contributor wants to be notified. 
# Extract the subject and the datamodel that has been change.  
# Send them customized emails depending on the change. 

########################################################################
#                                 TODO                                 #
########################################################################

# to dedetct the chnge = we need to have a db of versions 
# we can not trust the publications in portal of sdms 
# pull request 
# registry of the ppl that have been already warned that somthing has happened 
# warning typs: 
# say thank you and send an attestation 
# https://smartdatamodels.org/index.php/contributors/ 
# example of attestations in the portal for the ppl that want that
# we need to check if the user has an attestation then we can send him notifs 
# if he does not have an attestaion, than there is an unvalid email or name 
# only users that fil the info on github are the once that want to be noitfied 

# TODO due to a mistake that user makes, so we need to also reach out to them. 
# contribution that breaks the compatibility 
# I need to send to the contributor of the subject a text: 
#"there is a potential conflict, and I need to have their opinion"

# if there is a new datamodel, into a subject:
# then we need to notify the contributor
# we notify subject wise. 
# all the members could be also interested and just say to explore it via email 
# TODO: explore the database of notification: 
# who is the person, subject, when, name, surname, email, topic, text of notif (or a json file)
# depends on how we want to stor this data

# when the process should be launched:
# when there is datamodel 

# when there is a breaking verions update/ major version update: TODO: notify in this case as well 
# e.g 6 new attributes this makes the version change to a major change
# we need to detect the major version update 

# priorities which parts of the notifs/waterverse 
# last step : make this notif automatic (also part of waterverse)


########################################################################
#                                 Imports                              #
########################################################################
from socket import gethostname
#import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def send_email(msg_subject, message, destination):
    """
    Sends an email to the specified destination with the given message subject and content.

    Args:
        msg_subject (str): The subject of the email message.
        message (str): The content of the email message.
        destination (str): The email address of the recipient.

    Returns:
        None
    """
    server = smtplib.SMTP('mail.smartdatamodels.org', 587)
    server.starttls()
    server.login('info@smartdatamodels.org', "NDZkMjQwZDg1NWI3")
        # Craft message (obj)
    msg = MIMEMultipart()

    message = f'{message}\nSend from Hostname: {gethostname()}'
    msg['Subject'] = msg_subject
    msg['From'] = 'info@smartdatamodels.org'
    msg['To'] = destination
    # Insert the text to the msg going by e-mail
    msg.attach(MIMEText(message, "plain"))
    
    # send msg
    server.send_message(msg)
    print("sent email to " + destination)