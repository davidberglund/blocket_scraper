#!/usr/bin/env python

import re
import requests

#f = open('butik?cg=7020&c=7021&o=9', 'r+')
#htmlfile = f.read()

#r = requests.get("https://www.blocket.se/hela_sverige/affarsoverlatelser/butik?cg=7020&c=7021&o=1")
#html = str(r.content)

#print (r.content)
#print (r.headers)
#print (r.status_code)

def get_body(htmlfile):
    start_link = htmlfile.find('<body')
    if start_link == -1: 
        return None, 0
    start_quote = htmlfile.find('"', start_link)
    end_quote = htmlfile.find('</body>', start_quote + 1)
    url = htmlfile[start_quote + 1:end_quote]
    return url, end_quote

def get_only_body(htmlfile):
    links = []
    while True:
        url,endpos = get_body(htmlfile)
        if url:
            links.append(url)
            htmlfile = htmlfile[endpos:]
        else:
            break
    return links

#r = requests.get("https://www.blocket.se/hela_sverige/affarsoverlatelser/butik?cg=7020&c=7021&o=1")
#html = str(r.content)

#page = get_only_body(html)
#pageStr = ''.join(page)

def get_next_article(page):
    start_link = page.find("""<article id="item""")
    if start_link == -1: 
        return None, 0
    start_quote = page.find('_', start_link)
    end_quote = page.find('/article>', start_quote + 1)
    url = """<article id="item_"""+page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_articles(page):
    links = []
    while True:
        url,endpos = get_next_article(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def get_next_target(page):
    start_link = page.find("""href=""")
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def get_next_image(page):
    start_link = page.find("""<meta property="og:image""")
    if start_link == -1: 
        return None, 0
    start_quote = page.find('="h', start_link)
    end_quote = page.find('">', start_quote + 1)
    url = page[start_quote + 2:end_quote]
    return url, end_quote

def get_all_images(page):
    links = []
    while True:
        url,endpos = get_next_image(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def images_from_ad(links):
    links = []
    for item in all_links:
        if re.findall(r"\D(\d{8})\D", item):
            #print (item)
            links.append(item)
    for item in links:
        print ("Annons: " + item)
        r = requests.get(item)
        html = str(r.content)
        all_images = str(get_all_images(html))
        print (all_images)


#x = str(9)
#r = requests.get("https://www.blocket.se/hela_sverige/affarsoverlatelser/butik?cg=7020&c=7021&o="+x)
#html = str(r.content)
#page = get_only_body(html)
#pageStr = ''.join(page)
#print (len(pageStr))
#all_articles = str(get_all_articles(pageStr))
#all_links = list(set(get_all_links(all_articles)))
#print (images_from_ad(all_links))


#https://www.blocket.se/hela_sverige?q=&cg=7040&w=3&st=s&c=&ca=11&l=0&md=th&o=2 //inventarier o maskiner
#https://www.blocket.se/stockholm/lokaler_fastigheter?w=3&st=s&ca=11&l=0&md=th&cg=7060&o=2 //lokaler o fastigheter
#https://www.blocket.se/hela_sverige/affarsoverlatelser/butik?cg=7020&c=7021&o= //butiker

y = 0
while True:
    y = y+1
    print (y)
    x = str(y)
    r = requests.get("https://www.blocket.se/stockholm/lokaler_fastigheter?w=3&st=s&ca=11&l=0&md=th&cg=7060&o="+x)    
    html = str(r.content)
    page = get_only_body(html)
    pageStr = ''.join(page)
    if len(pageStr) > 151000:
        all_articles = str(get_all_articles(pageStr))
        all_links = list(set(get_all_links(all_articles)))
        #print (all_links)
        print (images_from_ad(all_links))
    else:
        break
