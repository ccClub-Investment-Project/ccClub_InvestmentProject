function showStrategy(strategyNumber) {
  const strategies = document.querySelectorAll(".strategy");
  strategies.forEach((strategy) => strategy.classList.remove("active"));
  document.getElementById(`strategy${strategyNumber}`).classList.add("active");
}

function addStrategy() {
  // 添加新策略的邏輯
}

function startCountdown(timerId, endDate) {
  const timerElement = document.getElementById(timerId);
  function updateCountdown() {
    const now = new Date().getTime();
    const distance = endDate - now;
    if (distance < 0) {
      clearInterval(interval);
      timerElement.innerHTML = "已過期";
    } else {
      const days = Math.floor(distance / (1000 * 60 * 60 * 24));
      const hours = Math.floor(
        (distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
      );
      const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((distance % (1000 * 60)) / 1000);
      timerElement.innerHTML = `${days}天 ${hours}時 ${minutes}分 ${seconds}秒`;
    }
  }
  updateCountdown();
  const interval = setInterval(updateCountdown, 1000);
}

// 假設換股日期
const swapDate1 = new Date("2024-06-30T00:00:00").getTime();
const swapDate2 = new Date("2024-07-10T00:00:00").getTime();

startCountdown("timer1", swapDate1);
startCountdown("timer2", swapDate2);
function showStrategy(strategyNumber) {
  const strategies = document.querySelectorAll(".strategy");
  strategies.forEach((strategy) => strategy.classList.remove("active"));
  document.getElementById(`strategy${strategyNumber}`).classList.add("active");
}

function addStrategy() {
  // 添加新策略的邏輯
}

function startCountdown(timerId, endDate) {
  const timerElement = document.getElementById(timerId);
  function updateCountdown() {
    const now = new Date().getTime();
    const distance = endDate - now;
    if (distance < 0) {
      clearInterval(interval);
      timerElement.innerHTML = "已過期";
    } else {
      const days = Math.floor(distance / (1000 * 60 * 60 * 24));
      const hours = Math.floor(
        (distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
      );
      const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((distance % (1000 * 60)) / 1000);
      timerElement.innerHTML = `${days}天 ${hours}時 ${minutes}分 ${seconds}秒`;
    }
  }
  updateCountdown();
  const interval = setInterval(updateCountdown, 1000);
}

// 假設換股日期
const swapDate1 = new Date("2024-06-30T00:00:00").getTime();
const swapDate2 = new Date("2024-07-10T00:00:00").getTime();

startCountdown("timer1", swapDate1);
startCountdown("timer2", swapDate2);
