import * as fs from "fs";
import path from "path";
import axios from "axios";
import { Octokit } from "octokit";

const GH_TOKEN = process.env.GH_TOKEN || "";

// whitelist files: allow download non-md files
const WHITELIST_FILENAMES = ["variables.json"];

const octokit = GH_TOKEN
  ? new Octokit({
      auth: GH_TOKEN,
    })
  : new Octokit();

const getLocalCfg = () => {
  const fileContent = fs.readFileSync("./latest_translation_commit.json");
  const data = JSON.parse(fileContent);
  return data;
};

const writeLocalCfg = (cfg) => {
  const data = JSON.stringify(cfg);
  fs.writeFileSync("./latest_translation_commit.json", data);
};

const ghGetBranch = async (branchName = "master") => {
  const result = await octokit.request(
    `GET /repos/pingcap/docs/branches/${branchName}`,
    {
      owner: "pingcap",
      repo: "docs",
      branch: branchName,
    }
  );
  if (result.status === 200) {
    const data = result.data;
    return data;
  }
  throw new Error(`ghGetBranch error: ${result}`);
};

const ghCompareCommits = async (base = "", head = "") => {
  const basehead = `${base}...${head}`;
  const result = await octokit.request(
    `GET /repos/pingcap/docs/compare/${basehead}`,
    {
      owner: "pingcap",
      repo: "docs",
      basehead,
    }
  );
  if (result.status === 200) {
    const data = result.data;
    return data;
  }
  throw new Error(`ghGetBranch error: ${result}`);
};

