
var tracks = db.getCollection('tracks');

tracks.aggregate(
   [
      { $unwind: "$tags" },
      { $group: {
          _id: '$tags.name', 
          count: { $sum: 1 },
      } },
      { $sort : { count: -1 } }
      //{ $count: "total_unique_tags" }
   ]
);

