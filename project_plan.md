Objective:

Build a audio search engine.

Method:

1. Learn a audio embedding model.
2. Allow user to upload/select audio similar to desired.
3. Return ranked list of similar audio

### APIs

### Search API:

* Get audio mp3 by audio ID
* Search initiate (Post)
	* Generates new search ID
    * Can happen as page loads, no need for user to wait for this to complete to start filling out form, only for form to be successfully sent.
* Update search criterion
    * Selects learned model from list
    * Selects any metadata filters
        * dataset name
        * author
        * title
* Upload audio mp3 for search
    * Inputs:
        * Search ID
        * audio mp3 file
    * Returns
        * Audio ID
* Set weight of audio ID in search
    * Inputs:
        * Search ID
        * audio ID
        * weight
* Get current ranking
    * Inputs:
        * Search ID
    * Returns
        * List of
            * Audio ID
* Get current search criterion/weights
* Automatically deletes search, uploaded audio IDs when search expires

### Embedding service API

* Get embedding with Audio ID
    * Result can be cached

### Nearest Neighbors DB

* Add key with value
* Query key

### Audio DB

* Private API
    * Add audio file/metadata return ID
* Public API
    * Get file via ID
    * Get metadata

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
