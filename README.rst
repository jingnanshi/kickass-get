kickass-get
===============

A command-line interface for scraping Kickass torrents (kat.cr). Provides command-line tools to scrap top torrents in given categories, or obtaining specific torrents. Users can then store data in file for mass-download, or choose one magnet link to show on terminal.

Features:
---------

- All Kat.cr categories supported: movies, books, music, anime, games, tv, new, apps, xxx and other
- Search keyword supported
- Export data to csv file option
- Export magnet links to txt file option
- Parallel Processing enabled (default 8 workers, you can change this number according to your CPU cores)


Usage
=====
Command-line usage::

    usage: kickass_parse.py [-h] [--category FIELD] [--workers WORKERS] 
                            [--magnet2file] [--csvfile] [--counts COUNTS]


+--------------------+--------------------------------------------------+
|Optional Arguments  | Description                                      |
+====================+==================================================+
| -h, --help         | show this help message and exit                  |
+--------------------+--------------------------------------------------+
| --category FIELD   | get the specific category                        |
+--------------------+--------------------------------------------------+
| --workers WORKERS  | number of workers to use, 8 by default.          |
+--------------------+--------------------------------------------------+
| --magnet2file      | export the magnet links in file                  |
+--------------------+--------------------------------------------------+
| --csvfile          | export the data in csv file                      |
+--------------------+--------------------------------------------------+
| --counts COUNTS    | number of top torrent links to scrap, default 25.|
+--------------------+--------------------------------------------------+


Disclaimer
==========
MIT License
