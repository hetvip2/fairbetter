import React from 'react';
import PropTypes from 'prop-types'; 

export default function BasicButton({ text }) {
  return (
    <button type="submit" style={{ padding: "10px" }}>
      {text}
    </button>
  );
}


BasicButton.propTypes = {
  text: PropTypes.string.isRequired, 
};