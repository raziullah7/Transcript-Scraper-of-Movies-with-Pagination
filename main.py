import requests
from bs4 import BeautifulSoup
import time
import urllib.request
import urllib.error

# getting the soup
root = "https://subslikescript.com"
website = f"{root}/movies_letter-A"

result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, "lxml")

# handling pagination
pagination = soup.find("ul", class_="pagination")
pages = pagination.find_all("li", class_="page-item")
last_page = pages[-2].text

# getting each page in pagination
# range(1, i]
links = []
count = 1
for page in range(1, int(last_page) + 1)[:2]:
    result = requests.get(f"{website}?page={page}")
    content = result.text
    soup = BeautifulSoup(content, "lxml")

    box = soup.find("article", class_="main-article")

    for link in box.find_all("a", href=True):
        links.append(link["href"])

    for link in links:
        try:
            print(f"{count}. {link}")
            count += 1

            result = requests.get(f"{root}/{link}")
            content = result.text
            soup = BeautifulSoup(content, "lxml")

            box = soup.find("article", class_="main-article")
            title = box.find("h1").get_text()
            transcript = box.find("div", class_="full-script").get_text(strip=True, separator=" ")

            print(f"TITLE: {title}\nTRANSCRIPT: \n{transcript}\n--------------------------------------------------")

            # with open(f"{title}.txt", "w") as file:
            #     file.write(transcript)
        except:
            # continue to next iteration
            print("---------- Link Not Found ----------")
