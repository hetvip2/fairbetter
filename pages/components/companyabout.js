import styles from "../../styles/Home.module.css";
import React from 'react';

// include companyInfo data here to display
export default function About() {
  return (
    <section className={styles.sections} style={{backgroundColor: "#4B97BB"}}>
      <h2>ABOUT THE COMPANY</h2>
      <p>enter a company url to get general info about the company</p>
    </section>
  );
}
