import { useEffect, useRef } from "react";
import { Outlet, useLocation } from "react-router-dom";
import Sidebar from "./Components/Sidebar";
import Navbar from "./Components/Navbar";

import "./Layout.css";

export default function Layout() {
  const { pathname } = useLocation();
  const pageContentRef = useRef(null);

  useEffect(() => {
    if (pageContentRef.current) {
      pageContentRef.current.scrollTop = 0;
    }
  }, [pathname]);

  return (
    <div className="layout">
      <Sidebar />

      <div className="main-content">
        <Navbar />

        <div className="page-content" ref={pageContentRef}>
          <Outlet />
        </div>
      </div>
    </div>
  );
}