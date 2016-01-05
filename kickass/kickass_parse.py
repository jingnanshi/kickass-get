""" 
    kar.cr torrenting site scrapper

"""

import requests
import bs4
import argparse
import command_line
import string
# import timeit
import termcolor
import os.path
from torrent import Torrent
from multiprocessing.pool import ThreadPool as Pool

root_url = 'http://kat.cr'

categories = {'movies' : '/movies', 'new': '/new', 'music': '/music', 'books': '/books', 'xxx':'/xxx',
                'anime':'/anime', 'tv': '/tv', 'games':'/games', 'apps':'/applications', 'other':'/other' }

# session = requests.session()
# session.max_redirects = 100

# process ANSI color for windows terminal
import colorama
colorama.init()

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
    # response = session.get(page_url)

    soup = bs4.BeautifulSoup(response.text,"html.parser")
    page_links = [root_url + a.attrs.get('href') for a in soup.select('a.cellMainLink')]
    return page_links

def get_page_torrents(page_url, workers, numbers):
    """ return a list containing Torrent objects
    """
    pool = Pool(processes=workers)
    page_links = get_page_torrent_links(page_url)

    while len(page_links) > numbers:
        page_links.pop()
    assert (len(page_links) != 0), 'Number of torrent pages equals to 0!'
    torrents = pool.map(get_torrent_info, page_links)
    # pool.close()
    # pool.join()
    return torrents

def get_torrent_info(page_url):
    """ get a torrent's info from kickass torrent page
        info includes: title, magnet link, torrent link, size, seeders,
                        leechers, update time and upload time
        return a Torrent object
    """
    # response = session.get(page_url)
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

        # filter function to remove non-ascii characters from showing up in terminal
        print termcolor.colored('Processing torrent info at {} succeeded.'.format(filter(lambda x: x in string.printable, page_url)), 'green')
        return torrent

    except IndexError:
        # torrent page has been deleted
        print termcolor.colored('Torrent at {} deleted!'.format(page_url), 'red')
        return Torrent(title = 'Deleted!')

def page_torrents_traverser(options):
    """ get total_counts number of torrents (in Torrent objects) on kat.cr
        maximum: 10000
    """
    # check whether arguments are valid
    command_line.check_args(options)

    all_torrents = []

    # enable custom searching
    if options.keyword != None:
        index_url = root_url + '/usearch' + '/{}'.format(options.keyword)
        if options.category != 'all':
            index_url += ' category:{}'.format(options.category)
    else:
        index_url = root_url + categories[options.category]

    try: 
        # base index url
        # change this to enable scrapping of torrents in searched results
        # eg: index_url = 'https://kat.cr/usearch/revenant/'
        # index_url = root_url + categories[options.category]

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

        all_torrents += page_torrents

        # floor the number of pages
        pages = int(total_counts / len(page_torrents))

        for i in range(1, pages):
            page_torrents= get_page_torrents(index_url + '/' + str(i+1), options.workers, per_page_torrents)
            all_torrents += page_torrents

        # add the remaining torrents
        if (total_counts-len(all_torrents)) != 0:
            page_torrents = get_page_torrents(index_url + '/' + str(pages+1), options.workers, total_counts-len(all_torrents))
            all_torrents += page_torrents

    except UnicodeEncodeError:
        print 'UnicodeEncodeError. Prepare to dump current data.'

    except requests.exceptions.TooManyRedirects:
        print 'Too many redirects. Prepare to dump current data.'
        
    # except requests.exceptions.ConnectionError:
    #     print 'ConnectionError. Prepare to dump current data.'
    if options.csvfile or options.magnet2file:
        while True:
            usr_input = raw_input("Enter the path to store file to (q to quit): ").strip()
            if os.path.exists(usr_input):
                break;
            elif usr_input == 'q':
                break;
            else:
                print termcolor.colored('Path does not exist. \n', 'red')

        if options.csvfile:
            write_torrents_to_file(all_torrents, usr_input) # csv data output to file

        if options.magnet2file:
            write_torrents_to_file(all_torrents, usr_input, True) # write magnet links to file
    else: # print torrents to screen
        print termcolor.colored('Torrents displayed: {}'.format(len(all_torrents)).center(50, '='), 'red', attrs=['bold'])

        for i in range(len(all_torrents)):
            print termcolor.colored('Torrent {}: \n'.format(i), 'red', attrs=['blink'])
            print str(all_torrents[i]) + '\n'

        # asking for which one to display
        index = command_line.readInt("Which torrent's magnet link would you like to display? (q to quit) ", 'q', 0, len(all_torrents))

        print 'Magnet link: \n'
        print all_torrents[int(index)].getMagnet() + '\n \n'
        print termcolor.colored('Enjoy the ride!', 'magenta', attrs=['blink'])

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

def write_torrent_to_file(torrent, save_path, onlyMagnet = False, allData = True):
    """ write a torrent to file
    """
    delim = '\n'
    csvdelim = ',' + delim

    file_path_m = os.path.join(save_path,'magnet_links.txt')
    file_path_t = os.path.join(save_path,'torrents.csv')

    if onlyMagnet:
        f = open(file_path_m,'w')
        f.write(torrent.magnet + delim) 
        f.close() 

    if allData:
        f = open(file_path_t,'w')
        f.write(str(torrent) + csvdelim) 
        f.close()

def write_torrents_to_file(torrents_list, save_path, onlyMagnet = False, allData = True):
    """ write the list to a file, if csv, add comma before line change
    """
    delim = '\n'
    csvdelim = ',' + delim

    file_path_m = os.path.join(save_path,'magnet_links.txt')
    file_path_t = os.path.join(save_path,'torrents.csv')

    if onlyMagnet:
        f = open(file_path_m,'w')
        for torrent in torrents_list:
            f.write(torrent.magnet + delim) 
        f.close() 

    if allData:
        f = open(file_path_t,'w')
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

def main():
    page_torrents_traverser(command_line.parse_args())

if __name__ == '__main__':
    
    # start = timeit.default_timer()
    
    main()
    
    # stop = timeit.default_timer()

    # print stop - start  
    
