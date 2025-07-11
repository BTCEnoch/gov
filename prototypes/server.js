const http = require('http');
const fs = require('fs');
const path = require('path');

const server = http.createServer((req, res) => {
    // Add CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    // Handle OPTIONS requests for CORS
    if (req.method === 'OPTIONS') {
        res.writeHead(204);
        res.end();
        return;
    }

    console.log('\n=== New Request ===');
    console.log('Original URL:', req.url);

    // Remove any path traversal attempts
    let filePath = path.normalize(req.url).replace(/^(\\.\\.[/\\\\])+/, '');
    console.log('Normalized path:', filePath);
    
    // Handle root path
    if (filePath === '/' || filePath === '') {
        filePath = '/index.html';
        console.log('Root path detected, serving:', filePath);
    }
    
    // Remove leading slash for local file path
    filePath = filePath.replace(/^\//, '');
    console.log('Final relative path:', filePath);

    // Check if we're requesting a file from pkg directory
    let fullPath;
    if (filePath.startsWith('pkg/')) {
        fullPath = path.join(__dirname, '..', filePath);
    } else {
        fullPath = path.join(__dirname, filePath);
    }
    console.log('Full resolved path:', fullPath);

    const extname = path.extname(filePath);
    let contentType = 'text/html';
    
    switch (extname) {
        case '.js':
            contentType = 'text/javascript';
            break;
        case '.wasm':
            contentType = 'application/wasm';
            break;
        case '.json':
            contentType = 'application/json';
            break;
        case '.png':
            contentType = 'image/png';
            break;
        case '.jpg':
        case '.jpeg':
            contentType = 'image/jpeg';
            break;
        case '.css':
            contentType = 'text/css';
            break;
    }
    console.log('Content type:', contentType);

    // Read and serve the file
    fs.readFile(fullPath, (error, content) => {
        if (error) {
            console.error('Error details:', error);
            if (error.code === 'ENOENT') {
                console.error(`File not found: ${fullPath}`);
                res.writeHead(404);
                res.end('File not found');
            } else {
                console.error(`Error reading file: ${error.code}`);
                console.error(error);
                res.writeHead(500);
                res.end(`Server error: ${error.code}`);
            }
            return;
        }

        // Special handling for WASM files
        if (extname === '.wasm') {
            res.setHeader('Content-Type', 'application/wasm');
            res.setHeader('Cross-Origin-Opener-Policy', 'same-origin');
            res.setHeader('Cross-Origin-Embedder-Policy', 'require-corp');
        } else {
            res.setHeader('Content-Type', contentType);
        }
        res.writeHead(200);
        res.end(content);
        console.log(`Successfully served ${filePath}`);
    });
});

const port = 3000;
server.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
    console.log(`Serving files from: ${__dirname}`);
    console.log(`WASM files from: ${path.join(__dirname, '..', 'pkg')}`);
}); 