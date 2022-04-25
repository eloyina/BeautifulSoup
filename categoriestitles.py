import requests
import time
import csv
import re

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

def probar():
       
    a=[]
    a_=[]
    # Download and Parse the HTML
    start_url = 'http://books.toscrape.com/index.html'
    category=0
    # Download the HTML from start_url
    downloaded_html = requests.get(start_url)

    # Parse the HTML with BeautifulSoup and create a soup object
    soup = BeautifulSoup(downloaded_html.text, "lxml")

    full_list = soup.select('.side_categories ul li ul li')

    regex = re.compile(r'\n[ ]*')

    book_dict = [{}]
    for element in full_list:
        category+=1
        link_text = element.get_text()
        link_text = regex.sub('', link_text)

        anchor_tag = element.select('a')
        fullbooklink = "http://books.toscrape.com/"+anchor_tag[0]['href']

        if (len(link_text) > 0 or len(fullbooklink) > 0):
           respuesta=[category, link_text]
           a.append(respuesta)
           
    for i in range(len(a)):
        for j in range(len(a[i])):
            o=[a[i][0],a[i][1]]
            a_.append(o)
    return a_
            





def scrape(source_url, soup,category):  # Takes the driver and the subdomain for concats as params
    # Find the elements of the article tag
    books = soup.find_all("article", class_="product_pod")
    a=[]
    
    # Iterate over each book article tag
    filename = ("Books.csv")
    f = open(filename, "w")
    for each_book in books:
        info_url = source_url+"/"+each_book.h3.find("a")["href"]
        #print(info_url)

        title = each_book.h3.find("a")["title"]
        print(title)#,tre[category],category)
        text=[title ]
        f.write(str(text))
       
        rating = each_book.find("p", class_="star-rating")["class"][1]
        # can also be written as : each_book.h3.find("a").get("title")
        price = each_book.find("p", class_="price_color").text.strip().encode(
            "ascii", "ignore").decode("ascii")
        availability = each_book.find(
            "p", class_="instock availability").text.strip()
        
        # Invoke the write_to_csv function
        #write_to_csv([info_url, cover_url, title, rating, price, availability])
    f.close()



def browse_and_scrape(seed_url, page_number=1):
    f = open('eli', 'w')

    # Fetch the URL - We will be using this to append to images and info routes
    url_pat = re.compile(r"(http://.*\.com)")
    source_url = url_pat.search(seed_url).group(0)
    a=[]
   # Page_number from the argument gets formatted in the URL & Fetched
    formatted_url = seed_url.format(str(page_number))
    try:
        html_text = requests.get(formatted_url).text
        # Prepare the soup
        soup = BeautifulSoup(html_text, "html.parser")
        print(f"Now Scraping - {formatted_url}")
        print( page_number)
        # This if clause stops the script when it hits an empty page
        if soup.find("li", class_="next") != None:
            scrape(source_url, soup,page_number)
            
            # Invoke the scrape function
            # Be a responsible citizen by waiting before you hit again
            time.sleep(3)
            page_number+=1
            
            # Recursively invoke the same function with the increment
            browse_and_scrape(seed_url, page_number)
            
        else:
            scrape(source_url, soup)     # The script exits here
            return True
        return True
    except Exception as e:
        return e


if __name__ == "__main__":
   seed_url = "http://books.toscrape.com/catalogue/page-{}.html"
   tre=probar()
   print(tre)
      
   
   print("Web scraping has begun")
   result = browse_and_scrape(seed_url)
   if result == True:
       print("Web scraping is now complete!")
   else:
        print(f"Oops, That doesn't seem right!!! - {result}")
