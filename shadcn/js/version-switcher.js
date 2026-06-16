async function fetchVersionsJson() {
  const candidates = ["./versions.json", "../versions.json", "/versions.json"];

  for (const path of candidates) {
    try {
      const url = new URL(path, window.location.href);
      const res = await fetch(url.href, { cache: "no-store" });

      if (res.ok) {
        console.log("versions.json loaded from:", url.href);
        return await res.json();
      }
    } catch (e) {
      // ignore and try next
    }
  }

  throw new Error("Could not locate versions.json");
}

let options = [];

async function loadVersions() {
  const data = await fetchVersionsJson();

  options = data.map((item) => {
    const alias = item.aliases.length ? ` (${item.aliases.join(", ")})` : "";
    return {
      value: item.version,
      label: item.title + alias,
    };
  });

  if (options.length > 0) {
    document.getElementById("dropdownBtn").innerText = options[0].value;
  }
}

async function toggleDropdown() {
  const btn = document.getElementById("dropdownBtn");
  const list = document.getElementById("dropdownList");

  if (options.length === 0) {
    await loadVersions();
  }

  const rect = btn.getBoundingClientRect();
  list.style.top = rect.bottom + "px";
  list.style.left = rect.left + "px";
  list.style.position = "fixed";
  list.style.zIndex = "9999";

  list.innerHTML = options
    .map(
      (opt) => `
    <div
      onclick="selectVersion('${opt.value}')"
      style="padding:8px 12px;cursor:pointer;"
      onmouseover="this.style.background='#f3f4f6'"
      onmouseout="this.style.background='#fff'"
    >
      ${opt.label}
    </div>
  `,
    )
    .join("");

  list.style.display = list.style.display === "none" ? "block" : "none";
}

function buildVersionRoot(version) {
  return "/" + version + "/";
}

function selectVersion(version) {
  document.getElementById("dropdownBtn").innerText = version;
  document.getElementById("dropdownList").style.display = "none";

  const segments = window.location.pathname.split("/").filter(Boolean);
  const rest = segments.slice(1).join("/");
  window.location.href = buildVersionRoot(version) + rest;
}

// Close dropdown when clicking outside
document.addEventListener("click", function (e) {
  const list = document.getElementById("dropdownList");
  const btn = document.getElementById("dropdownBtn");
  if (list && btn && !btn.contains(e.target) && !list.contains(e.target)) {
    list.style.display = "none";
  }
});

// Auto-initialize on page load
document.addEventListener("DOMContentLoaded", loadVersions);
