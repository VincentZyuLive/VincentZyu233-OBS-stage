import { readFile, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";

const repositories = [
  "VincentZyuLive/VincentZyu233-OBS-stage",
  "VincentZyuLive/splayer-status-html-overlay-for-obs",
  "VincentZyuLive/go-musicfox-vincentzyu-fork",
  "VincentZyuLive/bili-live-danmaku",
];

const outputPath = fileURLToPath(new URL("../data/github-topics.json", import.meta.url));
const token = process.env.GITHUB_TOKEN?.trim();

let existing = {};
try {
  existing = JSON.parse(await readFile(outputPath, "utf8"));
} catch {
  existing = {};
}

const headers = {
  Accept: "application/vnd.github+json",
  "User-Agent": "VincentZyuLive-OBS-Stage-Topic-Sync",
  "X-GitHub-Api-Version": "2022-11-28",
};
if (token) headers.Authorization = `Bearer ${token}`;

const topics = {};
let failed = 0;

for (const repository of repositories) {
  try {
    const response = await fetch(`https://api.github.com/repos/${repository}/topics`, { headers });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload = await response.json();
    if (!Array.isArray(payload.names)) throw new Error("GitHub API 未返回 topics 数组");
    topics[repository] = payload.names;
    console.log(`${repository}: ${payload.names.length} topics`);
  } catch (error) {
    failed += 1;
    topics[repository] = Array.isArray(existing[repository]) ? existing[repository] : [];
    console.warn(`${repository}: 同步失败，${existing[repository] ? "保留缓存" : "使用空列表"} (${error.message})`);
  }
}

await writeFile(outputPath, `${JSON.stringify(topics, null, 2)}\n`, "utf8");
console.log(`topics snapshot written to ${outputPath}`);
if (failed) console.warn(`${failed} 个仓库同步失败；构建将使用现有快照继续。`);
