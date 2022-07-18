def scrape_mars():

    # import all necessary libraries
    from splinter import Browser
    from bs4 import BeautifulSoup
    from webdriver_manager.chrome import ChromeDriverManager
    import selenium
    import pandas as pd
    import numpy as np
    import time

    # creating link variables
    NASA_MARS_NEWS_LINK="https://redplanetscience.com"
    JPL_MARS_SPACE_IMAGES="https://spaceimages-mars.com"
    MARS_FACTS="https://galaxyfacts-mars.com/"
    MARS_HEMISPHERE="https://marshemispheres.com/"

    # opening the webscraping tab
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #extracting information from NASA Mars News
    browser.visit(NASA_MARS_NEWS_LINK)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    titles=soup.body.find_all('div',class_="content_title")
    first_title=titles[0].text
    paragraphs=soup.body.find_all('div',class_="article_teaser_body")
    first_paragraph=paragraphs[0].text

    # extravting url from JPL MARS SPACE
    browser.visit(JPL_MARS_SPACE_IMAGES)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_image=soup.body.find('img',class_="headerimage")['src']
    featured_image_url=JPL_MARS_SPACE_IMAGES+"/"+featured_image

    # extracting table from MARS FACTS and then converting into html string
    MARS_FACTS_TABLE = pd.read_html(MARS_FACTS)[0]
    temp_html=MARS_FACTS_TABLE.to_html()
    temp=temp_html.split('class="')
    html_code=temp[0]+' class="table '+temp[1]
    

    # finding all urls
    browser.visit(MARS_HEMISPHERE)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    url_links=list(np.array(soup.body.find_all("a",class_="itemLink"),dtype=object)[[0,2,4,6]])
    # then getting name and url from each page
    name_list=[]
    url_list=[]
    for url in url_links:
        link=f"{MARS_HEMISPHERE}{url['href']}"
        browser.visit(link)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        name_list.append(" ".join(((soup.body.find_all("h2",class_="title")[0].text).split(" "))[0:len((soup.body.find_all("h2",class_="title")[0].text).split(" "))-1]))
        url_list.append(MARS_HEMISPHERE+(soup.body.find("div",class_="downloads").find("li").find("a")['href']))
    #putting data into dictionary
    MARS_HEMISPHERE_DICT=[]
    for name, url in zip(name_list, url_list):
        MARS_HEMISPHERE_DICT.append({"title":name,"img_url":url})

    # closing webscraping program
    browser.quit()



    return [first_title,first_paragraph,featured_image_url,html_code,MARS_HEMISPHERE_DICT]

