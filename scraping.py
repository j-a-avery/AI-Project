#!/usr/bin/python3

import os, time, requests, re, random

from bs4 import BeautifulSoup

from PCPartPicker_API import pcpartpicker as pcpp

import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from typing import NewType, Optional, Set, Any, Tuple, List
PartId = NewType('PartId', str)



def download_html(product_id: PartId) -> Optional[BeautifulSoup]:
    """
    Downloads (or attempts to download) the text of a webpage
    Returns a BeautifulSoup object if successful, or None
    """
    
    url = f"https://pcpartpicker.com/product/{product_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
                      'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
        'Accept': 'text/html,application/xhtml+xml,application/xml;'
                  'q=0.9,image/webp,*/*;q=0.8'
    }
    
    connected = False
    tries = 10
    
    while not connected:
        try:
            response = requests.get(url, headers=headers)
            connected = True
        except ConnectionError:
            tries -= 1
            if tries == 0:
                print("Unable to connect, and out of retries.")
                return None
            print("Unable to connect. Trying again in 10 seconds.")
            time.sleep(10)
    return BeautifulSoup(response.text, 'lxml')



def download_part_specs(part_id: PartId) -> Set[Tuple[str, Any]]:
    """
    Each specification is listed in <div class="... group--spec">.
    Download these specs, and parse them into a set.
    
    Specs will be different for each part type,
    and values will need some post-processing,
    but this works as a base for all part types.
    """
    soup = download_html(part_id)
    specs = soup.find_all('div', {'class': 'group--spec'})
    specvals = dict()
    
    # Clean up specs
    for spec in specs:
        specname = re.sub('#', 'Number', spec.h3.text)
        specval = spec.div.p
        
        # Replace <br>'s with \n and turn them into commas
        while specval.find('br'):
            specval.br.replace_with('\n')
        specval = specval.text.strip()
        # Geting rid of "\n(or)" has to be done before replacing \n with comma
        specval = re.sub('\\n\(or\) ', ' / ', specval)
        specval = ', '.join(specval.split('\n'))
        
        # Replace Yes and No with Booleans
        # If there's a second part (e.g.: "Yes: Hyperthreading"),
        # split it into two specs
        if ('Yes' in specval or 'No' in specval) and ':' in specval:
            specval = specval.split(':')
            specval[0] = True if 'Yes' else False
            
            specvals[specname] = specval[0]
            specval = ' '.join(specval[1:]).strip()
            specname = specname + " Detail"
        elif specval == "Yes":
            specval = True
        elif specval == "No":
            specval = False
        
        specvals[specname] = specval
        
    return specvals



def download_part_ids_list(part_type: str) -> List[PartId]:
    """
        On April 26, 2019, four days before this project is due,
        pcpartpicker.com went down for maintenance,
        and when it came back up, it had a new site design
        that is incompatible with the old API,
        because it uses JavaScript to render certain page elements.
        
        This updated function uses selenium to load pages via Chrome,
        and scrapes the data after it's been loaded.
    """
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(
        executable_path = './chromedriver',
        options = chrome_options)
    
    # Get number of pages to scrape.
    # The old API still works for this
    # (...for now...)
    num_pages = pcpp.productLists.getListInfo('cpu')['pageCount']
    
    # Scrape the pages into a list of product IDs
    # to be downloaded by another function
    product_ids = set()
    for page in range(1, num_pages+1):
        time.sleep(3) # be polite (but not too polite, otherwise this will take all day)
        url = f"https://pcpartpicker.com/products/{part_type}/#page={page}"
        driver.get(url)
        
        successful = False
        tries = 0
        while not successful and tries < 10:
            try:
                tries += 1
                WebDriverWait(driver, 15).until(
                    EC.presence_of_all_elements_located(
                        (By.CLASS_NAME, 'td__name')))
                successful = True
            except:
                print("Something went wrong. Trying again in 30 seconds.")
                time.sleep(30)
                successful = False
            finally:
                if not successful and tries >= 10:
                    print(f"Tried {tries} times without success. Giving up now.")

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        product_rows = soup.find('table', {
            'class': 'productList--detailed'
        }).find_all('tr')

        for row in product_rows:
            # Somehow the wrong kind of tr got through. Ignore it
            if not row.find('td', {'class': 'td__name'}):
                continue
            # Old products don't have prices. Ignore them.
            if row.find('td', {'class': 'td__price'}).text.strip() == "":
                continue
            try:
                a = row.find('td', {'class': 'td__name'}).a
                href = a['href']
                url_parts = href.split('/')

                if 'product' in url_parts:
                    product_ids.add(url_parts[2])
            except Exception as e:
                print(e)
                raise
        
    return list(product_ids)



def download_parts(part_type: str) -> None:
    """
    Download parts list and save to CSV
    """
    
    parts = []
    
    print(f"Downloading {part_type} data.")
    
    part_ids = download_part_ids_list(part_type)
    
    for part in part_ids:
        time.sleep(random.randint(2, 5)) # Be unsuspiciously polite
        part_specs = download_part_specs(part)
        try:
            part_specs['Part Number']
            parts.append(part_specs)
            print(part_specs['Part Number'], end=', ', flush=True)
        except KeyError:
            print()
            print(f"Error downloading {part}. Received: ", part_specs)
    print("Done!")
    
    # Save to CSV, but make Pandas do all the heavy lifting
    df = pd.DataFrame(parts)
    filename = f"{part_type}.csv"
    df.to_csv(filename)
    print(f"Saved {filename}")
    sleeptime = random.randint(55, 65)
    print(f"Being polite. Waiting {sleeptime} seconds before scraping the next part.")
    time.sleep(sleeptime)



if __name__ == "__main__":
    download_parts('cpu')
    download_parts('cpu-cooler')
    download_parts('motherboard')
    download_parts('memory')
    download_parts('internal-hard-drive')
    download_parts('video-card')
    download_parts('power-supply')
    download_parts('case')
