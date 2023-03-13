import re
import string


def remove_emojis( text ):
    emoji_pattern = re.compile( "["
                                u"\U0001F600-\U0001F64F"  # emoticons
                                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                u"\U00002702-\U000027B0"
                                u"\U000024C2-\U0001F251"
                                u"\U0001F917"
                                "]+", flags = re.UNICODE )
    return emoji_pattern.sub( r'', text )


def remove_punctuation( text ):
    """
    
    :param text: string from which to replace punctionation with ' '
    :return: the string, but with spaces instead of punctuation
    """
    # remove punctuation recognized by string
    for punctuation in string.punctuation:
        text = text.replace( punctuation, ' ' )
    
    # remove hyphen
    text = text.replace( '-', ' ' )
    
    # remove emojis
    text = remove_emojis( text )
    
    return text


"""
MISC
"""


# there's no good list of all updated emoji unicode values in order
def emoji_to_unicode( emoji ):
    return 'U+{:X}'.format( ord( emoji ) )
