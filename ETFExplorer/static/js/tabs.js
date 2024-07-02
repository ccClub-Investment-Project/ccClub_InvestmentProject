document.addEventListener("DOMContentLoaded", function () {
  // 初始化時隱藏所有非預設顯示的 tab 內容
  document.querySelectorAll(".custom-rounded-box").forEach((div) => {
    if (div.id !== "01") { // 預設顯示的 tab 的 id
      div.style.display = "none";
    }
  });

  // 綁定點擊事件
  document.querySelectorAll(".custom-tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      const divId = tab.getAttribute("data-div-id"); // 或者根據實際情況獲取 id
      showDiv(divId);

      // 更新所有 tab 的 active 狀態
      document.querySelectorAll(".custom-tab").forEach((t) => {
        t.classList.remove("active");
      });
      tab.classList.add("active");
    });
  });

  // 預設顯示第一個策略
  showDiv("01");
});