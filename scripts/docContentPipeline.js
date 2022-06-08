import * as fs from "fs";
import path from "path";
import glob from "glob";

import { fromMarkdown } from "mdast-util-from-markdown";
import { frontmatter } from "micromark-extension-frontmatter";
import {
  frontmatterFromMarkdown,
  frontmatterToMarkdown,
} from "mdast-util-frontmatter";
import { gfm } from "micromark-extension-gfm";
import { gfmFromMarkdown, gfmToMarkdown } from "mdast-util-gfm";
import { mdxjs } from "micromark-extension-mdxjs";
import { mdxFromMarkdown, mdxToMarkdown } from "mdast-util-mdx";
import { toMarkdown } from "mdast-util-to-markdown";

import { visit } from "unist-util-visit";

import {
  copySingleFileSync,
  writeFileSync,
  getMdFileList,
  // generateMdAstFromFile,
  astNode2mdStr,
} from "./utils.js";

const myArgs = process.argv.slice(2);

const currentPlatform = myArgs[0] || "tidb";
const outputPath = myArgs[1] || "tmp";

const generateMdAstFromFile = (fileContent) => {
  const mdAst = fromMarkdown(fileContent, {
    extensions: [frontmatter(["yaml", "toml"]), gfm(), mdxjs()],
    mdastExtensions: [
      mdxFromMarkdown(),
      frontmatterFromMarkdown(["yaml", "toml"]),
      gfmFromMarkdown(),
    ],
  });
  return mdAst;
};

const handleCustomContentNode = (mdAst) => {
  visit(mdAst, (node) => {
    if (node.type === "mdxJsxFlowElement" && node?.name === "CustomContent") {
      // linkList.push(node.url);
      // console.log(node);
      const attributesList = node?.attributes?.length ? node?.attributes : [];
      const platformItem = attributesList.find((i) => i.name === "platform");
      const platformVal = platformItem?.value;
      if (platformVal !== currentPlatform) {
        node.type = "text";
        node.value = "";
      }
    }
  });
};

const handleMdFile = (filePath) => {
  const mdFileContent = fs.readFileSync(filePath);
  if (mdFileContent.includes(`<CustomContent`)) {
    const mdAst = generateMdAstFromFile(mdFileContent);
    handleCustomContentNode(mdAst);
    const newMdStr = astNode2mdStr(mdAst);
    return writeFileSync(`${outputPath}/${filePath}`, newMdStr);
  }
  return copySingleFileSync(filePath, `${outputPath}/${filePath}`);
};

const main = () => {
  const srcList = getMdFileList(".");
  // console.log(srcList);

  for (let file of srcList) {
    // console.log(a);
    handleMdFile(file);
  }
};

/**
 * This file is used to remove specified content in markdown, then apply to PDF.
 * 2022 Jun 7: Add CustomContent support, remove unmatch platform content (tidb/tidb-cloud)
 */
main();
