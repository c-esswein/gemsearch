# Gemsearch - Graph embedding music search

This repository contains the Python Gemsearch server module which provides:
* an music embedding mechanism which allows you to model the music ecosystem as heterogeneous graph and then create embeddings where proximities can be computed by the vector cosinus distance.

* a flexible query mechanism to search for music using those embedding

* an evaluation framework for those embeddings to evalute the performance on playlist track prediction and classic user-track recommendations

* a REST API to expose the query mechanisms


## Installation
The code is optimized for Python 3. 
Install python dependencies with running:

```
pip3 install -r requirements.txt
```

Copy the `.env.example` to create an environment file `.env` to adapt the following runtime parameters:

* `SLACK_API_TOKEN=token` A valid slack api token to send notifications about long running tasks
* `USE_WINDOWS_BASH=False` Set to true if you are running this package on a Windows computer. Linux executables (e.g. node2vec) are then executed with the Windows bash subsystem.
* `SPOTIFY_CLIENT_ID=id` A valid Spotify API client id to access the Spotify API.
* `SPOTIFY_CLIENT_SECRET=secret` A valid Spotify API secret to access the Spotify API.
* `LASTFM_API_KEY=key` A valid Last-fm API key.
* `GEMSEARCH_API_KEY=secret` A random API key to authorize special API routes (primary /api/reload_embedding which reloads the current embedding). The same token has to be used by the `Embedding service` to notify about a new embedding.
* `GEMSEARCH_API_URL=http://localhost:8080/api` The URL to the running Gemsearch API (used for the `Embedding service`).


To run the playlist evaluation and auto-suggest service, a running Elasticsearch database is required.


See `/gemsearch/runners/` for possible script entry points.

## Folder overview

For further explanations look at the README files within the folders.

* **data** This folder is used to store intermediate datasets and computed embeddings
* **deepwalk** A fork of the Deepwalk algorithm (https://github.com/phanein/deepwalk/) with adaptions for Python3 and to extend existing embeddings on the fly
* **gem** A fork of the GEM package (https://github.com/palash1992/GEM) with adaptions for Python3 and Bugfixes
* **gemsearch** The actual Gemsearch implementation (see Section *Gemsearch package*) as Python package
* **mongo-queries** MongoDB queries to mostly perform statistical analysis


## Gemsearch package

* **api** REST API to access the query service
* **core** Core classes to load and generate data
* **crawler** Different crawlers for Last.fm and Spotify
* **embedding** Classes to create, load and compute results on embeddings
* **evaluation** Evaluation methods
* **graph** Graph abstraction classes
* **query** methods to construct vector-queries out of unstructured text
* **runners** executable program entry points for specific tasks
* **services** Service runners for the API server
* **storage** Data-Wrapper classes to access MongoDB data and to an import script for csv playlist data
* **utils** Utility functions

