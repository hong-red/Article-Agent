/* 智能精灵 · 公众号文章生成器 —— 前端逻辑 */
const $ = (id) => document.getElementById(id);

const state = {
  step: 1,
  topic: "", style: "", extra: "", template: "general",
  titles: [], selectedTitle: "",
  title: "",
  contentMd: "",
  theme: "default",
  tone: "", addSummary: false, addGolden: false, addFollow: false, polish: true,
  contentHtml: "",
  articleId: null,
  coverUrl: "",
  themes: [],
};

/* ---------- 基础 ---------- */
async function api(path, opts = {}) {
  const res = await fetch(path, opts);
  let data = null;
  try { data = await res.json(); } catch (e) {}
  if (!res.ok) {
    const msg = (data && (data.detail || data.message)) || `请求失败 (${res.status})`;
    throw new Error(msg);
  }
  return data;
}
const post = (path, body) => api(path, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(body),
});

let toastTimer = null;
function toast(msg, type = "info") {
  const t = $("toast");
  t.textContent = msg;
  t.className = "toast show " + type;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { t.className = "toast hidden"; }, 3200);
}

function debounce(fn, ms) {
  let t = null;
  return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
}

/* ---------- 步骤切换 ---------- */
function goTo(n) {
  state.step = n;
  [1, 2, 3].forEach((i) => {
    $("step-" + i).classList.toggle("hidden", i !== n);
    const stepEl = document.querySelector(`.step[data-step="${i}"]`);
    stepEl.classList.toggle("active", i === n);
    stepEl.classList.toggle("done", i < n);
  });
  window.scrollTo({ top: 0, behavior: "smooth" });
}

document.querySelectorAll("[data-goto]").forEach((b) => {
  b.addEventListener("click", () => goTo(parseInt(b.dataset.goto)));
});

/* ---------- 预览（实时） ---------- */
async function renderPreview(md, title, targetId, theme) {
  if (!md.trim()) { $(targetId).innerHTML = '<p class="muted">暂无内容</p>'; return; }
  try {
    const r = await post("/api/render", { content: md, title, theme: theme || "default" });
    $(targetId).innerHTML = r.html;
  } catch (e) { /* 预览失败静默处理 */ }
}

/* ---------- 第 1 步 ---------- */
$("btn-gen-titles").addEventListener("click", async () => {
  const topic = $("s1-topic").value.trim();
  if (!topic) { toast("请先填写文章主题", "error"); return; }
  state.topic = topic;
  state.style = $("s1-style").value.trim();
  state.extra = $("s1-extra").value.trim();
  state.template = $("s1-template").value;
  const count = parseInt($("s1-count").value);

  const btn = $("btn-gen-titles");
  btn.disabled = true; btn.textContent = "生成中…";
  try {
    const r = await post("/api/generate/titles", { topic, count, style: state.style, extra: state.extra, template: state.template });
    state.titles = r.titles;
    renderTitles();
    toast("题目已生成，请选择一个", "success");
  } catch (e) {
    toast(e.message, "error");
  } finally {
    btn.disabled = false; btn.textContent = "生成题目";
  }
});

function renderTitles() {
  const box = $("titles-box");
  if (!state.titles.length) { box.innerHTML = ""; return; }
  box.innerHTML = state.titles.map((t, i) => `
    <label class="title-opt">
      <input type="radio" name="title" value="${i}">
      <span>${escapeHtml(t)}</span>
    </label>
  `).join("");
  box.querySelectorAll(".title-opt").forEach((opt) => {
    opt.addEventListener("click", () => {
      box.querySelectorAll(".title-opt").forEach((o) => o.classList.remove("selected"));
      opt.classList.add("selected");
      state.selectedTitle = state.titles[parseInt(opt.querySelector("input").value)];
      $("btn-to-step2").disabled = false;
    });
  });
}

$("btn-to-step2").addEventListener("click", () => {
  state.title = state.selectedTitle;
  $("s2-title").value = state.title;
  $("s2-topic").innerHTML = `主题：<b>${escapeHtml(state.topic)}</b>` +
    (state.style ? ` · 风格：${escapeHtml(state.style)}` : "") +
    (state.extra ? ` · 说明：${escapeHtml(state.extra)}` : "");
  goTo(2);
});

/* ---------- 第 2 步 ---------- */
$("btn-gen-content").addEventListener("click", async () => {
  state.title = $("s2-title").value.trim();
  if (!state.title) { toast("请先填写/选择文章标题", "error"); return; }
  const btn = $("btn-gen-content");
  btn.disabled = true; btn.textContent = "写作中…";
  try {
    const r = await post("/api/generate/content", {
      topic: state.topic, title: state.title,
      style: state.style, extra: state.extra, template: state.template,
      feedback: "", previous_content: "",
    });
    state.contentMd = r.content;
    $("s2-md").value = r.content;
    renderPreview(r.content, state.title, "s2-preview", state.theme);
    toast("正文已生成", "success");
  } catch (e) {
    toast(e.message, "error");
  } finally {
    btn.disabled = false; btn.textContent = "生成正文";
  }
});

