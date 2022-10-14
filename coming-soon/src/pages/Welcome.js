import React from "react";
import logo from "../assets/images/veeta logo-white-text.svg";
import { ReactComponent as Arrow } from "../assets/icons/arrow.svg";
import { Link } from "react-router-dom";

const Welcome = () => {
  return (
    <>
      <div className="banner bg-black py-4 py-sm-5 d-flex justify-content-center align-items-center">
        <div className="container px-3">
          <div className="contents text-center">
            <figure className="logo m-0 text-center">
              <img src={logo} alt="logo" style={{ maxHeight: "330px" }} />
              <h4 style={{color: 'white'}}>Any Work,</h4>
              <h4 style={{marginLeft:'120px', color: 'white'}}>Any Time,</h4>
              <h4 style={{marginLeft:'250px', color:'white'}}>Any Where</h4>
            </figure>
            <Link to="/home">
              <button className="btn btn-gradient font-24 px-3 text-white mt-5">
                CONTINUE <Arrow className="arrow-icon mb-1" />
              </button>
            </Link>
          </div>
        </div>
      </div>
    </>
  );
};

export default Welcome;
