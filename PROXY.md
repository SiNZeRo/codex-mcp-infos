# Codex MCP 代理配置说明

## 配置位置

配置文件：`~/.claude.json`

## 代理设置

```json
{
  "mcpServers": {
    "codex-cli": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "codex-mcp-server"],
      "env": {
        "HTTP_PROXY": "http://127.0.0.1:8888",
        "HTTPS_PROXY": "http://127.0.0.1:8888",
        "http_proxy": "http://127.0.0.1:8888",
        "https_proxy": "http://127.0.0.1:8888"
      }
    }
  }
}
```

## 代理地址

- **HTTP_PROXY**: `http://127.0.0.1:8888`
- **HTTPS_PROXY**: `http://127.0.0.1:8888`

## 验证方法

```bash
# 测试连接
mcporter call codex-cli.ping

# 查看配置
cat ~/.claude.json | jq '.mcpServers["codex-cli"]'
```

## 注意事项

1. 确保 8888 端口代理服务正在运行
2. 代理需要支持 HTTP 和 HTTPS 流量
3. 如需修改代理地址，更新 `~/.claude.json` 中的 env 配置
4. 修改配置后需要重启 Claude Code

## 故障排除

### 问题：无法连接到 Codex API

**检查：**
1. 代理服务是否运行：`curl -x http://127.0.0.1:8888 https://api.openai.com`
2. 配置是否正确：`cat ~/.claude.json | jq '.mcpServers["codex-cli"].env'`
3. Claude Code 是否重启

### 问题：代理超时

**解决：**
- 检查代理服务状态
- 尝试使用其他代理端口
- 检查防火墙设置

## 相关文档

- [README.md](./README.md) - 主文档
- [QUICKREF.md](./QUICKREF.md) - 快速参考
- [COMPARISON.md](./COMPARISON.md) - 方案对比
