import React from "react";
import logo from "../../assets/images/veeta-logo.svg";
import { FaLinkedin, FaTwitterSquare, FaFacebookSquare } from "react-icons/fa";
import { Link } from "react-router-dom";

const Footer = () => {
  return (
    <footer id="footer">
      <div className="footer-top py-4 py-sm-5">
        <div className="container px-4">
          <div className="row justify-content-end">
            <div className="footer-content col-6 col-sm-12 col-md-3 col-lg-3 col-xl-4 mb-4 d-flex flex-column flex-sm-row flex-md-column flex-xl-row justify-content-center align-items-center gap-3">
              <figure className="navbar__logo m-0">
                <img src={logo} alt="logo" />
              </figure>
              <ul className="list-unstyled">
                <h5 className="text-black">Contact Us</h5>
                <li>info@veeta.co.uk</li>
                <li>5 Brett Drive</li>
                <li>Bexhill-on-Sea</li>
                <li>East Sussex</li>
                <li>TN40 2JP</li>
                <li>United Kingdom</li>
              </ul>
            </div>
            <div className="footer-content content2 col-6 col-sm-4 col-md-3 col-lg-3 col-xl-2 mb-4">
              <ul className="list-unstyled">
                <h5 className="text-black">Important Links</h5>
                <li>
                  <Link to="/">View Job Positions</Link>
                </li>
                <li>
                  <Link to="/">Become an Employer</Link>
                </li>
              </ul>
            </div>
            <div className="footer-content col-6 col-sm-4 col-md-3 col-lg-3 col-xl-2 mb-4">
              <ul className="list-unstyled">
                <li>
                  <Link to="/">FAQS</Link>
                </li>
                <li>
                  <Link to="/">TERMS & CONDITIONS</Link>
                </li>
                <li>
                  <Link to="/">ABOUT US</Link>
                </li>
              </ul>
            </div>
            <div className="footer-content col-6 col-sm-4 col-md-3 col-lg-3 col-xl-3 d-flex justify-content-sm-center justify-content-md-between justify-content-between  ">
              <ul className="list-unstyled social-icons">
                <h5 className="text-black">Social Platforms</h5>
                <li>
                  <a href="/" target="_blank" className="icon1">
                    <FaFacebookSquare />
                  </a>
                </li>
                <li>
                  <a href="/" target="_blank" className="icon2">
                    <FaTwitterSquare />
                  </a>
                </li>
                <li>
                  <a href="/" target="_blank" className="icon3">
                    <FaLinkedin />
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
