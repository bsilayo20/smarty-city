// Synthetic dataset loaded from local JSON file (for demo)
let arushaData = null;
const districtByCode = {};

async function loadData() {
  if (arushaData) return arushaData;
  const res = await fetch("arusha_data.json");
  arushaData = await res.json();
  arushaData.districts.forEach((d) => {
    districtByCode[d.code] = d;
  });
  return arushaData;
}

// ---------- Map + UI Initialization ----------

async function initMap() {
  const data = await loadData();
  const map = L.map("map").setView([-3.3869, 36.6829], 8); // Arusha region

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors",
  }).addTo(map);

  // Add markers for health facilities
  data.health_facilities.forEach((f) => {
    const d = districtByCode[f.district_code];
    L.marker([f.lat, f.lng]).addTo(map).bindPopup(
      `<strong>${f.name}</strong><br/>Wilaya: ${d.name}<br/>Kata: ${f.ward}<br/>Vitanda: ${f.bed_capacity}`
    );
  });

  // Add markers for education centers (circle markers)
  data.education_centers.forEach((s) => {
    const d = districtByCode[s.district_code];
    L.circleMarker([s.lat, s.lng], {
      color: "#00a3dd",
      radius: 5,
      fillOpacity: 0.9,
    })
      .addTo(map)
      .bindPopup(
        `<strong>${s.name}</strong><br/>Wilaya: ${d.name}<br/>Kata: ${s.ward}<br/>Uwezo: ${s.student_capacity}`
      );
  });
}

async function initTables() {
  const data = await loadData();
  const healthBody = document.querySelector("#health-table tbody");
  const eduBody = document.querySelector("#education-table tbody");

  healthBody.innerHTML = "";
  data.health_facilities.forEach((f) => {
    const d = districtByCode[f.district_code];
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${f.name}</td>
      <td>${d.name}</td>
      <td>${f.ward}</td>
      <td>${f.bed_capacity}</td>
      <td>${f.specialized_services.join(", ")}</td>
    `;
    healthBody.appendChild(tr);
  });

  eduBody.innerHTML = "";
  data.education_centers.forEach((s) => {
    const d = districtByCode[s.district_code];
    const ratio = s.student_teacher_ratio.toFixed(1);
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${s.name}</td>
      <td>${d.name}</td>
      <td>${s.ward}</td>
      <td>${s.student_capacity.toLocaleString("sw-TZ")}</td>
      <td>${ratio}:1</td>
    `;
    eduBody.appendChild(tr);
  });
}

async function initStats() {
  const data = await loadData();
  const { population_stats, weather_logs } = data;
  const totalPop = population_stats.reduce((sum, p) => sum + p.population, 0);

  // Simple "hotspots" by growth rate
  const sortedByGrowth = [...population_stats].sort(
    (a, b) => b.annual_growth_rate - a.annual_growth_rate
  );
  const topHotspots = sortedByGrowth.slice(0, 2);

  document.getElementById("stat-population").textContent =
    totalPop.toLocaleString("sw-TZ");
  document.getElementById(
    "stat-hotspot-ward"
  ).textContent = `${topHotspots
    .map((p) => `${p.ward} (${districtByCode[p.district_code].name})`)
    .join(", ")}`;

  // Take latest weather log for Arusha City (Sekei) as headline
  const sekeiWeather = weather_logs.find(
    (w) => w.district_code === "ARU" && w.ward === "Sekei"
  );
  if (sekeiWeather) {
    document.getElementById("stat-temp").textContent =
      sekeiWeather.temperature_c.toFixed(1) + " °C";
    document.getElementById(
      "stat-weather-desc"
    ).textContent = `${sekeiWeather.condition}, mvua ${sekeiWeather.rain_mm.toFixed(
      1
    )} mm, unyevunyevu ${sekeiWeather.humidity_pct}%`;
  }

  // Example derived alerts
  const alertsCount = weather_logs.filter(
    (w) => w.rain_mm > 6 || w.humidity_pct > 85
  ).length;
  document.getElementById("stat-alerts-count").textContent = alertsCount;

  // Datetime
  document.getElementById("current-datetime").textContent =
    new Date().toLocaleString("sw-TZ");
}

// ---------- AI Reasoning Core (Rule-Based Demo) ----------

function analyzePopulationHotspots(data, options = {}) {
  const {
    densityThreshold = 1000,
    growthThreshold = 0.035, // 3.5%+
  } = options;

  const hotspots = data.population_stats.filter(
    (p) =>
      p.density_per_km2 >= densityThreshold ||
      p.annual_growth_rate >= growthThreshold
  );

  return hotspots.map((p) => {
    const district = districtByCode[p.district_code];
    const projected = Math.round(p.population * (1 + p.annual_growth_rate));
    const ratio = p.annual_growth_rate * 100;
    return {
      ward: p.ward,
      district: district.name,
      current_population: p.population,
      projected_next_year: projected,
      density: p.density_per_km2,
      growth_rate_pct: ratio,
      recommendation:
        "Inapendekezwa kuongeza vituo vya afya na shule katika kata hii ili kukidhi mahitaji ya idadi ya watu na kupunguza msongamano.",
    };
  });
}

