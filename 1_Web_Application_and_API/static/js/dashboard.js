/**
 * Social Pulse Analytics - Interactive Dashboard Controller
 * Handles Chart.js Visualizations, REST API Integration, and Interactive Analytics.
 */

// Global State
let globalCharts = {};
let globalSummary = null;
let globalDescriptive = null;
let globalCorrelations = null;
let globalPlatforms = null;
let globalPersonas = null;
let globalHypothesis = null;
let globalOutliers = null;
let currentCorrMethod = "pearson";
let dataTableSearchDebounce = null;
let simDebounceTimer = null;

// Platform Color Palette
const PLATFORM_COLORS = {
  "Instagram": "#e1306c",
  "TikTok": "#00f2fe",
  "YouTube": "#ff0000",
  "Twitter/X": "#1da1f2",
  "LinkedIn": "#0a66c2",
  "Facebook": "#1877f2"
};

// Initialization on DOM ready
document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  loadAllDashboardData();
  loadDataTable(1);
  runPredictionSimulator();
});

// ----------------------------------------------------------------------------
// Theme Toggle & Tab Navigation
// ----------------------------------------------------------------------------

function initTheme() {
  const isDark = localStorage.getItem("theme") !== "light";
  if (isDark) {
    document.documentElement.classList.add("dark");
    document.getElementById("themeIcon").className = "fa-solid fa-sun text-amber-400";
  } else {
    document.documentElement.classList.remove("dark");
    document.getElementById("themeIcon").className = "fa-solid fa-moon text-indigo-600";
  }
}

function toggleTheme() {
  const isDark = document.documentElement.classList.toggle("dark");
  localStorage.setItem("theme", isDark ? "dark" : "light");
  document.getElementById("themeIcon").className = isDark ? "fa-solid fa-sun text-amber-400" : "fa-solid fa-moon text-indigo-600";
  
  // Re-render charts to adapt to dark/light theme grids
  Object.values(globalCharts).forEach(chart => {
    if (chart && typeof chart.update === "function") chart.update();
  });
}

function switchTab(tabId) {
  document.querySelectorAll(".tab-content").forEach(el => el.classList.add("hidden"));
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.classList.remove("active-tab");
    btn.classList.add("inactive-tab");
  });

  const targetTab = document.getElementById(`tab-${tabId}`);
  const targetBtn = document.getElementById(`tab-btn-${tabId}`);
  
  if (targetTab) targetTab.classList.remove("hidden");
  if (targetBtn) {
    targetBtn.classList.add("active-tab");
    targetBtn.classList.remove("inactive-tab");
  }

  // Trigger chart updates on tab switch
  setTimeout(() => {
    if (tabId === "correlations" && !globalCharts.customScatter) {
      updateCustomScatter();
    }
    if (tabId === "descriptive" && !globalCharts.distHist) {
      renderDistributionChart();
    }
    if (tabId === "platforms" && !globalCharts.platformRadar) {
      renderPlatformRadar();
    }
  }, 50);
}

// ----------------------------------------------------------------------------
// Fetch All Dashboard Data
// ----------------------------------------------------------------------------

async function loadAllDashboardData() {
  try {
    const [summaryRes, descRes, corrRes, hypoRes, outlierRes] = await Promise.all([
      fetch("/api/summary").then(r => r.json()),
      fetch("/api/descriptive").then(r => r.json()),
      fetch("/api/correlations").then(r => r.json()),
      fetch("/api/hypothesis-tests").then(r => r.json()),
      fetch("/api/outliers").then(r => r.json())
    ]);

    if (summaryRes.success) {
      globalSummary = summaryRes;
      updateKpisUI(summaryRes.kpis);
      renderOverviewCharts(summaryRes);
      renderPersonas(summaryRes.personas);
      renderPlatformTable(summaryRes.platforms);
    }

    if (descRes.success) {
      globalDescriptive = descRes.descriptive_statistics;
      renderDescriptiveTable(globalDescriptive);
      renderDistributionChart();
    }

    if (corrRes.success) {
      globalCorrelations = corrRes.correlation_data;
      renderCorrelationHeatmap();
      renderCorrelationInsights();
      updateCustomScatter();
    }

    if (hypoRes.success) {
      globalHypothesis = hypoRes.hypothesis_tests;
      renderHypothesisTests(globalHypothesis);
    }

    if (outlierRes.success) {
      globalOutliers = outlierRes.outliers;
      renderOutliers(globalOutliers);
    }

    initRegressionTab();

  } catch (err) {
    console.error("Failed to load dashboard data:", err);
    showToast("Error loading analytics data", "error");
  }
}

// ----------------------------------------------------------------------------
// Overview TAB: KPIs & Charts
// ----------------------------------------------------------------------------

function updateKpisUI(kpis) {
  if (!kpis) return;
  document.getElementById("kpiAvgScreenTime").innerHTML = `${kpis.avg_screen_time_hours} <span class="text-xs font-normal text-gray-400">hrs/day</span>`;
  document.getElementById("kpiMedScreenTime").textContent = kpis.median_screen_time_hours;
  document.getElementById("kpiAvgPosts").textContent = kpis.avg_posts_per_week;
  document.getElementById("kpiTotalPosts").textContent = kpis.total_weekly_posts.toLocaleString();
  document.getElementById("kpiAvgLikes").textContent = kpis.avg_likes_per_post.toLocaleString();
  document.getElementById("kpiMedLikes").textContent = kpis.median_likes_per_post.toLocaleString();
  document.getElementById("kpiAvgFollowers").textContent = kpis.avg_followers.toLocaleString();
  document.getElementById("kpiMedFollowers").textContent = kpis.median_followers.toLocaleString();
  document.getElementById("kpiAvgEngagement").textContent = `${kpis.avg_engagement_rate}%`;
  document.getElementById("kpiTopPlatform").textContent = kpis.top_platform;
  document.getElementById("datasetRecordsCount").textContent = kpis.total_users.toLocaleString();
}

