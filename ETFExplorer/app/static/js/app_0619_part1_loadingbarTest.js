document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("backtest-button")
    .addEventListener("click", toggleBacktestWindow);

  // 你的其他現有代碼
  document.querySelectorAll(".custom-tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      document
        .querySelectorAll(".custom-tab")
        .forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");
    });
  });

  // 預設顯示第一個策略
  showDiv("01");

  // 渲染圖表
  renderGraphs(graphJSON, graphJSON1, graphJSON2);
});

function updateLoadingBar(progress) {
  var loadingBar = document.querySelector(".loading-bar");
  loadingBar.style.width = progress + "%";
}

function renderGraphs(graphJSON, graphJSON1, graphJSON2) {
  var loadingProgress = 0;
  updateLoadingBar(loadingProgress); // 初始化 loading 條

  console.log("Graph Data:", graphJSON, graphJSON1, graphJSON2); // 调试信息

  // 假設這些操作是異步的，每個步驟完成後更新 loading 條
  setTimeout(function () {
    var graph = JSON.parse(graphJSON);
    Plotly.newPlot("graph", graph.data, graph.layout, { responsive: true });
    loadingProgress += 33; // 更新進度
    updateLoadingBar(loadingProgress);
  }, 100);

  setTimeout(function () {
    var graph1 = JSON.parse(graphJSON1);
    Plotly.newPlot("graph1", graph1.data, graph1.layout, { responsive: true });
    loadingProgress += 33; // 更新進度
    updateLoadingBar(loadingProgress);
  }, 200);

  setTimeout(function () {
    var graph2 = JSON.parse(graphJSON2);
    Plotly.newPlot("graph2", graph2.data, graph2.layout, { responsive: true });
    loadingProgress += 34; // 更新進度
    updateLoadingBar(loadingProgress);
  }, 300);

  // 所有圖表渲染完成後，隱藏 loading 條
  setTimeout(function () {
    document.querySelector(".loading-bar-container").style.display = "none";
  }, 400);
}

function toggleBacktestWindow() {
  var backtestWindow = document.getElementById("backtest-window");
  if (
    backtestWindow.style.display === "none" ||
    backtestWindow.style.display === ""
  ) {
    backtestWindow.style.display = "block"; // 先顯示元素，才能進行高度變化
    setTimeout(function () {
      backtestWindow.classList.add("open");
    }, 10); // 小延遲，確保 display 變化被應用
  } else {
    backtestWindow.classList.remove("open");
    setTimeout(function () {
      backtestWindow.style.display = "none";
    }, 500); // 等待動畫完成後再隱藏元素
  }
}
