/**
 * Find playlists with equal track array.
 * 
 * - per playlist: calculate hash of all track_uri's
 * - find duplicate hashes
 */

// calculate hash

var playlists = db.getCollection('playlists');
var counter = 0;

playlists.find({}).forEach(function(playlist){ 
    counter = counter + 1;

    var trackNames = '';
    playlist.tracks.forEach(function(track) {
        trackNames += track.track_uri;
    });

    playlists.update(
        { _id: playlist._id }, 
        { "$set": { "tracksHash": hex_md5(trackNames) } }
    );
});

print("counter:")
print(counter)


return;

// find duplicate
var playlists = db.getCollection('playlists');

playlists.aggregate(
   [
      {
        $group : {
            _id: "$tracksHash",
            count: { $sum: 1 },
            playLists: {$push: "$key"}
        }
      },
      { $match : { count : { $gt: 1 } } },
      //{ $sort : { count : -1 } }
      
      {
        $group : {
            _id: null,
            totalCount: { $sum: 1 },
            avgCount: { $avg: "$count" },
            minCount: { $min: "$count" },
            maxCount: { $max: "$count" },
        }
      },
   ]
)
