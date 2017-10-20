
dataFolder=../data/export

mongoexport --db dbis --collection playlists --out $dataFolder/playlists.json
mongoexport --db dbis --collection tracks --out $dataFolder/tracks.json
mongoexport --db dbis --collection artists --out $dataFolder/artists.json
mongoexport --db dbis --collection users --out $dataFolder/users.json
