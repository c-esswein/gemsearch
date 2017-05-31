
var tracks = db.getCollection('tracks');

tracks.aggregate(
   [
      { $unwind: "$artists" },
      { $group: {_id: '$artists.id', 'artist': {$first: '$artists'}} },
      {
         $replaceRoot: { newRoot: "$artist" }
       },
      { $out: "artists" }
   ]
)
