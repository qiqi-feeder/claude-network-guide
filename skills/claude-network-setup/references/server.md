# 服务端：sing-box + VLESS Reality

适用于用户已授权部署的自有 Linux VPS。已有业务先发现和备份，不重装系统，不停用未知服务，不盲目占用 443。

## 安装与版本

优先用 [官方软件源](https://sing-box.sagernet.org/installation/package-manager/) 的稳定版；记录实际版本，重查 Reality/VLESS 字段。不要让教程中的固定版本号永久替代更新审查。

Ubuntu/Debian 的基本过程是建立官方 APT keyring、添加签名校验的软件源、更新索引、安装 sing-box。安装前检查源冲突，安装后检查 unit 实际运行用户与启动路径。不要关闭 APT 签名校验或任意执行第三方一键脚本。

## 配置骨架

通过 `sing-box generate uuid`、`sing-box generate reality-keypair` 和安全随机数生成每台服务器独立的 UUID、Reality 密钥和 Short ID。私钥不传到客户端，不在日志打印。

服务端核心字段：VLESS inbound、实际监听地址和 TCP 端口、users.uuid、flow 为 xtls-rprx-vision、TLS enabled、Reality enabled、handshake server/port、private_key、short_id；默认 direct outbound。字段以当前官方文档及 `sing-box check` 为准。

候选握手站点必须从 VPS 实测 TLS 能力、SNI 和证书，不把任意示例站点当作永远可用。客户端连接地址是 VPS，servername 与 Reality 约定一致。

配置文件按服务用户设置最小读取权限；若发行版服务用户为 sing-box，root:sing-box、640 是一种可行方式，先确认 unit 再使用。现有配置先备份，不静默生成全新密钥覆盖。

## 启用

先 `sing-box check -C /etc/sing-box`；通过后启用并启动服务，查看日志、监听地址和 CPU/内存。服务运行正常不等于客户端已连接成功。

启用 UFW 等防火墙前，先放行实际 SSH 端口和节点端口，核对云安全组并验证另一条 SSH 会话可连接。不要默认管理端口是 22。仅在授权范围内收紧入站，不开放管理面板或 DNS 递归入口。

## 验证与维护

先在 Windows 独立临时端口运行不带 TUN 的节点配置，实测 HTTPS 和出口，再接入全机。临时测试进程完成后停止，不与正式端口冲突。

更新前备份、检查版本迁移说明、配置校验、重启并复测；不要为了“自动更新”无条件追 beta。定期检查服务重启、日志容量与 SSH 安全。迁移到密钥登录前先验证密钥，再关闭密码登录。

交付私密节点文件与服务端恢复位置给用户，不发布到 GitHub。服务端不能访问某目标 IPv6 时，请求应失败，不在客户端增加 DIRECT 回退。
