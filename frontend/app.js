const API_BASE = "";
let activeModules = {};

function updateClock() {
  const now = new Date();
  document.getElementById("clock").textContent =
    now.toLocaleTimeString("en-GB", { hour12: false });
  document.getElementById("date").textContent =
    now.toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "short" });
}

function formatUptime(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  return `${h}h ${m}m`;
}

async function loadModules() {
  try {
    const res = await fetch(`${API_BASE}/api/config`);
    const cfg = await res.json();
    activeModules = cfg.modules || {};
    document.getElementById("env-card").style.display =
      activeModules.environment ? "flex" : "none";
    document.getElementById("lighting-panel").style.display =
      activeModules.lighting ? "flex" : "none";
  } catch (err) {
    console.error("config load failed", err);
  }
}

async function pollSystem() {
  try {
    const res = await fetch(`${API_BASE}/api/system`);
    const data = await res.json();

    document.getElementById("cpu").textContent = `${data.cpu}%`;
    document.getElementById("memory").textContent = `${data.memory}%`;
    document.getElementById("storage").textContent = `${data.storage}%`;
    document.getElementById("network").textContent = data.network;
    document.getElementById("uptime").textContent = formatUptime(data.uptime);

    document.getElementById("status-dot").classList.add("online");
    document.getElementById("status-text").textContent = data.simulated
      ? "SYSTEM ONLINE (SIMULATED)"
      : "SYSTEM ONLINE";
  } catch (err) {
    document.getElementById("status-dot").classList.remove("online");
    document.getElementById("status-text").textContent = "CONNECTION LOST";
  }
}

async function pollEnvironment() {
  if (!activeModules.environment) return;
  try {
    const res = await fetch(`${API_BASE}/api/environment`);
    const data = await res.json();
    document.getElementById("env-temp").textContent = `${data.temperature}°C`;
    document.getElementById("env-humidity").textContent = `${data.humidity}% HUMIDITY`;
  } catch (err) {
    console.error("environment poll failed", err);
  }
}

async function setLedMode(mode) {
  try {
    await fetch(`${API_BASE}/api/leds`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mode }),
    });
    document.querySelectorAll(".led-btn").forEach(btn => btn.classList.remove("active"));
    document.getElementById(`led-${mode.toLowerCase()}`)?.classList.add("active");
  } catch (err) {
    console.error("led set failed", err);
  }
}

function wireLedButtons() {
  document.querySelectorAll(".led-btn").forEach(btn => {
    btn.addEventListener("click", () => setLedMode(btn.dataset.mode));
  });
}

async function init() {
  await loadModules();
  wireLedButtons();
  updateClock();
  pollSystem();
  pollEnvironment();
  setInterval(updateClock, 1000);
  setInterval(pollSystem, 2000);
  setInterval(pollEnvironment, 3000);
}

init();