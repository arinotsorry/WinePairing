'''
Author: Ari Wisenburn
Date: Feb 06, 2023
'''

import json
import time

from bs4 import BeautifulSoup  # can only use for static page scraping of DOMs.
# This is a dynamic site, so we need some way to execute JS:
from selenium import webdriver

# constants
URL = 'https://www.vivino.com/explore?e' \
      '=eJzLLbI11rNQy83MszVVy02ssDUxUEuutA0NVksGEi5qBbaGaulptmWJRZmpJYk5avlFKbYpqcXJavlJlbZFiSWZeenF8YllqUWJ6alq5SXRsUD1YMoIQhlDKBMIZQ6VM1Erts2rBADymCky '
base_url = 'https://www.vivino.com'
driver = webdriver.Firefox( '../FlavorSiteScraper/' )


# find a page given a url
def find_page( url, t = 1 ):
    driver.execute_script( f"location.href='{url}';" )  # changed from driver.get() bc get() times out
    time.sleep( t )
    return driver.page_source


''' Get wine pages given links '''


# main function to get wines
def get_wines( links ):
    start = time.time()
    length = len( links )
    print( 'Length:', length )
    count = 0
    for link in links:
        try:  # if a wine fails for some reason, just skip it
            wine_soup, notes = find_soup_with_notes( link )
            
            # write page's html to file for debugging/general knowledge
            file = open( './wine_page.html', 'w' )
            file.write( str( wine_soup ) )
            file.close()
            
            # add wine's info to json
            interpret_wine_page( wine_soup, count, length, notes, start )
            count += 1
        except:
            print( "Couldn't find wine page :(" )
    
    # remove the last comma in the json file
    with open( '../Database/Wine/wines.json', 'rb+' ) as file:
        file.seek( -2, 2 )  # the second 2 represents enum value for setting the reference point at end of the file
        file.truncate()


# scroll page until we find notes, return the page soup along with parsed list of notes
def find_soup_with_notes( link ):
    js = driver
    
    # get page
    wine_page = find_page( link )
    
    # make soup!
    wine_soup = BeautifulSoup( driver.page_source, 'html.parser' )
    
    # find notes
    keyword_soup = wine_soup.findAll( 'div', { 'class': 'tasteNote__popularKeywords--1gIa2' } )
    category_soup = wine_soup.findAll( 'span', { 'class': 'tasteNote__flavorGroup--1Uaen' } )
    count = 0
    
    while len( keyword_soup ) == 0 and count < 20:
        js.execute_script( "window.scrollBy(0,500)" )
        time.sleep( 1 )
        wine_soup = BeautifulSoup( driver.page_source, 'html.parser' )
        keyword_soup = wine_soup.findAll( 'div', { 'class': 'tasteNote__popularKeywords--1gIa2' } )
        category_soup = wine_soup.findAll( 'span', { 'class': 'tasteNote__flavorGroup--1Uaen' } )
        count += 1
    
    # create notes list
    # create place to store the wine's notes
    notes = [ ]  # ('comma-separated list of food', 'category')
    for i in range( len( keyword_soup ) ):
        keywords = keyword_soup[ i ].text
        if '...' in keywords:
            # if there's a truncated word, find the last comma and remove last item of list
            split_index = keywords.rfind( ',' )
            keywords = keywords[ 0:split_index ]
        
        notes.append( (keywords, category_soup[ i ].text) )
    
    return wine_soup, notes


# parse one wine's page soup and turn it into unfiltered, raw json
def interpret_wine_page( wine_soup, count, length, notes, start ):
    # yuck, wine soup
    # try loop because the information isn't consistent - ideally I would've used a nonrelational db, but we already
    # have the mysql one so we're chugging along and skipping wines we can't do. We do have 11,000 after all...
    # most of the information we'll handle below, but we can get the notes of the wine here.
    try:
        # find what type of wine it is
        type = wine_soup.find( 'a', {
            'class': 'anchor_anchor__m8Qi- breadCrumbs__link--1TY6b', 'data-cy': 'breadcrumb-winetype' } )
        if type:
            type = type.text
        
        # find the block of text with the JSON object
        script_soup = wine_soup.find_all( 'script' )
        text = 'window.__PRELOADED_STATE__.offerPageInformation = '
        text2 = 'window.__PRELOADED_STATE__.vintagePageInformation = '
        
        page_information = ''
        index = 0
        for script in script_soup:
            if text in script.text:
                page_information = script.text
                index = page_information.index( text ) + len( text )
            elif text2 in script.text:
                page_information = script.text
                index = page_information.index( text2 ) + len( text2 )
        
        # get index where our json object begins - the same index where the 'text' in the var above ends
        page_information = page_information[ index: ]
        # now we get the index of the first newline, which only works since we're already looking at the line we
        # want
        index = page_information.index( '\n' )
        page_information = page_information[ :index ]
        
        # remove semicolons
        index = -1 if '};' not in page_information else page_information.index( '};' )
        while index != -1:
            page_information = page_information[ 0:index + 1 ] + page_information[ index + 2: ]
            index = -1 if '};' not in page_information else page_information.index( '};' )
        
        # replace words in the file so they're python-friendly
        page_information = page_information.replace( 'false', '\"False\"' )
        page_information = page_information.replace( 'true', '\"True\"' )
        page_information = page_information.replace( 'null', '\"None\"' )
        
        # convert the string to a json object
        wine_json = populate_wine_json( json.loads( page_information ), notes, type )
        
        # estimate how much time is left
        now = time.time()
        time_str = ''
        if count > 0:
            estimate = (((now - start) / count) * length) - (now - start)  # estimated total time - elapsed time
            hours = int( estimate / 3600 )
            mins = int( (estimate / 60) ) % 60
            time_str = str( hours ) + 'hr ' + "{:02d}".format( mins ) + 'min | '
        
        print( "{:.2f}".format( 100 * count / length ) + '% | ' + time_str + wine_json[ 'general' ][ 'winery' ] + ', ' +
               wine_json[ 'general' ][ 'wine' ] )
        
        write_json_file = open( '../Database/Wine/wines.json', 'a' )
        json.dump( wine_json, write_json_file, indent = 2 )
        write_json_file.write( ',\n' )
        write_json_file.close()
    except Exception as e:
        try:  # stupid little try-except block to print error message nicely
            print( e )
            title = wine_soup.find( 'title' )
            title = title.text
            title = title[ 5: title.index( '|' ) - 1 ]
            print( "Couldn't add", title, "to the database :(" )
        except:
            print( "Couldn't add wine to the database :(" )


