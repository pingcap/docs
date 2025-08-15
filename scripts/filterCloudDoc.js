import {
  getAllCloudMdList,
  copySingleFileSync,
  copyFileWithCustomContentSync,
  copyDirectoryWithCustomContentSync,
  removeCustomContent,
} from "./utils.js";

const contentHandler = (content = "") => {
  return removeCustomContent("tidb-cloud", content);
};

const extractFilefromList = (
  fileList = [],
  inputPath = ".",
  outputPath = "."
) => {
  fileList.forEach((filePath) => {
    copyFileWithCustomContentSync(
      `${inputPath}/${filePath}`,
      `${outputPath}/${filePath}`,
      contentHandler
    );
  });
};

const main = () => {
  const allFilePaths = getAllCloudMdList();

  extractFilefromList(allFilePaths, "./", "./tmp");
  copySingleFileSync("TOC-tidb-cloud.md", "./tmp/TOC.md");
  copyDirectoryWithCustomContentSync(
    "./tidb-cloud/",
    "./tmp/tidb-cloud/",
    contentHandler
  );
};

main();
