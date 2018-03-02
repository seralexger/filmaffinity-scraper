# -*- encoding: utf-8 -*-

#########################################################
#
# Alejandro German
# 
# https://github.com/seralexger/filmaffinity-scraper
#
#########################################################

from lxml import html
from lxml import etree
import requests
import re
from tqdm import tqdm
import json

class Filmaffinity:
	"""

	Filmaffinity v 1.0

	This is an unofficial class for recollect info from Filmmaffinity.
	This class was developed by alexgerser, it's main goal is give an easy way to interact with filmaffinity webpage for studies purposes.

	"""

	allfilms_url = "https://www.filmaffinity.com/es/allfilms.html"

	def get_indice(self, proxy = None):
		""" Get Filmaffinity indice and total pages per item """

		response = requests.get(self.allfilms_url, proxies = proxy, timeout = 30)
		tree = html.fromstring(response.content)
		indice_html = tree.xpath('//*[@id="mt-content-cell"]/table/tr[2]/td/table/tr/td')
		indice = []
		for element in tqdm(indice_html):
			indice_item = element.xpath('a/b/text()')
			if indice_item == []:
				indice_item = element.xpath('b/text()')
			try:
				indice_item = indice_item[0].replace("[","").replace("]","") 
				indice_response = requests.get(self.allfilms_url.replace(".html","") + "_" + indice_item + "_1.html")
				indice_tree = html.fromstring(indice_response.content)
				pager = indice_tree.xpath('(//div[@class="pager"])[1]/a/text()')
				total_pages = pager[len(pager)-2]
				indice.append({'indice_item': indice_item, 'total_pages': int(total_pages)})
			except Exception as e:
				print(e)

		return indice


	def scrap_indice_web(self, indice_url, proxy = None):
		""" Get movies from indice item link """

		response = requests.get(indice_url, proxies = proxy, timeout = 30)
		tree = html.fromstring(response.content)
		all_films_wrapper = tree.xpath('//div[@id="all-films-wrapper"]/div[@class="all-films-movie fa-shadow"]/div[@class="movie-card movie-card-1"]')
		movies_info = []
		for movie in tqdm(all_films_wrapper):

			try:
				movie_dic = {}

				try:
					movie_dic["movie_id"] = int(movie.xpath('@data-movie-id')[0])
				except:
					print("Movie id not found")

				try:
					movie_dic["movie_poster"] = movie.xpath('div[@class="mc-poster"]/a/img/@src')[0]
				except:
					print("Movie image not found")

				try:
					movie_dic["movie_link_es"] = "https://www.filmaffinity.com" + movie.xpath('div[@class="mc-poster"]/a/@href')[0]
				except:
					print("Movie spanish link not found")

				try:
					movie_dic["movie_link_en"] = "https://www.filmaffinity.com" + movie.xpath('div[@class="mc-poster"]/a/@href')[0].replace("/es/","/en/")
				except:
					print("Movie english link not found")

				try:
					movie_dic["movie_title"] = movie.xpath('div[@class="mc-info-container"]/div[@class="mc-title"]/a/@title')[0].encode("latin-1").decode("utf-8")
				except:
					print("Movie title not found")

				try:
					movie_year = movie.xpath('div[@class="mc-info-container"]/div[@class="mc-title"]/text()')[0]
					movie_dic["movie_year"] = int(re.sub(r'[^\w]', '', str(movie_year.strip())))
				except:
					print("Movie year not found")

				try:
					movie_dic["movie_country"] = movie.xpath('div[@class="mc-info-container"]/div[@class="mc-title"]/img/@title')[0].encode("latin-1").decode("utf-8")
				except:
					print("Movie country not found")

				try:
					movie_dic["movie_rating"] = movie.xpath('div[@class="mc-info-container"]/div[@class="mr-rating"]/div/text()')[0].replace(",",".")
				except:
					print("Movie rating not found")

				try:
					movie_rating_count = movie.xpath('div[@class="mc-info-container"]/div[@class="mr-rating"]/div[@class="ratcount-box"]/text()')
					if movie_rating_count != []:
						movie_rating_count = int(re.sub(r'[^\w]', '', str(movie_rating_count[0].strip())))
					else:
						movie_rating_count = 0
					movie_dic["movie_rating_count"] = movie_rating_count
				except:
					print("Movie rating count not found")

				try:
					movie_dic["movie_director"] = movie.xpath('div[@class="mc-info-container"]/div[@class="mc-director"]/div/span/a/@title')[0].encode("latin-1").decode("utf-8")
				except:
					print("Movie director not found")

				try:
					movie_cast = movie.xpath('div[@class="mc-info-container"]/div[@class="mc-cast"]/div/span/a/@title')
					movie_dic["movie_cast"] = list(map((lambda x: x.encode("latin-1").decode("utf-8")), movie_cast))
				except:
					print("Movie cast not found")

				movies_info.append(movie_dic)

			except Exception as e:
				print("PARSER MOVIE EXCEPTION: " + str(e))
		
		return movies_info


	def scrap_movie_web(self, movie_url, lng = "en", proxy = None):
		""" Get movie info from its url """

		if lng == "en":
			movie_url = movie_url.replace("/es/", "/en/")
			music_flag = "Music"
			photo_flag = "graphy"
			writer_flag = "eenwriter"
			producer_flag = "roducer"
		else:
			movie_url = movie_url.replace("/en/", "/es/")
			music_flag = "sica"
			photo_flag = "Fotogra"
			writer_flag = "Guion"
			producer_flag = "ductora"
		try:
			response = requests.get(movie_url, proxies = proxy, timeout = 30)
			
			if response.status_code != 200:
				return None

			tree = html.fromstring(response.content)

			movie_dic = {}

			try:
				movie_dic["id"] = int(re.sub('[^0-9]','', movie_url))
			except:
				print("Movie id not found")

			try:
				movie_dic["title"] = tree.xpath('//h1[@id="main-title"]/span[@itemprop="name"]/text()')[0]
			except:
				print("Movie title not found")

			try:
				movie_dic["movie_link_es"] = movie_url.replace("/en/","/es/")
				movie_dic["movie_link_en"] = movie_url.replace("/es/","/en/")
			except:
				print("Movie link not found")

			try:
				movie_dic["director"] = tree.xpath('//dd[@class="directors"]/span/a/span[@itemprop="name"]/text()')
			except:
				print("Movie director not found")

			try:
				movie_dic["cast"] = tree.xpath('//dd/span[@itemprop="actor"]/a/span[@itemprop="name"]/text()')
			except:
				print("Movie cast not found")

			try:
				movie_dic["year"] = int(tree.xpath('//dd[@itemprop="datePublished"]/text()')[0])
			except:
				print("Movie year not found")

			try:
				movie_dic["duration"] = tree.xpath('//dd[@itemprop="duration"]/text()')[0]
				movie_dic["duration"] = int(re.sub('[^0-9]','', movie_dic["duration"]))
			except:
				print("Movie duration not found")

			try:
				movie_dic["country"] = tree.xpath('//dd/span[@id="country-img"]/img/@title')[0]
			except:
				print("Movie country not found")

			try:
				movie_dic["screenwriter"] = tree.xpath('//dt[contains(text(),"'+ writer_flag +'")]/following::dd/div[@class="credits"]')[0].xpath('span/span/text()')
			except:
				print("Movie writer not found")

			try:
				movie_dic["music"] = tree.xpath('//dt[contains(text(),"'+ music_flag +'")]/following::dd/div[@class="credits"]')[0].xpath('span/span/text()')
			except:
				print("Movie music not found")

			try:
				movie_dic["photo"] = tree.xpath('//dt[contains(text(),"'+ photo_flag +'")]/following::dd/div[@class="credits"]')[0].xpath('span/span/text()')
			except:
				print("Movie photography not found")

			try:
				movie_dic["producer"] = list(map((lambda x: x.strip()), tree.xpath('//dt[contains(text(),"'+ producer_flag +'")]/following::dd/div[@class="credits"]')[0].xpath('span/span/text()')[0].split("/")))
			except:
				print("Movie producer not found")

			try:
				movie_dic["genre"] = tree.xpath('//span[@itemprop="genre"]/a/text()')
			except:
				print("Movie genre not found")

			try:
				movie_dic["subgenre"] = tree.xpath('//a[contains(@href,"https://www.filmaffinity.com/'+ lng +'/movietopic")]/text()')
			except:
				print("Movie subgenre not found")

			try:
				movie_dic["group"]=tree.xpath('//a[contains(@href,"/'+ lng +'/movie-group.php?group-id=")]/text()')
			except:
				print("Movie group not found")

			try:
				movie_dic["rating"] = float(tree.xpath('//div[@id="movie-rat-avg"]/@content')[0])
			except:
				print("Movie rating not found")

			try:
				movie_dic["synopsis"] = tree.xpath('//dd[@itemprop="description"]/text()')[0]
			except:
				print("Movie synopsis not found")

			try:
				movie_dic["rating_count"] = int(tree.xpath('//span[@itemprop="ratingCount"]/@content')[0])
			except:
				print("Movie rating_count not found")

			try:
				movie_dic["reviews_count"] = int(tree.xpath('//span[@id="movie-reviews-box"]/text()')[0].strip())
			except:
				if lng == "es":
					print("Movie reviews not found")

			try:
				movie_dic["movie_relations"] = list(map((lambda x: {'rel_id': int(re.sub('[^0-9]','', x.xpath("a/@href")[0])),'rel_title': x.xpath("a/@title")[0], "rel_link": x.xpath("a/@href")[0]}), tree.xpath('//div[@class="poster-rel"]')))
			except:
				print("Movie relations not found")

			return movie_dic
		except Exception as e:
			print("PARSER FILM ERROR: " + str(e))
			return None

	def get_movie_review_indice(self, movie_id, proxy = None):
		"""  """
		
		try:
			review_link = "https://www.filmaffinity.com/es/reviews/1/"+str(movie_id)+".html?orderby=5"
			response = requests.get(review_link, proxies = proxy, timeout = 30)
			tree = html.fromstring(response.content)

			review_dic = {}
			pages = tree.xpath('(//div[@class="pager"])[1]/a/text()')
			review_dic["total_pages"] = int(pages[len(pages)-2])
			review_dic["order_code"] = 5
			review_dic["order_by"] = "date"
			review_dic["review_link"] = review_link 

			return review_dic
			
		except Exception as e:
			print("ERROR PARSER REVIEW INDICE: " + str(e))

	def scrap_movie_review(self, movie_review_url, proxy = None):
		"""  """

		try:
			response = requests.get(movie_review_url, proxies = proxy, timeout = 30)
			tree = html.fromstring(response.content)
			reviews_wrapper = tree.xpath('//div[@class="reviews-wrapper"]/div[@class="fa-shadow movie-review-wrapper rw-item"]')
			movie_reviews = []
			for review in reviews_wrapper:
				movie_review = {}

				try:
					movie_review["movie_id"] = int(tree.xpath('//div[@class="moviecard-section-container"]/@data-movie-id')[0])
				except:
					print("Movie id not found")

				try:
					movie_review["user_name"] = review.xpath('div[@class="mr-user-info-wrapper sn"]/div[@class="user-info"]/div[@class="mr-user-nick"]/a/b/text()')[0]
				except:
					print("User name not found")

				try:
					movie_review["user_id"] = int(review.xpath('div[@class="mr-user-info-wrapper sn"]/div[@class="user-info"]/@data-user-id')[0])
				except:
					print("User id not found")

				try:
					movie_review["user_country"] = review.xpath('div[@class="mr-user-info-wrapper sn"]/div[@class="user-info"]/div[@class="mr-user-country"]/i/text()')[0].encode("latin-1").decode("utf-8")
				except:
					print("User country text not found")

				try:
					movie_review["review_rating"] = int(review.xpath('div[@class="mr-user-info-wrapper sn"]/div[@class="user-reviews-movie-rating"]/text()')[0].strip())
				except:
					print("Review rating not found")

				try:
					movie_review["review_title"] = review.xpath('div[@class="review-title"]/a/text()')[0].encode("latin-1").decode("utf-8")
				except:
					print("Review title not found")

				try:
					movie_review["review_date"] = review.xpath('div/div[@class="review-date"]/text()')[0]
				except:
					print("Review date not found")
				
				try:
					movie_review["review_text"] = review.xpath('div[@class="review-text1"]/text()')[0].encode("latin-1").decode("utf-8")
				except:
					print("Review text not found")

				movie_reviews.append(movie_review)
			return movie_reviews

		except Exception as e:
			print("ERROR PARSER REVIEW: " + str(e))

