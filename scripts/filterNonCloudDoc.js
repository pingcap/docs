import {
  getMdFileList,
  copySingleFileSync,
  copyFileWithCustomContentSync,
  removeCustomContent,
} from "./utils.js";

const contentHandler = (content = "") => {
  return removeCustomContent("tidb", content);
};

const extractFilefromList = (
  fileList = [],
  inputPath = ".",
  outputPath = "."
) => {
  fileList.forEach((filePath) => {
    if (
      filePath.includes(`/tidb-cloud/`) ||
      filePath.includes(`TOC-tidb-cloud.md`)
    ) {
      return;
    }
    copySingleFileSync(`${inputPath}/${filePath}`, `${outputPath}/${filePath}`);
    copyFileWithCustomContentSync(
      `${inputPath}/${filePath}`,
      `${outputPath}/${filePath}`,
      contentHandler
    );
  });
};

const main = () => {
  const filteredLinkList = getMdFileList(".");

  extractFilefromList(filteredLinkList, ".", "./tmp");
};

main();
