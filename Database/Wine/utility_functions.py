"""
A kind-of-disconjoint list of utility functions I sometimes use/need on a case-by-case basis. Mostly documentation.
"""


# find max space each wine attribute takes up for table generation
def find_max_value_of_everything_clunky( wines ):
    """
    Brute force, print maximum values stored in each wine's attribute.
    Helps me know how much space to allocate in each table's column
    :param wines: List of JSON wine objects
    :return: nothing, prints max size of various wine JSON attributes
    """
    values = [ 0 ] * 22
    for wine in wines:
        # id
        if not (wine[ 'general' ][ 'id' ] == None or wine[ 'general' ][ 'id' ] == 'None') and wine[ 'general' ][
            'id' ] > values[ 0 ]:
            values[ 0 ] = wine[ 'general' ][ 'id' ]
        # id_without_vintage
        if not (wine[ 'general' ][ 'id_without_vintage' ] == None or wine[ 'general' ][
            'id_without_vintage' ] == 'None') and wine[ 'general' ][ 'id_without_vintage' ] > values[
            1 ]:
            values[ 1 ] = wine[ 'general' ][ 'id_without_vintage' ]
        # wine
        if not (wine[ 'general' ][ 'wine' ] == None or wine[ 'general' ][ 'wine' ] == 'None') and len(
                wine[ 'general' ][ 'wine' ] ) > values[ 2 ]:
            values[ 2 ] = len( wine[ 'general' ][ 'wine' ] )
        # winery
        if not (wine[ 'general' ][ 'winery' ] == None or wine[ 'general' ][ 'winery' ] == 'None') and len(
                wine[ 'general' ][ 'winery' ] ) > values[ 3 ]:
            values[ 3 ] = len( wine[ 'general' ][ 'winery' ] )
        # wine_description
        if not (wine[ 'general' ][ 'wine_description' ] == None or wine[ 'general' ][
            'wine_description' ] == 'None') and len( wine[ 'general' ][ 'wine_description' ] ) > values[
            4 ]:
            values[ 4 ] = len( wine[ 'general' ][ 'wine_description' ] )
        # grape_list
        if not (wine[ 'general' ][ 'grape_list' ] == None or wine[ 'general' ][ 'grape_list' ] == 'None') and len(
                wine[ 'general' ][ 'grape_list' ] ) > values[ 5 ]:
            values[ 5 ] = len( wine[ 'general' ][ 'grape_list' ] )
        # region
        if not (wine[ 'general' ][ 'region' ] == None or wine[ 'general' ][ 'region' ] == 'None') and len(
                wine[ 'general' ][ 'region' ] ) > values[ 6 ]:
            values[ 6 ] = len( wine[ 'general' ][ 'region' ] )
        # country
        if not (wine[ 'general' ][ 'country' ] == None or wine[ 'general' ][ 'country' ] == 'None') and len(
                wine[ 'general' ][ 'country' ] ) > values[ 7 ]:
            values[ 7 ] = len( wine[ 'general' ][ 'country' ] )
        # rating
        if not (wine[ 'general' ][ 'rating' ] == None or wine[ 'general' ][ 'rating' ] == 'None') and wine[ 'general' ][
            'rating' ] > values[ 8 ]:
            values[ 8 ] = wine[ 'general' ][ 'rating' ]
        # price
        if not (wine[ 'general' ][ 'price' ] == None or wine[ 'general' ][ 'price' ] == 'None') and wine[ 'general' ][
            'price' ] > values[ 9 ]:
            values[ 9 ] = wine[ 'general' ][ 'price' ]
        # image_link
        if not (wine[ 'general' ][ 'image_link' ] == None or wine[ 'general' ][ 'image_link' ] == 'None') and len(
                wine[ 'general' ][ 'image_link' ] ) > values[ 10 ]:
            values[ 10 ] = len( wine[ 'general' ][ 'image_link' ] )
        
        # food_list
        if not (wine[ 'traits' ][ 'food_list' ] == None or wine[ 'traits' ][ 'food_list' ] == 'None') and len(
                wine[ 'traits' ][ 'food_list' ] ) > values[ 11 ]:
            values[ 11 ] = len( wine[ 'traits' ][ 'food_list' ] )
        # alcohol_content
        if not (wine[ 'traits' ][ 'alcohol_content' ] == None or wine[ 'traits' ][ 'alcohol_content' ] == 'None') and \
                wine[ 'traits' ][ 'alcohol_content' ] > values[ 12 ]:
            values[ 12 ] = wine[ 'traits' ][ 'alcohol_content' ]
        # sweetness
        if not (wine[ 'traits' ][ 'sweetness' ] == None or wine[ 'traits' ][ 'sweetness' ] == 'None') and \
                wine[ 'traits' ][ 'sweetness' ] > values[ 13 ]:
            values[ 13 ] = wine[ 'traits' ][ 'sweetness' ]
        # style_description
        if not (wine[ 'traits' ][ 'style_description' ] == None or wine[ 'traits' ][
            'style_description' ] == 'None') and len( wine[ 'traits' ][ 'style_description' ] ) > values[
            14 ]:
            values[ 14 ] = len( wine[ 'traits' ][ 'style_description' ] )
        # style_blurb
        if not (wine[ 'traits' ][ 'style_description' ] == None or wine[ 'traits' ][
            'style_description' ] == 'None') and len( wine[ 'traits' ][ 'style_description' ] ) > values[
            15 ]:
            values[ 15 ] = len( wine[ 'traits' ][ 'style_description' ] )
        # body
        if not (wine[ 'traits' ][ 'body' ] == None or wine[ 'traits' ][ 'body' ] == 'None') and wine[ 'traits' ][
            'body' ] > values[ 16 ]:
            values[ 16 ] = wine[ 'traits' ][ 'body' ]
        # body_description
        if not (wine[ 'traits' ][ 'body_description' ] == None or wine[ 'traits' ][
            'body_description' ] == 'None') and len(
            wine[ 'traits' ][ 'body_description' ] ) > values[
            17 ]:
            values[ 17 ] = len( wine[ 'traits' ][ 'body_description' ] )
        # acidity
        if not (wine[ 'traits' ][ 'acidity' ] == None or wine[ 'traits' ][ 'acidity' ] == 'None') and wine[ 'traits' ][
            'acidity' ] > values[ 18 ]:
            values[ 18 ] = wine[ 'traits' ][ 'acidity' ]
        # acidity_description
        if not (wine[ 'traits' ][ 'acidity_description' ] == None or wine[ 'traits' ][
            'acidity_description' ] == 'None') and len( wine[ 'traits' ][ 'acidity_description' ] ) > \
                values[ 19 ]:
            values[ 19 ] = len( wine[ 'traits' ][ 'acidity_description' ] )
        # oak
        if not (wine[ 'traits' ][ 'oak' ] == None or wine[ 'traits' ][ 'oak' ] == 'None') and wine[ 'traits' ][
            'oak' ] > \
                values[ 20 ]:
            values[ 20 ] = wine[ 'traits' ][ 'oak' ]
        # notes
        if not (wine[ 'traits' ][ 'notes' ] == None or wine[ 'traits' ][ 'notes' ] == 'None') and len(
                wine[ 'traits' ][ 'notes' ] ) > values[ 21 ]:
            values[ 21 ] = len( wine[ 'traits' ][ 'notes' ] )
    
    print( values )


"""
Max values for everything:
"""
# num of wines: 9238
# Max value/length for:
# id: 172831218
# id_without_vintage: 11062103
# wine: 69
# winery: 51
# wine_description: 1137
# winery_description: 3723
# grape_list: 9 (individual len max: 23? 28? I forget)
# region: 43
# country: 31
# rating: 4.6
# price: 54.99
# image_link: 59

# food_list: 11
# alcohol_content: 20
# sweetness: 8
# style_description: 1490
# style_blurb: 1490
# body: 5
# body_description: 17
# acidity: 3
# acidity_description: 6
# oak: 120
# notes: 13
