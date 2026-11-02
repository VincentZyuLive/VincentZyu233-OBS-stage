# 🌊 OBS Stage

<p align="center">
  <img src="src/obs_stage/static/assets/obs-stage-avatar.png" width="160" alt="OBS Stage logo">
</p>

<p align="center">
  <a href="https://live.bilibili.com/5861873" target="_blank" rel="noopener noreferrer"><img src="https://img.shields.io/badge/Bilibili-5861873-00A1D6?style=for-the-badge&logo=bilibili&logoColor=white" alt="Bilibili 直播间 5861873"></a>
  <a href="https://vincentzyulive.github.io/" target="_blank" rel="noopener noreferrer"><img src="https://img.shields.io/badge/Live_Environment-Pages-7FA8E8?style=for-the-badge&logo=githubpages&logoColor=white" alt="Live Environment Pages"></a>
  <a href="https://github.com/VincentZyuLive/VincentZyu233-OBS-stage" target="_blank" rel="noopener noreferrer"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
</p>

给 OBS 直播间增加一套可编辑的水色雾蓝主题舞台。OBS 负责采集与合成，浏览器中的 WebUI 负责背景、圆角边框、头像徽章、标题和轻动态装饰。

> [!TIP]
> 这是 VincentZyu 的自用版本，主要服务个人直播舞台与 OBS 环境。项目会按实际使用需求持续迭代，也欢迎体验、提交 Issue 或 PR。
> 组织主页：[VincentZyuLive](https://github.com/VincentZyuLive)

## 🖼️ 预览

在线环境站：https://vincentzyulive.github.io/

### 🎛️ WebUI

![OBS Stage WebUI](docs/images/preview.webui.png)

### 🖥️ 直播画面

![OBS Stage 直播画面效果](docs/images/preview.stream-only.png)

### 🎬 OBS 半屏实机

![OBS Stage 在 OBS 中的半屏效果](docs/images/preview.obs.png)

### 📺 B站直播姬实机

![OBS Stage 在 B站直播姬中的效果](docs/images/preview.bili-livehime.png)

## ✨ 能力

- 三套独立布局：`no-screen`、`half-screen`、`full-screen`
- 水色雾蓝主题，可调整完整调色板、背景风格、圆角、辉光、粒子与字体
- 内置 LXGW WenKai Mono Medium（SIL OFL 1.1），WebUI 和舞台默认统一使用霞鹜文楷
- 支持上传头像并作为舞台品牌徽章，也可一键恢复内置默认头像
- 默认头像源文件随仓库分发，运行时生成到 `<data_dir>/avatar/avatar.png`
- WebUI 提供 16:9 实时设计预览和内容源位置参考
- 可选 B站状态 HUD：通过 `?hud=corner|bottom|top|none` 选择左下角卡片、底部横条、顶部横条或不显示
- 可选 OBS WebSocket：测试连接、抓取真实场景截图、一键创建或更新舞台层
- 一键套用只管理 `Stage BG` 和 `Stage Frame`，不移动现有采集、播放器或弹幕
- 背景为静态 PNG，前景为轻量 Browser Source；场景隐藏时可关闭浏览器源
- 资源版本可配置：默认每次加载生成新的 Unix 毫秒版本，避免 OBS 继续使用旧 CSS/JS 缓存
- 配置、头像和导出背景存放在应用数据目录，不进入 Git

## 🚀 启动

需要 [uv](https://docs.astral.sh/uv/)；Python 3.12 或更新版本由 uv 管理。

```bash
uv sync
uv run obs-stage
```

控制台默认打开：

```text
http://127.0.0.1:6162/admin
```

### 🖥️ 启动脚本

Windows 双击 `scripts/start-obs-stage.cmd` 即可检查并启动本地服务；Linux/macOS 使用：

```bash
./scripts/start-obs-stage.sh
```

脚本会先检查服务是否已经运行；已运行时只打开 WebUI，未运行时通过 `uv run obs-stage` 启动。安装后的 Windows 桌面快捷方式名为 `OBS Stage`，关闭终端或控制台窗口即可停止服务。

启动参数会原样传给 `obs-stage`，并支持 `--port 7000` 或 `--port=7000` 动态调整健康检查和 Admin 地址：

```powershell
.\scripts\start-obs-stage.cmd --port 16162 --verbose
```

```bash
./scripts/start-obs-stage.sh --data-dir "/path/to/data" --port 16162
```

脚本只额外解析 `--port`、`--no-browser`、`--help` 和 `--version`，其余参数全部原样交给 CLI。服务已运行时使用 `--no-browser` 会打印 Admin URL，而不是再次启动或打开页面。

## 🎛️ OBS 分层

推荐每个场景按以下顺序叠加：

```text
1. Stage BG [scene]       WebUI 导出的静态背景图
2. 显示器采集 / 窗口采集 / SPlayer
3. Stage Frame [scene]    WebUI 的透明前景浏览器源
4. 弹幕浏览器源
5. 通知、字幕等临时层
```

舞台前景在内容槽位处透明，在槽位外绘制背景、圆角边框、标题、头像和轻动态装饰。浏览器源不能直接显示 OBS 内部的采集画面，因此必须由 OBS 把真实内容夹在背景层和前景层之间。

完整步骤见 [docs/obs-setup.md](docs/obs-setup.md)。

## 🔌 可选 OBS WebSocket

在 OBS 的“工具 → WebSocket 服务器设置”中启用服务器，然后把地址和密码填入 WebUI。WebUI 可以：

- 测试连接并读取场景列表
- 抓取当前场景真实截图
- 为当前场景或全部场景创建/更新舞台层
- 已存在的舞台源会更新，不会重复创建

密码只保留在页面内存或 `OBS_WEBSOCKET_PASSWORD` 环境变量中，不写入配置文件。更多说明见 [docs/obs-websocket.md](docs/obs-websocket.md)。

## 📺 B站状态 HUD

通过 Scene URL 的 `hud` 参数选择只读 B站状态 HUD 的位置：

| `hud` 值 | 效果 |
| --- | --- |
| `corner` | 左下角卡片，显示完整 HUD |
| `bottom` | 底部近满宽单行横条 |
| `top` | 顶部近满宽单行横条，品牌和时钟自动下移避让 |
| `none` | 不显示 HUD |

```text
http://127.0.0.1:6162/stage/full-screen?hud=corner
http://127.0.0.1:6162/stage/full-screen?hud=bottom
http://127.0.0.1:6162/stage/full-screen?hud=top
http://127.0.0.1:6162/stage/full-screen?hud=none
```

`bottom` 和 `top` 在 1600×900 下左右各保留 34px，宽度约 1532px，只占一行；`bottom` 模式会把右下场景标识移到横条上方。任意场景都可使用上述参数，只需替换 `/stage/full-screen` 中的场景名。

HUD 显示直播状态、标题、分区、人气、粉丝数、开播时间和更新时间，数据来自 B站公开房间接口。不传 `hud`、传 `none` 或传非法值时都不会创建 HUD，也不会请求 `/api/live-status`。旧的 `?status=verbose` 已移除，不再兼容。

## 📁 布局

- `no-screen`：中央主播放器卡，顶部品牌栏，无弹幕槽位。
- `half-screen`：左侧固定弹幕，右侧主采集卡和横向播放器卡。
- `full-screen`：全屏采集内容，左侧固定弹幕，右下悬浮播放器。

三个舞台页原生使用 `1600×900` 的 16:9 设计坐标；OBS 浏览器源宽高请设置为 `1600×900`。坐标见 [docs/layout-spec.md](docs/layout-spec.md)。

## 🗂️ 数据位置

Windows 默认：

```text
%LOCALAPPDATA%\VincentZyu-OBS-stage\
```

macOS 与 Linux 使用各自的平台应用数据目录。可用 `--data-dir` 覆盖。

## 🧩 资源缓存

`config.json` 中的 `assets.cache_bust` 默认开启。开启时，Stage 与 Admin 的 CSS/JS URL 会在每次页面请求时带上当前 Unix 毫秒版本参数，避免 OBS Browser Source 继续使用旧缓存；关闭后使用固定的 `v=stable` 版本，允许正常缓存。

## 🛠️ 开发

```bash
uv sync
uv run ruff check .
uv run mypy src
uv run pytest -q
```

跨平台进程采样：

```bash
uv run scripts/measure_processes.py --name python --name obs-browser-page --seconds 10
```

直播环境站已迁移到独立仓库：

- 线上地址：<https://vincentzyulive.github.io/>
- 源码仓库：<https://github.com/VincentZyuLive/VincentZyuLive.github.io>

## 📄 License

MIT。页面与桌面快捷方式使用“OBS Studio logo + VincentZyu233 GitHub 头像”组合图标；其中 OBS logo 派生资源按 GPL-2.0 单独分发，来源与许可说明见
[src/obs_stage/static/assets/OBS-LOGO-NOTICE.md](src/obs_stage/static/assets/OBS-LOGO-NOTICE.md)。