function renderOverviewCharts(data) {
  const isDark = document.documentElement.classList.contains("dark");
  const textColor = isDark ? "#9ca3af" : "#4b5563";
  const gridColor = isDark ? "#1f2937" : "#f3f4f6";

  // 1. Platform Donut Chart
  const platData = data.platforms.platforms;
  const platLabels = Object.keys(platData);
  const platCounts = platLabels.map(k => platData[k].user_count);
  const platColors = platLabels.map(k => PLATFORM_COLORS[k] || "#6366f1");

  if (globalCharts.platformDonut) globalCharts.platformDonut.destroy();
  const ctxPlat = document.getElementById("platformDonutChart").getContext("2d");
  globalCharts.platformDonut = new Chart(ctxPlat, {
    type: "doughnut",
    data: {
      labels: platLabels,
      datasets: [{
        data: platCounts,
        backgroundColor: platColors,
        borderWidth: 0,
        hoverOffset: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "right", labels: { color: textColor, font: { size: 11 } } }
      },
      cutout: "68%"
    }
  });

  // 2. Health Donut Chart
  const healthData = data.kpis.screen_time_health_breakdown;
  if (globalCharts.healthDonut) globalCharts.healthDonut.destroy();
  const ctxHealth = document.getElementById("healthDonutChart").getContext("2d");
  globalCharts.healthDonut = new Chart(ctxHealth, {
    type: "doughnut",
    data: {
      labels: ["Healthy (<2.5h)", "Moderate (2.5-5h)", "Heavy (>5h)"],
      datasets: [{
        data: [healthData.healthy, healthData.moderate, healthData.heavy],
        backgroundColor: ["#10b981", "#f59e0b", "#ef4444"],
        borderWidth: 0,
        hoverOffset: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "bottom", labels: { color: textColor, font: { size: 11 } } }
      },
      cutout: "68%"
    }
  });

  // 3. Post Type Bar Chart
  const postTypes = data.platforms.post_types;
  const ptLabels = Object.keys(postTypes);
  const ptEngagement = ptLabels.map(k => postTypes[k].avg_engagement_rate);
  const ptLikes = ptLabels.map(k => postTypes[k].avg_likes);

  if (globalCharts.postTypeBar) globalCharts.postTypeBar.destroy();
  const ctxPt = document.getElementById("postTypeBarChart").getContext("2d");
  globalCharts.postTypeBar = new Chart(ctxPt, {
    type: "bar",
    data: {
      labels: ptLabels,
      datasets: [{
        label: "Avg Engagement %",
        data: ptEngagement,
        backgroundColor: "#8b5cf6",
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: { ticks: { color: textColor }, grid: { display: false } },
        y: { ticks: { color: textColor }, grid: { color: gridColor }, title: { display: true, text: "Engagement Rate (%)", color: textColor, font: { size: 10 } } }
      }
    }
  });

  // 4. Platform Metrics Grouped Bar Chart
  const avgScreenTimes = platLabels.map(k => platData[k].avg_screen_time_hours);
  const avgWeeklyPosts = platLabels.map(k => platData[k].avg_posts_per_week);
  const avgEngRates = platLabels.map(k => platData[k].avg_engagement_rate);

  if (globalCharts.platformMetricsBar) globalCharts.platformMetricsBar.destroy();
  const ctxMetrics = document.getElementById("platformMetricsBarChart").getContext("2d");
  globalCharts.platformMetricsBar = new Chart(ctxMetrics, {
    type: "bar",
    data: {
      labels: platLabels,
      datasets: [
        { label: "Daily Screen Time (hrs)", data: avgScreenTimes, backgroundColor: "#6366f1", borderRadius: 6 },
        { label: "Weekly Posts", data: avgWeeklyPosts, backgroundColor: "#38bdf8", borderRadius: 6 },
        { label: "Engagement Rate (%)", data: avgEngRates, backgroundColor: "#f43f5e", borderRadius: 6 }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: textColor } }
      },
      scales: {
        x: { ticks: { color: textColor }, grid: { display: false } },
        y: { ticks: { color: textColor }, grid: { color: gridColor } }
      }
    }
  });
}

// ----------------------------------------------------------------------------
// TAB 2: DESCRIPTIVE STATISTICS
// ----------------------------------------------------------------------------

