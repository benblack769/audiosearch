Objective:

Build a audio search engine.

Method:

1. Learn a audio embedding model.
2. Allow user to upload/select audio similar to desired.
3. Return ranked list of similar audio

### APIs

### Search API:

* Get audio mp3 by audio ID
* Upload audio

* Submit search
    * Selects learned model/comparator/other filters from list
    * Submits audio URL and weight
    * Gets back ranked audio files
* Get search options

### Embedding service API

* Get embedding with Audio ID
    * Result can be cached

### Nearest Neighbors DB

* Add key with value
* Query key

### Temp DB

* Upload file
* Download file

File will expire and be deleted after a certain length of time.

### Phase 1: Static database

Audio database can only be extended through a CLI interface

* Audio DB
	* Contents
		* Name
		* Hash
		* Expire
		* Audio
* Add to database CLI
* Learner CLI
* Embedding DB
	* Ranking query
	* Nearest neighbors query

### Phase 2: Adding to database via service


Replace add to database CLI with

* Preprocessing Service
	* Input: Name/hash of audio
	* Output: None
* Sequence DB
	* Contents
		* Name
		* Hash
		* Expire
* Sequence Evaluator Service
