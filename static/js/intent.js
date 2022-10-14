/* ------- UI helpers ------- */
// Shows a success message when the payment is complete
var orderComplete = function (paymentIntentId) {
  document
    .querySelector(".result-message a")
    .setAttribute(
      "href",
      "https://dashboard.stripe.com/test/payments/" + paymentIntentId
    );
  document.querySelector(".result-message").classList.remove("hidden");
  document.querySelector("button").disabled = true;
};

// Show the customer the error from Stripe if their card fails to charge
var showError = function (errorMsgText) {
  var errorMsg = document.querySelector("#card-error");
  errorMsg.textContent = errorMsgText;
  setTimeout(function () {
    errorMsg.textContent = "";
  }, 4000);
};

// Calls stripe.confirmCardPayment
// If the card requires authentication Stripe shows a pop-up modal to
// prompt the user to enter authentication details without leaving your page.
var payWithCard = function (stripe, card, clientSecret) {
  stripe
    .confirmCardPayment(clientSecret, {
      payment_method: {
        card: card,
      },
    })
    .then(function (result) {
      if (result.error) {
        // Show error to your customer
        showError(result.error.message);
      } else {
        // The payment succeeded!
        orderComplete(result.paymentIntent.id);
      }
    });
};

// Get Stripe publishable key
fetch("http://localhost:8000/payments/config/")
  .then((result) => {
    return result.json();
  })
  .then((data) => {
    console.log(data);

    // Initialize Stripe.js
    const stripe = Stripe(data.publicKey);
    var form = document.getElementById("payment-form");
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      // Complete payment when the submit button is clicked
      const product_id = document.getElementById("product_id").value;
      const package_type = document.getElementById("package_type").value;
      const ccnum = document.getElementById("ccnum").value;
      const zip = document.getElementById("zip").value;
      const expmonth = document.getElementById("expmonth").value;
      const expyear = document.getElementById("expyear").value;
      const cvv = document.getElementById("cvv").value;
      const email = document.getElementById("email").value;
      const fname = document.getElementById("fname").value;

      fetch("http://localhost:8000/payments/create-payment-intent/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          fname: fname,
          email: email,
          ccnum: ccnum,
          cvv: cvv,
          zip: zip,
          expmonth: expmonth,
          expyear: expyear,
          package_type: package_type,
          stripe_package_id: product_id,
        }),
      })
        .then(function (result) {
          return result.json();
        })
        .then(function (data) {
          const secret = data.clientSecret;
          const card = stripe
            .createPaymentMethod({
              type: "card",
              card: {
                number: ccnum,
                exp_month: expmonth,
                exp_year: expyear,
                cvc: cvv,
              },
              billing_details: {
                name: fname,
              },
            })
            .then(() => {
              payWithCard(stripe, card, secret);
            })
            .catch((err) => {
              console.log(err);
            });
        });
    });
    // END
  });
