import React from "react";

function TextInput({ label, value, onChange, textAreaRef, onScroll }) {
  return React.createElement(
    "div",
    { className: "text-input-container" },
    React.createElement(
      "label",
      { className: "text-input-label" },
      label
    ),
    React.createElement("textarea", {
      ref: textAreaRef,
      value: value,
      onChange: (e) => onChange(e.target.value),
      onScroll: onScroll,
      rows: 15,
      className: "text-input-field",
      placeholder: `Enter ${label.toLowerCase()} here...`
    })
  );
}

export default TextInput;
