import * as fs from "fs";
import path from "path";
import axios from "axios";
import { Octokit } from "octokit";

const GH_TOKEN = process.env.GH_TOKEN || "";

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

const parseTOCFile = (tocPath) => {
  try {
    const tocContent = fs.readFileSync(tocPath, "utf8");
    const lines = tocContent.split("\n");
    const filePaths = new Set();

    for (const line of lines) {
      const linkMatch = line.match(/\[([^\]]+)\]\(\/([^)]+)\)/);
      if (linkMatch) {
        const filePath = linkMatch[2];
        if (filePath.endsWith(".md")) {
          filePaths.add(filePath);
        }
      }
    }

    console.log(`Found ${filePaths.size} files in TOC: ${tocPath}`);
    return filePaths;
  } catch (error) {
    console.error(`Error parsing TOC file ${tocPath}:`, error);
    return new Set();
  }
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
  fs.rmSync(targetFile);
};

const handleFiles = async (fileList = [], tocFilePaths) => {
  console.log(`Processing ${fileList.length} files...`);

  const addedModifiedFiles = fileList.filter((file) => {
    if (!file.filename.endsWith(".md")) {
      return false;
    }
    if (file.status === "added" || file.status === "modified") {
      return tocFilePaths.has(file.filename);
    }
    if (file.status === "removed") {
      return true;
    }
    if (file.status === "renamed") {
      return tocFilePaths.has(file.filename);
    }
    return false;
  });

  console.log(`Filtered to ${addedModifiedFiles.length} files to process`);

  for (let file of addedModifiedFiles) {
    const { status, raw_url, filename, previous_filename } = file;
    console.log(`Processing: ${filename} (${status})`);

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

const TOC_FILE_PATH = "./TOC-tidb-cloud.md";

const main = async () => {
  const { target: branchName, sha: base } = getLocalCfg();
  const targetBranchData = await ghGetBranch(branchName);
  const head = targetBranchData?.commit?.sha;
  const comparedDetails = await ghCompareCommits(base, head);
  const files = comparedDetails?.files || [];

  const tocFilePaths = parseTOCFile(TOC_FILE_PATH);

  handleFiles(files, tocFilePaths);
  writeLocalCfg({
    target: branchName,
    sha: head,
  });
};

main();
