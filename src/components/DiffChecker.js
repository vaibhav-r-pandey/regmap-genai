import React, { useState, useRef } from "react";
import TextInput from "./TextInput";
import HighlightText from "./HighlightText";

function DiffChecker() {
  const [text1, setText1] = useState("");
  const [text2, setText2] = useState("");
  const [differences, setDifferences] = useState([]);
  const [loading, setLoading] = useState(false);
  const textArea1Ref = useRef(null);
  const textArea2Ref = useRef(null);

  const handleFileUpload = (e, inputSetter) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        const text = reader.result;
        inputSetter(text);
      };
      reader.readAsText(file);
    }
  };

  const handleScroll = (sourceRef, targetRef) => {
    if (sourceRef.current && targetRef.current) {
      targetRef.current.scrollTop = sourceRef.current.scrollTop;
    }
  };

  const compareTexts = () => {
    const diff = [];
    const text1Lines = text1.split("\n");
    const text2Lines = text2.split("\n");

    text1Lines.forEach((line, index) => {
      if (line !== text2Lines[index]) {
        diff.push({
          line: index + 1,
          text1: line || "",
          text2: text2Lines[index] || "",
        });
      }
    });

    setDifferences(diff);
  };

  const saveComparison = async () => {
    setLoading(true);
    try {
      const apiUrl = process.env.REACT_APP_API_URL || "/api";
      const response = await fetch(`${apiUrl}/files`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text1, text2, differences }),
      });
      const data = await response.json();
      alert("Comparison saved successfully!");
    } catch (error) {
      console.error("Error saving comparison:", error);
    }
    setLoading(false);
  };

  return React.createElement(
    "div",
    { className: "diff-checker" },
    React.createElement(
      "div",
      { className: "text-inputs" },
      React.createElement(
        "div",
        { className: "text-input" },
        React.createElement(TextInput, {
          label: "Text 1",
          value: text1,
          onChange: setText1,
          textAreaRef: textArea1Ref,
          onScroll: () => handleScroll(textArea1Ref, textArea2Ref),
        }),
        React.createElement(
          "div",
          { className: "file-upload" },
          React.createElement("input", {
            type: "file",
            id: "file1",
            accept: ".txt",
            onChange: (e) => handleFileUpload(e, setText1),
          }),
          React.createElement(
            "label",
            { htmlFor: "file1" },
            "Upload Text 1 File"
          )
        )
      ),
      React.createElement(
        "div",
        { className: "text-input" },
        React.createElement(TextInput, {
          label: "Text 2",
          value: text2,
          onChange: setText2,
          textAreaRef: textArea2Ref,
          onScroll: () => handleScroll(textArea2Ref, textArea1Ref),
        }),
        React.createElement(
          "div",
          { className: "file-upload" },
          React.createElement("input", {
            type: "file",
            id: "file2",
            accept: ".txt",
            onChange: (e) => handleFileUpload(e, setText2),
          }),
          React.createElement(
            "label",
            { htmlFor: "file2" },
            "Upload Text 2 File"
          )
        )
      )
    ),
    React.createElement(
      "button",
      { className: "compare-button", onClick: compareTexts },
      "Compare Texts"
    ),
    React.createElement(
      "button",
      { className: "save-button", onClick: saveComparison, disabled: loading },
      loading ? "Saving..." : "Save Comparison"
    ),
    React.createElement(HighlightText, { differences: differences })
  );
}

export default DiffChecker;
