# CLAUDE.md

> 🤖 这个文件用于 Claude Code 助手理解和贡献这个项目

---

## 项目定位

这是一个关于 **Codex MCP Server** 的实践文档仓库，目标是：

1. **通用实践指南** - 帮助开发者选择和使用 Codex MCP Server
2. **公开知识共享** - 提供方案对比、最佳实践、实战案例
3. **持续维护更新** - 随着项目发展更新内容

---

## 项目结构

```
.
├── README.md          # 主文档（安装、使用、最佳实践）
├── QUICKREF.md        # 快速参考手册
├── COMPARISON.md      # 5个方案详细对比
└── CLAUDE.md          # 本文件（项目说明）
```

---

## 如何使用这个仓库

### 对于初学者

1. 阅读 `README.md` 了解 Codex MCP Server 是什么
2. 查看 `COMPARISON.md` 选择适合的方案
3. 参考 `QUICKREF.md` 快速上手

### 对于贡献者

- **发现问题？** 提 Issue
- **有改进建议？** 提 PR
- **想补充内容？** 欢迎贡献！

---

## 内容规范

### ✅ 应该包含的内容

- 通用的安装步骤
- 标准的配置方法
- 最佳实践和设计模式
- 故障排除指南
- 实战案例和示例代码
- 工具对比和选型建议

### ❌ 不应该包含的内容

- 个人 API Keys 或密钥
- 本地路径（如 `/home/username/`）
- 内网地址或私有服务
- 特定环境配置
- 敏感信息

---

## 维护原则

1. **保持通用性** - 内容适用于大多数场景
2. **避免硬编码** - 使用占位符或通用示例
3. **及时更新** - 跟进上游项目变化
4. **验证准确性** - 确保命令和步骤可执行
5. **文档质量** - 清晰、简洁、易读

---

## 贡献指南

### 提交前检查

- [ ] 内容是否通用？（不依赖特定环境）
- [ ] 命令是否可执行？（经过测试）
- [ ] 格式是否规范？（Markdown 语法正确）
- [ ] 是否有敏感信息？（API keys、路径等）

### 提交规范

```
<type>: <subject>

<body>

<footer>
```

**Type:**
- `docs`: 文档更新
- `fix`: 修正错误
- `feat`: 新增内容
- `refactor`: 重构内容
- `chore`: 杂项更新

**示例:**
```
docs: 添加 Session 管理最佳实践

- 补充 session 生命周期说明
- 添加常见问题解决方案
- 优化代码示例

Closes #12
```

---

## 技术栈

- **核心工具：** Codex CLI + MCP Server
- **实现语言：** TypeScript (tuannvm/codex-mcp-server)
- **部署方式：** npx / npm

---

## 参考资源

- **Codex MCP Server:** https://github.com/tuannvm/codex-mcp-server
- **Codex CLI:** https://github.com/openai/codex-cli
- **MCP 协议:** https://modelcontextprotocol.io
- **Claude Code:** https://claude.ai/code

---

## 常见问题

### Q: 这个仓库是官方的吗？

**A:** 不是。这是个人整理的实践文档，基于开源项目 tuannvm/codex-mcp-server。

### Q: 内容是否准确？

**A:** 力求准确，但建议参考官方文档验证。如有问题请提 Issue。

### Q: 可以直接复制命令吗？

**A:** 大部分命令可以直接使用，但需要替换占位符（如 API keys、路径等）。

### Q: 如何保持更新？

**A:** 关注上游项目，定期同步最新变化。可以 Watch 这个仓库获取更新通知。

---

## 许可证

MIT License - 自由使用、修改、分享

---

## 联系方式

- **Issues:** 用于报告问题或建议
- **Pull Requests:** 欢迎贡献代码或文档
- **Discussions:** 一般性讨论（如果启用）

---

**最后更新：** 2026-02-18
**维护状态：** 活跃维护
**贡献者：** 欢迎加入
