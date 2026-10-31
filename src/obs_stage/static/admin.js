const byId = (id) => document.getElementById(id);
const fields = [...document.querySelectorAll("[data-bind]")];

const elements = {
  saveState: byId("saveState"),
  notice: byId("notice"),
  sceneTabs: byId("sceneTabs"),
  previewTitle: byId("previewTitle"),
  previewViewport: byId("previewViewport"),
  previewStage: byId("previewStage"),
  previewFrame: byId("previewFrame"),
  stageUrl: byId("stageUrl"),
  downloadBgBtn: byId("downloadBgBtn"),
  sourceGuide: byId("sourceGuide"),
  avatarFile: byId("avatarFile"),
  realPreview: byId("realPreview"),
  obsPassword: byId("obsPassword"),
  obsResult: byId("obsResult"),
};

const state = {
  config: null,
  avatarRevision: "none",
  activeScene: "full-screen",
  stageUrls: {},
};

function getPath(object, path) {
  return path.split(".").reduce((value, key) => value?.[key], object);
}

function setPath(object, path, value) {
  const parts = path.split(".");
  let cursor = object;
  for (const part of parts.slice(0, -1)) cursor = cursor[part];
  cursor[parts.at(-1)] = value;
}

function inputValue(input) {
  if (input.type === "checkbox") return input.checked;
  if (input.type === "number" || input.type === "range") return Number(input.value);
  return input.value;
}

function showNotice(message, error = false) {
  elements.notice.textContent = message;
  elements.notice.classList.toggle("error", error);
  elements.notice.classList.add("visible");
  window.clearTimeout(showNotice.timer);
  showNotice.timer = window.setTimeout(() => elements.notice.classList.remove("visible"), 5000);
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    let detail = `HTTP ${response.status}`;
    try {
      const body = await response.json();
      detail = body.detail || detail;
    } catch {
      // Keep the HTTP status fallback.
    }
    throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
  }
  return response.json();
}

function updateOutputs() {
  for (const input of fields) {
    if (!input.dataset.output) continue;
    const output = byId(input.dataset.output);
    if (output) output.textContent = Number(input.value).toFixed(2);
  }
}

function fillForm() {
  for (const input of fields) {
    const value = getPath(state.config, input.dataset.bind);
    if (input.type === "checkbox") input.checked = Boolean(value);
    else input.value = String(value ?? "");
  }
  updateOutputs();
}

function collectForm() {
  for (const input of fields) setPath(state.config, input.dataset.bind, inputValue(input));
}

function sendPreview() {
  elements.previewFrame.contentWindow?.postMessage(
    {
      type: "stage-config",
      config: state.config,
      avatarRevision: state.avatarRevision,
    },
    location.origin,
  );
}

function resizePreview() {
  const width = 960;
  const height = 540;
  const availableWidth = Math.max(300, elements.previewViewport.clientWidth - 32);
  const availableHeight = Math.min(520, Math.max(280, window.innerHeight * 0.46));
  const scale = Math.min(availableWidth / width, availableHeight / height, 1);
  elements.previewFrame.style.width = `${width}px`;
  elements.previewFrame.style.height = `${height}px`;
  elements.previewFrame.style.transform = `scale(${scale})`;
  elements.previewStage.style.width = `${Math.floor(width * scale)}px`;
  elements.previewStage.style.height = `${Math.floor(height * scale)}px`;
}

function updateSceneUi() {
  const layout = state.config.layouts[state.activeScene];
  elements.previewTitle.textContent = layout.label;
  for (const tab of elements.sceneTabs.querySelectorAll(".scene-tab")) {
    tab.classList.toggle("active", tab.dataset.scene === state.activeScene);
  }
  elements.previewFrame.src = `/stage/${state.activeScene}?preview=1`;
  const stageUrl = state.stageUrls[state.activeScene] || `${location.origin}/stage/${state.activeScene}`;
  elements.stageUrl.textContent = stageUrl;
  elements.downloadBgBtn.href = `/api/background/${state.activeScene}.png`;
  elements.downloadBgBtn.download = `obs-stage-${state.activeScene}-background.png`;
  elements.previewFrame.hidden = false;
  elements.realPreview.hidden = true;
  elements.sourceGuide.replaceChildren();
  for (const slot of layout.slots) {
    const row = document.createElement("div");
    row.className = "source-row";
    const name = document.createElement("strong");
    name.textContent = slot.label;
    row.append(
      name,
      document.createTextNode(`X ${slot.rect.x}`),
      document.createTextNode(`Y ${slot.rect.y}`),
      document.createTextNode(`W ${slot.rect.width}`),
      document.createTextNode(`H ${slot.rect.height}`),
    );
    elements.sourceGuide.append(row);
  }
  window.setTimeout(() => {
    resizePreview();
    sendPreview();
  }, 80);
}

