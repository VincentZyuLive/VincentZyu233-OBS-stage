# OBS WebSocket 集成

在 OBS 打开“工具 → WebSocket 服务器设置”，启用 WebSocket 服务器。OBS 32.x 默认端口通常为 `4455`。

WebUI 中的密码不会写入 `config.json`。也可以设置环境变量：

```text
OBS_WEBSOCKET_PASSWORD=your-password
```

## 一键套用范围

只创建、更新和排序：

```text
Stage BG [scene]
Stage Frame [scene]
```

不会移动或删除现有内容源。舞台背景被放到场景最底层；前景放在最上层源之前，通常即弹幕源下方。

## 真实预览

“抓取当前场景”调用 OBS WebSocket v5 的 `GetSourceScreenshot`，返回的是应用舞台层后的真实场景。设计中的未保存颜色仍以 WebUI 里的 16:9 设计预览为准。
