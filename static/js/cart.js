"use strict";

const updateUserOrder = async (productId, action) => {
  console.log("User is logged in, sending data...");

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
    console.log(data);
    location.reload();
  } catch (e) {
    console.log(e);
  }
};

const updateBtns = document.getElementsByClassName("update-cart");

for (let btn of updateBtns) {
  btn.addEventListener("click", function () {
    const productId = this.dataset.product;
    const action = this.dataset.action;
    console.log(`productId: ${productId}, Action: ${action}`);

    console.log(`USER: ${user}`);
    if (user === 'AnonymousUser') {
      console.log("Not logged in");
    } else {
      updateUserOrder(productId, action);
    }
  });
}
