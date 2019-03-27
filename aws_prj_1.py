'''
This is a sample Lambda function that sends an email on click of a
button. It requires these SES permissions.
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ses:GetIdentityVerificationAttributes",
                "ses:SendEmail",
                "ses:VerifyEmailIdentity"
            ],
            "Resource": "*"
        }
    ]
}

The following JSON template shows what is sent as the payload:
{
    "serialNumber": "GXXXXXXXXXXXXXXXXX",
    "batteryVoltage": "xxmV",
    "clickType": "SINGLE" | "DOUBLE" | "LONG"
}

A "LONG" clickType is sent if the first press lasts longer than 1.5 seconds.
"SINGLE" and "DOUBLE" clickType payloads are sent for short clicks.

For more documentation, follow the link below.
http://docs.aws.amazon.com/iot/latest/developerguide/iot-lambda-rule.html
'''

from __future__ import print_function

import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ses = boto3.client('ses')
################## create a variable 'email_address' with email address you want to send msg.
#from_email_address = ''
#to_email_address = ''

# Check whether email is verified. Only verified emails are allowed to send emails to or from.
def check_email(email):
    result = ses.get_identity_verification_attributes(Identities=[email])
    attr = result['VerificationAttributes']
    if (email not in attr or attr[email]['VerificationStatus'] != 'Success'):
        logging.info('Verification email sent. Please verify it.')
        ses.verify_email_identity(EmailAddress=email)
        return False
    logger.info('######email verified.')
    return True


def lambda_handler(event, context):
    logging.info(' ********** Received event: ' + json.dumps(event))

    if not check_email(from_email_address):
        logging.error('Email is not verified')
        return
    ################## create a variable 'subject' of email.
    # subject = 'Hello from your IoT button %s' % event['serialNumber']

    ################## create a variable 'body_text' of email.
    # body_text = 'Hello from your IoT Button %s. Here is the full event: %s' % (event['serialNumber'], json.dumps(event))

    response = ses.send_email(Source=from_email_address,
                   Destination={'ToAddresses': [to_email_address]},
                   Message={'Subject': {'Data': subject}, 'Body': {'Text': {'Data': body_text}}})
    logger.info('Email has been sent')
    print(response)
    logger.info(response)
    
