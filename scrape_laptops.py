# imports
import pandas as pd
import random
import requests
import time
from bs4 import BeautifulSoup

####### scraper

def scrape_website(headers, page_number=1):

    more_pages=True

    # loop until button for more pages is not there anymore
    while more_pages==True:

        url=f"https://www.saturn.de/de/category/laptops-66.html?filter=marketplace:SATURN&page={page_number}"

        # send a GET request to the search result page
        response = requests.get(url,headers=headers)
        if response.status_code!=200:
            raise Exception(f'Request failed with status code {response.status_code}')
            
        # create a BeautifulSoup object from the response
        soup = BeautifulSoup(response.content, 'html.parser')

        # find all laptops that are in the class below
        search_results = soup.find_all(class_='sc-fc180512-0 eelRbG')


        for result in search_results:
            # extract the information from each search result div
            title=result.find("p").text.strip()
            price = result.find('span', {'class': 'sc-e0c7d9f7-0 bPkjPs'}).text
            print(title)
            print(price)
            # append data
            data.append([title,price])

        # check if button for more pages is still on the website
        if soup.select(".cUSFpa > button:nth-child(1)"):
            print("Button found")
            page_number+=1
        else:
            more_pages = False

    results = pd.DataFrame(data, columns=['Title', 'Price'])
    return results


# define header, as in my tests without it my requests are denied
headers = {
    #"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.131 Safari/537.36",
    "User-Agent":"Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.131 Mobile Safari/537.36",
    "Referer":"https://www.mediamarkt.de/de/category/"
}

# set empty var
data=[]

df=scrape_website(headers)

print(df.shape)

df.to_csv("data/scraped_laptops.csv",index=False)