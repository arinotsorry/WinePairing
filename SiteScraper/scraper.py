'''
Author: Ari Wisenburn
Date: January 22, 2023
'''

import requests
from bs4 import BeautifulSoup  # can only use for static page scraping of DOMs.
import time

# This is a dynamic site, so we need some way to execute JS:
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# constants
base_url = 'https://www.flavorfox.app'
URL = 'https://www.flavorfox.app/en/flavors'
flavors = [ 'cocktail', 'savory', 'sweet' ]
# initializing the web driver, including the path where the driver is (it's in this directory)
driver = webdriver.Firefox( '.' )


def find_page( url ):
    driver.get( url )
    # TODO: print console loading bar here, that'd be cute
    time.sleep( 0.5 )
    return driver.page_source


def get_food_link_text( link ):
    return link.find( 'div' ).text.strip()


'''
creates dictionary of spices/foods with one link
key-pair: { food : link }
'''


def get_list_of_foods( page_soup ):
    # get all divs
    all_links = page_soup.find_all( 'a' )
    
    # extract flavor and link text from html
    foods = {
        get_food_link_text( link_html ): link_html[ 'href' ] for link_html in all_links if
        'kitchen' in link_html[ 'href' ]
    }
    
    return foods


'''
returns tuple of food, category
'''


def get_flavor_link_text( link ):
    food = link.find( 'div', class_ = 'Card_title__1yJ7t' ).text.strip()
    category = link.find( 'div', class_ = 'Pill_pill__3_rT4 mr-s mt-s' ).text.strip()
    return food, category


'''
returns list of foods that match the initial food as [(food, category), (food, category), ... ]
'''


def get_list_of_matches( page_soup ):
    # TODO: change all_links back
    all_links = page_soup.find_all( 'a' )
    matches = [ ]
    
    for link in all_links:
        href = link[ 'href' ]
        if 'pairings' in href:
            matches.append( get_flavor_link_text( link ) )
    
    return matches


'''
gets flavors for a given food. Returns a tuple of 3 lists: cocktail_link, savory_link, sweet_link, 0 if there isn't one
'''


def get_flavors( food, link ):
    # separate link
    index_of_equals = link.find( '=' )
    base_flavor_link = base_url + link[ 0:index_of_equals + 1 ]
    
    flavor_dictionary = { }
    
    # check if there is a cocktail
    for flavor in flavors:
        flavor_link = base_flavor_link + flavor
        flavor_soup = BeautifulSoup( find_page( flavor_link ), 'html.parser' )
        flavor_headers = flavor_soup.find_all(
            'h2', string = lambda text: 'Flavors matching ' + flavor
        )
        
        if len( flavor_headers ) >= 2:
            flavor_dictionary[ flavor ] = get_list_of_matches( flavor_soup )
        else:
            flavor_dictionary[ flavor ] = None
            
    return flavor_dictionary


def main():
    # get base page:
    base_page_soup = BeautifulSoup( find_page( URL ), 'html.parser' )
    
    foods = get_list_of_foods( base_page_soup )
    
    foods_with_flavors = {
        food: get_flavors(food, foods[ food ]) for food in foods
    }
    
    print(foods_with_flavors)


main()
