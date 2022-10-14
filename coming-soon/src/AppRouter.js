import React, { Suspense } from "react";
import { Spinner } from "react-bootstrap";
import { Route, Routes } from "react-router-dom";
import Welcome from "./pages/Welcome";
const Footer = React.lazy(() => import("./components/layout/Footer"));
const MainNavBar = React.lazy(() => import("./components/layout/MainNavBar"));
const Home = React.lazy(() => import("./pages/Home"));




const AppRouter = () => {
  return (
    <Suspense
      fallback={
        <div
          style={{ height: "100vh" }}
          className="d-flex align-items-center justify-content-center text-danger"
        >
          <Spinner variant="danger" animation="grow" />
        </div>
      }
    >
      <MainNavBar />
      <Routes>
        <Route path="/" element={<Welcome />} />    
        <Route path="/home" element={<Home />} />
      </Routes>
      <Footer />
    </Suspense>
  );
};

export default AppRouter;
