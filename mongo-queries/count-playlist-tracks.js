var playlists = db.getCollection('playlists');

playlists.aggregate(
   [
      {
         $project: {
            key: 1,
            numberOfTracks: { $size: "$tracks" }
         }
      },
      {
        $group : {
            _id: "$numberOfTracks",
            count: { $sum: 1 },
            playLists: {$push: "$key"}
        }
      },
      { $sort : { count : -1 } }
   ]
)

/**
 * 12 tracks are most common.
 * in 1332 playlists
 */



// count total amount of tracks
var playlists = db.getCollection('tmp_playlists_cleaned');

playlists.aggregate(
   [
      {
         $project: {
            key: 1,
            numberOfTracks: { $size: "$tracks" }
         }
      },
      {
        $group : {
            _id: null,
            count: { $sum: "$numberOfTracks" },
        }
      }
   ]
)