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

const ghGetFileContent = async (filePath, branchName = "master") => {
  try {
    const result = await octokit.request(
      `GET /repos/pingcap/docs/contents/${filePath}`,
      {
        owner: "pingcap",
        repo: "docs",
        path: filePath,
        ref: branchName,
      }
    );

    if (result.status === 200) {
      return result.data;
    }
  } catch (error) {
    console.error(`Error fetching file ${filePath}:`, error.message);
    return null;
  }
  return null;
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

// filter files by extension and whitelist
const filterFiles = (files) => {
  return files.filter((filename) => {
    // md files are always processed
    if (filename.endsWith(".md")) {
      return true;
    }

    // check if the file is in the whitelist
    return WHITELIST_FILENAMES.includes(filename);
  });
};

const handleFiles = async (fileList, branchName) => {
  console.log(`Processing ${fileList.length} files from branch: ${branchName}`);

  for (let filename of fileList) {
    console.log(`Processing file: ${filename}`);

    const fileData = await ghGetFileContent(filename, branchName);
    if (fileData && fileData.download_url) {
      await downloadFile(fileData.download_url, `tmp/${filename}`);
      console.log(`Downloaded: ${filename}`);
    } else {
      console.log(`Failed to download: ${filename}`);
    }
  }
};

const main = async (specifiedFiles = []) => {
  const { target: branchName } = getLocalCfg();
  console.log(`Target branch: ${branchName}`);

  if (specifiedFiles.length === 0) {
    console.error("Error: You must specify file_names");
    process.exit(1);
  }

  // filter files by extension and whitelist
  const filesToProcess = filterFiles(specifiedFiles);
  console.log(`Files to process: ${filesToProcess.length}`);
  console.log("Files:", filesToProcess);

  if (filesToProcess.length === 0) {
    console.log("No valid files to process");
    return;
  }

  // create tmp directory if it doesn't exist
  if (!fs.existsSync("tmp")) {
    fs.mkdirSync("tmp", { recursive: true });
  }

  // download all files
  await handleFiles(filesToProcess, branchName);

  console.log(`Successfully processed ${filesToProcess.length} files`);
};

const args = process.argv.slice(2);

// parse file names from --files argument
let specifiedFiles = [];
const filesIndex = args.indexOf("--files");
if (filesIndex !== -1 && filesIndex + 1 < args.length) {
  const filesArg = args[filesIndex + 1];
  specifiedFiles = filesArg
    .split(",")
    .map((file) => file.trim())
    .filter((file) => file.length > 0);
  console.log("Specified files:", specifiedFiles);
}

main(specifiedFiles);
