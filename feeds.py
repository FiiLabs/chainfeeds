import feedparser
import opml
from pathlib import Path

def get_main_outlines_from_chain_feeds():
    # Parse the content using opml package
    opml_dir = Path(__file__).parent.resolve() / "opml"
    outline =  opml.parse(opml_dir / "RAW.opml")
    main_outline_dict = {}

    # Loop through each outline element and parse its feed url using feedparser
    for i in range(0, len(outline) - 1):
        # Get the feed url from xmlUrl attribute
        title = outline[i].title
        main_outline_dict[title] = {}
        for j in range(0, len(outline[i]) - 1):
            sub_outline = outline[i][j]
            main_outline_dict[title][sub_outline.title] = sub_outline
    
    return main_outline_dict

global_main_outlines = get_main_outlines_from_chain_feeds()
global_feeds_cache = {}

# feeds parser
def parse_feeds(subOutlines):
    for sub_outline_title in subOutlines:
        xmlUrl = subOutlines[sub_outline_title].xmlUrl
        feed = feedparser.parse(xmlUrl)
        if not xmlUrl in global_feeds_cache:
            global_feeds_cache[xmlUrl] = feed


# define a background thread to parse all of the feeds
def parse_feeds_background():
    for main_outline_title in global_main_outlines:
        suboutlines = global_main_outlines[main_outline_title]
        parse_feeds(suboutlines)   