function switchScene(scene) {
  state.activeScene = scene;
  updateSceneUi();
}

async function saveConfig(showMessage = true) {
  collectForm();
  const response = await fetchJson("/api/config", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(state.config),
  });
  state.config = response;
  elements.saveState.textContent = "已保存";
  elements.saveState.dataset.state = "ok";
  if (showMessage) showNotice("舞台配置已保存，OBS 前景源会实时更新。");
}

async function uploadAvatar() {
  const file = elements.avatarFile.files?.[0];
  if (!file) {
    showNotice("请先选择头像图片。", true);
    return;
  }
  const form = new FormData();
  form.append("file", file);
  const result = await fetchJson("/api/avatar", { method: "POST", body: form });
  state.avatarRevision = result.revision;
  sendPreview();
  showNotice("头像已更新。");
}

async function deleteAvatar() {
  await fetchJson("/api/avatar", { method: "DELETE" });
  state.avatarRevision = "none";
  sendPreview();
  showNotice("头像已移除，舞台将使用默认占位图。");
}

async function testObs() {
  await saveConfig(false);
  elements.obsResult.textContent = "正在连接 OBS...";
  const result = await fetchJson("/api/obs/test", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password: elements.obsPassword.value }),
  });
  elements.obsResult.textContent = JSON.stringify(result, null, 2);
  showNotice("OBS WebSocket 连接成功。");
}

async function previewObs() {
  await saveConfig(false);
  elements.previewFrame.hidden = true;
  elements.realPreview.hidden = false;
  elements.realPreview.src = "/static/assets/avatar-placeholder.svg";
  const result = await fetchJson(`/api/obs/preview/${state.activeScene}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password: elements.obsPassword.value }),
  });
  elements.realPreview.src = result.image;
  showNotice("已抓取当前 OBS 场景截图。刷新页面可返回设计预览。");
}

async function applyObs(allScenes) {
  await saveConfig(false);
  elements.obsResult.textContent = "正在应用舞台层...";
  const result = await fetchJson("/api/obs/apply", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      scene: allScenes ? null : state.activeScene,
      password: elements.obsPassword.value,
    }),
  });
  elements.obsResult.textContent = JSON.stringify(result, null, 2);
  showNotice(allScenes ? "三个场景的舞台层已更新。" : `${state.activeScene} 的舞台层已更新。`);
}

async function boot() {
  const data = await fetchJson("/api/config");
  state.config = data.config;
  state.avatarRevision = data.avatar_revision;
  state.stageUrls = data.stage_urls;
  fillForm();
  switchScene(state.activeScene);
}

for (const field of fields) {
  field.addEventListener("input", () => {
    collectForm();
    updateOutputs();
    elements.saveState.textContent = "未保存";
    elements.saveState.dataset.state = "";
    sendPreview();
  });
  field.addEventListener("change", () => {
    collectForm();
    sendPreview();
  });
}

elements.sceneTabs.addEventListener("click", (event) => {
  const tab = event.target.closest(".scene-tab");
  if (tab) switchScene(tab.dataset.scene);
});
elements.previewFrame.addEventListener("load", () => {
  resizePreview();
  sendPreview();
});
byId("saveBtn").addEventListener("click", () => saveConfig().catch((error) => showNotice(error.message, true)));
elements.avatarFile.addEventListener("change", () => uploadAvatar().catch((error) => showNotice(error.message, true)));
byId("deleteAvatarBtn").addEventListener("click", () => deleteAvatar().catch((error) => showNotice(error.message, true)));
byId("testObsBtn").addEventListener("click", () => testObs().catch((error) => {
  elements.obsResult.textContent = error.message;
  showNotice(error.message, true);
}));
byId("previewObsBtn").addEventListener("click", () => previewObs().catch((error) => {
  elements.previewFrame.hidden = false;
  elements.realPreview.hidden = true;
  elements.obsResult.textContent = error.message;
  showNotice(error.message, true);
}));
byId("applySceneBtn").addEventListener("click", () => applyObs(false).catch((error) => showNotice(error.message, true)));
byId("applyAllBtn").addEventListener("click", () => applyObs(true).catch((error) => showNotice(error.message, true)));
byId("copyUrlBtn").addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(elements.stageUrl.textContent);
    showNotice("OBS 舞台源地址已复制。");
  } catch {
    showNotice("复制失败，请手动选择地址。", true);
  }
});
window.addEventListener("resize", resizePreview);

boot().catch((error) => showNotice(`初始化失败：${error.message}`, true));