function analyzeWeatherHealthRisks(data) {
  const risks = [];
  data.weather_logs.forEach((w) => {
    const district = districtByCode[w.district_code];
    if (w.rain_mm >= 6 && w.humidity_pct >= 85) {
      risks.push({
        ward: w.ward,
        district: district.name,
        issue:
          "Hatari ya mafuriko na kuongezeka kwa magonjwa yanayohusiana na maji (mf. kuhara, kipindupindu).",
        suggestion:
          "Imependekezwa kuimarisha mifereji ya maji, kutoa elimu ya usafi wa mazingira, na kuandaa vituo vya afya kwa ongezeko la wagonjwa.",
      });
    } else if (w.rain_mm >= 4 && w.humidity_pct >= 80) {
      risks.push({
        ward: w.ward,
        district: district.name,
        issue:
          "Hali ya hewa inaweza kuchochea kuongezeka kwa mbu na malaria.",
        suggestion:
          "Panga kampeni za kupulizia viuatilifu, kugawa vyandarua, na kuimarisha huduma za uchunguzi wa malaria.",
      });
    }
  });
  return risks;
}

// High-level "reasoning loop" that chains analyses
function reasoningLoop(question, data) {
  const steps = [];
  const lowerQ = question.toLowerCase();

  steps.push("Hatua 1: Kuchambua swali na kubaini mada kuu.");
  let topic = "general";

  if (
    lowerQ.includes("idadi ya watu") ||
    lowerQ.includes("ongezeko") ||
    lowerQ.includes("msongamano") ||
    lowerQ.includes("population")
  ) {
    topic = "population";
  } else if (
    lowerQ.includes("afya") ||
    lowerQ.includes("hospital") ||
    lowerQ.includes("vituo vya afya")
  ) {
    topic = "health";
  } else if (lowerQ.includes("shule") || lowerQ.includes("elimu")) {
    topic = "education";
  } else if (
    lowerQ.includes("hali ya hewa") ||
    lowerQ.includes("mvua") ||
    lowerQ.includes("weather")
  ) {
    topic = "weather";
  }

  steps.push(`Hatua 2: Mada iliyotambuliwa ni: ${topic}.`);

  let answer = "";
  if (topic === "population") {
    steps.push(
      "Hatua 3: Kuwatambua wakazi wengi / maeneo yenye kasi kubwa ya ukuaji."
    );
    const hotspots = analyzePopulationHotspots(data);
    if (hotspots.length === 0) {
      answer =
        "Kwa mujibu wa takwimu zilizopo, hakuna kata zinazovuka viwango vya juu vya msongamano au ukuaji wa idadi ya watu kwa sasa.";
    } else {
      const bullets = hotspots
        .map(
          (h) =>
            `- ${h.ward} (${h.district}): watu ${h.current_population.toLocaleString(
              "sw-TZ"
            )}, msongamano ${h.density.toFixed(
              0
            )} kwa km², ukuaji ${h.growth_rate_pct.toFixed(1)}% kwa mwaka. ${
              h.recommendation
            }`
        )
        .join("\n");

      answer =
        "Kata zifuatazo zina ongezeko kubwa la watu au msongamano mkubwa:\n" +
        bullets;
    }

    steps.push(
      "Hatua 4: Kutoa mapendekezo ya upangaji wa miundombinu (shule na vituo vya afya)."
    );
  } else if (topic === "weather") {
    steps.push(
      "Hatua 3: Kuchambua rekodi za mvua, joto na unyevunyevu na kuoanisha na hatari za kiafya."
    );
    const risks = analyzeWeatherHealthRisks(data);
    if (risks.length === 0) {
      answer =
        "Kutokana na takwimu za sasa za hali ya hewa, hakuna maeneo yenye hatari kubwa iliyotambuliwa. Hata hivyo, ufuatiliaji endelevu unapendekezwa.";
    } else {
      const bullets = risks
        .map(
          (r) =>
            `- ${r.ward} (${r.district}): ${r.issue} ${r.suggestion}`
        )
        .join("\n");
      answer =
        "Kuna maeneo yenye hali ya hewa inayoweza kuleta changamoto za kiafya:\n" +
        bullets;
    }
    steps.push(
      "Hatua 4: Kutoa mapendekezo ya kinga na maandalizi ya huduma za afya."
    );
  } else if (topic === "health") {
    steps.push(
      "Hatua 3: Kutumia data ya vituo vya afya kuonyesha upatikanaji wa huduma muhimu."
    );
    const facilities = data.health_facilities;
    const summary = facilities
      .map((f) => {
        const d = districtByCode[f.district_code];
        return `- ${f.name} (${d.name}, ${f.ward}): vitanda ${
          f.bed_capacity
        }, huduma maalumu: ${f.specialized_services.join(", ")}`;
      })
      .join("\n");
    answer =
      "Muhtasari wa vituo vikuu vya afya katika Arusha:\n" +
      summary +
      "\nKwa kata zenye ongezeko kubwa la watu, inapendekezwa kuongeza au kupanua huduma katika vituo vilivyopo au kujenga vituo vipya vya afya vya ngazi ya kata.";
    steps.push(
      "Hatua 4: Kutoa mapendekezo ya kuongeza vituo vya afya kwenye kata zenye uhitaji mkubwa."
    );
  } else if (topic === "education") {
    steps.push(
      "Hatua 3: Kuchambua uwezo wa shule na uwiano wa mwalimu kwa mwanafunzi."
    );
    const schools = data.education_centers;
    const crowded = schools.filter((s) => s.student_teacher_ratio > 25);
    const lines = crowded
      .map((s) => {
        const d = districtByCode[s.district_code];
        return `- ${s.name} (${d.name}, ${s.ward}): uwiano ${s.student_teacher_ratio.toFixed(
          1
        )}:1`;
      })
      .join("\n");
    if (crowded.length === 0) {
      answer =
        "Hakuna shule zilizo na uwiano wa juu sana wa mwalimu kwa mwanafunzi kulingana na vigezo vilivyowekwa. Hata hivyo, ufuatiliaji wa mara kwa mara unahitajika.";
    } else {
      answer =
        "Shule zifuatazo zina uwiano wa juu wa mwalimu kwa mwanafunzi, hivyo zinahitaji kuongezewa walimu au miundombinu:\n" +
        lines;
    }
    steps.push(
      "Hatua 4: Kupendekeza kuongeza rasilimali za elimu katika maeneo yenye msongamano."
    );
  } else {
    steps.push("Hatua 3: Kutumia muhtasari wa jumla wa takwimu.");
    answer =
      "Mfumo huu unaunganisha data za idadi ya watu, elimu, afya na hali ya hewa kwa Jiji la Arusha na wilaya jirani (Meru, Karatu, Monduli). Uliza swali mahsusi kuhusu 'idadi ya watu', 'shule', 'vituo vya afya' au 'hali ya hewa' ili kupata uchambuzi unaolengwa.";
  }

  steps.push("Hatua 5: Kurudisha jibu la mwisho na maelezo ya hoja zilizotumika.");
  return { answer, steps };
}

