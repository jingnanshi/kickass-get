# Kickass Scrapper

A scrapper for Kickass torrents (kat.cr). Provides command-line tools to scrap top torrents in given categories. Users can then store data in file for mass-download.

Users can choose to export all data related to torrents in a csv file or only export magnet links.

# Features
* All Kat.cr categories supported: movies, books, music, anime, games, tv, new, apps, xxx and other. 
* Export data to csv file option
* Export magnet links to txt file option
* Multiprocess enabled (default 8 workers, you can change this number according to your CPU cores)


# Usage
```
usage: kickass_parse.py [-h] [--category FIELD] [--workers WORKERS]
                        [--magnet2file] [--csvfile] [--counts COUNTS]

Optional Arguments  | Description
--------------------|---------------------------------------------------
 -h, --help         | show this help message and exit
 --category FIELD   | get the specific category
 --workers WORKERS  | number of workers to use, 8 by default.
 --magnet2file      | export the magnet links in file
 --csvfile          | export the data in csv file
 --counts COUNTS    | number of top torrent links to scrap, default 25.
```

# Screenshots
![movies](/screenshots/movies.png)


# Advanced Usage
You can change the `index_url` in `page_torrents_traverser(options)` to enable scrapping torrents in searched results. For example, if you want to scrap torrent info with a search keyword 'test', you can use `index_url = 'https://kat.cr/usearch/test/`.

# Disclaimer
See the [license](license.md).
