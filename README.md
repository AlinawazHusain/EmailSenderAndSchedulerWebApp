# Mass Email Sender with Dashboard

This project is a mass email sender application where users can upload a CSV file with contact information, fill out other required fields, and send or schedule emails. The application also provides a dashboard to view the status of sent, scheduled, or failed emails.

## Features

- **CSV Upload**: Upload a CSV file with contact details (`name`, `email`, `company_name`). check data.csv for reference. 
- **Email Sending**: Send emails instantly or schedule them for a later time.
- **Dashboard**: View the status of sent, scheduled, and failed emails.
- **Configurable API**: Easily configure Mailgun API credentials for email sending.

## Requirements

Before running the application, ensure you have the following installed:

- Python 3.13.0
- `pip` (Python package manager)

### Required Python Libraries

The required Python libraries are listed in `requirements.txt`. To install the necessary packages, run:

```bash
pip install -r requirements.txt

```

## HOW TO RUN?

- **RUN APP.PY**: After installing all dependencies run app.py file.
- **WARNING AND TIP**: If you are using FREE API key make sure to register the mail which you want to send mail first , else it dont supports on FREE API KEY
