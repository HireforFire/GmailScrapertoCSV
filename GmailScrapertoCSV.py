import imaplib
import email
import requests
import csv
import io
from bs4 import BeautifulSoup
import datetime
from datetime import date, timedelta

# Make sure IMAP is enabled through the settings in the Gmail account you're accessing
# IMAP client setup
imap_server = 'imap.gmail.com'
username = 'username'
password = 'password'

# Connect to the IMAP server
imap = imaplib.IMAP4_SSL(imap_server)
imap.login(username, password)
imap.select('inbox')

# Search for emails with the CSV file download link
yesterday = date.today() - timedelta(days=1)
search_criteria = f'FROM reporting@vonagebusiness.com SUBJECT "Users Summary: {yesterday.strftime("%m/%d/%Y")}"'
response, messages = imap.search(None, search_criteria)

# Download the CSV file from the download link
most_recent_email_date = None
most_recent_email = None
for message_id in messages[0].split():
    response, message_parts = imap.fetch(message_id, '(RFC822)')
    email_body = message_parts[0][1]
    email_message = email.message_from_bytes(email_body)
    email_date = datetime.datetime.strptime(email_message['date'][:-6], '%a, %d %b %Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    if most_recent_email_date is None or email_date > most_recent_email_date:
        most_recent_email_date = email_date
        most_recent_email = email_message
for part in most_recent_email.walk():
    if part.get_content_type() == 'text/html':
        html_body = part.get_payload(decode=True).decode('utf-8')
        soup = BeautifulSoup(html_body, 'html.parser')
        # Find the hyperlink with the text "CSV" and get the download link
        csv_link = soup.find('a', text='CSV')
        if csv_link is not None and csv_link.has_attr('href'):
            download_link = csv_link['href']
            # Send an HTTP GET request to the download link
            response = requests.get(download_link, auth=(username, password))
            # Decode the response content using the appropriate encoding
            csv_data_decoded = response.content.decode('utf-8')
            # Create a file-like object from the decoded CSV data
            csv_file = io.StringIO(csv_data_decoded)
            # Read the CSV data using the csv module, specifying the appropriate encoding
            csv_reader = csv.reader(csv_file, delimiter=',')
            # Process the CSV file data
            rows = []
            for i, row in enumerate(csv_reader):
                if i == 0:
                    # Add 'Record ID' and 'Date' headers to the CSV file
                    row.insert(0, 'Record ID')
                    row.insert(1, 'Date')
                else:
                    # Add 'Record ID' and 'Date' values to the CSV file
                    record_id = int(str(i) + yesterday.strftime('%m%d%Y'))
                    row.insert(0, record_id)
                    row.insert(1, yesterday.strftime('%m/%d/%Y'))
                rows.append(row)
            # Save the CSV file to the same directory as the job
            file_name = f"users_summary_report{yesterday.strftime('%m%d%Y')}.csv"
            with open(file_name, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            break

# Close the IMAP connection
imap.close()
imap.logout()
