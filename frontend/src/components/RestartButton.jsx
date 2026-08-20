import React, { useState, useEffect, useRef } from "react";

export default function RestartButton({ onRestartAll, onRestartSamProxy, disabled }) {
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(event) {
      if (containerRef.current && !containerRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isOpen]);

  const handleToggle = () => {
    if (!disabled) {
      setIsOpen((prev) => !prev);
    }
  };

  const handleRestartAll = () => {
    onRestartAll();
    setIsOpen(false);
  };

  const handleRestartSamProxy = () => {
    onRestartSamProxy();
    setIsOpen(false);
  };

  return (
    <div className="restart-dropdown" ref={containerRef}>
      <button
        className="btn"
        disabled={disabled}
        onClick={handleToggle}
        aria-haspopup="true"
        aria-expanded={isOpen}
      >
        Restart ▾
      </button>
      {isOpen && (
        <div className="restart-dropdown-menu">
          <button
            className="restart-dropdown-item"
            onClick={handleRestartAll}
          >
            Restart all components
          </button>
          <button
            className="restart-dropdown-item"
            onClick={handleRestartSamProxy}
          >
            Restart SAM & proxy
          </button>
        </div>
      )}
    </div>
  );
}
