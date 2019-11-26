from ApiRequests import ApiRequests
import requests
import requests_mock
import unittest
from unittest.mock import patch
import json

session = requests.Session()
adapter = requests_mock.Adapter()
session.mount('mock', adapter)

class TestApiMethods(unittest.TestCase):

	def testBuildUrl(self):
		url = ApiRequests.buildUrl(self, "artist", "Nirvana")
		self.assertEqual(url, 'https://api.deezer.com/artist/Nirvana/')

		url = ApiRequests.buildUrl(self, "artist", "415", "albums", 5)
		self.assertEqual(url, 'https://api.deezer.com/artist/415/albums/?limit=5')

		url = ApiRequests.buildUrl(self, "album", "116585992", "tracks")
		self.assertEqual(url, 'https://api.deezer.com/album/116585992/tracks/')

	def testGetArtistDetailsSuccess(self):
		sampleResp = "{'id': 415, 'name': 'Nirvana', 'link': 'https://www.deezer.com/artist/415', 'share': 'https://www.deezer.com/artist/415?utm_source=deezer&utm_content=artist-415&utm_term=0_1574766108&utm_medium=web', 'picture': 'https://api.deezer.com/artist/415/image', 'picture_small': 'https://cdns-images.dzcdn.net/images/artist/3ec5542ff520ee74e2befdaba32ef2ef/56x56-000000-80-0-0.jpg', 'picture_medium': 'https://cdns-images.dzcdn.net/images/artist/3ec5542ff520ee74e2befdaba32ef2ef/250x250-000000-80-0-0.jpg', 'picture_big': 'https://cdns-images.dzcdn.net/images/artist/3ec5542ff520ee74e2befdaba32ef2ef/500x500-000000-80-0-0.jpg', 'picture_xl': 'https://cdns-images.dzcdn.net/images/artist/3ec5542ff520ee74e2befdaba32ef2ef/1000x1000-000000-80-0-0.jpg', 'nb_album': 19, 'nb_fan': 7108710, 'radio': True, 'tracklist': 'https://api.deezer.com/artist/415/top?limit=50', 'type': 'artist'}"
		adapter.register_uri('GET', 'mock://https://api.deezer.com/artist/Nirvana/', json=sampleResp, status_code=200)
		resp = session.get('mock://https://api.deezer.com/artist/Nirvana/')
		respJson = resp.json()

		with patch('ApiRequests.ApiRequests.getArtistDetails') as getArtistDetailsMock:
			getArtistDetailsMock.return_value = respJson
			getArtistDetailsMock.status_code = 200

		result = getArtistDetailsMock(self, "Nirvana")

		getArtistDetailsMock.assert_called_with(self, "Nirvana") 

		self.assertEqual(result, resp.json())
		self.assertEqual(resp.status_code, 200)

	def testGetArtistDetailsInvalidName(self):
		sampleResp = "{'error': {'type': 'DataException','message': 'no data','code': 800}}"
		adapter.register_uri('GET', 'mock://https://api.deezer.com/artist/bbbb/', json=sampleResp, status_code=200)
		resp = session.get('mock://https://api.deezer.com/artist/bbbb/')
		respJson = resp.json()

		with patch('ApiRequests.ApiRequests.getArtistDetails') as getArtistDetailsMock:
			getArtistDetailsMock.return_value = None

		result = getArtistDetailsMock(self, "bbbb")

		getArtistDetailsMock.assert_called_with(self, "bbbb") 

		self.assertEqual(result, None)
		self.assertEqual(resp.status_code, 200)

	def testGetArtistAlbumsSuccess(self):
		sampleResp = "{'data':[{'id':'116585992','title':'MTVUnpluggedInNewYork(25thAnniversary–Live)','link':'https://www.deezer.com/album/116585992','cover':'https://api.deezer.com/album/116585992/image','cover_small':'https://cdns-images.dzcdn.net/images/cover/7e021a4689fd4c8d540e7f1ceadca925/56x56-000000-80-0-0.jpg','cover_medium':'https://cdns-images.dzcdn.net/images/cover/7e021a4689fd4c8d540e7f1ceadca925/250x250-000000-80-0-0.jpg','cover_big':'https://cdns-images.dzcdn.net/images/cover/7e021a4689fd4c8d540e7f1ceadca925/500x500-000000-80-0-0.jpg','cover_xl':'https://cdns-images.dzcdn.net/images/cover/7e021a4689fd4c8d540e7f1ceadca925/1000x1000-000000-80-0-0.jpg','genre_id':85,'fans':3502,'release_date':'2019-11-01','record_type':'album','tracklist':'https://api.deezer.com/album/116585992/tracks','explicit_lyrics':false,'type':'album'}],'total':19,'next':'https://api.deezer.com/artist/415/albums?limit=1&index=1'}"
		adapter.register_uri('GET', 'mock://https://api.deezer.com/artist/415/albums?limit=1', json=sampleResp, status_code=200)
		resp = session.get('mock://https://api.deezer.com/artist/415/albums?limit=1')
		respJson = resp.json()

		with patch('ApiRequests.ApiRequests.getArtistAlbums') as getArtistAlbumssMock:
			getArtistAlbumssMock.return_value = respJson

		result = getArtistAlbumssMock(self, "415", "Nirvana", 1)

		getArtistAlbumssMock.assert_called_with(self, "415", "Nirvana", 1)

		self.assertEqual(result, sampleResp)
		self.assertEqual(resp.status_code, 200)

	def testGetArtistAlbumsInvalidId(self):
		sampleResp = "{'data': [],'total': 0}"
		adapter.register_uri('GET', 'mock://https://api.deezer.com/artist/415555/albums?limit=1', json=sampleResp, status_code=200)
		resp = session.get('mock://https://api.deezer.com/artist/415555/albums?limit=1')
		respJson = resp.json()

		with patch('ApiRequests.ApiRequests.getArtistAlbums') as getArtistAlbumsMock:
			getArtistAlbumsMock.return_value = respJson

		result = getArtistAlbumsMock(self, "415555", "Nirvana", 1)

		getArtistAlbumsMock.assert_called_with(self, "415555", "Nirvana", 1)

		self.assertEqual(result, sampleResp)
		self.assertEqual(resp.status_code, 200)

	def testGetAlbumTracksSuccess(self):
		sampleResp = "{'data':[{'id':'771738022','readable':true,'title':'Rune','title_short':'Rune','title_version':','isrc':'GBKPL1971955','link':'https://www.deezer.com/track/771738022','duration':'209','track_position':1,'disk_number':1,'rank':'377991','explicit_lyrics':false,'explicit_content_lyrics':0,'explicit_content_cover':2,'preview':'https://cdns-preview-c.dzcdn.net/stream/c-ca5723a2ab397206428913d93c1296ba-4.mp3','artist':{'id':'1623786','name':'ClamsCasino','tracklist':'https://api.deezer.com/artist/1623786/top?limit=50','type':'artist'},'type':'track'}],'total':1}"
		adapter.register_uri('GET', 'mock://https://api.deezer.com/album/114253302/tracks', json=sampleResp, status_code=200)
		resp = session.get('mock://https://api.deezer.com/album/114253302/tracks')
		respJson = resp.json()

		with patch('ApiRequests.ApiRequests.getAlbumTracks') as getAlbumTracksMock:
			getAlbumTracksMock.return_value = respJson

		result = getAlbumTracksMock(self, "album", "771738022", "tracks")

		getAlbumTracksMock.assert_called_with(self, "album", "771738022", "tracks")

		self.assertEqual(result, sampleResp)
		self.assertEqual(resp.status_code, 200)

	def testGetAlbumTracksInvalidId(self):
		sampleResp = "{'error': {'type': 'DataException','message': 'no data','code': 800}"
		adapter.register_uri('GET', 'mock://https://api.deezer.com/album/1142533022/tracks', json=sampleResp, status_code=200)
		resp = session.get('mock://https://api.deezer.com/album/1142533022/tracks')
		respJson = resp.json()

		with patch('ApiRequests.ApiRequests.getAlbumTracks') as getAlbumTracksMock:
			getAlbumTracksMock.return_value = respJson

		result = getAlbumTracksMock(self, "album", "7717380222", "tracks")

		getAlbumTracksMock.assert_called_with(self, "album", "7717380222", "tracks")

		self.assertEqual(result, sampleResp)
		self.assertEqual(resp.status_code, 200)

if __name__ == '__main__':
    unittest.main()