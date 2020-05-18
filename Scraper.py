import re
import os
import json
import datetime
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from colorama import Back, Fore, Style, deinit, init

init()

def Check():
    pass

def Scrap():
    pass

os.system("cls")
print(Fore.CYAN + Style.NORMAL)
print("▄▄▄▄· ▄▄▄▄· .▄▄ ·  ▄▄· ▄▄▄   ▄▄▄·  ▄▄▄·▄▄▄ .▄▄▄  ")
print("▐█ ▀█▪▐█ ▀█▪▐█ ▀. ▐█ ▌▪▀▄ █·▐█ ▀█ ▐█ ▄█▀▄.▀·▀▄ █·")
print("▐█▀▀█▄▐█▀▀█▄▄▀▀▀█▄██ ▄▄▐▀▀▄ ▄█▀▀█  ██▀·▐▀▀▪▄▐▀▀▄ ")
print("██▄▪▐███▄▪▐█▐█▄▪▐█▐███▌▐█•█▌▐█ ▪▐▌▐█▪·•▐█▄▄▌▐█•█▌")
print("·▀▀▀▀ ·▀▀▀▀  ▀▀▀▀ ·▀▀▀ .▀  ▀ ▀  ▀ .▀    ▀▀▀ .▀  ▀")
print("-------------------------------------------------")
print(Style.RESET_ALL)

print(Fore.WHITE + Style.NORMAL)
date = input("Date (or any search terms)(MM/DD/YYYY): ")
deep = input("Deep Scraper (more working links, take longer)(y|n): ")
experimental = input("Experimental mode (more links, but some don't work)(y|n): ")

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
scrap_url = f"https://www.google.com/search?q=intext:.bbcollab.com/guest/+{date}&start=0&num=1000&source=lnt&tbas=0&filter=0&sa=X&biw=1920&bih=973"

print(f"\n{Fore.BLACK + Style.BRIGHT}[1/3] {Fore.WHITE + Style.NORMAL}Scraping...         {Fore.BLACK + Style.BRIGHT}(using dork: intext:.bbcollab.com/guest/+{date}){Fore.BLACK + Style.BRIGHT}\n")

response = requests.get(scrap_url, headers=headers)

unchecked = []
checked = []
collabs = []
urls = []

if deep == "y":
    soup = BeautifulSoup(response.text, 'html.parser')
    for g in soup.find_all('div', {'class': 'g'}):
        rc = g.find('div', {'class': 'rc'})
        r = rc.find('div', {'class': 'r'})
        a = r.find('a')
        urls.append(a['href'])
        
    for url in tqdm(urls):
        response = requests.get(url, headers=headers)
        collabs.extend(re.findall(r"(https:\/\/[a-zA-Z\d]{2}.bbcollab.com/guest\/[a-fA-F\d]{32})", response.text))

data = json.dumps(response.text).replace('<em>', '').replace('</em>', '').replace('<span>', '').replace('</span>', '').replace('<wbr>', '')
urls = re.findall(r"(https:\/\/[a-zA-Z\d]{2}.bbcollab.com/guest\/[a-fA-F\d]{32})", data)
urls.extend(collabs)

times = []

for time_ in re.findall(r"([0-9]{2}:[0-9]{2}|[0-9]{1}:[0-9]{2}|[0-9]{2}h[0-9]{2}|[0-9]{1}h[0-9]{2})", data):
    try:
        times.append(datetime.datetime.strptime(time_, "%Hh%M").time())
    except:
        pass

    try:
        times.append(datetime.datetime.strptime(time_, "%H:%M").time())
    except:
        pass

print(f"\nTimespan: {min(times)} - {max(times)}")

print(f"\n{Fore.BLACK + Style.BRIGHT}[2/3]{Fore.WHITE + Style.NORMAL} Checking...         {Fore.BLACK + Style.BRIGHT}({len(urls)} URLs){Fore.BLACK + Style.BRIGHT}\n")

for i in tqdm(range(0, len(urls))):
    unchecked.append(urls[i].replace('bbcollab.com/guest', 'bbcollab.com/collab/api/guest'))
    response = requests.get(unchecked[i], headers=headers)
    status = response.status_code
    if status == 200:
        checked.append(unchecked[i].replace('bbcollab.com/collab/api/guest', 'bbcollab.com/guest'))
    if experimental == "y":
        if status == 403:
            checked.append(unchecked[i].replace('bbcollab.com/collab/api/guest', 'bbcollab.com/guest'))
    else:
        pass

print(f"\n{Fore.BLACK + Style.BRIGHT}[3/3] {Fore.WHITE + Style.NORMAL}Removing dupes...   {Fore.BLACK + Style.BRIGHT}(on {len(checked)} checked URLs)\n")

checked = list(set(checked))

print(f'{Fore.YELLOW + Style.NORMAL}Successfully scraped {len(checked)} bbcollab URLs for {date}\n')

for url in checked:
    print(Fore.GREEN + Style.NORMAL + url + Style.RESET_ALL)

deinit()