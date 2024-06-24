// Plotly graph rendering function
function renderGraphs(graphJSON, graphJSON1, graphJSON2) {
  console.log("Graph Data:", graphJSON, graphJSON1, graphJSON2); // 调试信息
  var graph = JSON.parse(graphJSON);
  Plotly.newPlot("graph", graph.data, graph.layout, { responsive: true });

  var graph1 = JSON.parse(graphJSON1);
  Plotly.newPlot("graph1", graph1.data, graph1.layout, { responsive: true });

  var graph2 = JSON.parse(graphJSON2);
  Plotly.newPlot("graph2", graph2.data, graph2.layout, { responsive: true });
}

function showDiv(divId) {
  // 隱藏所有的 custom-rounded-box
  document.querySelectorAll(".custom-rounded-box").forEach((div) => {
    div.style.display = "none";
  });

  // 顯示被點擊的 custom-rounded-box
  document.getElementById(divId).style.display = "block";

  // 更新 tab 的 active 狀態
  document.querySelectorAll(".custom-tab").forEach((tab) => {
    tab.classList.remove("active");
  });
  document
    .querySelector(`.custom-tab[onclick="showDiv('${divId}')"]`)
    .classList.add("active");
}

// 預設顯示第一個策略
showDiv("01");