function renderDescriptiveTable(stats) {
  const tbody = document.getElementById("descriptiveStatsTableBody");
  tbody.innerHTML = "";

  Object.keys(stats).forEach(key => {
    const s = stats[key];
    const tr = document.createElement("tr");
    tr.className = "hover:bg-gray-50 dark:hover:bg-gray-800/40 transition cursor-pointer";
    tr.onclick = () => {
      document.getElementById("metricInspectorSelect").value = key;
      renderDistributionChart();
    };

    tr.innerHTML = `
      <td class="py-3 px-4 font-medium text-gray-900 dark:text-white flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-brand-500"></span> ${s.label}
      </td>
      <td class="py-3 px-3 text-right font-mono text-brand-600 dark:text-indigo-400 font-bold">${s.mean.toFixed(2)}</td>
      <td class="py-3 px-3 text-right font-mono">${s.median.toFixed(2)}</td>
      <td class="py-3 px-3 text-right font-mono text-gray-500">${s.mode.toFixed(1)}</td>
      <td class="py-3 px-3 text-right font-mono">${s.std_dev.toFixed(2)}</td>
      <td class="py-3 px-3 text-right font-mono text-gray-400">${s.variance.toFixed(1)}</td>
      <td class="py-3 px-3 text-right font-mono">${s.min.toFixed(1)}</td>
      <td class="py-3 px-3 text-right font-mono">${s.max.toFixed(1)}</td>
      <td class="py-3 px-3 text-right font-mono text-gray-500">${s.q1.toFixed(1)}</td>
      <td class="py-3 px-3 text-right font-mono text-gray-500">${s.q3.toFixed(1)}</td>
      <td class="py-3 px-3 text-right font-mono font-semibold text-emerald-600 dark:text-emerald-400">${s.iqr.toFixed(1)}</td>
      <td class="py-3 px-3 text-right font-mono ${s.skewness > 0.5 ? 'text-amber-500' : 'text-gray-400'}">${s.skewness > 0 ? '+' : ''}${s.skewness.toFixed(2)}</td>
      <td class="py-3 px-3 text-right font-mono text-gray-400">${s.kurtosis.toFixed(2)}</td>
    `;
    tbody.appendChild(tr);
  });
}

function renderDistributionChart() {
  if (!globalDescriptive) return;
  const metric = document.getElementById("metricInspectorSelect").value;
  const s = globalDescriptive[metric];
  if (!s) return;

  document.getElementById("distChartTitle").textContent = `Distribution & Density Curve: ${s.label}`;
  document.getElementById("skewnessTitle").textContent = `Skewness: ${s.skewness > 0 ? '+' : ''}${s.skewness.toFixed(2)}`;
  document.getElementById("skewnessText").textContent = s.skew_interpretation;
  document.getElementById("kurtosisTitle").textContent = `Kurtosis: ${s.kurtosis.toFixed(2)}`;
  document.getElementById("kurtosisText").textContent = s.kurt_interpretation;

  // Generate synthetic histogram bins from stats for snappy visualization
  const isDark = document.documentElement.classList.contains("dark");
  const textColor = isDark ? "#9ca3af" : "#4b5563";
  const gridColor = isDark ? "#1f2937" : "#f3f4f6";

  const numBins = 15;
  const step = (s.max - s.min) / numBins;
  const binLabels = [];
  const binFrequencies = [];

  for (let i = 0; i < numBins; i++) {
    const bStart = s.min + i * step;
    const bEnd = bStart + step;
    binLabels.push(`${bStart.toFixed(1)}-${bEnd.toFixed(1)}`);
    
    // Approximate skewed normal distribution curve
    const xMid = (bStart + bEnd) / 2;
    const z = (xMid - s.mean) / (s.std_dev || 1);
    const weight = Math.exp(-0.5 * z * z) / (Math.sqrt(2 * Math.PI) * (s.std_dev || 1));
    binFrequencies.push(Math.round(weight * s.count * step * 1.8));
  }

  if (globalCharts.distHist) globalCharts.distHist.destroy();
  const ctx = document.getElementById("distributionHistogramChart").getContext("2d");
  globalCharts.distHist = new Chart(ctx, {
    type: "bar",
    data: {
      labels: binLabels,
      datasets: [{
        label: "Estimated User Frequency",
        data: binFrequencies,
        backgroundColor: "rgba(99, 102, 241, 0.65)",
        borderColor: "#4f46e5",
        borderWidth: 1.5,
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: textColor } },
        tooltip: {
          callbacks: {
            footer: () => `Mean: ${s.mean.toFixed(2)} | Median: ${s.median.toFixed(2)}`
          }
        }
      },
      scales: {
        x: { ticks: { color: textColor, font: { size: 9 }, maxRotation: 45 }, grid: { display: false } },
        y: { ticks: { color: textColor }, grid: { color: gridColor } }
      }
    }
  });
}

// ----------------------------------------------------------------------------
// TAB 3: CORRELATIONS
// ----------------------------------------------------------------------------

function setCorrMethod(method) {
  currentCorrMethod = method;
  document.getElementById("btnCorrPearson").className = method === "pearson" ? "px-2.5 py-1 rounded-md bg-brand-600 text-white font-medium" : "px-2.5 py-1 rounded-md text-gray-500 dark:text-gray-400 font-medium";
  document.getElementById("btnCorrSpearman").className = method === "spearman" ? "px-2.5 py-1 rounded-md bg-brand-600 text-white font-medium" : "px-2.5 py-1 rounded-md text-gray-500 dark:text-gray-400 font-medium";
  renderCorrelationHeatmap();
}

