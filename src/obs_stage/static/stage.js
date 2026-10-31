const SVG_NS = "http://www.w3.org/2000/svg";
const stage = document.querySelector("#stage");
const previewContent = document.querySelector("#previewContent");
const mask = document.querySelector("#slotMask");
const background = document.querySelector("#stageBackground");
const glowLayer = document.querySelector("#glowLayer");
const slotBorders = document.querySelector("#slotBorders");
const avatarWrap = document.querySelector("#avatarWrap");
const avatar = document.querySelector("#avatar");
const brandTitle = document.querySelector("#brandTitle");
const brandSubtitle = document.querySelector("#brandSubtitle");
const sceneBadge = document.querySelector("#sceneBadge");
const clock = document.querySelector("#clock");
const particles = document.querySelector("#particles");

const scene = location.pathname.split("/").filter(Boolean).pop() || "no-screen";
const isPreview = new URLSearchParams(location.search).get("preview") === "1";
let config = null;
let avatarRevision = "none";

stage.dataset.scene = scene;
stage.dataset.preview = String(isPreview);

function svgElement(tag, attributes = {}) {
  const element = document.createElementNS(SVG_NS, tag);
  for (const [name, value] of Object.entries(attributes)) {
    element.setAttribute(name, String(value));
  }
  return element;
}

function colorVariables(palette) {
  const root = document.documentElement.style;
  root.setProperty("--bg", palette.background);
  root.setProperty("--surface", palette.surface);
  root.setProperty("--primary", palette.primary);
  root.setProperty("--highlight", palette.highlight);
  root.setProperty("--pink", palette.pink);
  root.setProperty("--cream", palette.cream);
  root.setProperty("--text", palette.text);
  root.setProperty("--muted", palette.muted);
}

function renderSlots(layout) {
  const oldRects = mask.querySelectorAll("rect[data-slot]");
  for (const rect of oldRects) rect.remove();
  previewContent.replaceChildren();
  slotBorders.replaceChildren();

  for (const slot of layout.slots) {
    const rect = slot.rect;
    const maskRect = svgElement("rect", {
      x: rect.x,
      y: rect.y,
      width: rect.width,
      height: rect.height,
      rx: rect.radius,
      ry: rect.radius,
      fill: "black",
      "data-slot": slot.name,
    });
    mask.append(maskRect);

    const placeholder = document.createElement("div");
    placeholder.className = "preview-slot";
    placeholder.style.left = `${(rect.x / 1600) * 100}%`;
    placeholder.style.top = `${(rect.y / 900) * 100}%`;
    placeholder.style.width = `${(rect.width / 1600) * 100}%`;
    placeholder.style.height = `${(rect.height / 900) * 100}%`;
    placeholder.style.borderRadius = `${rect.radius}px`;
    const label = document.createElement("span");
    label.textContent = slot.placeholder || slot.label;
    placeholder.append(label);
    previewContent.append(placeholder);

    const border = document.createElement("div");
    border.className = "slot-border";
    border.style.left = `${(rect.x / 1600) * 100}%`;
    border.style.top = `${(rect.y / 900) * 100}%`;
    border.style.width = `${(rect.width / 1600) * 100}%`;
    border.style.height = `${(rect.height / 900) * 100}%`;
    border.style.borderRadius = `${rect.radius}px`;
    slotBorders.append(border);
  }
}

function renderParticles(count) {
  particles.replaceChildren();
  for (let index = 0; index < count; index += 1) {
    const particle = document.createElement("i");
    particle.className = "particle";
    particle.style.left = `${8 + ((index * 37) % 84)}%`;
    particle.style.top = `${45 + ((index * 23) % 48)}%`;
    particle.style.setProperty("--duration", `${5 + (index % 5) * 1.7}s`);
    particle.style.setProperty("--delay", `${-(index % 9) * 0.8}s`);
    particle.style.setProperty("--drift", `${(index % 2 ? 1 : -1) * (18 + (index % 4) * 8)}px`);
    particles.append(particle);
  }
}

function renderBranding() {
  const branding = config.branding;
  brandTitle.textContent = branding.title;
  brandSubtitle.textContent = branding.subtitle;
  avatarWrap.hidden = !branding.show_avatar;
  clock.hidden = !branding.show_clock;
  sceneBadge.hidden = !branding.show_scene_label;
  sceneBadge.textContent = config.layouts[scene].label.toUpperCase();
  if (branding.show_avatar) {
    avatar.src = `/api/avatar?v=${avatarRevision}`;
    avatar.onerror = () => {
      avatar.src = "/static/assets/avatar-placeholder.svg";
      avatar.onerror = null;
    };
  }
}

function applyConfig(nextConfig, revision = avatarRevision) {
  config = nextConfig;
  avatarRevision = revision;
  const theme = config.theme;
  colorVariables(theme.palette);
  const root = document.documentElement.style;
  root.setProperty("--radius", `${theme.frame_radius}px`);
  root.setProperty("--frame-width", `${theme.frame_width}px`);
  root.setProperty("--font-family", `"${theme.font_family.replaceAll('"', "")}", sans-serif`);
  glowLayer.style.opacity = String(0.35 + theme.glow_strength * 0.65);
  const layout = config.layouts[scene];
  renderSlots(layout);
  renderBranding();
  renderParticles(theme.particle_count);
  const revisionValue = encodeURIComponent(JSON.stringify(theme));
  background.setAttribute("href", `/api/background/${scene}.png?rev=${revisionValue}`);
}

function updateClock() {
  if (!config?.branding.show_clock) return;
  clock.textContent = new Intl.DateTimeFormat("zh-CN", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).format(new Date());
}

async function boot() {
  const response = await fetch("/api/config", { cache: "no-store" });
  if (!response.ok) throw new Error(`配置加载失败：HTTP ${response.status}`);
  const data = await response.json();
  applyConfig(data.config, data.avatar_revision);
  updateClock();
  window.setInterval(updateClock, 1000);
}

const socketProtocol = location.protocol === "https:" ? "wss" : "ws";
const socket = new WebSocket(`${socketProtocol}://${location.host}/ws`);
socket.addEventListener("message", async (event) => {
  const message = JSON.parse(event.data);
  if (message.type === "config") {
    const response = await fetch("/api/config", { cache: "no-store" });
    const data = await response.json();
    applyConfig(message.payload, data.avatar_revision);
  }
});
socket.addEventListener("close", () => window.setTimeout(() => location.reload(), 2500));

window.addEventListener("message", (event) => {
  if (event.origin !== location.origin) return;
  if (event.data?.type === "stage-config") applyConfig(event.data.config, event.data.avatarRevision || avatarRevision);
});

boot().catch((error) => console.error(error));
