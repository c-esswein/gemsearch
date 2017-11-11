/**
 * Iterates over all tracks and creates new album collection.
 * Album document contains album data and track array.
 */

var tracks = db.getCollection('tracks');
var albums = db.getCollection('albums');

var totalCounter = 0;

tracks.find({}).forEach(function(track) {
    totalCounter++;

    if (track.album) {
        // check if album exists
        var dbAlbum = albums.findOne({'uri': track.album.uri});
        if (dbAlbum) {
            // append track
            dbAlbum.tracks.push(track.uri);
            albums.update(
                { _id: dbAlbum._id },
                { "$set": { "tracks": dbAlbum.tracks } }
            );
        } else {
            // insert new album
            var newAlbum = track.album;
            newAlbum.tracks = [track.uri];
            albums.insert(newAlbum);
        }
    }
});

print('Total track counter: ' + totalCounter);