function renderCorrelationHeatmap() {
  if (!globalCorrelations) return;
  const grid = document.getElementById("correlationHeatmapGrid");
  grid.innerHTML = "";

  const cols = globalCorrelations.columns;
  const labels = globalCorrelations.labels;
  const matrix = globalCorrelations[currentCorrMethod];

  // Table element
  const table = document.createElement("table");
  table.className = "min-w-full text-center text-xs font-mono";

  // Header
  const thead = document.createElement("thead");
  const trH = document.createElement("tr");
  trH.innerHTML = `<th class="p-2 text-left font-sans text-gray-400">Metric</th>`;
  cols.forEach(c => {
    const th = document.createElement("th");
    th.className = "p-2 font-sans text-gray-600 dark:text-gray-300 truncate max-w-[80px]";
    th.textContent = labels[c] ? labels[c].split(" ")[0] : c;
    th.title = labels[c] || c;
    trH.appendChild(th);
  });
  thead.appendChild(trH);
  table.appendChild(thead);

  // Body
  const tbody = document.createElement("tbody");
  cols.forEach(r => {
    const tr = document.createElement("tr");
    const tdLabel = document.createElement("td");
    tdLabel.className = "p-2 text-left font-sans font-medium text-gray-700 dark:text-gray-300 truncate max-w-[120px]";
    tdLabel.textContent = labels[r] || r;
    tr.appendChild(tdLabel);

    cols.forEach(c => {
      const val = matrix[r] ? matrix[r][c] : 0;
      const td = document.createElement("td");
      td.className = "p-2 font-bold corr-cell cursor-pointer rounded-lg";
      
      // Color interpolation: blue for negative, red/indigo for positive
      let bg = "rgba(100, 116, 139, 0.1)";
      let textColor = "#94a3b8";
      if (val > 0.1) {
        bg = `rgba(99, 102, 241, ${Math.min(1.0, val * 1.1)})`;
        textColor = val > 0.4 ? "#ffffff" : "#6366f1";
      } else if (val < -0.1) {
        bg = `rgba(239, 68, 68, ${Math.min(1.0, Math.abs(val) * 1.1)})`;
        textColor = Math.abs(val) > 0.4 ? "#ffffff" : "#ef4444";
      }

      td.style.backgroundColor = bg;
      td.style.color = textColor;
      td.textContent = val.toFixed(2);
      td.title = `${labels[r]} <-> ${labels[c]}: r = ${val.toFixed(3)}`;
      
      td.onclick = () => {
        document.getElementById("scatterXSelect").value = r;
        document.getElementById("scatterYSelect").value = c;
        updateCustomScatter();
      };

      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });

  table.appendChild(tbody);
  grid.appendChild(table);
}

function renderCorrelationInsights() {
  if (!globalCorrelations) return;
  const container = document.getElementById("correlationInsightsList");
  container.innerHTML = "";

  globalCorrelations.insights.forEach(ins => {
    const card = document.createElement("div");
    card.className = "p-3.5 rounded-xl bg-gray-50 dark:bg-gray-900/60 border border-gray-200 dark:border-gray-800 space-y-1 text-xs hover:border-brand-500/40 transition";
    
    const isPositive = ins.correlation > 0;
    const badgeColor = isPositive ? "bg-indigo-100 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300" : "bg-rose-100 dark:bg-rose-950 text-rose-700 dark:text-rose-300";

    card.innerHTML = `
      <div class="flex items-center justify-between">
        <strong class="text-gray-900 dark:text-white font-semibold">${ins.var1} <i class="fa-solid fa-arrows-left-right text-gray-400 mx-1 text-[10px]"></i> ${ins.var2}</strong>
        <span class="px-2 py-0.5 rounded-md ${badgeColor} font-mono font-bold">r = ${ins.correlation > 0 ? '+' : ''}${ins.correlation.toFixed(2)}</span>
      </div>
      <p class="text-gray-600 dark:text-gray-300 text-[11px]">${ins.explanation}</p>
      <div class="flex items-center gap-2 text-[10px] text-gray-400 pt-1">
        <span>Strength: <strong class="text-gray-300">${ins.strength} ${ins.direction}</strong></span>
        <span>&bull;</span>
        <span>${ins.significance}</span>
      </div>
    `;
    container.appendChild(card);
  });
}

async function updateCustomScatter() {
  const xCol = document.getElementById("scatterXSelect").value;
  const yCol = document.getElementById("scatterYSelect").value;

  try {
    const res = await fetch(`/api/regression?x=${encodeURIComponent(xCol)}&y=${encodeURIComponent(yCol)}`).then(r => r.json());
    if (!res.success) return;

    const reg = res.regression;
    document.getElementById("scatterEquation").textContent = reg.equation;
    document.getElementById("scatterR2").textContent = reg.r_squared.toFixed(4);
    document.getElementById("scatterR").textContent = `${reg.r_value > 0 ? '+' : ''}${reg.r_value.toFixed(4)}`;
    document.getElementById("scatterPVal").textContent = reg.p_value < 0.0001 ? "< 0.0001" : reg.p_value.toFixed(4);

    const isDark = document.documentElement.classList.contains("dark");
    const textColor = isDark ? "#9ca3af" : "#4b5563";
    const gridColor = isDark ? "#1f2937" : "#f3f4f6";

    if (globalCharts.customScatter) globalCharts.customScatter.destroy();
    const ctx = document.getElementById("customScatterChart").getContext("2d");
    globalCharts.customScatter = new Chart(ctx, {
      type: "scatter",
      data: {
        datasets: [
          {
            label: "User Data Points",
            data: reg.scatter_sample,
            backgroundColor: "rgba(56, 189, 248, 0.6)",
            borderColor: "#0ea5e9",
            borderWidth: 1,
            pointRadius: 4
          },
          {
            type: "line",
            label: `OLS Fit Line: ${reg.equation}`,
            data: reg.fit_line,
            borderColor: "#ef4444",
            borderWidth: 2.5,
            pointRadius: 0,
            fill: false
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: textColor } }
        },
        scales: {
          x: { ticks: { color: textColor }, grid: { color: gridColor }, title: { display: true, text: reg.x_label, color: textColor } },
          y: { ticks: { color: textColor }, grid: { color: gridColor }, title: { display: true, text: reg.y_label, color: textColor } }
        }
      }
    });

  } catch (err) {
    console.error("Error fetching regression data:", err);
  }
}

// ----------------------------------------------------------------------------
// TAB 4: REGRESSION MODELS
// ----------------------------------------------------------------------------

async function initRegressionTab() {
  try {
    const res = await fetch("/api/multiple-regression").then(r => r.json());
    if (!res.success) return;

    const mult = res.multiple_regression;
    if (mult.available) {
      document.getElementById("multRegFormula").textContent = mult.formula;
      document.getElementById("multRegR2").textContent = mult.r_squared.toFixed(4);
      document.getElementById("multRegAdjR2").textContent = mult.adjusted_r_squared.toFixed(4);

      const cardsContainer = document.getElementById("multRegCoeffsCards");
      cardsContainer.innerHTML = "";

      Object.keys(mult.coefficients).forEach(feat => {
        const item = mult.coefficients[feat];
        const card = document.createElement("div");
        card.className = "p-4 rounded-xl bg-gray-50 dark:bg-gray-900/60 border border-gray-200 dark:border-gray-800 space-y-2";
        card.innerHTML = `
          <div class="flex items-center justify-between">
            <span class="text-xs text-gray-400 font-medium">${item.label}</span>
            <span class="font-mono text-xs font-bold ${item.coefficient > 0 ? 'text-emerald-500' : 'text-rose-500'}">
              β = ${item.coefficient > 0 ? '+' : ''}${item.coefficient}
            </span>
          </div>
          <p class="text-xs text-gray-600 dark:text-gray-300">${item.impact}</p>
        `;
        cardsContainer.appendChild(card);
      });
    }
  } catch (err) {
    console.error("Error loading multiple regression:", err);
  }
}

// ----------------------------------------------------------------------------
// TAB 5: PREDICTIVE SIMULATOR
// ----------------------------------------------------------------------------

function setSimPreset(st, posts, foll) {
  document.getElementById("simScreenTimeSlider").value = st;
  document.getElementById("simPostsSlider").value = posts;
  document.getElementById("simFollowersSlider").value = foll;
  runPredictionSimulator();
}

function runPredictionSimulator() {
  const st = parseFloat(document.getElementById("simScreenTimeSlider").value);
  const posts = parseFloat(document.getElementById("simPostsSlider").value);
  const followers = parseFloat(document.getElementById("simFollowersSlider").value);

  document.getElementById("simScreenTimeVal").textContent = `${st.toFixed(2)} hrs/day`;
  document.getElementById("simPostsVal").textContent = `${posts} posts/week`;
  document.getElementById("simFollowersVal").textContent = `${followers.toLocaleString()} followers`;

  clearTimeout(simDebounceTimer);
  simDebounceTimer = setTimeout(async () => {
    try {
      const res = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ screen_time: st, posts_per_week: posts, followers: followers })
      }).then(r => r.json());

      if (res.success) {
        const pred = res.prediction;
        document.getElementById("simPredEngagement").textContent = `${pred.predicted_engagement_rate}%`;
        document.getElementById("simPredLikes").textContent = pred.predicted_avg_likes.toLocaleString();
        document.getElementById("simPredGrowthRate").textContent = `+${pred.predicted_monthly_growth_rate_pct}%`;
        document.getElementById("simPredNewFollowers").textContent = `+${pred.predicted_new_followers_per_month.toLocaleString()}`;

        // Recommendation dynamic advice
        let advice = "";
        if (st > 6.0) {
          advice = `High screen time (${st}h) may lead to diminishing creator returns. Consider batching content creation and keeping daily active screen time below 4.5 hours.`;
        } else if (posts >= 7 && st <= 4.0) {
          advice = `High publishing efficiency (${posts} posts/week with ${st}h screen time). Excellent creator balance yielding high compound follower growth!`;
        } else {
          advice = `Posting ${posts} times a week with ${st}h daily screen time provides steady audience engagement and a sustainable digital wellbeing balance.`;
        }
        document.getElementById("simRecommendationText").textContent = advice;

        renderProjectionChart(followers, pred.predicted_monthly_growth_rate_pct);
      }
    } catch (err) {
      console.error("Simulation error:", err);
    }
  }, 100);
}

