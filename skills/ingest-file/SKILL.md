---
name: ingest-file
description: 将文件录入知识库：识别并校验用户上传的文件（支持 pdf、pptx、docx、md），解析为 Markdown 并生成 metadata（source 与 derived artifacts）。当用户上传文件、并提到提到“导入到知识库”、“入库”、“写到知识库”、“解析文档并导入知识库”等需求时使用。
---

# Ingest File（文件入库技能）

## 功能概述

该技能用于完成“文件 → 知识库”的标准化入库流程，包括：

- 文件识别校验和导入
- 

该技能属于**多步骤工作流自动化（Workflow Automation）**类型。

---

## 工作流程（严格按顺序执行）

**重要**：所有操作脚本运行都基于 workspace，禁止 cd 命令

### Step 1：文件识别校验和导入

使用命令:

python scripts/ingest_file.py --input path/to/file

一个正确的最终输出应该如下（JSON）：

{
  "valid": true,
  "file_type": "xxx",
  "size_bytes": 12345,
  "markdown_path": "/path/to/file.md",
  "media_dir": "/path/to/media"
}

**重要**：任何 valid=false 必须立即终止流程，不得进入解析步骤

