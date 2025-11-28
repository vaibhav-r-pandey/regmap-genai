import React, { useState } from "react";

function RegMapper() {
  const [inputText, setInputText] = useState("");
  const [registerName, setRegisterName] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        const text = reader.result;
        setInputText(text);
      };
      reader.readAsText(file);
    }
  };

  const processInput = async () => {
    setLoading(true);
    
    // First test backend connectivity
    try {
      console.log('Testing backend connectivity...');
      const testResponse = await fetch('http://localhost:5001/api/test');
      const testResult = await testResponse.json();
      console.log('Backend test result:', testResult);
    } catch (error) {
      alert('Backend not running! Start with: python backend/test.py');
      setLoading(false);
      return;
    }
    
    // Now make the actual API call
    try {
      console.log('Making process request...');
      const response = await fetch('http://localhost:5001/api/process-registers', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          inputText: inputText,
          registerName: registerName
        })
      });
      
      console.log('Response status:', response.status);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      console.log('Process result:', result);
      
      if (result.success) {
        sessionStorage.setItem('analysisData', JSON.stringify(result));
        window.history.pushState({}, "", "/analyze");
        window.dispatchEvent(new PopStateEvent('popstate'));
      } else {
        alert('Error: ' + result.error);
      }
    } catch (error) {
      console.error('Process error:', error);
      alert('Process error: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return React.createElement(
    "div",
    { className: "reg-mapper" },
    React.createElement(
      "div",
      { className: "text-input", style: { maxWidth: "600px", margin: "0 auto 20px auto" } },
      React.createElement(
        "label",
        { className: "text-input-label" },
        "Enter Register Set"
      ),
      React.createElement("textarea", {
        value: inputText,
        onChange: (e) => setInputText(e.target.value),
        rows: 15,
        className: "text-input-field",
        placeholder: "Enter your text here or upload a file..."
      }),
      React.createElement(
        "div",
        { className: "file-upload" },
        React.createElement("input", {
          type: "file",
          id: "regmap-file",
          accept: ".txt",
          onChange: handleFileUpload,
        }),
        React.createElement(
          "label",
          { htmlFor: "regmap-file" },
          "📁 Upload File"
        )
      )
    ),
    React.createElement(
      "div",
      { className: "text-input", style: { maxWidth: "600px", margin: "0 auto 20px auto" } },
      React.createElement(
        "label",
        { className: "text-input-label" },
        "Enter Register Name"
      ),
      React.createElement("input", {
        type: "text",
        value: registerName,
        onChange: (e) => setRegisterName(e.target.value),
        className: "single-line-input",
        placeholder: "Enter register name..."
      })
    ),
    React.createElement(
      "button",
      { 
        className: "compare-button", 
        onClick: processInput, 
        disabled: loading || !inputText.trim() || !registerName.trim()
      },
      loading ? "Processing..." : "Process"
    )
  );
}

export default RegMapper;