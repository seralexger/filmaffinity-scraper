# -*- encoding: utf-8 -*-

#########################################################
#
# Alejandro German
# 
# https://github.com/seralexger/filmaffinity-scraper
#
#########################################################

import workerpool
import requests
import json
import random
import glob
import re
from scraper.filmaffinity import Filmaffinity
from proxy_manager.proxyManager import ProxyManager


PROXY_MANAGER = ProxyManager()
MOVIES_SAFE = []
for path in glob.glob("data/movies/*"):
    MOVIES_SAFE.append(int(re.sub('[^0-9]','', path)))


class URLObject(object):
    def __init__(self,id,url,proxy):
        self.id = str(id)
        self.url = url
        self.proxy = proxy

class ScrapParallel(object):
    
    def __init__(self, max_pool_size,destination_path, scraper):

        self.max_pool_size = max_pool_size
        self.destination_path = destination_path
        self.scraper = scraper

    def is_url(self, url):

        return url is not None and url != ""


    def scrap_web(self,urlObj):

        if self.is_url(urlObj.url):
            try:
                movie_info = self.scraper.scrap_movie_web(urlObj.url, "en", urlObj.proxy)
                if movie_info != None:
                    with open("data/movies/"+ str(urlObj.id) + '.json', 'w') as fp:
                        json.dump(movie_info, fp, indent = 4)
                else:
                    return None
            except Exception as e:
                return None
        else:
            return None


    def scrap_batch(self, urlObjects):
        pool = workerpool.WorkerPool(min(self.max_pool_size, len(urlObjects)))
        pool.map(self.scrap_web, urlObjects)
        pool.shutdown()
        pool.wait()
        print("Count of url send to scrap "+str(len(urlObjects)))


if __name__ == "__main__":

    proxies_list = manager.generate_proxies()
    links_to_scrap = []
    indice_arr = json.loads(open('data/indice.json').read())
    for item in indice_arr:
        if item["movId"] not in MOVIES_SAFE:
            links_to_scrap.append(URLObject(item["movId"], item["url"], {"https": proxies_list[random.randint(0,len(proxies_list)-1)]}))
    print("Commencing scraping for "+str(len(links_to_scrap))+ " urls")
    directory =  "data/movies"
    scraper = Filmaffinity()
    downloader = ScrapParallel(100,directory, scraper)
    downloader.scrap_batch(links_to_scrap)