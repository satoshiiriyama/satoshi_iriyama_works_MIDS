def scrape():

    # coding: utf-8

    # In[1]:


    # Dependencies
    from bs4 import BeautifulSoup
    import requests
    from splinter import Browser
    import pandas as pd
    import time


    # In[2]:


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[3]:


    # Getting NASA Mars News

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Retrieve page
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # In[4]:


    # get 1st HTML results of "li" and "slide" class
    result = soup.find('li', class_='slide')


    # In[5]:


    # get News Title 
    news_title = result.find('div', class_='content_title').text
    news_title


    # In[6]:


    # get News paragragh text of 1st article
    news_p = result.find('div', class_='article_teaser_body').text
    news_p


    # In[7]:


    # Getting JPL Mars Space Images - Featured Image

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # visit the page
    browser.visit(url)

    # click "FULL IMAGE"
    browser.click_link_by_partial_text('FULL IMAGE')

    # wait for 1 second
    time.sleep(1)

    # click "more info"
    browser.click_link_by_partial_text('more info')

    # Retrieve page
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # In[8]:


    # Getting image url element
    featured_image_url_element = soup.find('figure', class_='lede').a['href']
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image_url_element
    featured_image_url


    # In[9]:


    # Getting Mars Weather

    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')


    # In[10]:


    tweets = soup.find_all('div', class_='tweet')

    weather_list = []

    for tweet in tweets:
        if "Sol" in tweet.p.text and "high" in tweet.p.text and "low" in tweet.p.text and "pressure" in tweet.p.text and "daylight" in tweet.p.text :
            weather_list.append(tweet.p.text)
            
    mars_weather = weather_list[0]


    # In[11]:


    mars_weather


    # In[12]:


    # Getting Mars Facts
    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(url)
    tables


    # In[13]:


    mars_df = tables[0]
    mars_df.columns = ['Description', 'Value']
    mars_df.set_index('Description', inplace=True)
    mars_df


    # In[35]:


    # Converting HTML
    html_table = mars_df.to_html().replace('\n', '')
    html_table


    # In[17]:


    # Getting Mars Hemispheres

    # Main page URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    # Making product links
    products = soup.find_all('div', class_='item')

    product_links = []

    for product in products:
        link_element = product.a['href']
        link = 'https://astrogeology.usgs.gov' + link_element
        product_links.append(link)

    product_links


    # In[33]:


    # Empty List to collect information from 4 products
    hemisphere_image_urls = []

    # Scraping Title and Image link in each product link
    for product_link in product_links:
        url = product_link
        
        # Retrieve page with the requests module
        response = requests.get(url)
        
        # Create BeautifulSoup object; parse with 'html.parser'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Getting Title
        title = soup.find('h2').text
        
        # Getting the Link of full resolution image
        image_link = soup.find('div', class_='downloads').find_all('a')[1]['href']

        # Getting the Link of jpg image
        jpg_image_link = soup.find('div', class_='downloads').find_all('a')[0]['href']
        
        # Making dictionary
        product_dic =  {"title": title, "img_url": image_link, "jpg_img_url": jpg_image_link}
        
        # Add the dictionary to list
        hemisphere_image_urls.append(product_dic)
        
    hemisphere_image_urls


    scraped_data = {"news_title": news_title,
                    "news_p": news_p,
                    "featured_image": featured_image_url,
                    "mars_weather": mars_weather,
                    "mars_fact_html": html_table,
                    "hemispheres": hemisphere_image_urls}

    return scraped_data


