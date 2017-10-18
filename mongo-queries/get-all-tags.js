/**
 * Aggregate all tags and store them in new collection.
 */

var tracks = db.getCollection('tracks');

tracks.aggregate(
   [
      { $unwind: "$tags" },
      { $group: {
          _id: '$tags.name', 
          count: { $sum: 1 },
      } },
      //{ $sort : { count: -1 } },
      { $out: "tmp_tags" }
      //{ $count: "total_unique_tags" }
   ]
);