function renderProjectionChart(initialFollowers, monthlyGrowthRate) {
  const months = ["Month 1", "Month 2", "Month 3", "Month 4", "Month 5", "Month 6"];
  const projectedValues = [];
  let current = initialFollowers;
  const rate = 1 + (monthlyGrowthRate / 100);

  for (let i = 0; i < 6; i++) {
    current = Math.round(current * rate);
    projectedValues.push(current);
  }

  const isDark = document.documentElement.classList.contains("dark");
  const textColor = isDark ? "#9ca3af" : "#4b5563";
  const gridColor = isDark ? "#1f2937" : "#f3f4f6";

  if (globalCharts.projectionLine) globalCharts.projectionLine.destroy();
  const ctx = document.getElementById("projectionLineChart").getContext("2d");
  globalCharts.projectionLine = new Chart(ctx, {
    type: "line",
    data: {
      labels: months,
      datasets: [{
        label: "Projected Total Followers",
        data: projectedValues,
        borderColor: "#10b981",
        backgroundColor: "rgba(16, 185, 129, 0.15)",
        fill: true,
        tension: 0.35,
        pointRadius: 5,
        pointBackgroundColor: "#10b981"
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: textColor } }
      },
      scales: {
        x: { ticks: { color: textColor }, grid: { display: false } },
        y: { ticks: { color: textColor }, grid: { color: gridColor } }
      }
    }
  });
}

