"use strict";

const updateUserOrder = async (productId, action, currentUrl) => {
  try {
    const response = await fetch("/updateitem/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken
      },
      body: JSON.stringify({"productId": productId, "action": action, "currentUrl": currentUrl})
    });
    if (!response.ok) return;

    const data = await response.json();
    location.reload();
  } catch (e) {
    console.error(e);
  }
};

const updateBtns = document.getElementsByClassName("update-cart");

for (let btn of updateBtns) {
  btn.addEventListener("click", function () {
    try {
      const productId = this.dataset.product;
      const action = this.dataset.action;
      const currentUrl = window.location.href;

      if (productId && action) {
        updateUserOrder(productId, action, currentUrl);
      }
    } catch (e) {
      console.error(e);
    }
  });
}
