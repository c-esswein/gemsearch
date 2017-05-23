
var counter = 0;

db.getCollection('playlists').find({}).forEach(function(playlist) {
    counter++;
    
    playlist.tracks.forEach(function(track) {
        if (!track.track_id) {
            print(track.track_uri);
        }
   });
});

print('counter');
print(counter);