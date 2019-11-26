from ApiRequests import ApiRequests
from datetime import datetime
import sys
import json
import requests
import itertools
import numpy as np
import asyncio

class Artist:
	name=None
	id=None
	albums=[]
	totalWordCounts=[]
	totalWordStats={}
	diffs=[]

	def __init__(self):
		self.name=None
		self.id=None
		self.albums=[]
		self.totalWordCounts=[]
		self.totalWordStats={}	 	
		self.diffs=[]

class Album:
	name=None
	id=None
	date=None
	wordCounts=[]
	wordStats={}

	def __init__(self):
		self.name=None
		self.id=None
		self.date=None
		self.wordCounts=[]
		self.wordStats={}	

def getArtistNameInput():
	print("Please Enter Artist Name:")
	return str(input())

def getLimitInput():
	print("Limit number of albums?: (0 or no value = max limit)")
	try:
		return int(input())
	except:
		return 0

def extractAlbumData(albums):
	if albums:
		albumList = []
		try:
			for a in albums["data"]:
				albumObj = Album()
				albumObj.name=a["title"]
				albumObj.id = a["id"]
				albumObj.date = a["release_date"]
				albumList.append(albumObj)
			return albumList
		except:
			print("Could not extract data from album")

def getAlbumTitles(albumTracks):
	titles = []
	if "error" in albumTracks:
		titles=[]
	else:
		for t in albumTracks["data"]:
			try:
				title = t["title"]
				titles.append(title)
			except:
				print("Could not extract album title")
	return titles

def buildLyricsUrls(artistName, titles):
	urls=[]
	for t in titles:
		try:
			url="https://api.lyrics.ovh/v1/"+artistName+"/"+t
			urls.append(url)
		except:
			print("Failed to build url for title %s" % t)
	return urls

def countWords(lyrics, albumName):
	wordCounts = []
	fails=0
	for i in lyrics:
		if "lyrics" not in i or "error" in i:
			fails+=1
		else:
			try:
				elem = json.loads(i)
				lyrics = elem['lyrics']
				wordCount = len(lyrics.split())
				wordCounts.append(wordCount)
			except:
				pass
	if fails > 0:
		print("Could not retrieve full lyrics for album: %s, Skipping %d tracks..." % (albumName, fails))
	return wordCounts

def calcStats(wordCounts):
	wordStats={}
	wordStats["sum"] = np.sum(wordCounts)
	wordStats["avg"] = np.average(wordCounts)
	wordStats["min"] = np.min(wordCounts)
	wordStats["max"] = np.max(wordCounts)
	wordStats["var"] = np.var(wordCounts)
	wordStats["std"] = np.std(wordCounts)
	return wordStats

def calcDiffPercentages(albums):
	avgs=[]
	for q in albums:
		avgs.append(q.wordStats['avg'])

	diffs = np.diff(avgs) / avgs[1:] * 100
	return diffs

def calcDiffList(dates, diffs):
	alist=[]
	for i, j in itertools.zip_longest(dates, diffs):
		if i:
			alist.append(i)
		if j:
			alist.append(j)
	return alist

def displayAlbum(album):
	params = (album.name, album.date, len(album.wordCounts), album.wordStats["sum"], album.wordStats["avg"], album.wordStats["min"], album.wordStats["max"], album.wordStats["var"], album.wordStats["std"])
	print("Name: %s\nDate: %s\nTracks: %d\nTotal words: %d\nAverage Words: %d\nMinimun: %d\nMaximum: %d\nVariance: %s\nStandard Deviation: %d\n----------" % params)

def displayArtist(artist):
	params = (artist.name, len(artist.albums), len(artist.totalWordCounts), artist.totalWordStats["sum"], artist.totalWordStats["avg"], artist.totalWordStats["min"], artist.totalWordStats["max"],artist.totalWordStats["var"], artist.totalWordStats["std"], artist.diffs)
	print("Name: %s\nAlbums: %d\nTracks: %d\nTotal words: %d\nAverage Words: %d\nMinimun: %d\nMaximum: %d\nVariance: %s\nStandard Deviation: %d\nPercentage diff of avg words between albums: %s\n----------" % params)

def menu(artistObj):
	print("Enter number to select option:\n1.View Artist Stats\n2.View Album Stats\n3.Search Again\n4.Exit\n----------")
	try:
		opt = int(input())
		if opt == 1:
			print("-----Artist-----")
			displayArtist(artistObj)
		elif opt == 2:
			print("-----Albums for: %s-----" % artistObj.name)
			for i in artistObj.albums:
				displayAlbum(i)
		elif opt == 3:
			main(None, None)
		elif opt == 4:
				exit()
	except ValueError as e:
		pass

def main(artistName, albumLimit):
	apirequests = ApiRequests()
	artistObj = Artist() 

	#take user input
	while artistName == None: 
		artistName = getArtistNameInput()

	if albumLimit == None:
		albumLimit = getLimitInput()
	if albumLimit == 0:
		albumLimit=100

	artistObj.name = artistName

	#get artist details
	artistNameUrl = artistObj.name.replace(" ", "-")
	artistContent = apirequests.getArtistDetails(artistNameUrl)

	if artistContent:
		artistObj.id = str(artistContent["id"])
	else:
		main(None, None)

	#get artist albums
	albumResp = apirequests.getArtistAlbums(artistObj.id, artistObj.name, albumLimit)

	#extract album data from response
	albumList = extractAlbumData(albumResp)

	totalCounts=[]
	if albumList:
		for i in albumList:

			#get titles for album
			albumTracks = apirequests.getAlbumTracks(str(i.id), i.name)
			titles = getAlbumTitles(albumTracks)

			#make async requsts for lyrics
			urls=buildLyricsUrls(artistObj.name, titles)
			loop = asyncio.get_event_loop()
			future = asyncio.ensure_future(apirequests.runLyricRequests(urls))
			lyricsResp = loop.run_until_complete(future)
	
			#count words in lyrics
			wordCounts = countWords(lyricsResp, i.name)
			i.wordCounts=wordCounts
			totalCounts.extend(wordCounts)

			print("Found lyrics for %d tracks for album: %s\n----------" % (len(i.wordCounts), i.name))

			if wordCounts:
				#calc album stats
				stats = calcStats(i.wordCounts)
				i.wordStats=stats
				artistObj.albums.append(i)

	if totalCounts:
		#calc artist stats
		artistObj.totalWordCounts=totalCounts
		stats = calcStats(artistObj.totalWordCounts)
		artistObj.totalWordStats=stats

		print("Found %d total tracks over %d albums for artist: %s\n----------" % (len(artistObj.totalWordCounts), len(artistObj.albums), artistObj.name))

		#sort albums by date
		artistObj.albums.sort(key=lambda r: datetime.strptime(r.date, '%Y-%m-%d'))

		#get dates from albums
		dates=[]
		for q in artistObj.albums:
			dates.append(q.date)

		#get percentage difference of avg words between albums
		diffPercentages = calcDiffPercentages(artistObj.albums)

		#concat dates and percentage diffs
		diffs = calcDiffList(dates, diffPercentages)
		artistObj.diffs = diffs

		isMenu=True
		while isMenu:
			menu(artistObj)

	else:
		print("No lyrics available for artist: %s" % artistObj.name)
		main(None, None)

if __name__ == "__main__":
	artistName=''
	albumLimit=None

	#take params
	try:
		artistName = str(sys.argv[1])
	except:
		artistName = getArtistNameInput()

	try:
		albumLimit = int(sys.argv[2])
	except:
		albumLimit=None

	main(artistName, albumLimit)