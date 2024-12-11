import requests
from bs4 import BeautifulSoup


def get_all_events():
    # URL of the site to scrape
    url = 'https://gorodzovet.ru/rostov/'

    # Send a request to fetch the website content
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check if the request was successful

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract event blocks
    event_blocks = soup.find_all('div', class_='event-block')

    # Collect event details (title, date, price, and link)
    event_list = []
    for event in event_blocks:
        # Extract event title
        title_tag = event.find('h3', class_='lines')
        title = title_tag.get_text(strip=True) if title_tag else 'No title'

        # Extract event date
        date_tag = event.find('div', class_='event-date')
        date = date_tag.get_text(strip=True) if date_tag else 'No date provided'

        # Extract event price (if available)
        price_tag = event.find('div', class_='event-price')
        price = price_tag.get_text(strip=True) if price_tag else 'No price info'

        # Extract event link
        link_tag = event.find('a', href=True)
        link = 'https://gorodzovet.ru' + link_tag['href'] if link_tag else 'No link'

        event_data = {
            'title': title,
            'date': date,
            'price': price,
            'link': link
        }
        event_list.append(event_data)

    # Format the events as text for recommendations
    events_text = "\n\n".join(
        [f"Событие: {event['title']}\nДата: {event['date']}\nЦена: {event['price']}\nСсылка: {event['link']}" for event in event_list]
    )
    return events_text