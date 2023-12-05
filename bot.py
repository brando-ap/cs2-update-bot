import requests
import lxml
from bs4 import BeautifulSoup

def get_html_and_parse(url):
    # Send a GET request to the URL and get the HTML content
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "xml")
        entries = soup.find_all("item")

        if entries:
            latest_entry = entries[0]

            description = latest_entry.find("description")

            if description:
                description_text = description.get_text()

                description_soup = BeautifulSoup(description_text, 'html.parser')

                # Create a new line for each <li>
                plain_text = description_soup.get_text(separator='\n')

                print(plain_text.strip()) 
            else:
                print("No description found in the latest entry.")
        else:
            print("No entries found in the RSS feed.")
    else:
        print(f"Failed to fetch the HTML. Status code: {response.status_code}")


url = 'https://raw.githubusercontent.com/IceQ1337/CS-RSS-Feed/master/feeds/updates-feed-en.xml'
get_html_and_parse(url)
