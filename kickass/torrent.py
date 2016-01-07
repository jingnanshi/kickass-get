import string
import re
import gzip
import urllib2
import os
import data

from io import BytesIO


class Torrent:

    def __init__(self,**kwargs):
        self.title = None
        self.magnet = None
        self.torrent_cache = None
        self.size = None
        self.seeders = None
        self.leechers = None
        self.update_time = None
        self.upload_time = None

        try:
            self.title = kwargs['title']
            self.magnet = kwargs['magnet']
            self.torrent_cache = kwargs['torrent_cache']
            self.size = kwargs['size']
            self.seeders = kwargs['seeders']
            self.leechers = kwargs['leechers']
            self.update_time = kwargs['update_time']
            self.upload_time = kwargs['upload_time']
        except KeyError:
            pass

    def setMagnet(self,magnet):
        self.magnet = magnet

    def getMagnet(self):
        return self.magnet

    def setTorrentCache(self,torrent_cache):
        self.torrent_cache = torrent_cache 

    def setSize(self,size):
        self.size = size

    def setSeeders(self,seeders):
        self.seeders = seeders

    def setLeechers(self,leechers):
        self.leechers = leechers

    def setUploadTime(self,upload_time):
        self.upload_time = upload_time

    def setUpdateTime(self,update_time):
        self.update_time = update_time

    def getCleanedTitle(self):
        # match anything that's not alphanumeric or underscore
        cleaned_title = re.sub(r'[^\w]', ' ', self.title)
        return cleaned_title

    def __str__(self):
        remove_comma_title = self.title.replace(',','_') # change commas to underscore for csv 
        result = '{}, {}, {}, {}, Seeders: {}, Leechers: {}, Updated at: {}, Uploaded at: {}'.format(remove_comma_title, 
            self.magnet, self.torrent_cache, self.size, self.seeders, self.leechers, self.update_time, self.upload_time) 
        return filter(lambda x: x in string.printable, result)
        # return result

    def __repr__(self):
        return self.title 

    def get_torcache_torrent(self):
        """ return a torrent string from torrent link
        """
        url = self.torrent_cache[:self.torrent_cache.index('?')]
        # http://stackoverflow.com/questions/16895787/torrent-files-downloaded-using-python-urllib2-fail-to-open-in-bittorrent-client
        req = urllib2.Request(url,
                              headers=data.default_headers)
        req.add_header('Accept-encoding', 'gzip')

        torrent = urllib2.urlopen(req, timeout=data.default_timeout)
        if torrent.info().get('Content-Encoding') == 'gzip':
            torrent = gzip.GzipFile(fileobj=BytesIO(torrent.read()))

        return torrent.read()

    def save_to_file(self, save_path):
        torrent_string = self.get_torcache_torrent()
        filepath = os.path.join(save_path,'{}.torrent'.format(self.getCleanedTitle()))
        file1 = open(filepath, "w")
        file1.write(torrent_string)
        file1.close()

    def list_repr(self):
        """ return a list representation of the torrent itself:
            [title, size, seeders, leechers, update_time, upload_time]
        """
        tor_list = [self.getCleanedTitle(), self.size, self.seeders, self.leechers, self.upload_time]
        return tor_list

