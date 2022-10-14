import React from "react";
import { Modal } from "react-bootstrap";
import styled from "styled-components";
import logo from "../../assets/images/veeta-logo.svg";

const EmailErrorModal = ({ show, handleClose }) => {
  return (
    <>
      <ModalWrapper centered show={show} onHide={handleClose}>
        <Modal.Header closeButton className="py-0 pt-3 border-0 px-4">
          <figure className=" m-0">
            <LogoImage src={logo} alt="logo" />
          </figure>
        </Modal.Header>
        <h5 className="text-center text-red mb-0 px-4 px-sm-5 mt-3">
          THERE WAS AN ERROR SENDING YOUR MAIL
        </h5>

        <Modal.Body className="text-center px-4 px-sm-5">
          <p className="text-black font-18">
            There was an error sending your email, plaese try again in few hours. Thanks, Veeta Team.
          </p>
          <p className="text-gray font-12 mt-4 mb-2">
            <em>Questions? Email us at info@veeta.co.uk</em>
          </p>
        </Modal.Body>
      </ModalWrapper>
    </>
  );
};

export default EmailErrorModal;

const ModalWrapper = styled(Modal)`
  .modal-content {
    border-radius: 25px;
  }
`;
const LogoImage = styled.img`
  width: 70px;
  height: 35px;
`;
