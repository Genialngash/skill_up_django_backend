import React, { useRef, useState } from "react";
import CountdownTimer from "./countdownTimer/CountdownTimer";
import emailjs from "@emailjs/browser";
import EmailSuccessModal from "./modal/EmailSuccessModal";
import EmailErrorModal from "./modal/EmailErrorModal";

const Banner = () => {
  const [successModal, setSuccessModal] = useState(false);
  const [errorModal, setErrorModal] = useState(false);
const [inputVal, setInputVal] = useState('');

  const form = useRef();

  const sendEmail = (e) => {
    e.preventDefault();

    emailjs
      .sendForm(
        "service_nugk9pd",
        "template_tfx8hto",
        form.current,
        "user_m8CFNdL0XmSc6qdCXbhao"
      )
      .then(
        (result) => {
        setSuccessModal(true);
        setInputVal('');
          console.log(result);
        },
        (error) => {
          setErrorModal(true);
          setInputVal('');
          console.log(error.text);
        }
      );
  };

  return (
    <div className="banner bg-gradient-green py-4 py-sm-5 d-flex justify-content-center align-items-center">
      <div className="container px-3">
        <div className="contents">
          <div className="text-white">
            <h1 className="text-center text-white bg-primary">COMING SOON!</h1>
            <CountdownTimer countdownTimestampMs={1654084437000} />
            <p className="text-center font-18">
            At Veeta we wanted to simplify the process of hourly, daily, weekly, monthly or full time jobs for people looking for work. Allowing the individual to take back control of when, where, who and at a time that suits them to go to work.
            Without the hassle of joining a recruitment agency you will be available on Veeta to set up a profile listing all your skills, education, training and once verified instantly look for any available work you require.
            By doing this we aim to offer a service that will provide an instant solution for employers needing a position filling as soon as possible with a suitable candidate who is willing and capable to fulfil their needs.
            By joining the platform both people looking for work and businesses looking for staff will be able to view job positions available and suitable candidates available to work all in their area required.
            Instead of googling or having to call numerous agencys looking for suitable candidates we want Veeta to be your instant place to go to find the right people,at the right place, available at the right time when you need them.
            </p>
          </div>
          <div className="get-notified mx-auto mt-4">
            <form ref={form} onSubmit={sendEmail}>
              <div className="input-group mb-3">
                <input
                  type="email"
                  className="form-control font-18"
                  placeholder="Enter your email"
                  name="user_email"
                  onChange={(e) => setInputVal(e.target.value)}
                  value={inputVal}
                  required
                />
                <button
                  className="btn bg-black text-white px-3 px-md-4 font-18"
                  type="submit"
                >
                  Get notified
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
      {successModal && (
        <EmailSuccessModal
          show={successModal}
          handleClose={() => setSuccessModal(false)}
        />
      )}
       {errorModal && (
        <EmailErrorModal
          show={errorModal}
          handleClose={() => setErrorModal(false)}
        />
      )}
    </div>
  );
};

export default Banner;
