Install Dependencies:
Ensure you have Python installed. Then, install the required packages:

pip install -r requirements.txt

Install Tesseract OCR:

Windows: Download and install from https://github.com/UB-Mannheim/tesseract/wiki.

macOS: Install via Homebrew:
brew install tesseract
Linux: Install using your package manager, e.g., for Debian/Ubuntu:

sudo apt-get install tesseract-ocr
Install and Configure Tor:
Download Tor: Install the Tor Expert Bundle from https://www.torproject.org/download/.

Configure torrc File:
Locate your torrc file.

Add the following lines:
php-template
Copy
Edit
ControlPort 9051
HashedControlPassword <your_hashed_password>

To generate a hashed password, use:
tor --hash-password your_password
Replace <your_hashed_password> with the output from the above command.

Download ChromeDriver:

Ensure you have Google Chrome installed.

Download the ChromeDriver that matches your Chrome version from https://chromedriver.chromium.org/downloads.

Place the chromedriver executable in a known directory and update the CHROMEDRIVER_PATH variable in your script accordingly.

Configure the Script:

Set the TOR_PASSWORD variable in your script to match the password you used when generating the hashed control password.

Ensure all paths (e.g., to chromedriver and Tesseract OCR) are correctly set.

<b>Usage</b> 
Start the Tor service to ensure the SOCKS5 proxy is running.

Run the script:
Medium

python insta_scraper.py
When prompted, enter the public Instagram username you wish to scrape.

The script will:

Extract image URLs using Selenium.

Download images at 335px width, resizing if necessary.

Route requests through the Tor network, renewing the IP as configured.

Analyze each image for faces and sensitive text.

Log the results for your review.
