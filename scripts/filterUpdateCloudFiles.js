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

// 读取 TOC 文件并解析其中的文件路径
const parseTOCFile = (tocPath) => {
  try {
    if (!fs.existsSync(tocPath)) {
      console.log(`TOC file not found: ${tocPath}`);
      return new Set();
    }

    const content = fs.readFileSync(tocPath, "utf8");
    const filePaths = new Set();

    // 使用正则表达式匹配 markdown 链接中的文件路径
    // 匹配 [text](path) 格式的链接
    const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
    let match;

    while ((match = linkRegex.exec(content)) !== null) {
      const link = match[2];
      // 只处理以 .md 结尾的链接
      if (link.endsWith(".md")) {
        // 移除开头的 ./ 或 / 以确保路径一致性
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

// 获取 TOC 文件中的文件列表
const getTOCFiles = () => {
  // 优先检查 ./tmp/TOC-tidb-cloud.md
  const tmpTocPath = "./tmp/TOC-tidb-cloud.md";
  const localTocPath = "TOC-tidb-cloud.md";

  let tocFiles = parseTOCFile(tmpTocPath);

  // 如果 /tmp 中没有找到，则检查当前目录
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

const handleFiles = async (fileList = []) => {
  console.log(`Processing ${fileList.length} files...`);

  for (let file of fileList) {
    const { status, raw_url, filename, previous_filename } = file;
    if (!filename.endsWith(".md")) {
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

// 根据 TOC 文件过滤 tmp 目录中的文件
const filterFilesByTOC = () => {
  console.log("Filtering files in tmp directory by TOC...");

  // 获取 TOC 文件中的文件列表
  const tocFiles = getTOCFiles();

  if (tocFiles.size === 0) {
    console.log("No TOC files found, keeping all files in tmp directory");
    return;
  }

  // 获取 tmp 目录中的所有 .md 文件
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
    // 获取相对于 tmp 目录的路径
    const relativePath = path.relative(tmpDir, filePath);

    // 检查文件是否在 TOC 中
    if (tocFiles.has(relativePath)) {
      console.log(`Keeping file in TOC: ${relativePath}`);
      keptCount++;
    } else {
      console.log(`Deleting file not in TOC: ${relativePath}`);
      deleteFile(filePath);

      deletedCount++;
    }
  }

  console.log(
    `\nTOC Filter Summary: Kept ${keptCount} files, deleted ${deletedCount} files`
  );
};

const main = async () => {
  const { target: branchName, sha: base } = getLocalCfg();
  const targetBranchData = await ghGetBranch(branchName);
  const head = targetBranchData?.commit?.sha;
  const comparedDetails = await ghCompareCommits(base, head);
  const files = comparedDetails?.files || [];

  // 先处理所有文件
  await handleFiles(files);

  // 然后根据 TOC 过滤
  filterFilesByTOC();

  writeLocalCfg({
    target: branchName,
    sha: head,
  });
};

main();
