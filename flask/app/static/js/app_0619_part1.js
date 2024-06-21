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
