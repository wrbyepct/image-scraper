from selectolax.parser import HTMLParser
import requests as r
from dotenv import load_dotenv, find_dotenv
import os
_ = load_dotenv(find_dotenv())
API_KEY = os.environ.get('UNSPLASH_API_KEY')
API_KEY


def search_image_web(key="", number=0):
    ## Web side apprach
    url = "https://unsplash.com/s/photos/"
    resp = r.get(url + key)
    tree = HTMLParser(resp.content)
    imgs = tree.css('img[data-test*=photo-grid-masonry-img]:not([src^="https://plus"])')
    if number != 0:
        imgs = imgs[:number]
    
    return imgs


def scrape_images(imgs, number=0):
    imgs = search_image_web(imgs)
    
    for n, img in enumerate(imgs, start=1):
        img_url = img.attributes.get('src')
        img_resp = r.get(img_url)
        
        with open(f'images/img{n}.jpeg', 'wb') as f:
            f.write(img_resp.content)


def scrap_image_by_api(query="", number=10):
    
    # Decide how many pages to request
    if number > 0:
        temp = divmod(number, 30)
        remain = temp[1]
        pages = temp[0] + 1 if remain > 0 else temp[0]
               
    else:
        raise ValueError("Request integer should be positive integer")
    
    
    url = "https://api.unsplash.com/search/photos"
    
    if query == "":
        url = f"https://api.unsplash.com/photos"

    img_index = 1 
    limit = 30
    for page in range(1, pages + 1):
        ## Unsplash base_url
        ## check for last page
        if page == pages:
            limit = remain
            
        url = url
        params = {
            'query': query,
            'client_id': API_KEY,
            'per_page': limit,
            'page': page
        }
        
        # Request one page 
        data = r.get(url, params=params).json()
        imgs = data['results'] if query != "" else data
        
        for img in imgs:
            img_url = img['urls']['raw']
            img_resp = r.get(img_url)
            with open(f'images/img{img_index}.jpeg', 'wb') as f:
                f.write(img_resp.content)
            img_index += 1 


if __name__ == '__main__':
    scrap_image_by_api(number=2)

        