$("btn-refine").addEventListener("click", async () => {
  const feedback = $("s2-feedback").value.trim();
  if (!feedback) { toast("请先填写调试意见", "error"); return; }
  if (!state.contentMd) { toast("请先生成正文", "error"); return; }
  const btn = $("btn-refine");
  btn.disabled = true; btn.textContent = "改写中…";
  try {
    const r = await post("/api/generate/content", {
      topic: state.topic, title: state.title,
      style: state.style, extra: state.extra, template: state.template,
      feedback, previous_content: $("s2-md").value,
    });
    state.contentMd = r.content;
    $("s2-md").value = r.content;
    $("s2-feedback").value = "";
    renderPreview(r.content, state.title, "s2-preview", state.theme);
    toast("已按意见重新生成", "success");
  } catch (e) {
    toast(e.message, "error");
  } finally {
    btn.disabled = false; btn.textContent = "按意见重新生成";
  }
});

$("s2-md").addEventListener("input", debounce(() => {
  state.contentMd = $("s2-md").value;
  renderPreview(state.contentMd, state.title, "s2-preview", state.theme);
}, 500));

$("btn-to-step3").addEventListener("click", () => {
  if (!state.contentMd) { toast("请先生成正文", "error"); return; }
  state.contentMd = $("s2-md").value;
  state.title = $("s2-title").value.trim();
  $("s3-md").value = state.contentMd;
  renderPreview(state.contentMd, state.title, "s3-preview", state.theme);
  goTo(3);
});

/* ---------- 第 3 步 ---------- */
$("btn-format").addEventListener("click", async () => {
  state.contentMd = $("s3-md").value;
  state.title = $("s2-title").value.trim();
  if (!state.contentMd) { toast("正文为空", "error"); return; }
  const btn = $("btn-format");
  btn.disabled = true; btn.textContent = "排版中…";
  try {
    const r = await post("/api/generate/format", {
      content: state.contentMd, title: state.title,
      theme: state.theme, tone: state.tone, template: state.template,
      add_summary: $("s3-summary").checked,
      add_golden: $("s3-golden").checked,
      add_follow: $("s3-follow").checked,
      polish: $("s3-polish").checked,
    });
    state.contentMd = r.content;
    state.contentHtml = r.html;
    $("s3-md").value = r.content;
    $("s3-preview").innerHTML = r.html;
    toast("格式优化完成", "success");
  } catch (e) {
    toast(e.message, "error");
  } finally {
    btn.disabled = false; btn.textContent = "格式优化";
  }
});

$("btn-copy-html").addEventListener("click", async () => {
  const md = $("s3-md").value;
  const title = $("s2-title").value.trim();
  if (!md.trim()) { toast("正文为空", "error"); return; }
  try {
    const r = await post("/api/render", { content: md, title, theme: state.theme });
    await navigator.clipboard.writeText(r.html);
    toast("已复制 HTML，可粘贴到秀米或公众号编辑器", "success");
  } catch (e) {
    toast("复制失败：" + e.message, "error");
  }
});

$("s3-theme").addEventListener("change", () => {
  state.theme = $("s3-theme").value;
  renderPreview($("s3-md").value, state.title, "s3-preview", state.theme);
});
$("s3-tone").addEventListener("change", () => { state.tone = $("s3-tone").value; });
$("s3-md").addEventListener("input", debounce(() => {
  state.contentMd = $("s3-md").value;
  renderPreview(state.contentMd, state.title, "s3-preview", state.theme);
}, 500));

$("s3-cover").addEventListener("change", () => {
  const f = $("s3-cover").files[0];
  if (!f) return;
  const url = URL.createObjectURL(f);
  $("s3-cover-preview").innerHTML = `<img src="${url}" alt="封面预览">`;
});