// High-level chatbot entry
function answerQuery(question) {
  const { answer, steps } = reasoningLoop(question, arushaData);
  const explanation =
    "Muhtasari wa hoja za AI:\n" + steps.map((s) => `• ${s}`).join("\n");
  return { answer, explanation };
}

// ---------- Chat UI Wiring ----------

function appendChatMessage(role, text) {
  const body = document.getElementById("chat-body");
  const msgDiv = document.createElement("div");
  msgDiv.className = `chat-message ${role}`;
  const bubble = document.createElement("div");
  bubble.className = "chat-bubble";
  bubble.textContent = text;

  if (role === "bot") {
    const badge = document.createElement("div");
    badge.className = "chat-badge";
    badge.textContent = "AI";
    msgDiv.appendChild(badge);
    msgDiv.appendChild(bubble);
  } else {
    msgDiv.appendChild(bubble);
  }

  body.appendChild(msgDiv);
  body.scrollTop = body.scrollHeight;
}

function wireChat() {
  const form = document.getElementById("chat-form");
  const input = document.getElementById("chat-input");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const q = input.value.trim();
    if (!q) return;
    appendChatMessage("user", q);
    input.value = "";

    // Ensure data is loaded for reasoning
    await loadData();

    // Try backend AI first; fall back to local reasoning if unavailable
    try {
      const resp = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: q }),
      });

      if (resp.ok) {
        const data = await resp.json();
        appendChatMessage("bot", data.answer);
        if (Array.isArray(data.reasoning_steps)) {
          const explanation =
            "Muhtasari wa hoja za AI (backend):\n" +
            data.reasoning_steps.map((s) => `• ${s}`).join("\n");
          appendChatMessage("bot", explanation);
        }
        return;
      }
    } catch (err) {
      console.warn("Backend AI unavailable, using local reasoning.", err);
    }

    // Local in-browser reasoning fallback
    const { answer, explanation } = answerQuery(q);
    appendChatMessage("bot", answer);
    appendChatMessage("bot", explanation);
  });
}

// ---------- Bootstrap ----------

window.addEventListener("DOMContentLoaded", async () => {
  await loadData();
  initMap();
  initTables();
  initStats();
  wireChat();
});

