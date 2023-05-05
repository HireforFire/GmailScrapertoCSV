# User Summary Report Scraper

This Python script connects to a Gmail account via IMAP, searches for an email with a Users Summary report CSV attachment from Vonage Business, downloads the CSV file, processes its data, adds a unique identifier and a date column, and saves it to a file.

## Requirements

- Python 3.x
- `imaplib`
- `email`
- `requests`
- `csv`
- `io`
- `beautifulsoup4`

## Usage

1. Install the required Python packages by running `pip install imaplib email requests beautifulsoup4`.
2. Open the `UserSummaryReportScraper.py` file in a text editor.
3. Modify the `username` and `password` variables to match your Gmail account credentials.
4. Run the script using the command `python UserSummaryReportScraper.py`.

The script will search for an email with the subject "Users Summary: {yesterday's date in MM/DD/YYYY format}" from `reporting@vonagebusiness.com` and download the CSV attachment. It will then add a unique identifier and a date column to the CSV data and save it to a file named `users_summary_reportMMDDYYYY.csv` in the same directory as the script.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

This script was inspired by a similar script from [Dylan Wood](https://github.com/dylanjwood).
