from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old = '''const COUNTER_API_BASE =
  "https://script.google.com/macros/s/AKfycbxWJC2FBZvwX9FjiOUX5BFFuAb0aNwD3FoF9dp7ILzaIrsxYcNiKYeRKzgXQ2tHIUxG/exec";
function updateCounterDisplay(data) {
  const today = new Date().toISOString().slice(0, 10);
  document.getElementById("usageCount").textContent = data?.count ?? "—";

  const dateOnly = data?.lastUpdated
    ? data.lastUpdated.slice(0, 10)
    : today;

  document.getElementById("lastUpdated").textContent = dateOnly;
}

function readCounter() {
  fetch(`${COUNTER_API_BASE}?action=read&t=${Date.now()}`, { cache: "no-store" })
    .then((res) => res.json())
    .then(updateCounterDisplay)
    .catch(() => {
      document.getElementById("usageCount").textContent = "—";
      document.getElementById("lastUpdated").textContent = "—";
    });
}

function makeRid() {
  if (crypto && crypto.randomUUID) return crypto.randomUUID();
  return `${Date.now()}_${Math.random().toString(16).slice(2)}`;
}



function incrementCounterAndRefresh() {

  const rid = makeRid();

  const incUrl =
    `${COUNTER_API_BASE}?action=inc&rid=${encodeURIComponent(rid)}&t=${Date.now()}`;

  fetch(incUrl, {
    cache: "no-store",
    keepalive: true
  })
    .then((res) => res.json())
    .then(updateCounterDisplay)
    .catch(() => {});
}


goGemBtn.onclick = () => {
  if (!termsAgree.checked) return;
  incrementCounterAndRefresh();
  window.open(CHECK_URL, "_blank", "noopener,noreferrer");
};
'''

new = '''const COUNTER_API_BASE =
  "https://script.google.com/macros/s/AKfycbxWJC2FBZvwX9FjiOUX5BFFuAb0aNwD3FoF9dp7ILzaIrsxYcNiKYeRKzgXQ2tHIUxG/exec";

const COUNTER_CACHE_KEY = "thesisFormatCounterCacheV1";
let counterIncrementInFlight = false;
let goGemClickLocked = false;

function updateCounterDisplay(data) {
  if (data?.count !== undefined && data?.count !== null) {
    document.getElementById("usageCount").textContent = data.count;
  }
  if (data?.lastUpdated) {
    document.getElementById("lastUpdated").textContent = data.lastUpdated.slice(0, 10);
  }
}

function saveCounterCache(data) {
  if (data?.count === undefined || data?.count === null) return;
  try {
    localStorage.setItem(COUNTER_CACHE_KEY, JSON.stringify({
      count: data.count,
      lastUpdated: data.lastUpdated || "",
      savedAt: Date.now()
    }));
  } catch (e) {}
}

function loadCounterCache() {
  try {
    const cached = JSON.parse(localStorage.getItem(COUNTER_CACHE_KEY) || "null");
    if (!cached || cached.count === undefined || cached.count === null) return false;
    updateCounterDisplay(cached);
    return true;
  } catch (e) {
    return false;
  }
}

function readCounter() {
  const hasCache = loadCounterCache();
  fetch(`${COUNTER_API_BASE}?action=read&t=${Date.now()}`, { cache: "no-store" })
    .then((res) => {
      if (!res.ok) throw new Error(`Counter read failed: ${res.status}`);
      return res.json();
    })
    .then((data) => {
      updateCounterDisplay(data);
      saveCounterCache(data);
    })
    .catch(() => {
      if (!hasCache) {
        document.getElementById("usageCount").textContent = "—";
        document.getElementById("lastUpdated").textContent = "—";
      }
    });
}

function makeRid() {
  if (window.crypto && crypto.randomUUID) return crypto.randomUUID();
  return `${Date.now()}_${Math.random().toString(16).slice(2)}`;
}

function incrementCounterAndRefresh() {
  if (counterIncrementInFlight) return Promise.resolve(false);
  counterIncrementInFlight = true;
  const rid = makeRid();
  const incUrl = `${COUNTER_API_BASE}?action=inc&rid=${encodeURIComponent(rid)}&t=${Date.now()}`;
  return fetch(incUrl, { cache: "no-store", keepalive: true })
    .then((res) => {
      if (!res.ok) throw new Error(`Counter increment failed: ${res.status}`);
      return res.json();
    })
    .then((data) => {
      updateCounterDisplay(data);
      saveCounterCache(data);
      return true;
    })
    .catch(() => false)
    .finally(() => {
      counterIncrementInFlight = false;
    });
}


goGemBtn.onclick = () => {
  if (!termsAgree.checked || goGemClickLocked) return;
  goGemClickLocked = true;
  incrementCounterAndRefresh();
  window.open(CHECK_URL, "_blank", "noopener,noreferrer");
  setTimeout(() => {
    goGemClickLocked = false;
  }, 1500);
};
'''

if old not in s:
    raise SystemExit('Counter block not found')
s = s.replace(old, new, 1)

s = s.replace('''goGuideBtn.addEventListener("click", (e) => {
  e.preventDefault();
  incrementCounterAndRefresh();

  setTimeout(() => {
''', '''goGuideBtn.addEventListener("click", (e) => {
  e.preventDefault();

  setTimeout(() => {
''', 1)

s = s.replace('''    await navigator.clipboard.writeText(text);
    incrementCounterAndRefresh();
    alert("✅ 已複製「投稿分類建議指令」！''', '''    await navigator.clipboard.writeText(text);
    alert("✅ 已複製「投稿分類建議指令」！''', 1)

s = s.replace('''           await navigator.clipboard.writeText(text);
           incrementCounterAndRefresh();

         alert("✅ 已複製細項檢查指令！''', '''           await navigator.clipboard.writeText(text);

         alert("✅ 已複製細項檢查指令！''', 1)

s = s.replace('''    await navigator.clipboard.writeText(text);
    incrementCounterAndRefresh();
    alert(successMessage);''', '''    await navigator.clipboard.writeText(text);
    alert(successMessage);''', 1)

p.write_text(s, encoding='utf-8')
