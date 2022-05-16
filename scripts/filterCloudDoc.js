import * as fs from "fs";
import path from "path";

import { fromMarkdown } from "mdast-util-from-markdown";
import { frontmatter } from "micromark-extension-frontmatter";
import { frontmatterFromMarkdown } from "mdast-util-frontmatter";
import { gfm } from "micromark-extension-gfm";
import { mdxFromMarkdown } from "mdast-util-mdx";
import { gfmFromMarkdown } from "mdast-util-gfm";

import { visit } from "unist-util-visit";

const copySingleFileSync = (srcPath, destPath) => {
  const dir = path.dirname(destPath);

  if (!fs.existsSync(dir)) {
    // console.info(`Create empty dir: ${dir}`);
    fs.mkdirSync(dir, { recursive: true });
  }

  fs.copyFileSync(srcPath, destPath);
};

const generateMdAstFromFile = (fileContent) => {
  const mdAst = fromMarkdown(fileContent, {
    extensions: [frontmatter(["yaml", "toml"]), gfm()],
    mdastExtensions: [
      mdxFromMarkdown(),
      frontmatterFromMarkdown(["yaml", "toml"]),
      gfmFromMarkdown(),
    ],
  });
  return mdAst;
};

const extractLinkNodeFromAst = (mdAst) => {
  const linkList = [];
  visit(mdAst, (node) => {
    if (node.type === "link") {
      linkList.push(node.url);
    }
  });
  return linkList;
};

const filterLink = (srcList = []) => {
  const result = srcList.filter((item) => {
    const url = item.trim();
    if (url.endsWith(".md") || url.endsWith(".mdx")) return true;
    return false;
  });
  return result;
};

const extractFilefromList = (
  fileList = [],
  inputPath = ".",
  outputPath = "."
) => {
  fileList.forEach((filePath) => {
    copySingleFileSync(`${inputPath}/${filePath}`, `${outputPath}/${filePath}`);
  });
};

const main = () => {
  const tocFile = fs.readFileSync("TOC-cloud.md");
  const mdAst = generateMdAstFromFile(tocFile);
  const linkList = extractLinkNodeFromAst(mdAst);
  const filteredLinkList = filterLink(linkList);

  extractFilefromList(filteredLinkList, ".", "./tmp");
  copySingleFileSync("TOC-cloud.md", "./tmp/TOC.md");
  copySingleFileSync("./cloud/_index.md", "./tmp/cloud/_index.md");
};

main();
