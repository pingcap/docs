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

const tocCopyTargets = [
  { src: "TOC-tidb-cloud.md", dest: "./tmp/TOC.md" },
  {
    src: "TOC-tidb-cloud-starter.md",
    dest: "./tmp/TOC-tidb-cloud-starter.md",
  },
  {
    src: "TOC-tidb-cloud-essential.md",
    dest: "./tmp/TOC-tidb-cloud-essential.md",
  },
  {
    src: "TOC-tidb-cloud-premium.md",
    dest: "./tmp/TOC-tidb-cloud-premium.md",
  },
];
const tocFiles = tocCopyTargets.map(({ src }) => src);

const main = () => {
  const filteredLinkList = getAllMdList(tocFiles);

  extractFilefromList(filteredLinkList, ".", "./tmp");

  tocCopyTargets.forEach(({ src, dest }) => copySingleFileSync(src, dest));
  copyDirectoryWithCustomContentSync(
    "./tidb-cloud/",
    "./tmp/tidb-cloud/",
    contentHandler
  );
};

main();
