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
