kickass-get
===============
.. image:: https://img.shields.io/pypi/v/kickass-get.svg
    :target: https://img.shields.io/pypi/v/kickass-get
    
.. image:: https://img.shields.io/pypi/l/kickass-get.svg
    :target: https://img.shields.io/pypi/l/kickass-get
    
.. image:: https://img.shields.io/pypi/dm/kickass-get.svg
    :target: https://img.shields.io/pypi/dm/kickass-get
    

A command-line interface for scraping Kickass torrents (kat.cr). Provides command-line tools to scrap top torrents in given categories, or obtaining specific torrents. Users can then store data in file for mass-download, or choose one magnet link to show on terminal.

Features:
---------

- All Kat.cr categories supported: movies, books, music, anime, games, tv, new, apps, xxx and other
- Search keyword supported
- Export data to csv file option
- Export magnet links to txt file option
- Export torrent files supported
- Transmission-remote supported
- Parallel Processing enabled (default 8 workers, you can change this number according to your CPU cores)

Installation:
-------------

Use ``pip install kickass-get``


Usage
=====
Command-line usage::

   usage: kickass_parse.py [-h] [--category FIELD] [--magnet2file] [--csvfile]
                        [--counts COUNTS] [-T] [--workers WORKERS] [-t]
                        [-P PORT]
                        [keyword [keyword ...]]

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
| -T, --torrents     |   export the torrents files                      |
+--------------------+--------------------------------------------------+
| -t, --transmission |    open magnets with transmission-remote         |
+--------------------+--------------------------------------------------+
|-P PORT, --port PORT|  transmission-remote rpc port. default is 9091   | 
+--------------------+--------------------------------------------------+


Disclaimer
==========
The author explicitly does not approve the use of the software for illegal 
activities. The illegal use of this software can result in serious legal 
consequences for those who engage in it.

See the license for more information.

