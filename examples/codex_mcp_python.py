#!/usr/bin/env python3
"""
Codex MCP Server - Python Version
使用 FastMCP + uvloop 实现，性能接近 TypeScript 版本
"""

from fastmcp import FastMCP
import subprocess
import asyncio
import uvloop
from typing import Optional
import os

# 设置代理（如果需要）
os.environ.setdefault("HTTP_PROXY", "http://127.0.0.1:8888")
os.environ.setdefault("HTTPS_PROXY", "http://127.0.0.1:8888")

# 启用 uvloop（性能提升 2-4x）
uvloop.install()

mcp = FastMCP("Codex MCP 🚀")

# Session 存储（简单实现）
sessions = {}

@mcp.tool
async def codex(
    prompt: str,
    session_id: Optional[str] = None,
    model: str = "gpt-5.3-codex",
    reasoning_effort: Optional[str] = None,
    sandbox: str = "read-only"
) -> str:
    """
    Execute Codex CLI with prompt (async version)

    Args:
        prompt: The coding task or question
        session_id: Optional session ID for multi-turn conversation
        model: Model to use (gpt-5.3-codex, o3, gpt-4o, etc.)
        reasoning_effort: Reasoning depth (none/minimal/low/medium/high/xhigh)
        sandbox: Sandbox policy (read-only/workspace-write/danger-full-access)

    Returns:
        Codex execution result
    """
    # 构建命令
    cmd = ["codex", "exec", "--skip-git-repo-check", "-c", prompt]

    if model:
        cmd.extend(["-m", model])

    if reasoning_effort:
        cmd.extend(["--reasoning-effort", reasoning_effort])

    if sandbox:
        cmd.extend(["--sandbox", sandbox])

    # 异步执行（不阻塞事件循环）
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()

    # 处理结果
    if proc.returncode != 0:
        error_msg = stderr.decode() if stderr else "Unknown error"
        return f"❌ Error: {error_msg}"

    result = stdout.decode()

    # 保存到 session（如果指定）
    if session_id:
        if session_id not in sessions:
            sessions[session_id] = []
        sessions[session_id].append({"prompt": prompt, "result": result})

    return result

@mcp.tool
async def review(
    uncommitted: bool = True,
    base: Optional[str] = None
) -> str:
    """
    Review code changes using Codex

    Args:
        uncommitted: Review uncommitted changes
        base: Base branch/commit for comparison (e.g., 'main', 'HEAD~3')

    Returns:
        Code review results
    """
    cmd = ["codex", "review"]

    if uncommitted:
        cmd.append("--uncommitted")
    elif base:
        cmd.extend(["--base", base])

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        return f"❌ Error: {stderr.decode()}"

    return stdout.decode()

@mcp.tool
def list_sessions() -> str:
    """
    List all active sessions

    Returns:
        List of session IDs and their turn counts
    """
    if not sessions:
        return "No active sessions"

    result = "📋 Active Sessions:\n"
    for session_id, turns in sessions.items():
        result += f"  • {session_id}: {len(turns)} turns\n"

    return result

@mcp.tool
def ping() -> str:
    """Test server connection"""
    return "pong 🏓"

if __name__ == "__main__":
    # 启动 MCP server
    mcp.run()
