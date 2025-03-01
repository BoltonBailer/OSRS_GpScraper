import requests
from bs4 import BeautifulSoup

# URL of the webpage to scrape
url = 'https://www.eldorado.gg/osrs-gold/g/10-0-0'

# Set headers to mimic a real browser (helps bypass anti-scraping measures)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Send a GET request
response = requests.get(url, headers=headers)
response.raise_for_status()  # Ensure the request was successful

# Parse the content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Locate all offer seller cards (each seller's listing)
offer_cards = soup.find_all('div', class_='offer-seller-card')

# Extract relevant information (seller name, price, delivery time)
sellers_data = []

for card in offer_cards:
    try:
        # Extract Seller Name
        seller_name = card.find('a', class_='profile__username').text.strip()

        # Extract Price (inside the "price-details" div)
        price_container = card.find('div', class_='price-details')
        price = price_container.find('strong', class_='font-size-18').text.strip() if price_container else "N/A"

        # Extract Delivery Time
        delivery_time_container = card.find('div', class_='delivery-avg')
        delivery_time = delivery_time_container.text.strip() if delivery_time_container else "N/A"

        # Extract Stock Amount
        stock_container = card.find('div', class_='value')
        stock = stock_container.text.strip() if stock_container else "N/A"

        # Store extracted data
        sellers_data.append(f"Seller: {seller_name} | Price: {price} | Stock: {stock} | Delivery: {delivery_time}")

    except AttributeError:
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
