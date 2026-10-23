# Claude 网络环境检查与搭建指南

面向 **Windows + Clash Verge Rev + 自有 VPS** 的中文教程，同时提供可交给 AI 执行的 Skill。

从真实搭建与排障中整理：先检查环境，再部署 sing-box + VLESS Reality，使用独立社区规则分流，最后验证 DNS、WebRTC、IPv6、节点故障和微信兼容性。仓库只含通用流程，不含作者的服务器、账号或连接凭据。

**解决可验证的网络问题，不保证账号不受限制，也不改变实际所在地或服务使用资格。** 使用前核对 [Anthropic 官方支持地区](https://www.anthropic.com/supported-countries) 与适用条款，以当时生效版本为准。

## 开始使用

把仓库地址交给能读文件、执行命令的 AI，并发送：

```text
请阅读本仓库 skills/claude-network-setup/SKILL.md。
先只读检查我的 Windows、Clash Verge 和 VPS，给我检查结果与修改范围。
国内和局域网直连；Claude 等指定服务及其 DNS 走自有 VPS；未知海外流量默认代理。
需要代理的连接在 VPS 故障时只能失败，不能回退直连。
保留 UDP、现有数据和国内应用兼容性，完成真实验收与回滚说明。
先不要安装或修改，等我确认方案后执行。密码让我在安全界面输入。
```

已审查并决定部署时，再明确授权执行。已有可用 VPS 不必重买；没有 VPS 可先看 [选购与推荐](docs/vps.md)。

## 教程路线

| 阶段 | 阅读内容 | 交付结果 |
|---|---|---|
| 1 | [环境检查](skills/claude-network-setup/references/environment.md) | 代理、DNS、IPv6、VPS 状态与缺项 |
| 2 | [VPS 部署](skills/claude-network-setup/references/server.md) | sing-box、Reality、管理通道与服务 |
| 3 | [Clash 与独立规则](skills/claude-network-setup/references/windows.md) | 本地 YAML、分流、DNS、TUN |
| 4 | [验收与回滚](skills/claude-network-setup/references/verification.md) | 出口、DNS、UDP、IPv6、故障测试 |
| 5 | [常见排障](skills/claude-network-setup/references/troubleshooting.md) | 微信等国内应用兼容性 |
| 可选 | [本地凭据清理](skills/claude-network-setup/references/privacy.md) | 精确清理，不误删当前登录 |

网络验收后，可阅读 [首次使用、Google 地区与隐私设置](docs/claude-first-run.md)。

## 流量如何分配

| 流量 | 连接 | DNS |
|---|---|---|
| 本地、局域网 | 直连 | 本地解析／适当例外 |
| 已识别国内服务 | 直连 | 国内加密 DNS |
| Claude／Anthropic 等保护域名 | 固定 VPS | 海外 DoH，经 VPS |
| 未匹配流量 | 固定 VPS | 默认海外 DoH，经 VPS |

采用 Johnshall 白名单并补充保护规则。原白名单含部分境外直连例外，不等于“所有境外一律代理”；应用前审阅是否符合需求。

## 容易误解的边界

1. **分流不是全局匿名。** 网页可能调用允许直连的国内端点获知真实出口。更严格的要求需另设计隔离环境或全代理，不能靠补几个域名作保证。
2. **节点故障保护不是系统断网锁。** 默认验收以 Clash 和 TUN 运行为前提，退出、开机间隙、切换网络另测。
3. **DNS 出口不必等于 VPS IP。** Cloudflare／Google DoH 可能显示解析器自身的递归出口，应核对查询路径，不只比较 IP。

## 安装 Skill

克隆后将整个 `skills/claude-network-setup` 目录复制到工具的 Skill 目录。Codex 通常为 `~/.codex/skills/`，Claude Code 通常为 `~/.claude/skills/`；先核对目标工具当前文档，不覆盖已修改的同名 Skill。

也可以不安装，直接让 AI 阅读 SKILL.md。支持调用的工具可使用：

```text
使用 $claude-network-setup，只读检查我的网络环境。
```

## 维护与来源

- [维护、更新和本地验证](docs/maintaining.md)
- [推荐链接与推广披露](docs/vps.md)
- [安全与隐私](SECURITY.md) · [贡献](CONTRIBUTING.md) · [来源与致谢](docs/sources.md)

脚本测试覆盖转换和配置不变量，不等于在所有版本上实机部署成功。上线仍需真实验收。

文档和自有脚本采用 [MIT License](LICENSE)。社区规则运行时下载，不随仓库复制分发，上游规则及软件遵循各自许可。本项目不是 Anthropic、Clash Verge 或 VPS 服务商官方项目。
