import fs from 'fs';
import { Resvg } from '@resvg/resvg-js';
import path from 'path';

// 动态变量
const noteTitle = '#用到了AI的工作笔记#';
const number = 'NOTE: No. 1';
const title1 = '用AI从SOP一步步';
const title2 = '生成流程图';
const subtitle1 = '- 提示词要求提取节点';
const subtitle2 = '- AI生成Mermaid，再变流程图';
const date = 'DATE: 2025-06-13';

// const bgColor = '#fef9f6';DATE
const bgColor = '#ffffff';
const textColor = '#333';
const accentColor = '#6b7280';
const collectionsImagePath = './collections/mebrand_20250613_nobg.png';

const a = 50

// 读取SVG模板
if (!process.argv[2]) {
  console.error('请提供SVG模板文件路径作为命令行参数');
  process.exit(1);
}
const templatePath = process.argv[2];
let svg = fs.readFileSync(templatePath, 'utf-8');

// 替换模板中的变量
const variables = {
  bgColor,
  textColor,
  accentColor,
  collectionsImagePath,
  noteTitle,
  number,
  title1,
  title2,
  subtitle1,
  subtitle2,
  date,
  a
};

// 替换所有变量
for (const [key, value] of Object.entries(variables)) {
  const regex = new RegExp('\\${' + key + '}', 'g');
  svg = svg.replace(regex, value);
}

// 替换表达式 ${50 + a}
svg = svg.replace(/\${50 \+ a}/g, (50 + a).toString());
svg = svg.replace(/\${90 \+ a}/g, (90 + a).toString());
svg = svg.replace(/\${350 \+ a}/g, (350 + a).toString());
svg = svg.replace(/\${390 \+ a}/g, (390 + a).toString());
svg = svg.replace(/\${630 \+ a}/g, (630 + a).toString());
svg = svg.replace(/\${780 \+ a}/g, (780 + a).toString());

// 保存 SVG
fs.writeFileSync('page_cover1.svg', svg, 'utf-8');
console.log('✅ 已生成 page_cover1.svg');

const resvg = new Resvg(svg, {
  font: {
    loadSystemFonts: false, // 不加载系统字体
    fontFiles: ['./SmileySans-Oblique.ttf'], // 指定字体文件路径
  }
});
const pngBuffer = resvg.render().asPng();
fs.writeFileSync('page_cover1.png', pngBuffer);
console.log('✅ 已生成 page_cover1.png');