# -*- encoding: utf-8 -*-


#########################################################
#
# Alejandro German
# 
# https://github.com/seralexger/filmaffinity-scraper
#
#########################################################

import json
import time
import glob
import re
from tqdm import tqdm
from scraper.filmaffinity import Filmaffinity
from proxy_manager.proxyManager import ProxyManager



proxies_list = manager.generate_proxies()
indice_arr = json.loads(open('data/indice.json').read())

movies_safe = []
for path in glob.glob("data/movies/*"):
	movies_safe.append(int(re.sub('[^0-9]','', path)))

scraper = Filmaffinity()

for item in tqdm(indice_arr):
	if item["movId"] not in movies_safe:
		try:
			movie_info = scraper.scrap_movie_web(item["url"], "en", {"https": proxies_list[random.randint(0,len(proxies_list)-1)]})
			if movie_info != None:
				with open("data/movies/"+ str(item["movId"]) + '.json', 'w') as fp:
					json.dump(movie_info, fp, indent = 4)
		except Exception as e:
			print(e)
