import * as fs from "fs";
import path from "path";

// Read the TOC file
const tocContent = fs.readFileSync("TOC-tidb-cloud.md", "utf8");

// Regular expression to match markdown links
const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;

// Set to store unique file paths
const filePaths = new Set();

// Extract all file paths from markdown links
let match;
while ((match = linkRegex.exec(tocContent)) !== null) {
  const filePath = match[2];

  // Skip external links (starting with http/https)
  if (filePath.startsWith("http")) {
    continue;
  }

  // Skip anchor links (starting with #)
  if (filePath.startsWith("#")) {
    continue;
  }

  // Remove leading slash if present
  const cleanPath = filePath.startsWith("/") ? filePath.slice(1) : filePath;

  // Skip files in tidb-cloud folder
  if (cleanPath.startsWith("tidb-cloud/")) {
    continue;
  }

  filePaths.add(cleanPath);
}

// Create tmp directory if it doesn't exist
const tmpDir = "tmp";
if (!fs.existsSync(tmpDir)) {
  fs.mkdirSync(tmpDir, { recursive: true });
}

// Copy files to tmp directory
let copiedCount = 0;
let skippedCount = 0;

for (const filePath of filePaths) {
  const sourcePath = filePath;
  const targetPath = path.join(tmpDir, filePath);

  // Create target directory if it doesn't exist
  const targetDir = path.dirname(targetPath);
  if (!fs.existsSync(targetDir)) {
    fs.mkdirSync(targetDir, { recursive: true });
  }

  // Check if source file exists
  if (fs.existsSync(sourcePath)) {
    try {
      fs.copyFileSync(sourcePath, targetPath);
      console.log(`✓ Copied: ${filePath}`);
      copiedCount++;
    } catch (error) {
      console.error(`✗ Error copying ${filePath}: ${error.message}`);
    }
  } else {
    console.log(`⚠ Skipped (not found): ${filePath}`);
    skippedCount++;
  }
}

console.log(`\nSummary:`);
console.log(`- Total files referenced: ${filePaths.size}`);
console.log(`- Files copied: ${copiedCount}`);
console.log(`- Files skipped: ${skippedCount}`);
console.log(`- Files copied to: ${tmpDir}/`);
