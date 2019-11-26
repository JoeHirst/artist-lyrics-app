import ArtistLyricsApp
import unittest
import json

class TestApiMethods(unittest.TestCase):

	def testExtractAlbumDataSuccess(self):
		albums=b'{"data":[{"id":116585992,"title":"MTV Unplugged In New York (25th Anniversary \\u2013 Live)","link":"https:\\/\\/www.deezer.com\\/album\\/116585992","cover":"https:\\/\\/api.deezer.com\\/album\\/116585992\\/image","cover_small":"https:\\/\\/e-cdns-images.dzcdn.net\\/images\\/cover\\/7e021a4689fd4c8d540e7f1ceadca925\\/56x56-000000-80-0-0.jpg","cover_medium":"https:\\/\\/e-cdns-images.dzcdn.net\\/images\\/cover\\/7e021a4689fd4c8d540e7f1ceadca925\\/250x250-000000-80-0-0.jpg","cover_big":"https:\\/\\/e-cdns-images.dzcdn.net\\/images\\/cover\\/7e021a4689fd4c8d540e7f1ceadca925\\/500x500-000000-80-0-0.jpg","cover_xl":"https:\\/\\/e-cdns-images.dzcdn.net\\/images\\/cover\\/7e021a4689fd4c8d540e7f1ceadca925\\/1000x1000-000000-80-0-0.jpg","genre_id":85,"fans":3507,"release_date":"2019-11-01","record_type":"album","tracklist":"https:\\/\\/api.deezer.com\\/album\\/116585992\\/tracks","explicit_lyrics":false,"type":"album"}],"total":19,"next":"https:\\/\\/api.deezer.com\\/artist\\/415\\/albums\\/?limit=1&index=1"}'
		result = ArtistLyricsApp.extractAlbumData(json.loads(albums))

		self.assertEqual(len(result), 1)
		self.assertEqual(result[0].name, "MTV Unplugged In New York (25th Anniversary – Live)")
		self.assertEqual(result[0].id, 116585992)
		self.assertEqual(result[0].date, "2019-11-01")

	def testExtractAlbumDataError(self):
		albums="{\"data\": [],\"total\": 0}"
		result = ArtistLyricsApp.extractAlbumData(json.loads(albums))

		self.assertEqual(len(result), 0)

	def testGetAlbumTitlesSuccess(self):
		tracklist=b'{"data":[{"id":"788626102","readable":true,"title":"AboutAGirl","title_short":"AboutAGirl","title_version":"","isrc":"USGF19972701","link":"https://www.deezer.com/track/788626102","duration":"217","track_position":1,"disk_number":1,"rank":"564171","explicit_lyrics":false,"explicit_content_lyrics":0,"explicit_content_cover":0,"preview":"https://cdns-preview-2.dzcdn.net/stream/c-27af2ef7e4cab52253c8da5fa647ba01-4.mp3","artist":{"id":"415","name":"Nirvana","tracklist":"https://api.deezer.com/artist/415/top?limit=50","type":"artist"},"type":"track"}],"total":19,"next":"https://api.deezer.com/album/116585992/tracks?limit=1&index=1"}'
		result = ArtistLyricsApp.getAlbumTitles(json.loads(tracklist))

		self.assertEqual(len(result),1)
		self.assertEqual(result, ['AboutAGirl'])
		self.assertEqual(result[0], "AboutAGirl")


	def testGetAlbumTitlesError(self):
		tracklist=b'{"error": {"type": "DataException","message": "no data","code": 800}}'
		result = ArtistLyricsApp.getAlbumTitles(json.loads(tracklist))

		self.assertEqual(len(result),0)
		self.assertEqual(result, [])

	def testBuildLyricsUrls(self):
		titles = ['AboutAGirl', 'Come As You Are']
		result = ArtistLyricsApp.buildLyricsUrls("Nirvana", titles)

		self.assertEqual(len(result),2)
		self.assertEqual(result, ['https://api.lyrics.ovh/v1/Nirvana/AboutAGirl', 'https://api.lyrics.ovh/v1/Nirvana/Come As You Are'])

	def testCountWords(self):
		lyrics = "{\"lyrics\": \"Come, as you are, as you were, as I want you to be As a friend, as a friend, as an old enemy Take your time, hurry up, the choice is yours, don't be late Take a rest, as a friend, as an old Memoria, memoria, memoria, memoria  Come, doused in mud, soaked in bleach, as I want you to be As a trend, as a friend, as an old Memoria, memoria, memoria, memoria  And I swear that I, don't have a gun No, I don't have a gun, no, I don't have a gun  -ria, memoria, memoria, memoria (No, I don't have a gun)  Well, I swear that I don't have a gun No, I don't have a gun, no, I don't have a gun No, I don't have a gun, no, I don't have a gun  Memoria, memoria\"}"
		lyricslist=[]
		lyricslist.append(lyrics)
		result = ArtistLyricsApp.countWords(lyricslist, "MTV Unplugged In New York (25th Anniversary – Live)")

		self.assertEqual(result, [140])

	def testCalcStats(self):
		wordCounts = [148, 140, 182, 142, 90, 191, 205, 256, 159, 184, 156, 172, 250, 228, 140, 205, 184, 90, 142]
		result = ArtistLyricsApp.calcStats(wordCounts)

		self.assertEqual(str(result), "{'sum': 3264, 'avg': 171.78947368421052, 'min': 90, 'max': 256, 'var': 1973.6398891966762, 'std': 44.42566700902392}")

	def testCalcDiffPercentages(self):
		a1 = ArtistLyricsApp.Album()
		a1.wordStats={"avg":50}
		a2 = ArtistLyricsApp.Album()
		a2.wordStats={"avg":100}
		a3 = ArtistLyricsApp.Album()
		a3.wordStats={"avg":200}
		albums = []
		albums.extend([a1, a2, a3])

		result = ArtistLyricsApp.calcDiffPercentages(albums)
		self.assertEqual(str(result), "[50. 50.]")

	def testCalcDiffList(self):
		diffs = [50., 50.]
		dates = ["2018-12-20", "2019-04-15", "2019-11-01"]

		result = ArtistLyricsApp.calcDiffList(dates, diffs)


		self.assertEqual(len(result), 5)
		self.assertEqual(str(result), "['2018-12-20', 50.0, '2019-04-15', 50.0, '2019-11-01']")

if __name__ == '__main__':
    unittest.main()