/* ---------- 保存 / 推送 ---------- */
async function saveArticle() {
  const body = {
    topic: state.topic, title: state.title || $("s2-title").value.trim(),
    content_md: state.contentMd || $("s3-md").value,
    content_html: state.contentHtml || "",
    theme: state.theme, cover: "",
  };
  if (!body.title) throw new Error("缺少文章标题");
  if (!body.content_md) throw new Error("正文为空");

  let r;
  if (state.articleId) {
    r = await api(`/api/articles/${state.articleId}`, { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  } else {
    r = await post("/api/articles", body);
  }
  state.articleId = r.id;
  return r.id;
}

async function uploadCoverIfNeeded(id) {
  const f = $("s3-cover").files[0];
  if (!f) return;
  const fd = new FormData();
  fd.append("file", f);
  const r = await api(`/api/articles/${id}/cover`, { method: "POST", body: fd });
  state.coverUrl = r.cover_url;
}

$("btn-save").addEventListener("click", async () => {
  try {
    const id = await saveArticle();
    await uploadCoverIfNeeded(id);
    toast("已保存到本地库", "success");
  } catch (e) { toast(e.message, "error"); }
});

$("btn-push").addEventListener("click", async () => {
  const btn = $("btn-push");
  btn.disabled = true; btn.textContent = "推送中…";
  try {
    if (!state.articleId) {
      await saveArticle();
      await uploadCoverIfNeeded(state.articleId);
    }
    const r = await post(`/api/articles/${state.articleId}/push`, {});
    toast("已推送到公众号草稿箱", "success");
    console.log("draft_media_id:", r.draft_media_id);
  } catch (e) {
    toast(e.message, "error");
  } finally {
    btn.disabled = false; btn.textContent = "推送到草稿箱";
  }
});

/* ---------- 设置 ---------- */
$("btn-settings").addEventListener("click", () => openModal("modal-settings"));
$("btn-library").addEventListener("click", async () => {
  openModal("modal-library");
  await loadLibrary();
});

function openModal(id) { $(id).classList.remove("hidden"); }
function closeModal(id) { $(id).classList.add("hidden"); }
document.querySelectorAll("[data-close]").forEach((b) => {
  b.addEventListener("click", () => closeModal(b.dataset.close));
});
document.querySelectorAll(".modal-mask").forEach((m) => {
  m.addEventListener("click", (e) => { if (e.target === m) m.classList.add("hidden"); });
});

async function loadConfig() {
  try {
    const c = await api("/api/config");
    $("cfg-key").value = c.deepseek_api_key || "";
    $("cfg-model").value = c.deepseek_model || "deepseek-chat";
    $("cfg-appid").value = c.wechat_appid || "";
    $("cfg-secret").value = c.wechat_appsecret || "";
    $("cfg-author").value = c.wechat_author || "";
    $("cfg-source-url").value = c.wechat_source_url || "";
    $("cfg-comment").checked = !!c.wechat_need_open_comment;
    $("cfg-fans-comment").checked = !!c.wechat_only_fans_can_comment;
  } catch (e) {}
}

$("btn-save-config").addEventListener("click", async () => {
  const body = {
    deepseek_api_key: $("cfg-key").value.trim(),
    deepseek_model: $("cfg-model").value,
    wechat_appid: $("cfg-appid").value.trim(),
    wechat_appsecret: $("cfg-secret").value.trim(),
    wechat_author: $("cfg-author").value.trim(),
    wechat_source_url: $("cfg-source-url").value.trim(),
    wechat_need_open_comment: $("cfg-comment").checked ? 1 : 0,
    wechat_only_fans_can_comment: $("cfg-fans-comment").checked ? 1 : 0,
  };
  try {
    await post("/api/config", body);
    toast("设置已保存", "success");
    closeModal("modal-settings");
  } catch (e) { toast(e.message, "error"); }
});

$("btn-test-llm").addEventListener("click", async () => {
  const key = $("cfg-key").value.trim();
  // 先临时保存 key 再测试
  const body = { deepseek_api_key: key, deepseek_model: $("cfg-model").value };
  try {
    await post("/api/config", body);
    const r = await post("/api/test/llm", {});
    $("llm-test-result").textContent = "连接正常：" + (r.reply || "");
    $("llm-test-result").style.color = "#16a34a";
  } catch (e) {
    $("llm-test-result").textContent = e.message;
    $("llm-test-result").style.color = "#d92d20";
  }
});

/* ---------- 文章库 ---------- */
async function loadLibrary() {
  const list = $("library-list");
  list.innerHTML = '<p class="muted">加载中…</p>';
  try {
    const items = await api("/api/articles");
    if (!items.length) { list.innerHTML = '<p class="muted">暂无保存的文章</p>'; return; }
    list.innerHTML = items.map((a) => `
      <div class="lib-item">
        <div class="meta">
          <div class="title">${escapeHtml(a.title)}</div>
          <div class="sub">${escapeHtml(a.topic)} · ${a.updated_at || ""}
            <span class="badge ${a.status === "pushed" ? "pushed" : ""}">${a.status === "pushed" ? "已推送" : "草稿"}</span>
          </div>
        </div>
        <div class="ops">
          <button class="btn ghost small" data-load="${a.id}">载入</button>
          <button class="btn ghost small" data-del="${a.id}">删除</button>
        </div>
      </div>
    `).join("");
    list.querySelectorAll("[data-load]").forEach((b) => b.addEventListener("click", () => loadArticle(parseInt(b.dataset.load))));
    list.querySelectorAll("[data-del]").forEach((b) => b.addEventListener("click", () => delArticle(parseInt(b.dataset.del))));
  } catch (e) {
    list.innerHTML = `<p class="muted">加载失败：${escapeHtml(e.message)}</p>`;
  }
}

async function loadArticle(id) {
  try {
    const a = await api(`/api/articles/${id}`);
    state.articleId = a.id;
    state.topic = a.topic;
    state.title = a.title;
    state.contentMd = a.content_md;
    state.contentHtml = a.content_html;
    state.theme = a.theme;
    $("s1-topic").value = a.topic;
    $("s2-title").value = a.title;
    $("s2-md").value = a.content_md;
    $("s3-md").value = a.content_md;
    $("s3-theme").value = a.theme;
    renderPreview(a.content_md, a.title, "s3-preview", a.theme);
    if (a.cover_url) {
      $("s3-cover-preview").innerHTML = `<img src="${a.cover_url}" alt="封面">`;
    }
    closeModal("modal-library");
    goTo(3);
    toast("已载入文章", "success");
  } catch (e) { toast(e.message, "error"); }
}

async function delArticle(id) {
  if (!confirm("确定删除这篇文章？")) return;
  try {
    await api(`/api/articles/${id}`, { method: "DELETE" });
    if (state.articleId === id) state.articleId = null;
    toast("已删除", "success");
    await loadLibrary();
  } catch (e) { toast(e.message, "error"); }
}

/* ---------- 素材库 ---------- */
document.querySelectorAll(".tab").forEach((t) => {
  t.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((x) => x.classList.remove("active"));
    t.classList.add("active");
    const tab = t.dataset.tab;
    $("tab-articles").classList.toggle("hidden", tab !== "articles");
    $("tab-materials").classList.toggle("hidden", tab !== "materials");
    if (tab === "materials") loadMaterials();
  });
});

