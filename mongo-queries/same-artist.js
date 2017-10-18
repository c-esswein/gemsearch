/**
 * Find playlists with tracks from only one artist.
 */

var tracks = db.getCollection('tracks');
var playlists = db.getCollection('playlists');

var totalCounter = 0;
var missingTrackCounter = 0;
var sameArtistCounter = 0;
var goodPlaylistCtr = 0;

playlists.find({}).forEach(function(playlist){ 
    totalCounter++;

    var artist = null;
    var sameArtist = true;
    var validTrackCounter = 0;

    playlist.tracks.forEach(function(pTrack) {
        var track = tracks.findOne({'uri': pTrack.track_uri});
        
        if (track) {
            var trackArtist = track.artists[0].id;
            validTrackCounter++;

            if (!artist) {
                artist = trackArtist;
            } else {
                sameArtist = sameArtist && (artist == trackArtist);
            }
            
        } else {
            missingTrackCounter++;
        }
    });

    if (sameArtist) {
        sameArtistCounter++;
    }

    if (!sameArtist && validTrackCounter > 3) {
        goodPlaylistCtr++;
    }
});

print('Total: ' + totalCounter);
print('Missing: ' + missingTrackCounter);

print('Same Artists: ' + sameArtistCounter);
print('goodPlaylistCtr: ' + goodPlaylistCtr);