// ----------------------------------------------------------------------------
// TAB 6: HYPOTHESIS & OUTLIERS
// ----------------------------------------------------------------------------

function renderHypothesisTests(hypo) {
  const grid = document.getElementById("hypothesisCardsGrid");
  grid.innerHTML = "";

  Object.keys(hypo).forEach(key => {
    const test = hypo[key];
    const isSig = test.is_significant;
    const badgeColor = isSig ? "bg-emerald-100 dark:bg-emerald-950 text-emerald-700 dark:text-emerald-300" : "bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400";
    const statusText = isSig ? "Significant (Reject H₀)" : "Not Significant (Fail to Reject)";

    const card = document.createElement("div");
    card.className = "bg-white dark:bg-darkcard border border-gray-200 dark:border-darkborder rounded-2xl p-5 shadow-sm space-y-3";
    
    let statLine = "";
    if (test.t_statistic !== undefined) {
      statLine = `<span>t-Statistic: <strong class="font-mono text-gray-900 dark:text-white">${test.t_statistic}</strong></span> &bull; <span>p-value: <strong class="font-mono text-gray-900 dark:text-white">${test.p_value}</strong></span>`;
    } else if (test.f_statistic !== undefined) {
      statLine = `<span>F-Statistic: <strong class="font-mono text-gray-900 dark:text-white">${test.f_statistic}</strong></span> &bull; <span>p-value: <strong class="font-mono text-gray-900 dark:text-white">${test.p_value}</strong></span>`;
    }

    card.innerHTML = `
      <div class="flex items-center justify-between">
        <h4 class="text-sm font-bold text-gray-900 dark:text-white">${test.test_name}</h4>
        <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold ${badgeColor}">${statusText}</span>
      </div>
      <p class="text-xs text-gray-500 dark:text-gray-400">${test.hypothesis}</p>
      <div class="text-xs text-gray-500 flex items-center gap-2">
        ${statLine}
      </div>
      <div class="p-3 rounded-xl bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 text-xs text-gray-700 dark:text-gray-300 font-medium">
        <i class="fa-solid fa-square-check text-brand-500 mr-1.5"></i> ${test.conclusion}
      </div>
    `;
    grid.appendChild(card);
  });
}

function renderOutliers(outliers) {
  document.getElementById("outliersCountBadge").textContent = `${outliers.total_outliers_flagged} Outliers Flagged`;

  const summaryGrid = document.getElementById("outliersMetricSummary");
  summaryGrid.innerHTML = "";

  Object.keys(outliers.metrics_summary).forEach(k => {
    const item = outliers.metrics_summary[k];
    const card = document.createElement("div");
    card.className = "p-3 rounded-xl bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 space-y-1 text-xs";
    card.innerHTML = `
      <span class="text-gray-400 font-medium block truncate">${item.label}</span>
      <div class="text-base font-bold text-amber-500">${item.iqr_outlier_count} IQR Outliers</div>
      <span class="text-[10px] text-gray-500">Fence: [${item.lower_bound}, ${item.upper_bound}]</span>
    `;
    summaryGrid.appendChild(card);
  });

  const tbody = document.getElementById("outliersTableBody");
  tbody.innerHTML = "";

  outliers.sample_outlier_users.forEach(u => {
    const tr = document.createElement("tr");
    tr.className = "hover:bg-gray-50 dark:hover:bg-gray-800/40";
    tr.innerHTML = `
      <td class="py-2.5 px-3 font-medium text-gray-900 dark:text-white">${u.user_id}</td>
      <td class="py-2.5 px-3">${u.platform}</td>
      <td class="py-2.5 px-3 text-right font-mono">${u.screen_time}h</td>
      <td class="py-2.5 px-3 text-right font-mono">${u.posts_per_week}</td>
      <td class="py-2.5 px-3 text-right font-mono text-rose-400">${u.avg_likes.toLocaleString()}</td>
      <td class="py-2.5 px-3 text-right font-mono text-purple-400">${u.followers.toLocaleString()}</td>
      <td class="py-2.5 px-3 text-right font-mono text-emerald-400">${u.engagement_rate}%</td>
      <td class="py-2.5 px-3 text-gray-400 text-xs">${u.reason}</td>
    `;
    tbody.appendChild(tr);
  });
}

// ----------------------------------------------------------------------------
// TAB 7: PLATFORMS & PERSONAS
// ----------------------------------------------------------------------------