function fmtSize(n) {
  n = n || 0;
  if (n < 1024) return n + " B";
  if (n < 1024 * 1024) return (n / 1024).toFixed(1) + " KB";
  return (n / 1024 / 1024).toFixed(1) + " MB";
}

async function loadMaterials() {
  const list = $("materials-list");
  list.innerHTML = '<p class="muted">加载中…</p>';
  try {
    const items = await api("/api/materials");
    if (!items.length) {
      list.innerHTML = '<p class="muted">暂无素材，可上传 Word / PDF / 文本等文件</p>';
      return;
    }
    list.innerHTML = items.map((m) => `
      <div class="lib-item">
        <div class="meta">
          <div class="title">${escapeHtml(m.name)}</div>
          <div class="sub">${fmtSize(m.size)} · ${m.created_at || ""}</div>
        </div>
        <div class="ops">
          <a class="btn ghost small" href="/materials/${encodeURIComponent(m.name)}" target="_blank">打开</a>
          <button class="btn ghost small" data-mdel="${m.id}">删除</button>
        </div>
      </div>
    `).join("");
    list.querySelectorAll("[data-mdel]").forEach((b) =>
      b.addEventListener("click", () => delMaterial(parseInt(b.dataset.mdel)))
    );
  } catch (e) {
    list.innerHTML = `<p class="muted">加载失败：${escapeHtml(e.message)}</p>`;
  }
}

$("btn-upload-material").addEventListener("click", async () => {
  const files = $("mat-file").files;
  if (!files.length) { toast("请先选择文件", "error"); return; }
  const btn = $("btn-upload-material");
  btn.disabled = true;
  try {
    for (const f of files) {
      const fd = new FormData();
      fd.append("file", f);
      await api("/api/materials", { method: "POST", body: fd });
    }
    $("mat-file").value = "";
    toast("素材已上传", "success");
    await loadMaterials();
  } catch (e) {
    toast(e.message, "error");
  } finally {
    btn.disabled = false;
  }
});

async function delMaterial(id) {
  if (!confirm("确定删除这个素材？")) return;
  try {
    await api(`/api/materials/${id}`, { method: "DELETE" });
    toast("已删除", "success");
    await loadMaterials();
  } catch (e) { toast(e.message, "error"); }
}

/* ---------- 工具 ---------- */
function escapeHtml(s) {
  return String(s ?? "").replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

/* ---------- 初始化 ---------- */
async function init() {
  await loadConfig();
  try {
    const themes = await api("/api/themes");
    state.themes = themes;
    $("s3-theme").innerHTML = themes.map((t) => `<option value="${t.key}">${t.name}</option>`).join("");
  } catch (e) {}
  try {
    const tpls = await api("/api/templates");
    $("s1-template").innerHTML = tpls.map((t) => `<option value="${t.key}">${t.name}</option>`).join("");
    if (tpls.length) state.template = tpls[0].key;
  } catch (e) {}
}

init();