const downloadFile = async (url, targetPath) => {
  const response = await axios({
    method: "GET",
    url,
    responseType: "stream",
  });
  const dir = path.dirname(targetPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  // pipe the result stream into a file on disc
  response.data.pipe(fs.createWriteStream(targetPath));
  // return a promise and resolve when download finishes
  return new Promise((resolve, reject) => {
    response.data.on("end", () => {
      resolve();
    });

    response.data.on("error", () => {
      reject();
    });
  });
};

const deleteFile = (targetFile) => {
  try {
    if (fs.existsSync(targetFile)) {
      fs.rmSync(targetFile);
    }
  } catch (error) {
    console.error(`Error deleting file ${targetFile}:`, error);
  }
};

// read toc file and parse the file paths
const parseTOCFile = (tocPath) => {
  try {
    if (!fs.existsSync(tocPath)) {
      console.log(`TOC file not found: ${tocPath}`);
      return new Set();
    }

    const content = fs.readFileSync(tocPath, "utf8");
    const filePaths = new Set();

    // use regex to match the file paths in markdown links
    // match [text](path) format
    const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
    let match;

    while ((match = linkRegex.exec(content)) !== null) {
      const link = match[2];
      // only process links ending with .md
      if (link.endsWith(".md")) {
        // remove ./ or / at the beginning to ensure path consistency
        const normalizedPath = link.replace(/^\.?\//, "");
        filePaths.add(normalizedPath);
      }
    }

    console.log(`Found ${filePaths.size} files in TOC: ${tocPath}`);
    if (filePaths.size > 0) {
      console.log(
        "Files in TOC:",
        Array.from(filePaths).slice(0, 5).join(", "),
        filePaths.size > 5 ? `... and ${filePaths.size - 5} more` : ""
      );
    }
    return filePaths;
  } catch (error) {
    console.error(`Error parsing TOC file ${tocPath}:`, error);
    return new Set();
  }
};

// get the file list from the toc file
const getCloudTOCFiles = () => {
  // check ./tmp/TOC-tidb-cloud.md first
  const tmpTocPath = "./tmp/TOC-tidb-cloud.md";
  const localTocPath = "TOC-tidb-cloud.md";

  let tocFiles = parseTOCFile(tmpTocPath);

  // if not found in /tmp, check the current directory
  if (tocFiles.size === 0) {
    console.log(`No files found in ${tmpTocPath}, trying ${localTocPath}`);
    tocFiles = parseTOCFile(localTocPath);
  }

  if (tocFiles.size === 0) {
    console.log(
      "Warning: No TOC file found or no files in TOC. All .md files will be processed."
    );
  }

  return tocFiles;
};

// filter the files in tmp directory by the toc file
const filterFilesByTOC = (isInit = false) => {
  console.log("Filtering files in tmp directory by TOC...");

  // get the file list from the toc file
  const tocFiles = getCloudTOCFiles();

  if (tocFiles.size === 0) {
    console.log("No TOC files found, keeping all files in tmp directory");
    return;
  }

  // get all .md files in the tmp directory
  const tmpDir = "tmp";
  if (!fs.existsSync(tmpDir)) {
    console.log("tmp directory does not exist");
    return;
  }

  const getAllFiles = (dir) => {
    const files = [];
    const items = fs.readdirSync(dir);

    for (const item of items) {
      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);

      if (stat.isDirectory()) {
        files.push(...getAllFiles(fullPath));
      } else if (item.endsWith(".md")) {
        files.push(fullPath);
      }
    }

    return files;
  };

  const tmpFiles = getAllFiles(tmpDir);
  let deletedCount = 0;
  let keptCount = 0;

  for (const filePath of tmpFiles) {
    // get the relative path to the tmp directory
    const relativePath = path.relative(tmpDir, filePath);

    // only check markdown files, non-markdown files are kept
    if (relativePath.endsWith(".md")) {
      // if isInit is true and the file is in tidb-cloud directory, delete it
      if (isInit && relativePath.startsWith("tidb-cloud/")) {
        console.log(`Deleting tidb-cloud file during init: ${relativePath}`);
        deleteFile(filePath);
        deletedCount++;
        continue;
      }

      // check if the markdown file is in the toc
      if (tocFiles.has(relativePath)) {
        console.log(`Keeping markdown file in TOC: ${relativePath}`);
        keptCount++;
      } else {
        console.log(`Deleting markdown file not in TOC: ${relativePath}`);
        deleteFile(filePath);
        deletedCount++;
      }
    } else {
      // non-markdown files are kept
      console.log(`Keeping non-markdown file: ${relativePath}`);
      keptCount++;
    }
  }

  console.log(
    `\nTOC Filter Summary: Kept ${keptCount} files, deleted ${deletedCount} files`
  );
};

const handleFiles = async (fileList = []) => {
  console.log(fileList);
  for (let file of fileList) {
    const { status, raw_url, filename, previous_filename } = file;

    // check if the file should be processed
    const shouldProcessFile = () => {
      // md files are always processed
      if (filename.endsWith(".md")) {
        return true;
      }

      // check if the file is in the whitelist
      return WHITELIST_FILENAMES.includes(filename);
    };

    if (!shouldProcessFile()) {
      continue;
    }

    switch (status) {
      case "added":
      case "modified":
        await downloadFile(raw_url, `tmp/${filename}`);
        break;
      case "removed":
        deleteFile(filename);
        break;
      case "renamed":
        deleteFile(previous_filename);
        await downloadFile(raw_url, `tmp/${filename}`);
        break;
    }
  }
};

const main = async (isCloud = false, isInit = false) => {
  const { target: branchName, sha: base } = getLocalCfg();
  const targetBranchData = await ghGetBranch(branchName);
  const head = targetBranchData?.commit?.sha;
  const comparedDetails = await ghCompareCommits(base, head);
  const files = comparedDetails?.files || [];

  // first handle all files
  await handleFiles(files);

  // if it is cloud mode, filter the files by the toc
  if (isCloud) {
    filterFilesByTOC(isInit);
  }

  writeLocalCfg({
    target: branchName,
    sha: head,
  });
};

const args = process.argv.slice(2);
const isCloud = args.includes("--cloud");
// for cloud mode, we only need update files not in the tidb-cloud directory
const isInit = args.includes("--init");

main(isCloud, isInit);
