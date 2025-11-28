import React from "react";
import { diffChars } from "diff";

function HighlightText({ differences = [] }) { // Default value for differences
  const renderHighlightedText = (text1, text2) => {
    const diff = diffChars(text1 || "", text2 || ""); // Use empty strings if text1 or text2 is undefined
    return diff.map((part, index) => {
      const className = part.added
        ? "char-diff-added"
        : part.removed
        ? "char-diff-removed"
        : "char-diff-common";
      return (
        <span key={index} className={className}>
          {part.value}
        </span>
      );
    });
  };

  return (
    <div className="highlight-text">
      {Array.isArray(differences) && differences.length === 0 ? (
        <p className="no-differences">No differences found.</p>
      ) : (
        <ul className="differences-list">
          {differences.map((diff, index) => (
            <li key={index} className="difference-item">
              <div className="line-number">
                <strong>Line {diff.line}:</strong>
              </div>
              <div className="text-differences">
                <div className="text-diff text1-diff">
                  <span className="label">Text 1:</span>
                  {renderHighlightedText(diff.text1, diff.text2)}
                </div>
                <div className="text-diff text2-diff">
                  <span className="label">Text 2:</span>
                  {renderHighlightedText(diff.text2, diff.text1)}
                </div>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default HighlightText;
