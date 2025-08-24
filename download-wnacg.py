import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys
import os
import subprocess

map_img_url = {}

def download_image(url):
    print("Download file: " + url)
    # Extract the filename from the URL
    filename = os.path.basename(url)

    # Download and save
    response = requests.get(url)
    while response.status_code != 200:
        # Retry
        response = requests.get(url)
    
    with open(filename, "wb") as f:
        f.write(response.content)

def claim_image(url):
    response = requests.get(url)
    while response.status_code != 200:
        response = requests.get(url)
        
    soup = BeautifulSoup(response.content, "html.parser")

    img_tags = soup.find_all("img")
    img_links = [urljoin(url, img.get("src")) for img in img_tags if img.get("src")]

    # Print them
    for img_link in img_links:
        if "qy0" in img_link:
            if img_link not in map_img_url:
                map_img_url[img_link] = ""
                download_image(img_link)

def claim_url(url):
    # Fetch the page
    response = requests.get(url)
    while response.status_code != 200:
        response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    # Extract all hrefs
    hrefs = [a.get("href") for a in soup.find_all("a") if a.get("href")]

    # Print them
    for link in hrefs:
        if "photos-view-id" in link:
            sub_url = "https://www.wnacg.com/"+str(link)
            claim_image(sub_url)

def main():
    # Get URL by download-wnacg.py [url]
    url = sys.argv[1]
    number_page = int(sys.argv[2])
    print("Get URL: " + url)

    for i in range(1, number_page+1):
        new_url = url.replace("-aid-", "-page-" + str(i) + "-aid-")
        print("--> " + new_url)
        claim_url(new_url)

main()