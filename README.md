# Codex MCP Server 总结文档

> 📅 创建时间：2026-02-18
> 🎯 目标：让 Claude Code 能调用 Codex CLI，实现"干完活写说明"的自动化

---

## 📊 方案对比

### 方案一览

| 项目 | ⭐ Stars | 语言 | 特点 | 推荐度 | 状态 |
|------|---------|------|------|--------|------|
| **[tuannvm/codex-mcp-server](https://github.com/tuannvm/codex-mcp-server)** | 233 | TypeScript | 功能最全、结构化输出、Session 管理 | ⭐⭐⭐⭐⭐ | ⚡ 活跃 |
| [leonardsellem/codex-specialized-subagents](https://github.com/leonardsellem/codex-specialized-subagents) | 46 | TypeScript | 子 agent 系统、自动技能选择 | ⭐⭐⭐⭐ | ⚡ 新项目 |
| [leonardsellem/codex-subagents-mcp](https://github.com/leonardsellem/codex-subagents-mcp) | 150 | JavaScript | 子 agent (reviewer/debugger/security) | ⭐⭐⭐ | ⚠️ 已归档 |
| [w31r4/codex-mcp-go](https://github.com/w31r4/codex-mcp-go) | 47 | Go | 单文件部署、并发支持、中文文档 | ⭐⭐⭐⭐ | ⚡ 活跃 |
| [missdeer/codex-mcp-rs](https://github.com/missdeer/codex-mcp-rs) | 17 | Rust | Rust 实现、性能优秀 | ⭐⭐⭐ | 🔵 一般 |

---

## 🎯 最终选择：tuannvm/codex-mcp-server

### 选择理由

1. **社区最活跃**（233 stars）
2. **功能最完整**：
   - ✅ 结构化输出（带说明文档）
   - ✅ Session 多轮对话
   - ✅ 代码审查工具
   - ✅ 多模型支持（o3/gpt-5/gpt-4o）
   - ✅ 沙箱模式（安全执行）
   - ✅ 自动执行模式（fullAuto）

3. **开箱即用**：`npx -y codex-mcp-server`
4. **文档完善**：有 API 文档、Session 管理文档
5. **持续维护**：最近仍在活跃更新

### 备选方案

- **追求简洁部署** → 选 `w31r4/codex-mcp-go`（单二进制文件）
- **需要多个专门 agent** → 选 `codex-specialized-subagents`（有 reviewer/debugger/security）

---

## 🚀 安装方法

### 前置要求

```bash
# 1. 安装 Codex CLI
npm i -g @openai/codex

# 2. 配置 API Key
codex login --api-key "your-openai-api-key"
```

### 安装 MCP Server

**方式 1：自动配置（推荐）**

```bash
# 使用 Claude Code 命令
claude mcp add codex-cli -- npx -y codex-mcp-server
```

**方式 2：手动配置**

编辑 `~/.claude.json`，添加：

```json
{
  "mcpServers": {
    "codex-cli": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "codex-mcp-server"]
    }
  }
}
```

### 验证安装

```bash
# 测试连接
mcporter call codex-cli.ping

# 查看工具列表
mcporter list codex-cli --schema
```

---

## 📚 使用方法

### 可用工具

1. **codex** - 主力工具（代码生成/分析/重构）
2. **review** - 代码审查
3. **listSessions** - 查看活跃会话
4. **ping** - 测试连接

### 基础用法

**在 Claude Code 中直接说：**
```
用 codex 重构这个函数
让 codex 写个测试
用 codex 分析这段代码的性能问题
```

**通过 mcporter CLI：**

```bash
# 简单调用
mcporter call codex-cli.codex "写个 Python 快排"

# 指定模型
mcporter call codex-cli.codex "优化这段代码" --args '{"model":"o3"}'

# 多轮对话（保持上下文）
mcporter call codex-cli.codex "写个二叉树" --args '{"sessionId":"tree"}'
mcporter call codex-cli.codex "加上遍历方法" --args '{"sessionId":"tree"}'
mcporter call codex-cli.codex "写单元测试" --args '{"sessionId":"tree"}'

# 代码审查（uncommitted changes）
mcporter call codex-cli.review --args '{"uncommitted":true}'

# 代码审查（branch diff）
mcporter call codex-cli.review --args '{"base":"main"}'
```

### 高级用法

**1. 自动执行模式（fullAuto）**
```bash
# 自动执行，不需要人工确认
mcporter call codex-cli.codex "重构并优化这个模块" \
  --args '{"fullAuto":true, "sandbox":"workspace-write"}'
```

**2. 沙箱模式**
```bash
# read-only: 只读，不能修改文件
mcporter call codex-cli.codex "分析这个项目" \
  --args '{"sandbox":"read-only"}'

# workspace-write: 只在 workspace 目录写
mcporter call codex-cli.codex "写个测试文件" \
  --args '{"sandbox":"workspace-write"}'

# danger-full-access: 完全访问（危险！）
mcporter call codex-cli.codex "系统级操作" \
  --args '{"sandbox":"danger-full-access"}'
```

**3. 推理深度控制**
```bash
# 设置推理深度（none < minimal < low < medium < high < xhigh）
mcporter call codex-cli.codex "分析这个算法复杂度" \
  --args '{"reasoningEffort":"high"}'
```

**4. 指定工作目录**
```bash
mcporter call codex-cli.codex "重构这个项目" \
  --args '{"workingDirectory":"/path/to/project"}'
```

---

## 💡 最佳实践

### 1. Session 管理

**场景：多步骤任务**

```bash
# 第一步：分析
mcporter call codex-cli.codex "分析这个模块的问题" \
  --args '{"sessionId":"refactor-auth"}'

# 第二步：重构
mcporter call codex-cli.codex "重构这个模块" \
  --args '{"sessionId":"refactor-auth"}'

# 第三步：测试
mcporter call codex-cli.codex "写测试用例" \
  --args '{"sessionId":"refactor-auth"}'

# 查看所有 session
mcporter call codex-cli.listSessions

# 重置 session
mcporter call codex-cli.codex "重新开始" \
  --args '{"sessionId":"refactor-auth", "resetSession":true}'
```

### 2. 模型选择

| 任务类型 | 推荐模型 | 理由 |
|---------|---------|------|
| 代码生成 | `gpt-5.3-codex` | 默认，最平衡 |
| 复杂推理 | `o3` | 推理能力强 |
| 快速原型 | `gpt-4o` | 速度快、成本低 |
| 性能优化 | `o3` + `reasoningEffort:high` | 深度分析 |

### 3. 沙箱策略

| 沙箱模式 | 适用场景 | 风险 |
|---------|---------|------|
| `read-only` | 代码分析、审查 | 无风险 |
| `workspace-write` | 日常开发、写测试 | 低风险 |
| `danger-full-access` | 系统级操作 | ⚠️ 高风险 |

**建议：**
- 默认使用 `read-only` 或 `workspace-write`
- 只在必要时使用 `danger-full-access`
- 重要操作先用 `read-only` 分析，再用 `workspace-write` 执行

### 4. 代码审查工作流

```bash
# 1. 审查 uncommitted changes
mcporter call codex-cli.review --args '{"uncommitted":true}'

# 2. 审查当前分支相对 main 的改动
mcporter call codex-cli.review --args '{"base":"main"}'

# 3. 审查特定 commit
mcporter call codex-cli.review --args '{"base":"HEAD~3"}'
```

---

## 🔧 故障排除

### 问题 1：调用超时

**原因：** Codex CLI 响应慢或网络问题

**解决：**
```bash
# 增加超时时间
mcporter call codex-cli.codex "任务" --timeout 60000

# 或使用更快的模型
mcporter call codex-cli.codex "任务" --args '{"model":"gpt-4o"}'
```

### 问题 2：Session 丢失

**原因：** MCP server 重启会清空 session

**解决：**
- 避免在长任务中重启 server
- 重要任务完成后及时保存结果
- 使用 `listSessions` 监控活跃 session

### 问题 3：权限问题

**错误：** `EACCES: permission denied`

**解决：**
```bash
# 检查 Codex CLI 权限
which codex
codex --version

# 重新登录
codex login --api-key "your-key"
```

### 问题 4：找不到 codex 命令

**解决：**
```bash
# 检查 PATH
echo $PATH

# 重新安装
npm i -g @openai/codex

# 确认安装路径
which codex
```

---

## 📖 参考资源

- **项目主页：** https://github.com/tuannvm/codex-mcp-server
- **API 文档：** https://github.com/tuannvm/codex-mcp-server/blob/main/docs/api-reference.md
- **Session 管理：** https://github.com/tuannvm/codex-mcp-server/blob/main/docs/session-management.md
- **Codex CLI 文档：** https://github.com/openai/codex-cli
- **MCP 协议：** https://modelcontextprotocol.io

---

## 🎓 学习路径

### 初级（入门）

1. ✅ 安装 Codex CLI 和 MCP Server
2. ✅ 测试 `ping` 工具
3. ✅ 简单代码生成任务
4. ✅ 代码审查（uncommitted）

### 中级（日常使用）

1. ✅ Session 多轮对话
2. ✅ 模型选择（o3 vs gpt-5.3）
3. ✅ 沙箱模式控制
4. ✅ 指定工作目录

### 高级（自动化）

1. ✅ fullAuto 自动执行
2. ✅ 推理深度调优
3. ✅ 集成到 CI/CD
4. ✅ 自定义工作流

---

## 🎯 实战案例

### 案例 1：重构遗留代码

```bash
# Step 1: 分析
mcporter call codex-cli.codex "分析这个模块的代码质量问题" \
  --args '{"sessionId":"refactor-legacy", "model":"o3", "reasoningEffort":"high"}'

# Step 2: 制定计划
mcporter call codex-cli.codex "制定重构计划，保持向后兼容" \
  --args '{"sessionId":"refactor-legacy"}'

# Step 3: 逐步重构
mcporter call codex-cli.codex "重构第一部分：数据层" \
  --args '{"sessionId":"refactor-legacy", "sandbox":"workspace-write"}'

# Step 4: 写测试
mcporter call codex-cli.codex "为重构的部分写测试" \
  --args '{"sessionId":"refactor-legacy"}'

# Step 5: 审查改动
mcporter call codex-cli.review --args '{"uncommitted":true}'
```

### 案例 2：快速原型开发

```bash
# 快速生成原型
mcporter call codex-cli.codex "写个 FastAPI 后端，包含用户认证和 CRUD" \
  --args '{"model":"gpt-4o", "fullAuto":true, "sandbox":"workspace-write"}'
```

### 案例 3：性能优化

```bash
# 深度分析
mcporter call codex-cli.codex "分析这个算法的性能瓶颈，给出优化方案" \
  --args '{"model":"o3", "reasoningEffort":"xhigh", "sandbox":"read-only"}'
```

---

## 📝 总结

**为什么选择 codex-mcp-server？**
- ✅ 最成熟、最稳定
- ✅ 功能最全（结构化输出、session、审查）
- ✅ 社区最活跃（233 stars）
- ✅ 开箱即用（npx 一键启动）

**核心优势：**
1. **结构化输出** - 干完活自动写说明
2. **Session 管理** - 多轮对话保持上下文
3. **多模型支持** - 根据任务选模型
4. **沙箱安全** - 控制权限范围
5. **自动执行** - 无需人工确认

**适用场景：**
- 日常开发（写代码、测试、重构）
- 代码审查（uncommitted、branch diff）
- 性能优化（深度推理分析）
- 快速原型（自动执行）

**注意事项：**
- 重要操作先用 `read-only` 分析
- 避免在长任务中重启 server
- 合理选择模型（平衡成本和质量）
- 善用 session 管理复杂任务

---

## 🚀 快速开始

```bash
# 1. 安装
npm i -g @openai/codex
codex login --api-key "your-key"

# 2. 配置 Claude Code
claude mcp add codex-cli -- npx -y codex-mcp-server

# 3. 测试
mcporter call codex-cli.ping

# 4. 开始使用
mcporter call codex-cli.codex "你的第一个任务"
```

**祝你使用愉快！🎉**
