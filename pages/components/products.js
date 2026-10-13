import styles from "../../styles/Home.module.css";
import React from 'react';

export default function Products() {
  return (
    <section className={styles.sections} style={{backgroundColor: "rgb(26, 98, 87)"}}>
      <h2>PRODUCTS</h2>
      <p>enter a company url to get info about the company&apos;s products</p>
    </section>
  );
}
//the &apos; is apostrophe
