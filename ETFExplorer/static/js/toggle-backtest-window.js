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
    }, 200); // 等待動畫完成後再隱藏元素
  }
}
