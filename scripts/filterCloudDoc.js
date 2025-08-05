import {
  getAllMdList,
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

const CLOUD_TOC_LIST = [
  "TOC-tidb-cloud.md",
  "TOC-tidb-cloud-essential.md",
  "TOC-tidb-cloud-starter.md",
];

const main = () => {
  // Get all MD lists from each TOC file and deduplicate
  const allFilteredLinkLists = CLOUD_TOC_LIST.map((tocFile) =>
    getAllMdList(tocFile)
  );
  const flattenedList = allFilteredLinkLists.flat();
  const filteredLinkList = [...new Set(flattenedList)]; // Deduplicate

  extractFilefromList(filteredLinkList, ".", "./tmp");
  copySingleFileSync("TOC-tidb-cloud.md", "./tmp/TOC.md");
  copyDirectoryWithCustomContentSync(
    "./tidb-cloud/",
    "./tmp/tidb-cloud/",
    contentHandler
  );
};

main();
