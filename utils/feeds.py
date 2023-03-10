import feedparser
import opml
from pathlib import Path
import time
import locked_dict.locked_dict as locked_dict



def get_main_outlines_from_chain_feeds():
    # Parse the content using opml package
    opml_dir = Path(__file__).parent.parent.resolve() / "opml"
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





# get all sub outlines
def get_all_sub_outlines():
    sub_outlines = []
    mainoutlines = get_main_outlines_from_chain_feeds()
    for main_outline_title in mainoutlines:
        suboutlines = mainoutlines[main_outline_title]
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




