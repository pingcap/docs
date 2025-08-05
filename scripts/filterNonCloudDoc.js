import {
  getFileList,
  copySingleFileSync,
  copyFileWithCustomContentSync,
  removeCustomContent,
} from "./utils.js";

const CLOUD_TOC_LIST = [
  "TOC-tidb-cloud.md",
  "TOC-tidb-cloud-essential.md",
  "TOC-tidb-cloud-starter.md",
];

const contentHandler = (content = "") => {
  return removeCustomContent("tidb", content);
};

const extractFilefromList = (
  fileList = [],
  inputPath = ".",
  outputPath = "."
) => {
  fileList.forEach((filePath = "") => {
    if (
      filePath.includes(`/tidb-cloud/`) ||
      CLOUD_TOC_LIST.includes(filePath)
    ) {
      return;
    }
    if (filePath.endsWith(".md")) {
      copyFileWithCustomContentSync(
        `${inputPath}/${filePath}`,
        `${outputPath}/${filePath}`,
        contentHandler
      );
    } else {
      try {
        copySingleFileSync(
          `${inputPath}/${filePath}`,
          `${outputPath}/${filePath}`
        );
      } catch (error) {}
    }
  });
};

const main = () => {
  const filteredLinkList = getFileList(".");

  extractFilefromList(filteredLinkList, ".", "./tmp");
};

main();
