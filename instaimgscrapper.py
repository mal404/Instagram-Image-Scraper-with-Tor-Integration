import os
import time
import cv2
import pytesseract
import requests
from PIL import Image
from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# === USER CONFIGURATION ===
TOR_PASSWORD = "your_password_here"  # plaintext password used in torrc
CHROMEDRIVER_PATH = r"C:\Path\To\chromedriver.exe"  # path to chromedriver.exe
USERNAME = input("Enter Instagram username to scrape: ").strip()

# === PATHS ===
SAVE_DIR = os.path.join("ig_results", USERNAME)
os.makedirs(SAVE_DIR, exist_ok=True)

# === FACE DETECTOR ===
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# === TOR CONFIGURATION ===
TOR_SOCKS_PROXY = 'socks5h://127.0.0.1:9050'
TOR_CONTROL_PORT = 9051

def renew_tor_ip():
    with Controller.from_port(port=TOR_CONTROL_PORT) as controller:
        controller.authenticate(password=TOR_PASSWORD)
        controller.signal(Signal.NEWNYM)
    print("[TOR] New Tor identity requested.")
    time.sleep(10)

def resize_image_to_335px(image_path):
    try:
        img = Image.open(image_path)
        if img.width != 335:
            ratio = 335.0 / img.width
            height = int(img.height * ratio)
            img = img.resize((335, height), Image.ANTIALIAS)
            img.save(image_path)
            print(f"[+] Resized to 335px: {image_path}")
    except Exception as e:
        print(f"[!] Resize failed: {e}")

def analyze_image(path):
    result = {"file": path, "faces": 0, "sensitive": False, "ocr_text": ""}
    try:
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result["faces"] = len(face_cascade.detectMultiScale(gray, 1.1, 4))
        text = pytesseract.image_to_string(gray)
        result["ocr_text"] = text.strip()
        keywords = ["aadhaar", "passport", "id", "credit", "debit", "visa", "mastercard"]
        result["sensitive"] = any(k in text.lower() for k in keywords)
    except Exception as e:
        print(f"[!] Analysis failed: {e}")
    return result

def setup_selenium():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=service, options=options)

def download_image(url, index):
    try:
        renew_tor_ip()
        proxies = {'http': TOR_SOCKS_PROXY, 'https': TOR_SOCKS_PROXY}
        img_path = os.path.join(SAVE_DIR, f"img_{index}.jpg")
        r = requests.get(url, proxies=proxies, timeout=10)
        if r.status_code == 200:
            with open(img_path, 'wb') as f:
                f.write(r.content)
            print(f"[+] Downloaded: {img_path}")
            resize_image_to_335px(img_path)
            return img_path
        else:
            print(f"[!] Failed to download (status {r.status_code})")
    except Exception as e:
        print(f"[!] Download error: {e}")
    return None

def scrape_profile_images():
    driver = setup_selenium()
    driver.get(f"https://www.instagram.com/{USERNAME}/")
    time.sleep(5)
    images = driver.find_elements(By.TAG_NAME, 'img')
    image_urls = list({img.get_attribute('src') for img in images if img.get_attribute('src')})
    print(f"[i] Found {len(image_urls)} images")
    driver.quit()
    return image_urls[:10]  # limit to 10

def main():
    results = []
    urls = scrape_profile_images()
    for i, url in enumerate(urls):
        img_path = download_image(url, i)
        if img_path:
            result = analyze_image(img_path)
            results.append(result)
    print("\n📊 FINAL REPORT")
    for r in results:
        print(f"{r['file']} | 👥 Faces: {r['faces']} | 🔒 Sensitive: {r['sensitive']}")

if __name__ == "__main__":
    main()
