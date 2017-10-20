
dataFolder=../data/export
# --host $host

mongoimport --db dbis --collection playlists --file $dataFolder/playlists.json
mongoimport --db dbis --collection tracks --file $dataFolder/tracks.json
mongoimport --db dbis --collection artists --file $dataFolder/artists.json
mongoimport --db dbis --collection users --file $dataFolder/users.json
