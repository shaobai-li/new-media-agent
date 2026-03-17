import asyncio
from crawler_client import XHSClient
import json
import time

async def main():
    async with XHSClient() as client:
        note_res = await client.get_note_by_keyword("web3", 1, 20)
        print("# 打印结果...")
        print(note_res)

        print("# 获取笔记列表...")
        note_list = []
        for note_item in note_res.get("items", {}):
            if note_item.get("model_type") not in ("rec_query", "hot_query"):
                print(f"正在获取笔记 {note_item.get('id')}")
                note = await client.get_note_by_id(note_item.get("id"), note_item.get("xsec_source"), note_item.get("xsec_token"))
                note_list.append(note)
        
        print("# 保存笔记列表...")
            
        filename_note_markdown = f"note_list_output_{int(time.time())}.md"
        with open(filename_note_markdown, "w", encoding="utf-8") as md_file:
            for i, note in enumerate(note_list):
                title = note.get("title", "")
                desc = note.get("desc", "")
                md_file.write(f"## 【笔记{i+1}】{title}\n")
                md_file.write(f"{desc}\n\n")

        input("# 按任意键退出...")
        print("# 退出...")

asyncio.run(main())