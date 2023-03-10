import feedparser
from utils.feeds import get_main_outlines_from_chain_feeds
import time
# parsed feeds
global_feeds_cache = {}


# feeds parser
def parse_feeds(subOutlines):
    from model.feeds import Feeds
    from model.database import DataBase

    db = DataBase.instance().db
   

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
                db.session.commit()
            except Exception as e:
                print("database error:", e)
                #db.session.rollback()
                

# define a background thread to parse all of the feeds
def parse_feeds_background():
    main_outlines = get_main_outlines_from_chain_feeds()
    print("parse_feeds_background")
    while True:
        for main_outline_title in main_outlines:
            suboutlines = main_outlines[main_outline_title]
            parse_feeds(suboutlines)
        print("parse_feeds_background sleep 45 minutes") 
        time.sleep(45*60)


def parse_feed(xmlUrl):
    if not xmlUrl in global_feeds_cache:
        global_feeds_cache[xmlUrl] = feedparser.parse(xmlUrl)
    return global_feeds_cache[xmlUrl]