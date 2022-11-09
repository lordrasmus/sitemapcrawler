#!/usr/bin/python

import os
import sys
import requests

from bs4 import BeautifulSoup
from threading import Lock

import xml.dom.minidom as dom

from pprint import pprint

from multiprocessing import Pool

crawl_urls = []

def parse_sitemap( myURL ):
        global crawl_urls
        
        print( "parse : " + myURL )

        page = requests.get( myURL )
        soup = BeautifulSoup(page.content, 'xml')
        

        sitemaps = soup.find_all('sitemap')

        for m in sitemaps:
                locs = m.find_all("loc")
                
                for loc in locs:
                        parse_sitemap( loc.get_text() )
                        pass
                        
        
        
        urlset = soup.find_all("urlset")
        
        if len( urlset ) == 0 : return
        
        urls = urlset[0].findChildren()
        for url in urls:
                
                #pprint( url.name )
                #pprint( url.namespace )
                
                childs = url.findChildren();
                
                
                for c in childs:
                
                        if not c.name == "loc": continue
                        
                        if "sitemap-image" in c.namespace: continue
                        
                
                        #pprint( dir( c ) )
                        #print("-----------------")
                        #pprint( c.name )
                        #pprint( c.namespace )
                        #pprint( c.get_text() )
                
                        currentURL = c.get_text()
                        
                        if '.pdf' in currentURL: continue
                        
                        crawl_urls.append( currentURL )


lock = Lock()
crawled = 0        

def load( info ):
        global crawled, lock
        
        #pprint( info )
        
        with lock:
                #sys.stdout.write("\33[2K\r  {0} / {1}   url : {2}".format( info["idx"], info["total"], info["url"][:80] ) )
                sys.stdout.write("\33[2K\r  {0} / {1}   url : {2}".format( crawled, info["total"], info["url"][:80] ) )
                crawled+=1
        
        headers = {
                'User-Agent': info["agent"]
        }
        
        try:
                response = requests.get(info["url"],  headers=headers, timeout=10)
                if "x-litespeed-cache" in response.headers:
                        if not response.headers["x-litespeed-cache"] == "hit":
                                print("\n      caching startet") 
                #pprint( response )
                #pprint( response.headers )
                #exit(1)
        except Exception as e:
                print("\n        except url : " + info["url"] )
                print("         " + str( e ) )
        
        
def crawl( crawl_urls , agents ):                      
        
        print( "url   count : " + str( len ( crawl_urls ) ) )
        print( "agent count : " + str( len ( agents ) ) )
        
        liste = []
        
        idx = 0
        
        for agent in agents:
                for url in crawl_urls :
                        liste.append( { "idx": idx, "total": len ( crawl_urls ) * len( agents) , "url": url, "agent": agent } )
                        idx += 1
        
        print("liste : " + str( len( liste ) ) )
        #with Pool(3) as p:
                #print(p.map(load, [1, 2, 3]))
        #        p.map(load, liste)
        
        for l in liste:
                load( l )
        
        print("")

agents = []
agents.append( "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36" )
agents.append( "Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.109 Safari/537.36 CrKey/1.54.248666" )
agents.append( "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36" )
agents.append( "Mozilla/5.0 (Linux; Android 7.0; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4695.0 Mobile Safari/537.36 Chrome-Lighthouse" )
agents.append( "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36" )
agents.append( "Mozilla/5.0 (Linux; Android 11.0; Surface Duo) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36" )
agents.append( "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4695.0 Safari/537.36 Chrome-Lighthouse" )
agents.append( "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1" )
agents.append( "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1" )
agents.append( "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1" )
agents.append( "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1" )
agents.append( "lscache_runner Mobile iPhone")
agents.append( "lscache_runner" )



parse_sitemap( "https://casadentalis.tangotanzen.de/sitemap_index.xml" )

parse_sitemap( "https://www.tangotanzen.de/sitemap_index.xml" )

crawl( crawl_urls,  agents )

#exit(0)


