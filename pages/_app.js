import PropTypes from 'prop-types';
import React from 'react';
import '../styles/global.css'; // adjust path if css in different location

function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />;
}

MyApp.propTypes = {
  Component: PropTypes.elementType.isRequired, 
  pageProps: PropTypes.object.isRequired,
};

export default MyApp;