function renderPersonas(personas) {
  const container = document.getElementById("personasContainer");
  container.innerHTML = "";

  personas.forEach(p => {
    const card = document.createElement("div");
    card.className = "bg-white dark:bg-darkcard border border-gray-200 dark:border-darkborder rounded-2xl p-4 shadow-sm space-y-2 hover:border-brand-500/40 transition";
    card.innerHTML = `
      <div class="flex items-center justify-between">
        <div class="w-8 h-8 rounded-lg flex items-center justify-center text-white" style="background-color: ${p.color}">
          <i class="fa-solid ${p.icon} text-sm"></i>
        </div>
        <span class="text-lg font-bold text-gray-900 dark:text-white">${p.count}</span>
      </div>
      <h4 class="text-xs font-bold text-gray-900 dark:text-white">${p.name}</h4>
      <p class="text-[11px] text-gray-500 dark:text-gray-400">${p.description}</p>
      <div class="text-[10px] font-mono text-gray-400 bg-gray-50 dark:bg-gray-900 p-1.5 rounded-lg">${p.criteria}</div>
    `;
    container.appendChild(card);
  });
}

function renderPlatformRadar() {
  if (!globalSummary) return;
  const platData = globalSummary.platforms.platforms;
  const platLabels = Object.keys(platData);

  const isDark = document.documentElement.classList.contains("dark");
  const textColor = isDark ? "#9ca3af" : "#4b5563";

  // Normalize metrics on 0-100 scale for radar comparison
  const radarDatasets = platLabels.map(k => {
    const p = platData[k];
    const color = PLATFORM_COLORS[k] || "#6366f1";
    return {
      label: k,
      data: [
        Math.min(100, (p.avg_screen_time_hours / 6) * 100),
        Math.min(100, (p.avg_posts_per_week / 15) * 100),
        Math.min(100, (p.avg_likes_per_post / 500) * 100),
        Math.min(100, (p.avg_engagement_rate / 15) * 100),
        Math.min(100, (p.percentage_of_users / 30) * 100)
      ],
      borderColor: color,
      backgroundColor: `${color}25`,
      borderWidth: 2
    };
  });

  if (globalCharts.platformRadar) globalCharts.platformRadar.destroy();
  const ctx = document.getElementById("platformRadarChart").getContext("2d");
  globalCharts.platformRadar = new Chart(ctx, {
    type: "radar",
    data: {
      labels: ["Screen Time Intensity", "Posting Frequency", "Like Volume", "Engagement Rate", "User Share"],
      datasets: radarDatasets
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "right", labels: { color: textColor, font: { size: 10 } } }
      },
      scales: {
        r: {
          grid: { color: isDark ? "#1f2937" : "#e5e7eb" },
          pointLabels: { color: textColor, font: { size: 10 } },
          ticks: { display: false }
        }
      }
    }
  });
}

function renderPlatformTable(data) {
  const tbody = document.getElementById("platformTableBody");
  tbody.innerHTML = "";

  Object.keys(data.platforms).forEach(k => {
    const p = data.platforms[k];
    const tr = document.createElement("tr");
    tr.className = "hover:bg-gray-50 dark:hover:bg-gray-800/40";
    tr.innerHTML = `
      <td class="py-2.5 px-3 font-semibold text-gray-900 dark:text-white flex items-center gap-2">
        <span class="w-2.5 h-2.5 rounded-full" style="background-color: ${PLATFORM_COLORS[k] || '#6366f1'}"></span> ${k}
      </td>
      <td class="py-2.5 px-3 text-right font-mono">${p.percentage_of_users}%</td>
      <td class="py-2.5 px-3 text-right font-mono">${p.avg_screen_time_hours}h</td>
      <td class="py-2.5 px-3 text-right font-mono">${p.avg_posts_per_week}</td>
      <td class="py-2.5 px-3 text-right font-mono">${p.avg_likes_per_post.toLocaleString()}</td>
      <td class="py-2.5 px-3 text-right font-mono text-emerald-500 font-bold">${p.avg_engagement_rate}%</td>
    `;
    tbody.appendChild(tr);
  });
}

// ----------------------------------------------------------------------------
// TAB 8: DATA STUDIO & PAGINATION
// ----------------------------------------------------------------------------

let currentDataPage = 1;

