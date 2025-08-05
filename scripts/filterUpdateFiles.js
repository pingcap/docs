import * as fs from "fs";
import path from "path";
import axios from "axios";
import { Octokit } from "octokit";
import { CLOUD_TOC_LIST, getAllCloudMdList } from "./utils.js";

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

// get the file list from the toc file
const getCloudTOCFiles = () => {
  const tmpTocFiles = getAllCloudMdList([
    "./tmp/TOC-tidb-cloud.md",
    "./tmp/TOC-tidb-cloud-starter.md",
    "./tmp/TOC-tidb-cloud-essential.md",
  ]);
  const tocFiles = getAllCloudMdList(CLOUD_TOC_LIST);

  // Convert to Set
  const tmpTocFilesSet = new Set(tmpTocFiles);
  const tocFilesSet = new Set(tocFiles);

  // Use tmpTocFiles if not empty, otherwise use tocFiles
  const finalTocFiles = tmpTocFilesSet.size > 0 ? tmpTocFilesSet : tocFilesSet;

  if (finalTocFiles.size === 0) {
    console.log(
      "Warning: No TOC file found or no files in TOC. All .md files will be processed."
    );
  }

  return finalTocFiles;
};

// filter the files in tmp directory by the toc file
const filterFilesByTOC = () => {
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

const main = async (isCloud = false) => {
  const { target: branchName, sha: base } = getLocalCfg();
  const targetBranchData = await ghGetBranch(branchName);
  const head = targetBranchData?.commit?.sha;
  const comparedDetails = await ghCompareCommits(base, head);
  const files = comparedDetails?.files || [];

  // first handle all files
  await handleFiles(files);

  // if it is cloud mode, filter the files by the toc
  if (isCloud) {
    filterFilesByTOC();
  }

  writeLocalCfg({
    target: branchName,
    sha: head,
  });
};

const args = process.argv.slice(2);
const isCloud = args.includes("--cloud");

main(isCloud);
