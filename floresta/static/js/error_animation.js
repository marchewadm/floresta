"use strict";

try {
  const barEl = document.querySelector(".progress--bar");
  const errorBoxEl = document.querySelector(".msg--modal");

  if (barEl && errorBoxEl) {
    const load = () => {
      let width = 100;

      const id = setInterval(() => {
        if (width <= 0) {
          clearInterval(id);
          errorBoxEl.classList.add("disappear");

          const disappearEl = document.querySelector('.disappear');
          if (disappearEl) {
            disappearEl.addEventListener('animationend', () => {
              disappearEl.remove()
            });
          }
        } else {
          width -= 0.5;
          barEl.style.width = `${width}%`;
        }
      }, 10);
    };
    load();
  }
} catch (e) {
  console.error(e);
}
