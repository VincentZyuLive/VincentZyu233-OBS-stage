import { defineConfig } from "vitepress";

const base = "/VincentZyu233-OBS-stage/";
const repo = "https://github.com/VincentZyu233/VincentZyu233-OBS-stage";
const live = "https://live.bilibili.com/5861873";

export default defineConfig({
  lang: "zh-CN",
  title: "VincentZyu Live Lab",
  description: "VincentZyu 的直播环境、OBS 舞台与 B站弹幕工具展示",
  base,
  cleanUrls: true,
  lastUpdated: true,
  sitemap: {
    hostname: "https://vincentzyu233.github.io",
  },
  head: [
    ["link", { rel: "icon", type: "image/png", href: `${base}brand/obs-stage-avatar.png` }],
    ["meta", { name: "theme-color", content: "#08111F" }],
  ],
  themeConfig: {
    logo: {
      src: "/brand/obs-stage-avatar.png",
      alt: "VincentZyu Live Lab",
    },
    nav: [
      { text: "首页", link: "/" },
      { text: "本机环境", link: "/environment" },
      { text: "软件栈", link: "/software" },
      { text: "OBS", link: "/obs" },
      { text: "项目", link: "/projects/" },
      { text: "B站直播", link: live },
    ],
    sidebar: {
      "/": [
        {
          text: "直播环境",
          items: [
            { text: "🏠 首页", link: "/" },
            { text: "🖥️ 本机环境", link: "/environment" },
            { text: "🧰 软件栈", link: "/software" },
            { text: "🎛️ OBS 与插件", link: "/obs" },
            { text: "📺 B站直播间", link: "/live" },
          ],
        },
        {
          text: "项目",
          items: [
            { text: "📦 项目概览", link: "/projects/" },
            { text: "🌊 OBS Stage", link: "/projects/obs-stage" },
            { text: "🦊 go-musicfox", link: "/projects/musicfox" },
            { text: "💬 Bili Live Danmaku", link: "/projects/bili-live-danmaku" },
          ],
        },
      ],
    },
    socialLinks: [{ icon: "github", link: repo }],
    search: { provider: "local" },
    outline: { level: [2, 3], label: "本页目录" },
    docFooter: { prev: "上一页", next: "下一页" },
    lastUpdated: {
      text: "最后更新",
      formatOptions: { dateStyle: "medium", timeStyle: "short" },
    },
    footer: {
      message: "直播环境、OBS 舞台与弹幕工具记录",
    },
  },
});
