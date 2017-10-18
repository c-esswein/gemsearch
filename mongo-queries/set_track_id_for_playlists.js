/**
 * Set track id for tracks in playlists.
 */

var tracks = db.getCollection('tracks');
var playlists = db.getCollection('playlists');

var totalCounter = 0;
var missingCounter = 0;
playlists.find({}).forEach(function(playlist){ 
    totalCounter++;

    playlist.tracks.forEach(function(pTrack) {
        var track = tracks.findOne({'uri': pTrack.track_uri});
        
        if (track) {
            pTrack.track_id = track._id;
        } else {
            print("Track not found: " + pTrack.track_uri + " for Playlist: " + playlist._id);
            missingCounter++;
        }
    });
    
    playlists.update(
        { _id: playlist._id }, 
        { "$set": { "tracks": playlist.tracks } }
    );
});

print('Total: ' + totalCounter);
print('Missing: ' + missingCounter);
