function handlePayment(stripe, productId, paymentData) {
  // Get Checkout Session ID
  fetch(
    `http://localhost:8000/payments/create-checkout-session/${productId}/`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(paymentData),
    }
  )
    .then((result) => {
      return result.json();
    })
    .then((data) => {
      console.log(data);
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({ sessionId: data.sessionId });
    });
}

// Get Stripe publishable key
fetch("http://localhost:8000/payments/config/")
  .then((result) => {
    return result.json();
  })
  .then((data) => {
    // Initialize Stripe.js
    const stripe = Stripe(data.publicKey);

    // Event handlers
    document.querySelector("#allAccessProSub").addEventListener("click", () => {
      handlePayment(stripe, "prod_LEhv1kifx2ZZP6", {
        package_type: "all_access_sub",
        user_email: "ashley.meyers@company.com",
      });
    });

    document.querySelector("#basic").addEventListener("click", () => {
      handlePayment(stripe, "prod_LELe6q3up2mbWz", {
        package_type: "unlock_code",
      });
    });

    document.querySelector("#medium").addEventListener("click", () => {
      handlePayment(stripe, "prod_LEiHQv8ohaXrLY", {
        package_type: "unlock_code",
      });
    });

    document.querySelector("#premium").addEventListener("click", () => {
      handlePayment(stripe, "prod_LEiMRrZv4YT97n", {
        package_type: "unlock_code",
      });
    });
  });
