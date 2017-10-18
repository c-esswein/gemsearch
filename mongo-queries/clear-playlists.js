/**
 * Filter playlists: 
 *  - remove tracks without audio feature
 *  - remove playlists with less than N tracks
 * 
 * Store result in new collection.
 */
var audioTracks = db.getCollection('tmp_tracks_with_audio');
var storeColl = db.getCollection('tmp_playlists_cleaned');

var counter = 0;
var minTrackCount = 3;

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

   if (tracks.length > minTrackCount) {
       // store playlist
       playlist.tracks = tracks;
       storeColl.insert(playlist);
   }
});

print('counter');
print(counter);