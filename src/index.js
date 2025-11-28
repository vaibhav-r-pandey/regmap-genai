import React from "react";
import ReactDOM from "react-dom/client"; // Use ReactDOM from 'react-dom/client' in React 18
import App from "./App";
import "./App.css";

// Get the root element from index.html
const rootElement = document.getElementById("root");

// Create a root using React 18 API
const root = ReactDOM.createRoot(rootElement);

// Render the App component
root.render(React.createElement(App));
