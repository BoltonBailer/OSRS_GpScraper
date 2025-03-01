import requests
from bs4 import BeautifulSoup

# URL of the webpage to scrape
url = 'https://www.eldorado.gg/osrs-gold/g/10-0-0'

# Send a GET request to fetch the raw HTML content
response = requests.get(url)
response.raise_for_status()  # Ensure the request was successful

# Parse the content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Function to clean and extract text
def clean_text(element):
    return ' '.join(element.stripped_strings)

# Find the section containing gold prices
# This may vary depending on the website's structure
# Inspect the webpage to find the correct tag and class
price_section = soup.find('div', class_='offer-list-contents')

# Extract and clean the text
if price_section:
    cleaned_text = clean_text(price_section)
else:
    cleaned_text = 'Price section not found.'

# Save the cleaned text to a file
with open('Selected_Document.txt', 'w', encoding='utf-8') as file:
    file.write(cleaned_text)

print('Gold prices have been extracted and saved to Selected_Document.txt')
