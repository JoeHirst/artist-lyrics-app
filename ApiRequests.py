import requests
import json
import asyncio
from aiohttp import ClientSession

class ApiRequests:

	#takes (pathParam, identifier, pathParam, limit)
	def buildUrl(self, *params):
		#add try except
		url="https://api.deezer.com/"
		url+=params[0]+"/"
		if len(params) > 1: url+=params[1]+"/"
		if len(params) > 2: url+=params[2]+"/"
		if len(params) > 3: url+="?limit="+str(params[3])
		return url

	def getArtistDetails(self, artistName):
		try:	
			getArtistUrl = self.buildUrl("artist", artistName)
			artistResponse = requests.get(getArtistUrl)
			artistContent = json.loads(artistResponse.content)
			if "error" in artistContent:
				print("Artist %s not found!" % artistName)
			else:
				print("Found artist: %s" % artistName)
				return artistContent
		except: 
			print("Could not fetch data for artist: %s" % artistName)

	def getArtistAlbums(self, artistId, artistName, limit):
		try:
			getAlbumsUrl = self.buildUrl("artist", artistId, "albums", limit)
			albumsResponse = requests.get(getAlbumsUrl)
			albumsContent = json.loads(albumsResponse.content)
			if "error" in albumsContent:
				print("No albums found for artist %s" % artistName)
			else:
				print("Found %d albums for artist: %s" % (len(albumsContent["data"]), artistName))
				return albumsContent
		except:
			print("Failed to retrieve albums for artist: %s" % artistName)

	def getAlbumTracks(self, albumId, albumName):
		try:
			getAlbumsUrl = self.buildUrl("album", albumId, "tracks")
			tracksResponse = requests.get(getAlbumsUrl)
			tracklist = json.loads(tracksResponse.content)
			if "error" in tracklist:
				print("No tracks found for album: %s" % albumName)
			else:
				print("Found %d tracks for album: %s" % (len(tracklist["data"]), albumName))
				return tracklist
		except:
			print("Failed to retrieve tracks for album: %s" % albumName)

	async def getLyrics(self, url, session):
		try:
			async with session.get(url) as response:
				return await response.text(encoding="utf-8")
		except:
			print("Lyrics request failed for %s" %url)

	async def runLyricRequests(self, urls):
		tasks = []
		async with ClientSession() as session:
			for i in urls:
				try:
					task = asyncio.ensure_future(self.getLyrics(i, session))
					tasks.append(task)
				except:
					print("Lyrics request failed for %s" % i)
			responses = await asyncio.gather(*tasks)
		return responses