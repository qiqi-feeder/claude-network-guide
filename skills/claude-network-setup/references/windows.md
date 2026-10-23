# Windows：独立 YAML、规则与 DNS

## 生成客户端

需要 Python 3.10+ 与仓库根目录 requirements.txt。把私密节点参数放仓库外，例如系统用户自己的私密目录。

节点 JSON 的示例见仓库根目录 `examples/node.example.json`。其中是不可用的文档地址与示例认证值，必须使用自己的真实参数。构建器会拒绝示例节点，只有测试时才能用 `--allow-example`。

在克隆仓库根目录运行：

```powershell
python -m pip install -r requirements.txt
python skills/claude-network-setup/scripts/build_client.py --node C:\private\node.json --output outputs\clash.yaml --mihomo "C:\Program Files\Clash Verge\verge-mihomo.exe" --data-dir "$env:APPDATA\io.github.clash-verge-rev.clash-verge-rev"
```

默认下载明确列出的 Johnshall 白名单及其已审核 AppleNews 引用，保存来源哈希和构建日期。也可用 `--source-file` 与 `--nested-file` 读取已经取得的本地快照。不接受未知规则类型、未知动作或未经审核的新外部规则源。

`--mihomo` 会做真实配置语法校验，仍不会应用配置；若不提供则仅完成结构生成，不能报告成内核校验通过。配置与来源清单原子替换，失败保留旧输出；上线前另备份实际配置。

## 导入与持久化

推荐通过 Clash Verge 的本地文件导入新增独立配置并选择它，原机场配置留作备用。不要猜测用户 profile UID 或直接复制本仓库作者的数据目录。自动操作时先读当前结构；如需编辑注册信息，备份、校验并确保应用不会覆盖写入。

订阅更新可能覆盖生成文件，真正持久化的修改应写入本地源配置或适配当前版本的覆写入口。只改 clash-verge.yaml 不算交付完成。

## 分流与 DNS

- 固定 US-VPS 组只有自建节点，最后 MATCH 走该组；无 DIRECT 备用。
- 保留社区广告规则顺序，再在通用直连之前加入 Claude 等保护域名和关键词。上游广告拦截可能误伤功能，具体条目要通过实测决定例外，不一键放行整个广告列表。
- 国内白名单可直连，也含少量境外例外；展示边界。IP、GEOIP 添加 no-resolve，避免未知域名为匹配国内规则而先解析。
- 默认海外 DoH 明确使用 `#US-VPS`；国内解析例外使用 `#DIRECT`。保护域名明确指定海外解析，直连解析遵循域名 DNS 策略。源是 IP 时不需要再对 VPS 名称作引导解析。
- Fake-IP 地址不是泄漏证据。DNS 查询显示 Cloudflare/Google 递归 IP 是正常可能结果。

## TUN 与 IPv6

开启 TUN 自动路由、严格路由、接口探测和 TCP/UDP 53 接管。IPv6 网络存在时，确保双栈路由进入 TUN，再按相同策略分流；国内 IPv6 可直连，Claude 与未知海外路径仍走 VPS。不得全局拒绝 IPv6 来冒充防泄漏。

Verge 可能自动修改 dns.ipv6 与 fake-ip-range6。启用后读取实际运行配置、查 IPv6 路由、用 AAAA 发起受保护连接并核对链路。不要为让 YAML 看起来一致，冒然关闭物理网卡 IPv6、严格路由或整个 TUN。

浏览器安全 DNS、代理扩展、其他 VPN、WSL/虚拟机单独发现，变更前说明范围。并非所有浏览器 DoH 都必然泄漏，要测试其实际路由。
