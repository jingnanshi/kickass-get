class Torrent:

	def __init__(self,**kwargs):
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

	def __str__(self):
		return '{}, {}, {}, {}, Seeders: {}, Leechers: {}, Updated at: {}, Uploaded at: {}'.format(self.title, self.magnet, self.torrent_cache, 
				self.size, self.seeders, self.leechers, self.update_time, self.upload_time) 

	def __repr__(self):
		return self.title 

