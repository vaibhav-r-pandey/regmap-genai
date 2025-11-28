import React, { useState, useEffect } from "react";
import DiffChecker from "./components/DiffChecker";
import RegMapper from "./components/RegMapper";
import Analyze from "./components/Analyze";

function App() {
  const [currentPage, setCurrentPage] = useState("home");

  useEffect(() => {
    const handlePopState = () => {
      const path = window.location.pathname;
      if (path === "/diffchecker") {
        setCurrentPage("diff-checker");
      } else if (path === "/regmap") {
        setCurrentPage("reg-mapper");
      } else if (path === "/analyze") {
        setCurrentPage("analyze");
      } else {
        setCurrentPage("home");
      }
    };

    // Set initial page based on URL
    handlePopState();

    // Listen for browser back/forward button
    window.addEventListener('popstate', handlePopState);

    // Cleanup event listener
    return () => {
      window.removeEventListener('popstate', handlePopState);
    };
  }, []);

  const navigateTo = (page) => {
    setCurrentPage(page);
    if (page === "diff-checker") {
      window.history.pushState({}, "", "/diffchecker");
    } else if (page === "reg-mapper") {
      window.history.pushState({}, "", "/regmap");
    } else if (page === "analyze") {
      window.history.pushState({}, "", "/analyze");
    } else {
      window.history.pushState({}, "", "/");
    }
  };

  const renderPage = () => {
    switch (currentPage) {
      case "diff-checker":
        return React.createElement(DiffChecker, null);
      case "reg-mapper":
        return React.createElement(RegMapper, null);
      case "analyze":
        return React.createElement(Analyze, null);
      default:
        return React.createElement(
          "div",
          { className: "home-page" },
          React.createElement(
            "div",
            { className: "home-buttons" },
            React.createElement(
              "button",
              {
                className: "home-button diff-button",
                onClick: () => navigateTo("diff-checker")
              },
              "Diff Checker"
            ),
            React.createElement(
              "button",
              {
                className: "home-button reg-button",
                onClick: () => navigateTo("reg-mapper")
              },
              "Reg Mapper"
            )
          )
        );
    }
  };

  return React.createElement(
    "div",
    { className: "app" },
    React.createElement(
      "header",
      { className: "app-header" },
      React.createElement(
        "h1",
        { 
          style: { cursor: "pointer" },
          onClick: () => navigateTo("home")
        },
        currentPage === "home" ? "Welcome" : currentPage === "diff-checker" ? "Diff Checker" : currentPage === "reg-mapper" ? "Reg Mapper" : "Register Analysis"
      )
    ),
    React.createElement(
      "main",
      { className: "app-content" },
      renderPage()
    )
  );
}

export default App;
