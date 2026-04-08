#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const fetchScript = path.resolve(__dirname, '..', '..', 'wechat-article-search', 'scripts', 'fetch_wechat_content.js');

if (!fs.existsSync(fetchScript)) {
  console.error(`Missing fetch script: ${fetchScript}`);
  process.exit(1);
}

const child = spawn(process.execPath, [fetchScript, ...process.argv.slice(2)], {
  stdio: 'inherit',
});

child.on('error', (error) => {
  console.error(error.message);
  process.exit(1);
});

child.on('exit', (code) => {
  process.exit(code ?? 0);
});
