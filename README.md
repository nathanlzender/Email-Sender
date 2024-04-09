# Python Email Sender

This Python script is designed to automate the process of sending emails to a list of recipients pulled from a CSV file. It sets up an SMTP server, reads email addresses from a CSV file, and sends emails to each recipient.

## Features

- **SMTP Server Setup**: The script establishes a connection pool with an SMTP server for sending emails.
- **CSV Integration**: Recipient email addresses are extracted from a CSV file, allowing for easy management of email lists.
- **Single Email setup**:  Utilizes a single email body and text template that can be reused for every recipient, reducing redundancy.
- **Error Handling**: If an email fails to send, the script logs the error and writes the email address to an error log for later review.
- **Account Rotation**: Sending email addresses are extracted from a CSV file while adhering to predefined sending limits for each address. Once the limit is reached, the system seamlessly transitions to the next designated sending email address in rotation.

## Prerequisites

Before running the script, ensure you have the following:

- Python 3 installed on your system.
- Access to an SMTP server for sending emails.
- SMTP Authorization enabled for each account from which you will be sending emails.
- CSV files containing recipient email addresses (`sendto.csv`) , sender account details (`ouraccounts.csv`), and a blank file for storing bad email adresses (`erroraccounts.csv`).

## Usage

1. **Setup a Python Enviornment**: Set up a default Python enviornment (venv), Python version 3.12.2 works.

2. **Configure SMTP Settings**: Set up the SMTP server details, including host, port, email limits, sender email address, and password in the script.

3. **HTML Email Content**: Customize the HTML content of the email by editing the `mail.html` file.

4. **Prepare CSV Files**: Ensure your CSV files (`sendto.csv` and `ouraccounts.csv`) have the password and email addresses in the correct columns.

5. **Run the Script**: Execute the script by running the `main()` function. This will start sending emails to the recipients listed in the `sendto.csv` file using the sender accounts listed in `ouraccounts.csv`.

## Important Notes

- **SMTP Server Email Per Day Limits**: Each server will have varrying email limits per day, make sure to setup the email limit per account before running.
- **SMTP Server Email Per Minute Limits**: Each server will have varrying email limits per minute, make sure to setup the sleep time and time to sleep before running.
- **Error Handling**: Check the error log (`erroraccounts.csv`) if any emails fail to send.

## Contributors

- Nathan Zender
