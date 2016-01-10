"""
    command-line control for site scrappers

"""

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Kickass Command-line Interface: scraping torrents accelerated')
    parser.add_argument('--category', metavar='FIELD', 
                        choices=['movies', 'books', 'music', 'anime', 'games', 'tv', 'new', 'xxx', 'apps', 'other', 'all'],
                        default='movies', help='Get the specific category. "all" category only works when using --search')
    parser.add_argument('--magnet2file', action='store_true', default=False,
                        help='output the magnet links in file')
    parser.add_argument('--csvfile', action='store_true', default=False,
                        help='output the data in csv file')
    parser.add_argument('--counts', type=int, default=25,
                        help='number of top torrent links to scrap, default 25.')
    parser.add_argument('keyword', nargs='*', default = None, 
                        help='Search keywords. Does not work with "other" category.')
    parser.add_argument('-T', '--torrents', action='store_true', default=False,
                        help='export the torrents files')
    parser.add_argument('--workers', type=int, default=8,
                        help='number of workers to use, 8 by default.')
    parser.add_argument('-t', '--transmission',
                        action='store_true',
                        help='open magnets with transmission-remote')
    parser.add_argument('-P', '--port', dest='port',
                        help='transmission-remote rpc port. default is 9091')
    return parser.parse_args()

def check_args(options):
    """ check whether input arguments are valid
    """
    if (options.category == 'other' and options.keyword != None):
        raise AssertionError('--search does not work with "other" category.')

    if (options.category == 'all' and options.keyword == None):
        raise AssertionError('"all" category only works when using --search')

def readInt(prompt, sig, min_v, max_v):
    """ make sure user input integer, sig to break, range from min to max
        min inclusive
        max exclusive
    """
    while True:
        usr_input = raw_input(prompt)
        if usr_input == sig:
            break
        elif not isInt(usr_input):
            print 'Not a valid integer!'
        elif int(usr_input) < min_v or int(usr_input) >= max_v:
            print 'Number out of range!'
        else:
            return int(usr_input)

    return None

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
