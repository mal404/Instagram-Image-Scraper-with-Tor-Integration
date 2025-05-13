# 📸 Instagram Image Scraper with Tor Integration

A powerful Python tool that scrapes public Instagram profile images using Selenium, routes image downloads through the Tor network for anonymity, and analyzes the images using AI (OpenCV for face detection and Tesseract for OCR-based sensitive text detection).

---

## ✨ Features

- 🕵️‍♂️ Scrapes public profile images using **Selenium**
- 📏 Downloads images sized exactly **335px** wide (or resizes smaller ones)
- 🧅 Routes requests through the **Tor SOCKS5 proxy** (`socks5h://127.0.0.1:9050`)
- 🔁 Renews Tor IP:
  - After each image download
  - Every 10 seconds
- 👁️ Detects **faces** in images using OpenCV
- 🔐 Extracts and flags **sensitive text** using Tesseract OCR (e.g., `ID`, `passport`, `credit card`)
- 📋 Prints a **clean summary report** of all scanned images

---

## 📦 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

Your `requirements.txt` should include:

```
selenium
requests
opencv-python
pytesseract
Pillow
stem
```

---

## 🛠 Setup Instructions

### 🔹 1. Clone the Repository

```bash
git clone https://github.com/yourusername/instagram-image-scraper.git
cd instagram-image-scraper
```

---

### 🔹 2. Install Tesseract OCR

- **Windows**: [Download here](https://github.com/UB-Mannheim/tesseract/wiki) and add the path to your system environment variables.
- **macOS**:
  ```bash
  brew install tesseract
  ```
- **Linux**:
  ```bash
  sudo apt install tesseract-ocr
  ```

---

### 🔹 3. Install and Configure Tor

- **Download** the [Tor Expert Bundle](https://www.torproject.org/download/)
- Locate your `torrc` file and add:

```
ControlPort 9051
HashedControlPassword <your_hashed_password>
```

- To generate the password hash:

```bash
tor --hash-password your_password
```

Use this hash in your `torrc` file.

---

### 🔹 4. Install ChromeDriver

- Find your **Chrome version**
- Download matching **[ChromeDriver](https://chromedriver.chromium.org/downloads)**
- Add to system PATH or set the path in your script:
```python
CHROMEDRIVER_PATH = "C:/Path/To/chromedriver.exe"
```

---

## ⚙️ Script Configuration

At the top of the script, configure:

```python
TOR_PASSWORD = "your_password"  # The password used to generate hashed password in torrc
CHROMEDRIVER_PATH = "C:/Path/To/chromedriver.exe"
```

---

## 🚀 Usage

1. Make sure **Tor is running**
2. Run the script:

```bash
python insta_scraper.py
```

3. Enter the public Instagram username when prompted.

---

## 📁 Output

- All images are saved in:
  ```
  ig_results/<instagram_username>/
  ```
- Summary report includes:
  - File name
  - Face count
  - Sensitive text presence (True/False)

---

