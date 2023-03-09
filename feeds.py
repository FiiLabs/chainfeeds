import feedparser
import opml
from pathlib import Path
import time
import locked_dict.locked_dict as locked_dict

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

# parsed feeds
global_feeds_cache = {}

d = locked_dict.LockedDict()

# get all sub outlines
def get_all_sub_outlines():
    sub_outlines = []
    for main_outline_title in global_main_outlines:
        suboutlines = global_main_outlines[main_outline_title]
        for sub_outline_title in suboutlines:
           sub_outlines.append(suboutlines[sub_outline_title])
    return sub_outlines

def gen_all_suboutlines_cache():
    r = {}
    suboutlines = get_all_sub_outlines()
    for sub_outline in suboutlines:
        xmlUrl = sub_outline.xmlUrl
        r[xmlUrl] = sub_outline
    return r

# not parsed suboutlines
global_suboutlines_cache = gen_all_suboutlines_cache()


def parse_feed(xmlUrl):
    if not xmlUrl in global_feeds_cache:
        global_feeds_cache[xmlUrl] = feedparser.parse(xmlUrl)
    return global_feeds_cache[xmlUrl]

# feeds parser
def parse_feeds(subOutlines):
    from app import db, Feeds
   

    for sub_outline_title in subOutlines:
        xmlUrl = subOutlines[sub_outline_title].xmlUrl
        print("parsing_feed:", xmlUrl)
        feed = feedparser.parse(xmlUrl)
        print("parsed_feed:", xmlUrl)
        if not xmlUrl in global_feeds_cache:
            global_feeds_cache[xmlUrl] = feed
        else:
            old_feed = global_feeds_cache[xmlUrl]
            if (len(old_feed.entries) > 0 and len(feed.entries) > 0) and old_feed.entries[0].link != feed.entries[0].link:
                global_feeds_cache[xmlUrl] = feed

        # Write cache to db
        print("write cache to db")
       
        entries = global_feeds_cache[xmlUrl].entries
        for entry in entries:
            with db.app.app_context():
                feed_record = Feeds(xmlUrl, entry.title, entry.link, entry.author, entry.published, entry.summary, entry.content)
                db.session.add(feed_record)
                db.session.commit()
                print("write feed entry to db:", entry.title)
                print("write feed to db:", xmlUrl)

# define a background thread to parse all of the feeds
def parse_feeds_background():
    print("parse_feeds_background")
   # while True:
    for main_outline_title in global_main_outlines:
        suboutlines = global_main_outlines[main_outline_title]
        parse_feeds(suboutlines)   
       # time.sleep(5*60)