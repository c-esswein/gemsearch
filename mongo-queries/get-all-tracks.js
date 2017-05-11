
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
      { $out: "found_tracks" }
   ]
)


// find tracks without audio

var tracks = db.getCollection('tmp_found_tracks');

tracks.aggregate(
   [
      {
          $project: {
            track : { $arrayElemAt: ['$track',0] }
         }
      },
      {
        $lookup:
            {
                from: 'audios',
                localField: 'track._id',
                foreignField: 'track_id',
                as: 'audio'
            }
      },
      // find tracks without audio data
      { $match : { audio : { $size: 0 } } },

      /*
      {
          $project: {
            track_id : "$track._id"
         }
      }, */
   ]
)


