'''
Author: Ari Wisenburn
Date: Feb 06, 2023
'''

from pydub import AudioSegment
from pydub.playback import play

import requests
import time
from bs4 import BeautifulSoup  # can only use for static page scraping of DOMs.
# This is a dynamic site, so we need some way to execute JS:
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# constants
URL = 'https://www.vivino.com/explore?e' \
      '=eJzLLbI11rNQy83MszVVy02ssDUxUEuutA0NVksGEi5qBbaGaulptmWJRZmpJYk5avlFKbYpqcXJavlJlbZFiSWZeenF8YllqUWJ6alq5SXRsUD1YMoIQhlDKBMIZQ6VM1Erts2rBADymCky '
base_url = 'https://www.vivino.com'
driver = webdriver.Firefox( '../FlavorSiteScraper/' )


def find_page( url, t = 0.1 ):
    driver.get( url )
    # TODO: print console loading bar here, that'd be cute
    time.sleep( t )
    return driver.page_source


''' Get list of links, where each link redirects to the page for an individual wine '''
def make_list_of_links():
    # first: get list from file
    # file will be read as string
    file = open( './all_links.html' )
    anchor_data = file.read()[ 1:-1 ]  # remove [] around file content
    anchors = [ ]
    index = anchor_data.find( '</a>, <a' )
    while index != -1:
        anchors.append( anchor_data[ anchor_data.find( '<a' ):index + 4 ] )
        anchor_data = anchor_data[ index + 6: ]
        index = anchor_data.find( '</a>, <a' )
    
    anchors.append( anchor_data )
    
    # now we have a list of anchors that we can parse
    # get href from anchor
    # Winery: div, class='wineInfoVintage__truncate--3QAtw'
    # Wine: div, class='wineInfoVintage__vintage--VvWlU wineInfoVintage__truncate--3QAtw'
    # Region: div, class='wineInfoLocation__regionAndCountry--1nEJz'
    links = [ ]
    for anchor in anchors:
        anchor_soup = BeautifulSoup( anchor, 'html.parser' ).find( 'a' )
        links.append( base_url + anchor_soup[ 'href' ] )
        
    return links


''' Getting the list of wine anchors


def make_list_of_wine_anchors():
    # first, find the page initially, and use that to determine how many wines there are
    soup = BeautifulSoup( find_page( URL, 6 ), 'html.parser' )
    number_of_wines = get_number_of_wines( soup )
    
    # then, keep on scrolling down, waiting, and then getting the link until we have that many wines
    js = driver
    all_links = soup.find_all( 'a', { 'class': 'anchor_anchor__m8Qi- wineCard__cardLink--3F_uB' } )
    print_wine_list_percentage( all_links, number_of_wines )
    last_len = len( all_links )
    
    # while we haven't reached the bottom of the wine list...
    count = 0
    while len( all_links ) < number_of_wines:
        # scroll down and re-get the html from the page
        js.execute_script( "window.scrollTo(0,document.body.scrollHeight)" )
        time.sleep( 8 )
        soup = BeautifulSoup( driver.page_source, 'html.parser' )
        all_links = soup.find_all( 'a', { 'class': 'anchor_anchor__m8Qi- wineCard__cardLink--3F_uB' } )
        print_wine_list_percentage( all_links, number_of_wines )
        
        # if the page gets stuck on one percentage, scroll up a bit and try again
        # if it's stuck for more than 5 rounds, ding me so I can manually click and scroll up
        # (this only happened twice in 11,350 wines)
        if last_len == len( all_links ):
            element = driver.find_element( By.XPATH, '//html' )
            print( element )
            js.execute_script( "window.scrollTo(0,0)" )
            time.sleep( 1 )
            count += 1
            if count > 5:
                play( song )
                print( "I need your attention!!" )
        else:
            count = 0
        
        # write links to file
        f = open( 'all_links.html', 'w' )
        f.write( str( all_links ) )
        f.close()
        
        last_len = len( all_links )


def get_number_of_wines( soup ):
    h2 = soup.find( 'h2', { 'class': 'querySummary__querySummary--39WP2' } )
    return int( h2.text.strip().split( ' ' )[ 1 ] )


def scroll_down( self ):
    """A method for scrolling the page."""
    
    # Get scroll height.
    last_height = self.driver.execute_script( "return document.body.scrollHeight" )
    
    while True:
        
        # Scroll down to the bottom.
        self.driver.execute_script( "window.scrollTo(0, document.body.scrollHeight);" )
        
        # Wait to load the page.
        time.sleep( 2 )
        
        # Calculate new scroll height and compare with last scroll height.
        new_height = self.driver.execute_script( "return document.body.scrollHeight" )
        
        if new_height == last_height:
            break
        
        last_height = new_height


# print percentage of how far through making the list of wine anchors we are
def print_wine_list_percentage( all_links, number_of_wines ):
    print( "{:.2f}".format( 100 * len( all_links ) / number_of_wines ) + '%' + ' (' + str(
        len( all_links ) ) + '/' + str( number_of_wines ) + ')' )
'''


def main():
    links = make_list_of_links()


main()
