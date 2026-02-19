# Codex MCP 快速参考

## 常用命令

### 基础调用

```bash
# 简单任务
mcporter call codex-cli.codex "写个 Python 函数"

# 指定模型
mcporter call codex-cli.codex "任务" --args '{"model":"o3"}'

# 多轮对话
mcporter call codex-cli.codex "任务1" --args '{"sessionId":"my-task"}'
mcporter call codex-cli.codex "任务2" --args '{"sessionId":"my-task"}'

# 代码审查
mcporter call codex-cli.review --args '{"uncommitted":true}'
```

### 高级选项

```bash
# 自动执行
mcporter call codex-cli.codex "重构" --args '{"fullAuto":true, "sandbox":"workspace-write"}'

# 推理深度
mcporter call codex-cli.codex "分析" --args '{"reasoningEffort":"high"}'

# 工作目录
mcporter call codex-cli.codex "任务" --args '{"workingDirectory":"/path/to/project"}'
```

## 沙箱模式

| 模式 | 用途 | 风险 |
|-----|------|------|
| `read-only` | 分析、审查 | 无 |
| `workspace-write` | 写代码、测试 | 低 |
| `danger-full-access` | 系统操作 | 高 |

## 模型选择

| 任务 | 推荐 |
|-----|------|
| 代码生成 | `gpt-5.3-codex` |
| 复杂推理 | `o3` |
| 快速原型 | `gpt-4o` |
| 性能优化 | `o3` + `reasoningEffort:high` |

## 故障排除

```bash
# 测试连接
mcporter call codex-cli.ping

# 查看 session
mcporter call codex-cli.listSessions

# 重置 session
mcporter call codex-cli.codex "重新开始" --args '{"sessionId":"xxx", "resetSession":true}'
```

## 工作流示例

```bash
# 1. 分析
mcporter call codex-cli.codex "分析这个模块" --args '{"sessionId":"refactor"}'

# 2. 重构
mcporter call codex-cli.codex "重构这个模块" --args '{"sessionId":"refactor", "sandbox":"workspace-write"}'

# 3. 测试
mcporter call codex-cli.codex "写测试" --args '{"sessionId":"refactor"}'

# 4. 审查
mcporter call codex-cli.review --args '{"uncommitted":true}'
```
