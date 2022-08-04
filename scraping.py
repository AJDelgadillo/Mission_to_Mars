# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# Creating the Scrape All function
def scrape_all():
    # Setting up the executable path
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # Setting up the news title and paragraph variables
    news_title, news_paragraph = mars_news(browser)
    
    # Running the scraping functions and storing results in a dictionary
    data = {
    'news_title': news_title,
    'news_paragraph': news_paragraph,
    'featured_image': featured_image(browser),
    'facts': mars_facts(),
    'hemispheres': hemispheres(browser),
    'last_modified': dt.datetime.now()        
    }
    # Stop webdriver and return data
    browser.quit()
    return data
    
# Creating the mars_news function
def mars_news(browser):

    # Mars nasa news site URL
    url = 'https://redplanetscience.com'
    browser.visit(url)
    
    # Add an optional delay for the loading page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Utilizing the HTML parser and creating soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Try/except block
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use parent element to find first 'a' tag - save as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use parent element to find paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        
    except AttributeError:
        return None, None
    
    return news_title, news_p

# ### Featured images

# Creating the featured_image function
def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the 'Full Image' button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting HTML with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    # Try/except block
    
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
 
    except AttributeError:
        return None
        
    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
       
        
    return img_url

# Creating mars_facts function
def mars_facts():
    # Try/except block
    try:
        # Scrape the Mars facts table and convert into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
       
    except BaseException:
        return None
    
    # Assign dataframe columns and set the index
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert the dataframe back into HTML code
    return df.to_html()

# Creating Mars hemispheres function
def hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.

    html = browser.html
    img_soup = soup(html, 'html.parser')
    images = browser.find_by_css('img.thumb')
    
    for result in images: 
        hemispheres = {}
        
        result.click()
        
        html = browser.html
        img_soup = soup(html, 'html.parser')
        
        url_rel = img_soup.find('a', text='Sample').get('href')
        url = f'{url_rel}'
        title = img_soup.find('h2', class_='title').text

        image = {
            'img_url': url,
            'title': title
        }

        hemispheres.update(image)
        hemisphere_image_urls.append(hemispheres)
        browser.back() 
    # 4. Print the list that holds the dictionary of each image url and title.    
    return hemisphere_image_urls 


if __name__ == '__main__':
    # If running as script, print scraped data
    print(scrape_all())




