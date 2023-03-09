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
        #print("#######################################################")
        #print("parsing_feed:", xmlUrl)
        feed = feedparser.parse(xmlUrl)
        #kk = xmlUrl
        #print("parsed_feed:", kk)
        #print("#######################################################")
        if not xmlUrl in global_feeds_cache:
            global_feeds_cache[xmlUrl] = feed
        else:
            old_feed = global_feeds_cache[xmlUrl]
            if (len(old_feed.entries) > 0 and len(feed.entries) > 0) and old_feed.entries[0].link != feed.entries[0].link:
                global_feeds_cache[xmlUrl] = feed

        # Write cache to db
       
        entries = global_feeds_cache[xmlUrl].entries
        with db.app.app_context():
            try:
                for entry in entries:
                    published = ""
                    content = ""
                    author = ""
                    summary = ""
                    if hasattr(entry, 'published'):
                        published = entry.published
                    if hasattr(entry, 'content'):
                        content = str(entry.content)
                    if hasattr(entry, 'author'):
                        author  = entry.author
                    if hasattr(entry, 'summary'):
                        summary = entry.summary
                    feed_record = Feeds(xmlUrl.strip(), entry.title.strip(), entry.link.strip(), author.strip(), published.strip(),summary.strip(), content.strip())
                    db.session.add(feed_record)
                    print("add feed_record title:", entry.title)
                db.session.commit()
            except Exception as e:
                print("database error:", e)
                #db.session.rollback()
                

# define a background thread to parse all of the feeds
def parse_feeds_background():
    print("parse_feeds_background")
    while True:
        for main_outline_title in global_main_outlines:
            suboutlines = global_main_outlines[main_outline_title]
            parse_feeds(suboutlines)
        print("parse_feeds_background sleep 45 minutes") 
        time.sleep(45*60)