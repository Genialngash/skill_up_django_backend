import React from "react";
import { Modal } from "react-bootstrap";
import styled from "styled-components";
import logo from "../../assets/images/veeta-logo.svg";

const EmailSuccessModal = ({ show, handleClose }) => {
  return (
    <>
      <ModalWrapper centered show={show} onHide={handleClose}>
        <Modal.Header closeButton className="py-0 pt-3 border-0 px-4">
          <figure className=" m-0">
            <LogoImage src={logo} alt="logo" />
          </figure>
        </Modal.Header>
        <h5 className="text-center text-black mb-0 px-4 px-sm-5 mt-3">
          EMAIL SENT SUCCESSFULLY
        </h5>

        <Modal.Body className="text-center px-4 px-sm-5">
          <p className="text-black font-18">
            Thank You for your interest in Veeta. Our Team will notify you once we're live!
          </p>
          <p className="text-gray font-12 mt-4 mb-2">
            <em>Questions? Email us at info@veeta.co.uk</em>
          </p>
        </Modal.Body>
      </ModalWrapper>
    </>
  );
};

export default EmailSuccessModal;

const ModalWrapper = styled(Modal)`
  .modal-content {
    border-radius: 25px;
  }
`;
const LogoImage = styled.img`
  width: 70px;
  height: 35px;
`;
