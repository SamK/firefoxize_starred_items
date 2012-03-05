#!/usr/bin/env python
"""
firefoxize_starred_items.py

Reads a Google "Reader JSON" file exported from Google Reader and
outputs an HTML file suitable for importing into Firefox's 
bookmarks menu. This rescues you if you have been using Google 
Reader Starred Items as a bookmark file for feeds.

See http://googlereader.blogspot.com/2011/10/new-in-reader-fresh-design-and-google.html
and, when logged in, http://www.google.com/reader/settings?display=import

Webpage: http://innocentpastimes.blogspot.com/2011/11/converting-google-reader-starred-items.html
"""

__author__ = "Glyn Webster and Samuel Krieg"

import json, time, codecs
import sys
import os

def get_data(InputFile):
    with codecs.open(InputFile, 'r', encoding='utf-8') as f:
        GooglesItems = json.load(f)['items']
    return GooglesItems

def convert(data, subfolders=True):

    FeedURLs = {}
    FeedItems = {}

    #for item in GooglesItems:
    for item in data:
        feedTitle = item['origin']['title']
        feedUrl = item['origin']['htmlUrl']
        itemDate =  item['published']
        if item.has_key('title'):
            itemTitle = item['title'].split('\n')[0]
        else:
            itemTitle = feedTitle + ', ' +  time.strftime('%x', time.localtime(itemDate))
        if item.has_key('alternate'):
            itemURL = item['alternate'][0]['href']
        elif item.has_key('enclosure'):
            itemURL = item['enclosure'][0]['href']
        else:
            itemURL = feedURL
        FeedURLs[feedTitle] = feedUrl
        feedItems = FeedItems.setdefault(feedTitle, [])
        feedItems.append((itemTitle, itemURL, itemDate))

    t = []
    t.append('''<!DOCTYPE NETSCAPE-Bookmark-file-1>
    <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
    <TITLE>Bookmarks</TITLE>
    <H1>Bookmarks Menu</H1>''')
    t.append('<DL><p>')     # opening 1st definition list
    t.append('<DT><H2>Google Reader Starred Items</H2>')
    t.append('')
    t.append('<DL><p>')     # opening 2nd def. list
    for feedTitle, feedURL in FeedURLs.items():
        if subfolders:
            t.append('<DT><H3>%s</H3>' % feedTitle)
            t.append('<DL><p>')    # opening 3rd def. list
            t.append('<DT><A HREF="%s">(%s)</A>' % (feedURL, feedTitle))
        for (title, url, date) in FeedItems[feedTitle]:
            t.append('  <DT><A HREF="%s" LAST_MODIFIED="%i">%s</A></dt>' % (url, date, title))
        if subfolders:
            t.append('</DL><p>\n') # closing 3rd def. list
    t.append('</DL><p>\n\n')   # closing 2nd def. list
    t.append('</DL>')       # closing 1st def. list
    return t

def write_data(data,filename):
    file = codecs.open(filename, "w", "utf-8")
    for line in data:
        file.write(line)
        file.write('\n')
    file.close()

def parse_arguments(version=None):

    import argparse

    version_string = "%(prog)s-%(version)s" % {"prog": "%(prog)s",
                                               "version": version}

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="verbose output")
    parser.add_argument('-q', '--quiet', action='store_true',
                        help="quiet output")
    parser.add_argument('-V', '--version', action='version',
                        help="shows program version",
                        version=version_string)
    parser.add_argument('-s', '--subfolders', action='store_true',
                        help="Sort items into folders")
    parser.add_argument('-o', '--output', metavar='outfile.html',
                        help="determine output file. default is ./The input JSON filename.html"
                        )
    parser.add_argument('filename', metavar='filename.json', type=str, nargs=1,
                        help='The input JSON filename')
    return parser.parse_args()

if __name__ == '__main__':

    args = parse_arguments()

    # get the data
    try:
        data = get_data(args.filename[0])
    except IOError, err:
        sys.stderr.write("%s\n" % str(err)) 
        sys.exit(1)

    # convert the data
    result = convert(data, args.subfolders)

    # determine output 
    output = args.output
    if output is None:
        output = os.path.basename(args.filename[0]) + ".html"

    #do the output
    write_data(result, output)

