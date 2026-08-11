const API_BASE = ""; // same origin once served by the Pi

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

async function pollSystem() {
  try {
    const res = await fetch(`${API_BASE}/api/system`);
    if (!res.ok) throw new Error("bad response");
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

updateClock();
pollSystem();
setInterval(updateClock, 1000);
setInterval(pollSystem, 2000);