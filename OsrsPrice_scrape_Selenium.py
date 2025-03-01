from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Selenium WebDriver with headless mode
options = Options()
options.add_argument("--headless")  # Run in headless mode (no GUI)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the website
url = 'https://www.eldorado.gg/osrs-gold/g/10-0-0'
driver.get(url)

# Allow time for JavaScript to load
time.sleep(5)

# Locate all offer seller cards
offer_cards = driver.find_elements(By.CLASS_NAME, "offer-seller-card")

# Extract relevant information (seller name, price, stock, delivery time)
sellers_data = []

for card in offer_cards:
    try:
        # Extract Seller Name
        seller_name = card.find_element(By.CLASS_NAME, "profile__username").text.strip()

        # Extract Price
        price_element = card.find_element(By.CLASS_NAME, "price-details")
        price = price_element.find_element(By.TAG_NAME, "strong").text.strip()

        # Extract Stock Amount
        stock_element = card.find_elements(By.CLASS_NAME, "value")
        stock = stock_element[0].text.strip() if stock_element else "N/A"

        # Extract Delivery Time
        delivery_time_element = card.find_elements(By.CLASS_NAME, "delivery-avg")
        delivery_time = delivery_time_element[0].text.strip() if delivery_time_element else "N/A"

        # Store extracted data
        sellers_data.append(f"Seller: {seller_name} | Price: {price} | Stock: {stock} | Delivery: {delivery_time}")

    except Exception:
        continue  # Skip if any field is missing

# Save extracted data to a file
if sellers_data:
    with open('Selected_Document.txt', 'w', encoding='utf-8') as file:
        file.write("\n".join(sellers_data))

    print(f'Gold prices extracted and saved to Selected_Document.txt')
    for seller in sellers_data:
        print(f'- {seller}')
else:
    print('No gold prices found. The page structure may have changed.')

# Close the browser
driver.quit()
