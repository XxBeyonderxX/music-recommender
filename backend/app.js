const express = require('express');
const path = require('node:path');
const { spawn } = require('child_process');
const bodyParser = require('body-parser');
const ejs = require('ejs');

const SpotifyWebApi = require('spotify-web-api-node');
const dotenv = require('dotenv');

dotenv.config();

const clientId = process.env.SPOTIFY_CLIENT_ID;
const clientSecret = process.env.SPOTIFY_CLIENT_SECRET;

const spotifyApi = new SpotifyWebApi({ clientId, clientSecret });

const app = express();

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static(path.join(__dirname, '..', 'frontend')));

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, '..', 'frontend'));

app.get("/", (req, res) => {
    // res.sendFile(path.join(__dirname, '..', 'frontend', 'index.html'))
    res.render("index", { artist: [], tracks: [], stop: false, track_id: [] });
})

app.post("/", (req, res) => {
    // console.log(req.body);

    let details;
    let value;
    for (const key in req.body) {
        details = key.split(" ");
        value = req.body[key];
    }

    const input = value;
    // console.log(input);
    const clickedSpan = details[1];
    // console.log(clickedSpan);

    let route = `based_on_${clickedSpan}.py`;
    // console.log('route', route);

    // It is the same command if you wanted to write it in a shell to run the based_on_topic.py 
    const python = spawn('python', [path.join(__dirname, '..', 'model', route), input]);

    // This event is emitted when the script prints something in the console 
    // and returns a buffer that collects the output data.
    // to convert the buffer data to a readable form, we used data.toString() method 
    let output;

    python.stdout.on('data', (data) => {
        output = data.toString();
        // console.log(output);
    });

    // The 'close' event is emitted when the stdio streams of a child process have been closed.
    python.on('close', (code) => {
        // res.send(recommendedList)
        if (code === 0) {
            const result = JSON.parse(output);
            const artist = result.artist;
            const tracks = result.tracks;
            // console.log('Artist:', artist);
            // console.log('Tracks:', tracks);
            // res.send(`successful`)
            let tracks_id = [];
            (async function () {
                for (let i = 0; i < 5; i++) {
                    try {
                        const trackId = await getTrackId(tracks[i], artist[i]);
                        if (trackId) {
                            // console.log(trackId);
                            tracks_id.push(`https://open.spotify.com/track/${trackId}`);
                        } else {
                            console.log('No track found with the given track name and artist name.', i);
                            tracks_id.push('https://open.spotify.com/track/x');
                        }
                    } catch (error) {
                        console.log('Error:', error);
                    }
                }
                // console.log(tracks_id);
                res.render("index", { artist: artist, tracks: tracks, stop: true, track_id: tracks_id });
            })();
        } else {
            console.error('Child process exited with code', code);
            res.send("failed")
        }
    });
});

app.listen(3000, () => {
    console.log('Server started at port:3000');
})

async function getTrackId(trackName, artistName) {
    try {
        // Retrieve an access token
        const data = await spotifyApi.clientCredentialsGrant();
        const accessToken = data.body['access_token'];

        // Set the access token on the SpotifyWebApi instance
        spotifyApi.setAccessToken(accessToken);

        // Search for the track
        const query = `track:${trackName} artist:${artistName}`;
        const response = await spotifyApi.searchTracks(query, { limit: 1 });

        // Extract the track ID from the response
        if (response.body.tracks.items.length > 0) {
            const trackId = response.body.tracks.items[0].id;
            return trackId;
        }
        return null;
    } catch (error) {
        console.log('Error retrieving track ID:', error);
        return null;
    }
}