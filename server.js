const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.static('.'));

// Ensure data directories exist
const dataDir = path.join(__dirname, 'data');
const sequenceDataDir = path.join(__dirname, 'sequence_data');

if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir);
}
if (!fs.existsSync(sequenceDataDir)) {
    fs.mkdirSync(sequenceDataDir);
}

// Save image endpoint
app.post('/save-image', (req, res) => {
    const { filename, data, folder = 'data' } = req.body;
    const base64Data = data.replace(/^data:image\/png;base64,/, '');
    
    // Determine target directory
    const targetDir = folder === 'sequence_data' ? sequenceDataDir : dataDir;
    
    fs.writeFile(path.join(targetDir, filename), base64Data, 'base64', (err) => {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            res.json({ success: true, path: path.join(targetDir, filename) });
        }
    });
});

// Save JSON endpoint
app.post('/save-json', (req, res) => {
    const { filename, data, folder = 'data' } = req.body;
    
    // Determine target directory
    const targetDir = folder === 'sequence_data' ? sequenceDataDir : dataDir;
    
    fs.writeFile(path.join(targetDir, filename), JSON.stringify(data, null, 2), (err) => {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            res.json({ success: true, path: path.join(targetDir, filename) });
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

// List folders endpoint
app.get('/list-folders', (req, res) => {
    const baseDir = __dirname;
    
    fs.readdir(baseDir, { withFileTypes: true }, (err, entries) => {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            // Filter for directories only and check if they contain annotation files
            const folders = [];
            
            entries.forEach(entry => {
                if (entry.isDirectory() && !entry.name.startsWith('.') && entry.name !== 'node_modules') {
                    const folderPath = path.join(baseDir, entry.name);
                    
                    // Check if folder contains any .json files (potential annotation files)
                    try {
                        const folderContents = fs.readdirSync(folderPath);
                        const hasJsonFiles = folderContents.some(file => file.endsWith('.json'));
                        const hasImages = folderContents.some(file => 
                            file.endsWith('.png') || file.endsWith('.jpg') || file.endsWith('.jpeg')
                        );
                        
                        if (hasJsonFiles || hasImages) {
                            const jsonFiles = folderContents.filter(file => file.endsWith('.json'));
                            const imageCount = folderContents.filter(file => 
                                file.endsWith('.png') || file.endsWith('.jpg') || file.endsWith('.jpeg')
                            ).length;
                            
                            folders.push({
                                name: entry.name,
                                path: folderPath,
                                jsonFiles: jsonFiles,
                                imageCount: imageCount,
                                hasAnnotations: hasJsonFiles,
                                hasImages: hasImages
                            });
                        }
                    } catch (folderErr) {
                        // Skip folders we can't read
                    }
                }
            });
            
            res.json({ folders });
        }
    });
});

// Load dataset from specific folder endpoint
app.get('/load-dataset-from-folder', (req, res) => {
    const { folderName, filename } = req.query;
    
    if (!folderName || !filename) {
        return res.status(400).json({ error: 'Folder name and filename are required' });
    }
    
    const folderPath = path.join(__dirname, folderName);
    const annotationPath = path.join(folderPath, filename);
    
    // Security check - ensure the folder is within our project directory
    if (!annotationPath.startsWith(__dirname)) {
        return res.status(403).json({ error: 'Access denied' });
    }
    
    if (fs.existsSync(annotationPath)) {
        try {
            const data = JSON.parse(fs.readFileSync(annotationPath, 'utf8'));
            res.json(data);
        } catch (parseErr) {
            res.status(500).json({ error: `Failed to parse JSON file: ${parseErr.message}` });
        }
    } else {
        res.status(404).json({ error: `No dataset found at ${annotationPath}` });
    }
});

// Load dataset endpoint
app.get('/load-dataset', (req, res) => {
    const { folder = 'data', filename = 'annotations_coco.json' } = req.query;
    
    // Determine source directory
    const sourceDir = folder === 'sequence_data' ? sequenceDataDir : dataDir;
    const annotationPath = path.join(sourceDir, filename);
    
    if (fs.existsSync(annotationPath)) {
        const data = JSON.parse(fs.readFileSync(annotationPath, 'utf8'));
        res.json(data);
    } else {
        res.status(404).json({ error: `No dataset found at ${annotationPath}` });
    }
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
    console.log(`Regular files will be saved to: ${dataDir}`);
    console.log(`Sequence files will be saved to: ${sequenceDataDir}`);
});