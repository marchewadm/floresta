"use strict";

const updateUserOrder = async (productId, action) => {
  try {
    const response = await fetch("/updateitem/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken
      },
      body: JSON.stringify({"productId": productId, "action": action})
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

      if (productId && action) {
        updateUserOrder(productId, action);
      }
    } catch (e) {
      console.error(e);
    }
  });
}
