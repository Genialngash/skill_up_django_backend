import React, { useState } from "react";
import { Nav, Navbar } from "react-bootstrap";
import { Link, NavLink } from "react-router-dom";
import logo from "../../assets/images/veeta logo-grey.svg";

const MainNavBar = () => {
  const [mobileNav, setMobileNav] = useState(false);
  const [expanded, setExpanded] = useState(false);

  const closeMobileNav = () => {
    setMobileNav(false);
    setExpanded(false);
  };

  return (
    <>
      <header id="navbar" className={`${mobileNav && "mobile-nav"}`}>
        <Navbar
          expanded={expanded}
          expand="md"
          className="px-4 px-md-5 bg-black"
        >
          <Nav.Link href="/" className="p-0 me-4">
            <figure className="navbar__logo m-0">
              <img src={logo} alt="logo" />
            </figure>
          </Nav.Link>
          <Navbar.Toggle
            aria-controls="basic-navbar-nav"
            className={`${mobileNav ? "toggler-cross" : "toggler-main"}`}
            onClick={() => {
              setMobileNav(!mobileNav);
              setExpanded(expanded ? false : "expanded");
            }}
          />
          <Navbar.Collapse id="basic-navbar-nav" className="mt-5 mt-md-0">
            <Nav className="text-center text-md-start me-auto gap-3 gap-xl-5">
              <NavLink
                to="/#"
                className={({ isActive }) =>
                  `navbar-item`
                }
                onClick={closeMobileNav}
              >
                EMPLOYERS
              </NavLink>
              <NavLink
                to="/#"
                className={({ isActive }) =>
                  `navbar-item`
                }
                onClick={closeMobileNav}
              >
                EMPLOYEES
              </NavLink>
            </Nav>
            <div className="d-flex flex-column flex-md-row align-items-center gap-3 gap-md-4 mt-3 mt-md-0">
              <NavLink
                to="/#"
                className={({ isActive }) =>
                  `navbar-item`
                }
                onClick={closeMobileNav}
              >
                JOBS
              </NavLink>
              <Link to="/#">
                <button
                  onClick={() => {
                    setExpanded(false);
                    setMobileNav(false);
                  }}
                  className="btn-gradient font-14 signUp-btn"
                >
                  SIGN UP
                </button>
              </Link>
            </div>
          </Navbar.Collapse>
        </Navbar>
      </header>
      <div className="h-4"></div>
    </>
  );
};

export default MainNavBar;
