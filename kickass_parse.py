""" 
    kar.cr torrenting site scrapper

"""

import requests
import bs4
import argparse
import command_line
from torrent import Torrent
from bcolors import bcolors
from multiprocessing.pool import ThreadPool as Pool

root_url = 'http://kat.cr'

categories = {'movies' : '/movies', 'new': '/new', 'music': '/music', 'books': '/books', 'xxx':'/xxx',
                'anime':'/anime', 'tv': '/tv', 'games':'/games', 'apps':'/applications', 'other':'/other' }

def get_page_magnet_urls(page_url):
    """ get the magnet links on a single page of kat.cr
        tested@1/3/2016
    """
    response = requests.get(page_url)
    soup = bs4.BeautifulSoup(response.text,"html.parser")
    return [a.attrs.get('href') for a in soup.select('div.iaconbox.center.floatright a[href^="magnet:"]')]

def get_page_torrent_links(page_url):
    """ get links to each individual torrent page links on kat.cr page
    """
    response = requests.get(page_url)
    soup = bs4.BeautifulSoup(response.text,"html.parser")
    page_links = [root_url + a.attrs.get('href') for a in soup.select('a.cellMainLink')]
    return page_links

def get_page_torrents(page_url, workers, numbers):
    """ return a list containing Torrent objects
    """
    pool = Pool(workers)
    page_links = get_page_torrent_links(page_url)

    while len(page_links) > numbers:
        page_links.pop()

    torrents = pool.map(get_torrent_info, page_links)
    return torrents

def get_torrent_info(page_url):
    """ get a torrent's info from kickass torrent page
        info includes: title, magnet link, torrent link, size, seeders,
                        leechers, update time and upload time
        return a Torrent object
    """
    response = requests.get(page_url)
    soup = bs4.BeautifulSoup(response.text,"html.parser")

    try:
        c_title_and_size = soup.select('span.folderopen')[0].text.strip()
        size_beg_index = c_title_and_size.index('(Size: ')
        c_title = c_title_and_size[:size_beg_index].strip()
        c_size = c_title_and_size[size_beg_index:]
        c_size = c_size[c_size.index(' ') + 1:-1] # remove the '(Size: '  and ')'

        c_magnet = soup.select('a[href^="magnet:"]')[0].attrs.get('href')
        c_torrent_cache = u'http:' + soup.select('a[href^="//torcache.net"]')[0].attrs.get('href')

        c_seeders = soup.select('div.seedBlock > strong')[0].text
        c_leechers = soup.select('div.leechBlock > strong')[0].text
        c_update_time = soup.select('time.timeago')[0].text
        c_upload_time = soup.select('time.timeago')[1].text
        
        torrent = Torrent(title = c_title, magnet = c_magnet, torrent_cache = c_torrent_cache, 
                            size = c_size, seeders = c_seeders, leechers = c_leechers, 
                            update_time = c_update_time, upload_time = c_upload_time)

        print bcolors.OKGREEN + 'Processing torrent info at {} succeeded.'.format(page_url)+ bcolors.ENDC
        return torrent
    except IndexError:
        print bcolors.FAIL + 'Torrent at {} deleted!'.format(page_url)+ bcolors.ENDC
        return Torrent(title = 'Deleted!')

def page_torrents_traverser(options):
    """ get total_counts number of torrents (in Torrent objects) on kat.cr
        maximum: 10000
    """

    # base index url
    index_url = root_url + categories[options.category]

    # per page torrents
    per_page_torrents = len(get_page_torrent_links(index_url))

    # total counts
    total_counts = options.counts
    assert (total_counts <= 10000), "Maximum Counts Exceeded! Maximum 10000 links."
    page_torrents = []

    if total_counts < per_page_torrents:
        page_torrents = get_page_torrents(index_url,options.workers,total_counts)
    else:
        # torrents on the first page
        page_torrents = get_page_torrents(index_url,options.workers,per_page_torrents)

    all_torrents = []
    all_torrents += page_torrents

    # floor the number of pages
    pages = int(total_counts / len(page_torrents))

    for i in range(1, pages):
        page_torrents= get_page_torrents(index_url + '/' + str(i+1), options.workers, per_page_torrents)
        all_torrents += page_torrents

    # add the remaining torrents
    page_torrents = get_page_torrents(index_url + '/' + str(pages+1), options.workers, total_counts-len(all_torrents))
    all_torrents += page_torrents

    if options.csvfile:
        write_torrents_to_file(all_torrents) # csv data output to file

    if options.magnet2file:
        write_torrents_to_file(all_torrents, True) # write magnet links to file

    return all_torrents

def page_magnet_traverser(category,total_counts):
    """ get total_counts number of magnet links on kat.cr
        maximum: 10000
    """
    assert (total_counts <= 10000), "Maximum Counts Exceeded! Maximum 10000 links."

    # base index url
    index_url = root_url + categories[category]

    # magnets on the first page
    page_magnets = get_page_magnet_urls(index_url)
            
    all_magnets = []
    all_magnets += page_magnets

    # ceil the number of pages
    pages = int(total_counts / len(page_magnets) + 1)

    for i in range(1, pages):
        page_magnets = get_page_magnet_urls(index_url + '/' + str(i+1))
        all_magnets += page_magnets

    for i in range(len(all_magnets) - total_counts):
        all_magnets.pop()

    return all_magnets

def write_torrents_to_file(torrents_list, onlyMagnet = False, allData = True):
    """ write the list to a file, if csv, add comma before line change
    """
    delim = '\n'
    csvdelim = ',' + delim

    if onlyMagnet:
        f = open('top_{}_magnet_links.txt'.format(len(torrents_list)),'w')
        for torrent in torrents_list:
            f.write(torrent.magnet + delim) 
        f.close() 

    if allData:
        f = open('top_{}_torrents.txt'.format(len(torrents_list)),'w')
        for torrent in torrents_list:
            f.write(str(torrent) + csvdelim) 
        f.close()

def write_to_file(url_list, csv = False):
    """ write the list to a file, if csv, add comma before line change
    """
    delim = '\n'
    if csv:
        delim = ',' + delim

    f = open('results.txt','w')

    for link in url_list:
        f.write(link + delim) 

    f.close() 

if __name__ == '__main__':
    page_torrents_traverser(command_line.parse_args())
