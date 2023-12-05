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

                # Split the text on instances of '['
                blocks = description_text.split('[', 1)

                # Process and print each block
                for block in blocks:
                    # Skip empty blocks
                    if not block.strip():
                        continue

                    block_soup = BeautifulSoup(block, 'html.parser')
                    plain_text = block_soup.get_text(separator='\n')  # Create a new line for each <li>

                    print(plain_text.strip()) 
            else:
                print("No description found in the latest entry.")
        else:
            print("No entries found in the RSS feed.")
    else:
        print(f"Failed to fetch the HTML. Status code: {response.status_code}")


url = 'https://raw.githubusercontent.com/IceQ1337/CS-RSS-Feed/master/feeds/updates-feed-en.xml'
get_html_and_parse(url)
