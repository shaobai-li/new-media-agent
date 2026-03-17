import os
from pathlib import Path
from openai import OpenAI
import subprocess
import json



client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY", "sk-b3dac126ee83430abd8075e0d612d119"), 
    base_url="https://api.deepseek.com"  
)

WORKSPACE = (Path.cwd() / "agent_workspace").resolve()


def _resolve_path(path: str) -> Path:
    """安全解析路径，限制在 workspace 内"""
    full_path = (WORKSPACE / path).resolve()
    if not full_path.is_relative_to(WORKSPACE.resolve()):
        raise ValueError("Path outside workspace not allowed")
    return full_path


def read_file(path: str) -> str:
    file_path = _resolve_path(path)
    if not file_path.exists():
        return f"Error: File {path} does not exist"
    try:
        return file_path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(path: str, content: str) -> str:
    file_path = _resolve_path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        file_path.write_text(content, encoding="utf-8")
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

def run_command(command: str) -> str:
    """在指定 WORKSPACE 下执行 Shell 命令"""
    try:
        # 强制设置 cwd=WORKSPACE，确保所有相对路径命令都在此目录下执行
        result = subprocess.run(
            command,
            shell=True,
            cwd=str(WORKSPACE), 
            capture_output=True,
            text=True,
            timeout=30,
        )
        
        output = result.stdout
        if result.stderr:
            output += f"\n[Standard Error]:\n{result.stderr}"
        
        if not output.strip():
            return "Command executed successfully (no output)."
        return output
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds."
    except Exception as e:
        return f"Error: {str(e)}"


tools = [
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Execute a shell command (e.g., ls, pip install, python script.py) within the workspace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The shell command to run."}
                },
                "required": ["command"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read contents of a file. Path relative to workspace.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file (creates dirs if needed).",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["path", "content"],
            },
        }
    },
]

tool_map = {
    "read_file": read_file,
    "write_file": write_file,
    "run_command": run_command,
}

def agent_loop():
    system_prompt = (
        f"You are a coding assistant. All your work MUST stay within the directory: {WORKSPACE}\n"
        "You can use 'run_command' to execute shell commands and 'write_file' to save code."
    )
    
    messages = [{"role": "system", "content": system_prompt}]
    print(f"Agent started. Workspace: {WORKSPACE}")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]: break
        
        messages.append({"role": "user", "content": user_input})

        while True:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                tools=tools
            )

            response_message = response.choices[0].message
            messages.append(response_message)

            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    f_name = tool_call.function.name
                    f_args = json.loads(tool_call.function.arguments)
                    
                    print(f"\n[Action] {f_name}: {f_args.get('command') or f_args.get('path')}")
                    result = tool_map[f_name](**f_args)
                    
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": f_name,
                        "content": str(result),
                    })
                continue 
            else:
                print(f"\nAgent: {response_message.content}")
                break

if __name__ == "__main__":
    agent_loop()

