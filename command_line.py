"""
    command-line control for site scrappers

"""

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Show Kickass Magnet Links')
    parser.add_argument('--category', metavar='FIELD', choices=['movies', 'books', 'music', 'anime', 'games', 'tv', 'new', 'xxx', 'apps', 'other'],
                        default='movies', help='get the specific category')
    parser.add_argument('--workers', type=int, default=8,
                        help='number of workers to use, 8 by default.')
    parser.add_argument('--magnet2file', action='store_true', default=False,
                        help='output the magnet links in file')
    parser.add_argument('--csvfile', action='store_true', default=False,
                        help='output the data in csv file')
    parser.add_argument('--counts', type=int, default=25,
                        help='number of top torrent links to scrap, default 25.')
    return parser.parse_args()