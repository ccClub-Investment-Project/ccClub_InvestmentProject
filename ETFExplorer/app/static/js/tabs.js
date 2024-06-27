document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("backtest-button")
    .addEventListener("click", toggleBacktestWindow);

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
});
