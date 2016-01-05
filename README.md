# kickass-get

A command-line interface for scraping Kickass torrents (kat.cr). Provides command-line tools to scrap top torrents in given categories, or obtaining specific torrents. Users can then store data in file for mass-download, or choose one magnet link to show on terminal. 

# Features
* All Kat.cr categories supported: movies, books, music, anime, games, tv, new, apps, xxx and other. 
* Search keyword supported.
* Export data to csv file option
* Export magnet links to txt file option
* Parallel Processing enabled (default 8 workers, you can change this number according to your CPU cores)

# Usage
```
usage: kickass_parse.py [-h] [--category FIELD] [--magnet2file] [--csvfile]
                        [--counts COUNTS] [--search KEYWORD]
                        [--workers WORKERS]

Kickass Command-line Interface: scraping torrents accelerated

optional arguments:
  -h, --help         show this help message and exit
  --category FIELD   Get the specific category. "all" category only works when
                     using --search
  --magnet2file      output the magnet links in file
  --csvfile          output the data in csv file
  --counts COUNTS    number of top torrent links to scrap, default 25.
  --search KEYWORD   Search a keyword, replace space with hyphen. Does not
                     work with "other" category.
  --workers WORKERS  number of workers to use, 8 by default.

```

# Example
Suppose you want to search for torrents of the newest movie called 'Exploding Suns'. You want to look at the top 5 torrents, and only want one magnet link. The complete commands are therefore `python -i kickass_parse.py --search exploding-suns --category movies --counts 5`. 

![interaction_1](/screenshots/interaction_1.png)

The terminal will then show the 5 top torrents info. You can then enter the index of the torrent you want, and its magnet link will show on the screen. Similar to the screenshot below.

![interaction_2](/screenshots/interaction_2.png)


# Disclaimer
See the [license](license.md).
