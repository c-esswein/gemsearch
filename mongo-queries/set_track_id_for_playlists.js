var tracks = db.getCollection('tracks');
var playlists = db.getCollection('playlists');

playlists.find({}).forEach(function(playlist){ 
    playlist.tracks.forEach(function(pTrack) {
        var track = tracks.findOne({'uri': pTrack.track_uri});
        
        if (track) {
            pTrack.track_id = track._id;
        } else {
            print("Track not found: " + pTrack.track_uri + " for Playlist: " + playlist._id);
        }
    });
    
    playlists.update(
        { _id: playlist._id }, 
        { "$set": { "tracks": playlist.tracks } }
    );
});
