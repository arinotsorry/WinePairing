"""
Lazy parser for recipes.
Uses Natural Language Tool Kit
Ideally want to use BERT and some language things one day, but not right now
"""
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import json
import os
from os import listdir

WORDNET_TAGS = {  # 'n, s, a, r, v'
    "NN" : 'n',
    "NNS": 'n',
    "VBZ": 'v',
    "VBP": 'v',
    "VBN": 'v',
    "VBG": 'v',
    "VBD": 'v',
    "VB" : 'v',
    "JJ" : 'a',
    "JJR": 'a',
    "JJS": 'a',
    "RB" : 'r',
}
POS = {
    "NNP" : 'proper noun, singular (sarah)',
    "TO"  : 'infinite marker (to)',
    "VB"  : 'verb (ask)',
    "IN"  : 'preposition/subordinating conjunction',
    "NNS" : 'noun plural (desks)',
    "CC"  : 'coordinating conjunction',
    "CD"  : 'cardinal digit',
    "JJ"  : 'This NLTK POS Tag is an adjective (large)',
    "NN"  : 'noun, singular (cat, tree)',
    "VBP" : 'verb, present tense not 3rd person singular(wrap)',
    "DT"  : 'determiner',
    "RB"  : 'adverb (occasionally, swiftly)',
    "PRP$": 'possessive pronoun (her, his, mine, my, our )',
    "VBZ" : 'verb, present tense with 3rd person singular (bases)',
    "VBN" : 'verb past participle (reunified)',
    "JJS" : 'adjective, superlative (largest)',
    "VBG" : 'verb gerund (judging)',
    "PRP" : 'personal pronoun (hers, herself, him, himself)',
    "MD"  : 'modal (could, will)',
    "VBD" : 'verb past tense (pleaded)',
    "EX"  : 'existential there',
    "WRB" : 'wh- adverb (how)',
    "JJR" : 'adjective, comparative (larger)',
    "WP"  : 'wh- pronoun (who)',
    "RP"  : 'particle (about)',
    "POS" : 'possessive ending (parent\ ‘s)',
    "WDT" : 'wh-determiner (that, what)',
    "PDT" : 'predeterminer (all, both, half)',
    "NNPS": 'proper noun, plural (indians or americans)',
    "FW"  : 'foreign word',
    "RBR" : 'adverb, comparative (greater)',
    "UH"  : 'interjection (goodbye)',
    "RBS" : 'adverb, superlative (biggest)',
}

print( nltk.help )


def main():
    words = { }
    file = open( '../Recipes/Grilled Salmon.txt', 'r' )
    recipes = os.listdir( '../Recipes/' )
    
    for recipe in recipes:
        file = open( '../Recipes/' + recipe, 'r' )
        content = file.read()
        
        # get tokens
        tokens = nltk.word_tokenize( content.lower() )
        
        # remove stopwords from token set
        tokens = [ token for token in tokens if token not in set( stopwords.words( 'english' ) ) ]
        
        # lemmaatization - it sort of works
        lemmatizer = WordNetLemmatizer()
        
        tagged = nltk.pos_tag( tokens )
        print( tagged )
        
        lemmatized_tokens = [ ]
        
        # lemmatize all the words - this is more effective with the POS info along with the word
        for pair in tagged:
            if pair[ 1 ] in WORDNET_TAGS:
                lemmatized_tokens.append( lemmatizer.lemmatize( pair[ 0 ], WORDNET_TAGS[ pair[ 1 ] ] ) )
        
        # tag the lemmatized words
        lemmatized_tagged = nltk.pos_tag( lemmatized_tokens )
        
        # count and sort the lemmatized/tagged tokens
        for pair in lemmatized_tagged:
            if pair[ 1 ] in words:
                if pair[ 0 ] in words[ pair[ 1 ] ]:
                    words[ pair[ 1 ] ][ pair[ 0 ] ] = words[ pair[ 1 ] ][ pair[ 0 ] ] + 1
                else:
                    words[ pair[ 1 ] ][ pair[ 0 ] ] = 1
            else:
                words[ pair[ 1 ] ] = { pair[ 0 ]: 1 }
        
        file2 = open( './pos.json', 'w' )
        words_json = json.dumps( words, indent = 2 )
        file2.write( words_json )


main()
