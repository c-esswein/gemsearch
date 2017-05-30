
var tracks = db.getCollection('tracks');
/*
var tags = tracks.aggregate(
   [
      { $unwind: "$tags" },
      { $group: {_id: '$tags.name'} },
      //{ $limit : 5 }
   ]
);*/

var tags = ["rock", "pop", "alternative", "indie", "Love", "male vocalists", "american", "alternative rock", 
"beautiful", "electronic", "Awesome", "classic rock", "female vocalists", "singer-songwriter", "Mellow", "indie rock", "chill", "00s",  "dance", "chillout", 
"british", "80s", "90s", "soul", "hard rock", "folk", "male vocalist", "oldies", "guitar", "acoustic", "jazz", "classic", "catchy", "easy listening", "70s", 
"party", "pop rock", "love at first listen", "Soundtrack", "sexy", "blues", "indie pop", "happy"];

var playlists = db.getCollection('playlists');
var resultCollection = db.getCollection('tmp_tag_count');
tags.forEach(function(tag) {
    var re = new RegExp(tag['_id'], "gi");
    var found = playlists.find({'name': re}).toArray();
    
    if (found.length > 0) {
        resultCollection.insert({
            tag: tag['_id'],
            count: found.length,
            playlists: found
        });
    }
});
