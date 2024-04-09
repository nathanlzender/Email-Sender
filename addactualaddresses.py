import csv
import getpass
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from datetime import datetime

start_time = time.time()  # Get the current time when the script starts

HOST = "smtp-mail.outlook.com"
PORT = 587

FROM_EMAIL = ""
PASSWORD = ""
EMAIL_LIMIT_PER_MINUTE = 30
EMAIL_LIMIT_PER_ACCOUNT = 50000
TIME_TO_SLEEP = 60 # After sending the EMAIL_LIMIT_PER_MINUTE, sleep is engaged to prevent email timeout

html_file_path = "mail.html" # Email we will be sending

# Create a connection pool
smtp_pool = smtplib.SMTP(HOST, PORT)
smtp_pool.starttls()
smtp_pool.login(FROM_EMAIL, PASSWORD)

# Reads the html file and returns the html part of the email for future use
def readhtml():
    with open("mail.html", "r") as file:
        html = file.read()
    html_part = MIMEText(html, 'html')
    return html_part

# Sends the email
def send_email(TO_EMAIL, html_part):
    
    # Create the email message, attach the html part to it
    message = MIMEMultipart("alternative")
    message['Subject'] = "Mail sent using python"
    message['From'] = FROM_EMAIL
    message['To'] = TO_EMAIL

    message.attach(html_part)
    
    # Use the single SMTP connection to try to send the email, if it fails, log the error and write the email to the erroraccounts.csv file
    try:
        smtp_pool.sendmail(FROM_EMAIL, TO_EMAIL, message.as_string())
    except smtplib.SMTPException as e:
        print(f"Failed to send email to {TO_EMAIL}. Error: {e}")
        with open("erroraccounts.csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([TO_EMAIL,'', e])
            file.flush()
    
# Reads the csv file for all accounts we are sending to and sends the email
def read_csv_and_send_email(csv_sendtofile_path, ouraccounts_usernames_list, ouraccounts_passwords_list, column_index, html_part, FROM_EMAIL):
    email_counter = 0
    ouraccounts_email_counter = 0
    
    with open(csv_sendtofile_path, newline='') as csv_sendtofile_path:
        reader = csv.reader(csv_sendtofile_path)
        for index, row in enumerate(reader):
            if index >= 1:  # Skip header row
                TO_EMAIL = row[column_index]
                if TO_EMAIL != "":
                    email_counter += 1 # Moves the csv index forward 1 emails being sent out
                    send_email(TO_EMAIL, html_part)
                    
                    if email_counter % EMAIL_LIMIT_PER_MINUTE == 0: #tests for if we have sent 30 emails in the last minute
                        print("Waiting 5 seconds to prevent email timeout")
                        print("")
                        time.sleep(TIME_TO_SLEEP)
                
                    if email_counter % EMAIL_LIMIT_PER_ACCOUNT == 0: # checks if we have hit the output limit for the email service for this account
                        if ouraccounts_email_counter < len(ouraccounts_usernames_list):
                            FROM_EMAIL = ouraccounts_usernames_list[ouraccounts_email_counter]
                            PASSWORD = ouraccounts_passwords_list[ouraccounts_email_counter]
                            ouraccounts_email_counter += 1
                            print("Swapping sending email to:", FROM_EMAIL)
                        else:
                            return "Did not finish the whole list, last email sent to: " + TO_EMAIL  # Stop looping if column index is out of range, if you hit here, it means we have maxed out the emails that outlook allows in a day based on how many emails we have

    return "Finished"

#Creates a list from a csv, this is used for emails we are sending from and passwords for those accounts
def read_csv_column_to_list(column_index, csv_accounts_path):
    accounts_list = []
    try:
        with open(csv_accounts_path, mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if len(row) > column_index:
                    accounts_list.append(row[column_index])
    except FileNotFoundError as e:
        print(f"Error: {e}")
    return accounts_list

def main():
        
    csv_sendtofile_path = "sendto.csv" # Name of csv file we will be sending emails to
    csv_ouraccounts_path = "ouraccounts.csv" # Name of csv file we will be sending emails from
    column_index_usernames = 6  # Index of column G (0-based)
    ouraccounts_usernames_list = read_csv_column_to_list(6, csv_ouraccounts_path) # 6 is the index of column G (0-based)
    ouraccounts_passwords_list = read_csv_column_to_list(4, csv_ouraccounts_path) # 4 is the index of column E (0-based)

    html_part = readhtml()

    print(read_csv_and_send_email(csv_sendtofile_path, ouraccounts_usernames_list, ouraccounts_passwords_list, column_index_usernames, html_part, FROM_EMAIL))

    # Closing the SMTP connection
    smtp_pool.quit()

    end_time = time.time()

    start_time_str = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
    end_time_str = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')


    elapsed_time = end_time - start_time  # Calculate the elapsed time
    print(f"Script started at: {start_time_str} and ended at: {end_time_str}")
    print(f"Script completed in {elapsed_time:.2f} seconds.")

main()

