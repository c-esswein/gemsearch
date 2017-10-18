var playlists = db.getCollection('playlists');

playlists.aggregate(
   [
      { $unwind: "$tracks" },
      { $group: {_id: '$tracks.track_uri'} },
      //{ $count: "total_unique_tracks" }

      // find track in track db
      {
        $lookup:
            {
                from: 'tracks',
                localField: '_id',
                foreignField: 'uri',
                as: 'track'
            }
      },

      // find tracks without track data
      { $match : { track : { $size: 0 } } },

      // save in other collection
      { $out: "tmp_missing_tracks" }
   ]
)
