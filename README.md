# filmaffinity-scraper
I have built an unofficial class to give an easy way to interact with filmaffinity webpage.

## Getting Started

First of all, unzip 'data / index.json.zip' and 'data / movies.zip', with this you will have practically all the base of films of the English domain of filmaffinity.
All the necesary libraries for run the project are in the requirements.txt.

### Use of the class

There is a simple practical example in get_movies_simple.py, to be more efficient and avoid possible IP blocking, everything is adapted to be able to use proxies. There is an example in get_movies_paralell_scrap.py, where apart from using proxies the task is parallelized.

```
from scraper.filmaffinity import Filmaffinity

film_scraper = Filmaffinity()

film_scraper.get_indice(proxy = None)
film_scraper.scrap_indice_web(indice_url, proxy = None)
film_scraper.scrap_movie_web(movie_url, lng = "en", proxy = None)
film_scraper.get_movie_review_indice(movie_id, proxy = None)
film_scraper.scrap_movie_review(movie_review_url, proxy = None)
```




