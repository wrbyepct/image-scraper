
from httpx import get
from selectolax.parser import HTMLParser
import os
import logging

logging.basicConfig(
    level= logging.DEBUG,
    format="%(asctime)s- %(levelname)s - %(message)s"
)

def scrape_by_api(query="", number=10):
    
    # Decide how many pages to request
    if number > 0:
        temp = divmod(number, 30)
        remain = temp[1]
        pages = temp[0] + 1 if remain > 0 else temp[0]
               
    else:
        raise ValueError("Request integer should be positive integer")
        
    i = 1
    limit = 30
    for page in range(1, pages + 1):
        ## Unsplash base_url
        ## check for last page
        if page == pages:
            limit = remain
   
        url = 'https://unsplash.com/ngetty/v3/search/images/creative'

        params = {
            'fields': ['display_set', '2Creferral_destinations', '2Ctitle'],
            'page_size': limit,
            'phrase': query,
            'sort_order': 'best_match',
            'graphical_styles': 'photography',
            'page': page
        }

        resp = get(url, params=params)
        ## Check for response
        if resp.status_code != 200:
            raise Exception("Error getting response")

        data = resp.json()

        imgs = data['images']
        high_res_urls = [ img['display_sizes'][6]['uri'] for img in imgs ]

        folder_path = f"{query}-images"
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        for url in high_res_urls:
            resp = get(url)
            logging.info(f"Downloading {url}")
            file_name = f"{folder_path}/{query}-img{i}.jpeg"
            with open(file_name, "wb") as f:
                f.write(resp.content)
                logging.info(f"Saved {file_name} to {folder_path}, with size {round(len(resp.content) / 1024**2, 2)} MB.")

            i += 1