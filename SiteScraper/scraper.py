"""
Author: Ari WIsenburn
Date: January 22, 2023
"""

import requests
from bs4 import BeautifulSoup  # can only use for static page scraping of DOMs.
# This is a dynamic site, so we need some way to execute JS:
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# constants
base_url = "https://www.flavorfox.app"
URL = "https://www.flavorfox.app/en/flavors"
# initializing the web driver, including the path where the driver is (it's in this directory)
driver = webdriver.Firefox( '.' )


def find_page( url ):
    driver.get( URL )
    # TODO: print console loading bar here, that'd be cute
    time.sleep( 1 )
    return driver.page_source


def main():
    # get base page:
    base_page_soup = BeautifulSoup( find_page( URL ), "html.parser" )
    
    # get all divs
    all_links = base_page_soup.find_all( "a" )
    
    """
    <div>
        <a href="/en/flavors/balsamic?kitchen=savory">
            <div style="display: flex; align-items: center;">
                <div class="Avatar_avatar__2wdyL Avatar_size-m__3y37N mr-s"><img src="/img/64x64/balsamic.jpg" alt="Balsamic vinegar" width="36" height="36"></div>
                Balsamic vinegar
            </div>
        </a>
    </div>
    
    title = (job_element.find( "h2", class_ = "title" )).text.strip()
    """
    
    get_link_text = lambda link: link.find( 'div' ).text.strip()
    
    list_of_links = [
        (get_link_text( link_html ), link_html[ "href" ]) for link_html in all_links if "kitchen" in link_html[ "href" ]
    ]
    
    sweet = {}
    savory = {}
    cocktail = {}
    
    for link in list_of_links:
        print( str( link ) )
        if "cocktail" in link[1]:
            cocktail.update( { link[0] : link[1] } )
        elif "sweet" in link[ 1 ]:
            sweet.update( { link[ 0 ]: link[ 1 ] } )
        elif "savory" in link[ 1 ]:
            savory.update( { link[ 0 ]: link[ 1 ] } )
        

main()
