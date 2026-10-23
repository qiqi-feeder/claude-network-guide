# 维护与验证

在仓库根目录运行（Python 3.10+）：

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python skills/claude-network-setup/scripts/check_delivery.py .
```

配置脚本只生成文件，不能假装完成部署。以示例节点运行仅供语法测试：

```powershell
python skills/claude-network-setup/scripts/build_client.py --node examples/node.example.json --source-file tests/fixtures/whitelist.conf --nested-file tests/fixtures/apple-news.list --output outputs/example.yaml --allow-example
```

若本机有 Mihomo，可再加 `--mihomo` 指向实际内核，以及 `--data-dir` 指向已有规则数据库目录，进行真实语法校验。不要启动测试配置接管网络。单元测试不安装软件、登录服务或修改当前配置。

## 规则更新

用同一私密节点文件重新运行构建器；它重新下载并转换白名单，记录来源哈希。校验通过后备份当前配置，再导入新输出或通过当前客户端支持方式重载，完成相关验收。构建器自身不改活动配置，也不自动建定时任务。

上游新规则类型、新外部规则源或校验失败时停止并保留旧配置，不静默丢规则。上游列表有变不代表所有条目都重新人工验证。维护保护域名时同步路由与 DNS，并检查共享验证/静态资源。

## 发布前

检查 Git 工作区与暂存区，禁止上传 private/outputs/backups/reports、实际节点文件或用户检测截图。运行检查脚本后人工审阅；扫描器并非完整秘密检测工具。

更新测试结果只写真实运行的版本与项目。公开仓库不要承诺“防封”“100% 不泄漏”或“所有平台通用”。VPS 推荐更新时同步评测日期与推广披露。
