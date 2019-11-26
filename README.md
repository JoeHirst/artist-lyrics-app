# artist-lyrics-app
Python CLI app for retrieving lyric data and producing stats

Versioning
------------
The app uses python 3.6.8


Setup guide
-------------

Clone Project
	
	git clone https://github.com/JoeHirst/artist-lyrics-app.git
	cd artist-lyrics-app

It is recommended that you create a ``virtualenv`` before installing dependencies

	virtualenv env
	source /env/bin/activate 

Now install the dependencies with

	pip install -r requirements.txt

Running the app
-----------------

To run the app simply run the following command in the cloned driectory::

	python ArtistLyricsApp.py

Two optional parameters can be provided to skip the prompts when the app starts:
- The first being artist name which must be wrapped in quotes if it contains spaces
- The second being how many albums the search should be limited by, 0 will give the max 
	
	``python ArtistLyricsApp.py <artistname> <limit>``

If run without parameters, they can be provided when prompted


Running the tests
-------------------

To run the tests simply use the following command

	python -m unittest