from flask import Flask, render_template, redirect, request
import feedparser
import opml
import openai_davinci
import utils
import threading

app = Flask(__name__)


def get_main_outlines_from_chain_feeds():
    # Parse the content using opml package
    outline =  opml.parse('opml/RAW.opml')
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


# Get ouline title from index
def get_main_outline_title(index):
    return list(global_main_outlines.keys())[index]


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

# Define a route for the home page
@app.route('/')
def home():
    main_outlines = []
    for main_outline_title in global_main_outlines:
        main_outlines.append({
            'title': main_outline_title,
        })

    # run background thread to parse all of the feeds using threading
    threading.Thread(target=parse_feeds_background).start()

    # Render a template with the feeds data as context variable
    return render_template('home.html', mainoulines=main_outlines)
    
# router outline
@app.route('/api/mainoutline/<index>', methods = ["GET"])
def mainoutline(index):
    title = get_main_outline_title(int(index) - 1)
    outlines = []
    suboutlines = global_main_outlines[title]
    
    for sub_outline_title in suboutlines:
        outlines.append({
            'title': suboutlines[sub_outline_title].title,
        })
    
    # Render a template with the feeds data as context variable
    return render_template('mainoutline.html', suboutlines_page=outlines)

def get_suboutline(title):
    for main_outline_title in global_main_outlines:
        suboutlines = global_main_outlines[main_outline_title]
        if title in suboutlines:
            return suboutlines[title]
    return None

def check_suboutline(suboutlinetitle):
    for main_outline_title in global_main_outlines:
        suboutlines = global_main_outlines[main_outline_title]
        if suboutlinetitle in suboutlines:
            return True
    return False

@app.route('/api/suboutline', methods = ["GET"])
def suboutline():
    suboutlinetitle = request.args.get('suboutline_title')
    if len(suboutlinetitle) == 0:
        return "failed"
    
    if not check_suboutline(suboutlinetitle):
        return "has not suboutline"
    
    suboutline = get_suboutline(suboutlinetitle);
    
    feed = None
    if not suboutline.xmlUrl in global_feeds_cache:
        print("parseing  xmlUrl: ", suboutline.xmlUrl)
        feed = feedparser.parse(suboutline.xmlUrl)
        print("suboutline parse xmlUrl leave: ",suboutline.xmlUrl)
        global_feeds_cache[suboutline.xmlUrl] = feed
    else:
        feed = global_feeds_cache[suboutline.xmlUrl]
    
    feeds = []
    for entry in feed.entries:
        link = utils.remove_prefix(entry.link, "?source=rss")
        print("entry summary:", entry.summary)
        feeds.append({
            'title': entry.title,
            'link': link,
            'author': entry.author,
            'published': entry.published,
            'summary': entry.summary,
            'content': entry.content,
        })
    
    return render_template('feeds.html', suboutlines_page=feeds)