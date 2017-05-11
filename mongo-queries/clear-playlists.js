
var audioTracks = db.getCollection('tmp_tracks_with_audio');
var storeColl = db.getCollection('tmp_playlists_cleaned');

var counter = 0;

db.getCollection('playlists').find({}).forEach(function(playlist) {
    counter++;
    
    var tracks = [];
    playlist.tracks.forEach(function(track) {
        if (track.track_id) {
            var audioForTrack = audioTracks.findOne({'_id': track.track_uri});
            if (audioForTrack) {
                tracks.push(track);
            }
        }
   });

   if (tracks.length > 3) {
       // store playlist
       playlist.tracks = tracks;
       storeColl.insert(playlist);
   }
});

print('counter');
print(counter);