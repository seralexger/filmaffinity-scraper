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

### Movie data scheme example

```
{
    "id": 201496,
    "title": "Iron Man",
    "movie_link_es": "https://www.filmaffinity.com/es/film201496.html",
    "movie_link_en": "https://www.filmaffinity.com/en/film201496.html",
    "director": [
        "Jon Favreau"
    ],
    "cast": [
        "Robert Downey Jr.",
        "Terrence Howard",
        "Gwyneth Paltrow",
        "Jeff Bridges",
        "Stan Lee",
        "Leslie Bibb",
        "Clark Gregg",
        "Shaun Toub",
        "Faran Tahir",
        "Samuel L. Jackson"
    ],
    "year": 2008,
    "duration": 126,
    "country": "United States",
    "screenwriter": [
        "Arthur Marcum",
        "Matt Holloway",
        "Mark Fergus",
        "Hawk Ostby (Characters: Stan Lee)"
    ],
    "music": [
        "Ramin Djawadi"
    ],
    "photo": [
        "Matthew Libatique"
    ],
    "producer": [
        "Paramount Pictures",
        "Marvel Enterprises",
        "Marvel Studios"
    ],
    "genre": [
        "Fantasy",
        "Action",
        "Adventure",
        "Sci-Fi"
    ],
    "subgenre": [
        "Superheroes",
        "Based on a Comic",
        "Marvel Comics",
        "Robots"
    ],
    "group": [
        "Marvel Cinematic Universe",
        "Iron Man"
    ],
    "rating": 6.5,
    "synopsis": "Tony Stark is a billionaire industrialist and genius inventor who is kidnapped and forced to build a devastating weapon. Instead, using his intelligence and ingenuity, Tony builds a high-tech suit of armor and escapes captivity. When he uncovers a nefarious plot with global implications, he dons his powerful armor and vows to protect the world as Iron Man. ",
    "rating_count": 87979,
    "movie_relations": [
        {
            "rel_id": 250528,
            "rel_title": "Iron Man 2",
            "rel_link": "https://www.filmaffinity.com/en/film250528.html"
        },
        {
            "rel_id": 857963,
            "rel_title": "The Invincible Iron Man",
            "rel_link": "https://www.filmaffinity.com/en/film857963.html"
        }
    ]
}
```


