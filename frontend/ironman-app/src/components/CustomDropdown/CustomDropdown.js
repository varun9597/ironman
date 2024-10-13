import React, { useState, useEffect } from 'react';

const CustomDropdown = ({ options, isMultiSelect, placeholder, onChange }) => {
  const [selectedValues, setSelectedValues] = useState([]);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const handleSelect = (value) => {
    if (isMultiSelect) {
      if (selectedValues.includes(value)) {
        setSelectedValues(selectedValues.filter((item) => item !== value));
      } else {
        setSelectedValues([...selectedValues, value]);
      }
    } else {
      setSelectedValues([value]);
      setIsDropdownOpen(false);
    }
  };

  useEffect(() => {
    onChange(selectedValues);
  }, [selectedValues, onChange]);

  return (
    <div className="custom-dropdown">
      <div
        className="dropdown-header"
        onClick={() => setIsDropdownOpen(!isDropdownOpen)}
      >
        {selectedValues.length === 0
          ? placeholder
          : isMultiSelect
          ? selectedValues.join(', ')
          : selectedValues[0]}
      </div>
      {isDropdownOpen && (
        <ul className="dropdown-list">
          {options.map((option) => (
            <li
              key={option}
              className={`dropdown-item ${
                selectedValues.includes(option) ? 'selected' : ''
              }`}
              onClick={() => handleSelect(option)}
            >
              {option}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default CustomDropdown;
