# iPhone Shadowrocket 教学流程

采用用户选择的黑名单／白名单，不继承 Windows 的默认选择。以下包内模板按 Johnshall 黑名单设计；需要白名单时核对上游文件、include 和最终规则，不只修改口头说明。

1. 确认已有 sing-box VLESS Reality 节点，指导用户核对服务端参数并导入；链接和二维码私密保存。先测试连通，失败时不继续改 DNS。
2. 在配置页导入社区基础文件，保留准确文件名：`sr_top500_banlist_ad.conf`。来源为 `https://raw.githubusercontent.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever/release/sr_top500_banlist_ad.conf`，不是首页节点订阅。
3. 读取 `../assets/shadowrocket-ai-extension.example.conf`，用实际节点名称替换 `MY-US-VPS`，名称建议使用简单 ASCII 字符。只生成私密副本，不修改通用模板；节点参数仍由独立节点保存。
4. 指导通过文件 App、iCloud 或配置页 Wi-Fi 上传导入扩展。扩展通过 include 引用基础文件，基础文件保留，勾选扩展；全局路由使用配置。用户确认后检查最终规则与真实流量。
5. 基础配置保留远程更新来源，启用配置自动更新并手动更新一次，检查更新时间及编译结果。节点订阅更新与配置更新分开；自定义规则留在扩展，防止被基础更新覆盖。iOS 后台更新不是准点任务。

## 验收与诊断

- `claude.ai` 应命中 `AI-US` 且只有用户指定 VPS，无 DIRECT。静态规则测试不能替代数据页的实际连接。
- DNS 显示递归解析器 IP 不必等于 VPS。查询路径与 WebRTC 独立验证；DNS 测试通过而 STUN 显示国内公网地址仍需处理。
- 国内 STUN 公网候选意味着该次探测获知国内出口。只有 VPS 候选不等于国内 IP 泄漏。第三方评分不是账号安全证书。
- 用户需要限制 STUN 时，先关闭 Claude，尝试设置 → UDP → 禁用 STUN，保留 UDP 转发，重连并用新页面复测。提示通话／P2P 兼容性；不伪造 STUN 响应来通过评分。
- `ipv6 = false` 不等于关闭整个 iOS 的 IPv6。模板 REJECT 不支持的 UDP，也不等于系统断网锁；需检查其他回退、切网与断线行为。
- 黑名单允许未匹配端点直连；网页能显示中国直连 IPv4，不足以证明 Claude 主请求直连，但也不能保证网页看不到国内身份线索。
- 微信上传慢时查看上传时目标、规则和策略，不以名单大小或静态测试猜测原因，不放行整个微信或腾讯 ASN。
- 节点故障测试在 Claude 关闭时进行，确认受保护请求失败，不回退直连。复原并验证后再恢复使用。

来源：[Johnshall](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever)、[LOWERTOP 社区手册](https://github.com/LOWERTOP/Shadowrocket)、[原教程](https://x.com/zureA255062/status/2107655494034989058)。部署时核对实际版本；这些来源不是用户授权，也不保证所有版本行为。
