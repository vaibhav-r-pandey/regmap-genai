import React, { useState, useEffect } from "react";

function Analyze() {
  const [analysisData, setAnalysisData] = useState(null);
  const [parsedData, setParsedData] = useState(null);

  useEffect(() => {
    const storedData = sessionStorage.getItem('analysisData');
    if (storedData) {
      const data = JSON.parse(storedData);
      setAnalysisData(data);
      
      if (data.data) {
        const parsed = parseCSVData(data.data);
        setParsedData(parsed);
      }
    }
  }, []);

  const parseCSVData = (csvString) => {
    const lines = csvString.split('\n').filter(line => line.trim());
    const tables = [];
    let currentTable = null;
    
    lines.forEach(line => {
      const cells = line.split(',');
      if (cells.length > 0) {
        if (!currentTable || (cells[0] && !cells[0].startsWith(' '))) {
          currentTable = { headers: cells, rows: [] };
          tables.push(currentTable);
        } else {
          currentTable.rows.push(cells);
        }
      }
    });
    
    return tables;
  };

  const renderTable = (table, index) => {
    return React.createElement(
      "div",
      { key: index, style: { marginBottom: "20px" } },
      React.createElement(
        "table",
        { style: { width: "100%", borderCollapse: "collapse", border: "1px solid #999", backgroundColor: "#f9f9f9", fontSize: "12px" } },
        React.createElement(
          "thead",
          null,
          React.createElement(
            "tr",
            { style: { backgroundColor: "#666", color: "white" } },
            table.headers.map((header, i) => 
              React.createElement(
                "th",
                { key: i, style: { padding: "6px 8px", border: "1px solid #999", textAlign: "left", fontWeight: "bold", color: "white", fontSize: "11px" } },
                header
              )
            )
          )
        ),
        React.createElement(
          "tbody",
          null,
          table.rows.map((row, i) => 
            React.createElement(
              "tr",
              { key: i, style: { backgroundColor: i % 2 === 0 ? "#f0f0f0" : "#f9f9f9" } },
              row.map((cell, j) => 
                React.createElement(
                  "td",
                  { key: j, style: { padding: "4px 6px", border: "1px solid #ccc", color: "#000", fontWeight: "normal", fontSize: "11px" } },
                  cell
                )
              )
            )
          )
        )
      )
    );
  };

  return React.createElement(
    "div",
    { className: "analyze-container", style: { padding: "15px", maxWidth: "800px", margin: "0 auto", backgroundColor: "#f5f5f5", minHeight: "100vh" } },
    React.createElement(
      "h2",
      { style: { textAlign: "center", marginBottom: "20px", color: "#000", fontSize: "20px" } },
      "Register Analysis Results"
    ),
    analysisData ? 
      React.createElement(
        "div",
        { className: "analysis-results" },
        React.createElement(
          "div",
          { style: { marginBottom: "15px", padding: "10px", backgroundColor: "#e8e8e8", borderRadius: "4px", border: "1px solid #ccc" } },
          React.createElement("h3", { style: { color: "#000", margin: "0 0 5px 0", fontSize: "16px" } }, "Register: ", analysisData.register),
          React.createElement("p", { style: { color: "#000", margin: "0", fontSize: "14px" } }, "Status: ", analysisData.success ? "✅ Success" : "❌ Failed")
        ),
        parsedData && parsedData.length > 0 ? 
          React.createElement(
            "div",
            { style: { backgroundColor: "#f8f8f8", border: "1px solid #ccc", borderRadius: "4px", padding: "10px" } },
            React.createElement("h4", { style: { marginBottom: "15px", color: "#000", fontSize: "16px" } }, "Analysis Data:"),
            parsedData.map((table, index) => renderTable(table, index))
          ) :
          React.createElement(
            "div",
            { style: { padding: "15px", backgroundColor: "#ffffff", border: "2px solid #333", borderRadius: "5px" } },
            React.createElement("h4", { style: { color: "#000" } }, "Raw Data:"),
            React.createElement("pre", { style: { whiteSpace: "pre-wrap", fontSize: "14px", color: "#000", backgroundColor: "#f8f8f8", padding: "10px", border: "1px solid #ccc" } }, analysisData.data)
          )
      ) :
      React.createElement(
        "div",
        { style: { textAlign: "center", padding: "50px", color: "#000" } },
        React.createElement("p", { style: { color: "#000" } }, "No analysis data available. Please process a register first.")
      )
  );
}

export default Analyze;