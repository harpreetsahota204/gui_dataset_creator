const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.static('.'));

// Ensure data directory exists
const dataDir = path.join(__dirname, 'data');
if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir);
}

// Save image endpoint
app.post('/save-image', (req, res) => {
    const { filename, data } = req.body;
    const base64Data = data.replace(/^data:image\/png;base64,/, '');
    
    fs.writeFile(path.join(dataDir, filename), base64Data, 'base64', (err) => {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            res.json({ success: true, path: path.join(dataDir, filename) });
        }
    });
});

// Save JSON endpoint
app.post('/save-json', (req, res) => {
    const { filename, data } = req.body;
    
    fs.writeFile(path.join(dataDir, filename), JSON.stringify(data, null, 2), (err) => {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            res.json({ success: true, path: path.join(dataDir, filename) });
        }
    });
});

// List files endpoint
app.get('/list-files', (req, res) => {
    fs.readdir(dataDir, (err, files) => {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            res.json({ files });
        }
    });
});

// Load dataset endpoint
app.get('/load-dataset', (req, res) => {
    const annotationPath = path.join(dataDir, 'annotations_coco.json');
    if (fs.existsSync(annotationPath)) {
        const data = JSON.parse(fs.readFileSync(annotationPath, 'utf8'));
        res.json(data);
    } else {
        res.status(404).json({ error: 'No dataset found' });
    }
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
    console.log(`Files will be saved to: ${dataDir}`);
});