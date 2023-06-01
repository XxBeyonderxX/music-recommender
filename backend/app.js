const express = require('express');
const path = require('node:path');
const { spawn } = require('child_process');
const bodyParser = require('body-parser');
const ejs = require('ejs');

const app = express();

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static(path.join(__dirname, '..', 'frontend')));

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, '..', 'frontend'));

app.get("/", (req, res) => {
    // res.sendFile(path.join(__dirname, '..', 'frontend', 'index.html'))
    res.render("index", { artist: [], tracks: [], stop: false });
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
            res.render("index", { artist: artist, tracks: tracks, stop: true });
        } else {
            console.error('Child process exited with code', code);
            res.send("failed")
        }
    });
});

app.listen(3000, () => {
    console.log('Server started at port:3000');
})