# grab desired attributes from unfiltered, raw json for our new shiny wine json object
# returns new wine json object
def populate_wine_json( unfiltered_wine_json, notes, type ):
    image_link = extract_info_from_json( unfiltered_wine_json, [ 'vintage', 'image', 'variations', 'bottle_large' ] )
    return {
        'general': {
            'id'                : extract_info_from_json( unfiltered_wine_json, [ 'vintage', 'id' ] ),
            'id_without_vintage': extract_info_from_json( unfiltered_wine_json, [ 'vintage', 'wine', 'id' ] ),
            'wine'              : extract_info_from_json( unfiltered_wine_json, [ 'vintage', 'wine', 'name' ] ),
            'winery'            : extract_info_from_json( unfiltered_wine_json,
                                                          [ 'vintage', 'wine', 'winery', 'name' ] ),
            'type'              : type,
            'wine_description'  : extract_info_from_json( unfiltered_wine_json, [ 'vintage', 'wine', 'description' ] ),
            'winery_description': extract_info_from_json( unfiltered_wine_json,
                                                          [ 'vintage', 'wine', 'winery', 'description' ] ),
            'grape_list'        : [ grape_obj[ 'name' ] for grape_obj in
                                    unfiltered_wine_json[ 'vintage' ][ 'wine' ][ 'grapes' ] ],
            'region'            : extract_info_from_json( unfiltered_wine_json,
                                                          [ 'vintage', 'wine', 'region', 'name' ] ),
            'country'           : extract_info_from_json( unfiltered_wine_json,
                                                          [ 'vintage', 'wine', 'region', 'country', 'name' ] ),
            'rating'            : extract_info_from_json( unfiltered_wine_json,
                                                          [ 'vintage', 'statistics', 'ratings_average' ] ),
            'price'             : extract_info_from_json( unfiltered_wine_json, [ 'price', 'amount' ] ),
            'image_link'        : str( image_link )[ 2: ] if image_link is not None else None
        },
        'traits' : {
            'id'                 : extract_info_from_json( unfiltered_wine_json, [ 'vintage', 'id' ] ),
            'food_list'          : [ food[ 'name' ] for food in
                                     unfiltered_wine_json[ 'vintage' ][ 'wine' ][ 'foods' ] ],  # id and name
            'alcohol_content'    : extract_info_from_json(
                unfiltered_wine_json, [ 'vintage', 'wine', 'alcohol' ] ),
            'sweetness'          : extract_info_from_json(
                unfiltered_wine_json, [ 'vintage', 'wine', 'sweetness_id' ] ),
            'style_description'  : extract_info_from_json(
                unfiltered_wine_json, [ 'vintage', 'wine', 'style', 'description' ] ),
            'style_blurb'        : extract_info_from_json(
                unfiltered_wine_json, [ 'vintage', 'wine', 'style', 'blurb' ] ),
            'body'               : extract_info_from_json(
                unfiltered_wine_json, [ 'vintage', 'wine', 'style', 'body' ] ),
            'body_description'   : extract_info_from_json(
                unfiltered_wine_json, [ 'vintage', 'wine', 'style', 'body_description' ] ),
            'acidity'            : extract_info_from_json(
                unfiltered_wine_json, [ 'vintage', 'wine', 'style', 'acidity' ] ),
            'acidity_description': extract_info_from_json(
                unfiltered_wine_json, [ 'vintage', 'wine', 'style', 'acidity_description' ] ),
            'oak'                : extract_info_from_json( unfiltered_wine_json, [ 'vintage', 'wine_facts',
                                                                                   'oak_aged' ] ),
            'notes'              : notes if len( notes ) > 0 else None
        }
    }


# extract information from raw json, filling in None when there's no data for an attribute
def extract_info_from_json( unfiltered_wine_json, keys ):
    blob = unfiltered_wine_json
    for key in keys:
        if key in str( blob ):
            blob = blob[ key ]
        else:
            return None
    return blob


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
                print( 'I need your attention!!' )
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


# print percentage of how far through making the list of wine anchors we are
def print_wine_list_percentage( all_links, number_of_wines ):
    print( "{:.2f}".format( 100 * len( all_links ) / number_of_wines ) + '%' + ' (' + str(
        len( all_links ) ) + '/' + str( number_of_wines ) + ')' )
'''


def main():
    write_json_file = open( '../Database/Wine/wines.json', 'w' )
    write_json_file.close()
    
    links = make_list_of_links()
    
    get_wines( links )


main()
