from tabulate import tabulate
import termcolor

def print_torrents(torrent_list):
	""" print out a list of torrents
	"""
	tor_lol = [[index] + torrent_list[index].list_repr() for index in range(len(torrent_list))]
	print termcolor.colored(tabulate(tor_lol, headers=['Index',"Title","Size", 'Seeders', 'Leechers', 'Upload Time']), 'red')
	print '\n'
