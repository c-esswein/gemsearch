
var audioTracks = db.getCollection('tmp_tracks_with_audio');
var storeColl = db.getCollection('tmp_playlists_counter');

var counter = 0;

db.getCollection('playlists').find({}).forEach(function(playlist) {
    counter++;
    
    playlist.missingCount = 0;
    playlist.validCount = 0;
    playlist.tracks.forEach(function(track) {
        if (!track.track_id) {
            playlist.missingCount++;
        } else {
            playlist.validCount++;
        }
   });

   storeColl.insert(playlist);
});

print('counter');
print(counter);