async function loadDataTable(page = 1) {
  currentDataPage = page;
  const platform = document.getElementById("dataTablePlatformFilter").value;
  const search = document.getElementById("dataTableSearchInput").value;

  try {
    const url = `/api/data?page=${page}&limit=12&platform=${encodeURIComponent(platform)}&search=${encodeURIComponent(search)}`;
    const res = await fetch(url).then(r => r.json());

    if (res.success) {
      document.getElementById("dataCurrentPage").textContent = res.page;
      document.getElementById("dataTotalPages").textContent = res.total_pages;
      document.getElementById("dataTotalRecordsCount").textContent = res.total_records.toLocaleString();

      document.getElementById("btnPrevPage").disabled = res.page <= 1;
      document.getElementById("btnNextPage").disabled = res.page >= res.total_pages;

      const tbody = document.getElementById("rawDataTableBody");
      tbody.innerHTML = "";

      res.data.forEach(r => {
        const tr = document.createElement("tr");
        tr.className = "hover:bg-gray-50 dark:hover:bg-gray-800/40";
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-semibold text-gray-900 dark:text-white">${r.user_id}</td>
          <td class="py-2.5 px-3">${r.platform}</td>
          <td class="py-2.5 px-3 text-right font-mono">${r.daily_screen_time_hours}</td>
          <td class="py-2.5 px-3 text-right font-mono">${r.posts_per_week}</td>
          <td class="py-2.5 px-3 text-right font-mono">${r.avg_likes_per_post ? r.avg_likes_per_post.toLocaleString() : '-'}</td>
          <td class="py-2.5 px-3 text-right font-mono">${r.total_followers ? r.total_followers.toLocaleString() : '-'}</td>
          <td class="py-2.5 px-3 font-sans text-xs">${r.post_type || '-'}</td>
          <td class="py-2.5 px-3 text-right font-mono text-emerald-400">${r.engagement_rate}%</td>
          <td class="py-2.5 px-3 font-sans text-xs">${r.device || '-'}</td>
          <td class="py-2.5 px-3 font-sans text-xs">${r.primary_usage_purpose || '-'}</td>
        `;
        tbody.appendChild(tr);
      });
    }
  } catch (err) {
    console.error("Error loading data table:", err);
  }
}

function prevDataPage() {
  if (currentDataPage > 1) loadDataTable(currentDataPage - 1);
}

function nextDataPage() {
  loadDataTable(currentDataPage + 1);
}

function debounceSearch() {
  clearTimeout(dataTableSearchDebounce);
  dataTableSearchDebounce = setTimeout(() => {
    loadDataTable(1);
  }, 250);
}

// ----------------------------------------------------------------------------
// MODALS & UPLOADS
// ----------------------------------------------------------------------------

function openModal(modalId) {
  document.getElementById(modalId).classList.remove("hidden");
}

function closeModal(modalId) {
  document.getElementById(modalId).classList.add("hidden");
}

function toggleExportMenu() {
  const menu = document.getElementById("exportDropdown");
  menu.classList.toggle("hidden");
}

window.onclick = function(event) {
  if (!event.target.closest("#exportDropdown") && !event.target.closest("button[onclick='toggleExportMenu()']")) {
    document.getElementById("exportDropdown")?.classList.add("hidden");
  }
};

function onFileSelected(input) {
  if (input.files && input.files[0]) {
    document.getElementById("uploadFileNameDisplay").textContent = `Selected: ${input.files[0].name} (${(input.files[0].size / 1024).toFixed(1)} KB)`;
  }
}

async function handleCsvUpload(e) {
  e.preventDefault();
  const fileInput = document.getElementById("csvFileInput");
  if (!fileInput.files || !fileInput.files[0]) {
    showToast("Please choose a CSV file first", "warning");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  const btn = document.getElementById("btnSubmitUpload");
  btn.disabled = true;
  btn.textContent = "Analyzing...";

  try {
    const res = await fetch("/api/upload", { method: "POST", body: formData }).then(r => r.json());
    if (res.success) {
      showToast(res.message, "success");
      closeModal("uploadModal");
      loadAllDashboardData();
      loadDataTable(1);
    } else {
      showToast(res.error || "Failed to parse CSV", "error");
    }
  } catch (err) {
    showToast("Upload request failed", "error");
  } finally {
    btn.disabled = false;
    btn.textContent = "Analyze CSV";
  }
}

async function handleGenerateData(e) {
  e.preventDefault();
  const count = parseInt(document.getElementById("generateRecordCount").value);
  const btn = document.getElementById("btnSubmitGenerate");
  btn.disabled = true;
  btn.textContent = "Generating...";

  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ records: count })
    }).then(r => r.json());

    if (res.success) {
      showToast(res.message, "success");
      closeModal("generateModal");
      loadAllDashboardData();
      loadDataTable(1);
    } else {
      showToast(res.error, "error");
    }
  } catch (err) {
    showToast("Generation failed", "error");
  } finally {
    btn.disabled = false;
    btn.textContent = "Generate & Recalculate";
  }
}

async function resetToDefaultData() {
  try {
    const res = await fetch("/api/reset", { method: "POST" }).then(r => r.json());
    if (res.success) {
      showToast(res.message, "success");
      loadAllDashboardData();
      loadDataTable(1);
    }
  } catch (err) {
    showToast("Reset failed", "error");
  }
}

// ----------------------------------------------------------------------------
// Toast Notifications
// ----------------------------------------------------------------------------

function showToast(message, type = "info") {
  const container = document.getElementById("toastContainer");
  const toast = document.createElement("div");
  
  let bg = "bg-gray-900 text-white border-gray-700";
  let icon = "fa-circle-info text-blue-400";
  if (type === "success") {
    bg = "bg-emerald-950 text-emerald-100 border-emerald-800";
    icon = "fa-circle-check text-emerald-400";
  } else if (type === "error") {
    bg = "bg-rose-950 text-rose-100 border-rose-800";
    icon = "fa-circle-exclamation text-rose-400";
  } else if (type === "warning") {
    bg = "bg-amber-950 text-amber-100 border-amber-800";
    icon = "fa-triangle-exclamation text-amber-400";
  }

  toast.className = `toast-item flex items-center gap-3 px-4 py-3 rounded-xl border shadow-xl text-xs sm:text-sm font-medium ${bg}`;
  toast.innerHTML = `<i class="fa-solid ${icon} text-base"></i> <span>${message}</span>`;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transition = "opacity 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}
