import styles from "../../styles/Home.module.css";
import React from 'react';

// include companyInfo data here to display
export default function Position() {
  return (
    <section className={styles.sections} style={{backgroundColor: "#472C46"}}>
      <h2>POSITION-BASED QUESTIONS</h2>
      <p>enter a position url to get example questions</p>
    </section>
  );
}
