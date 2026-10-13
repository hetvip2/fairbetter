import styles from "../styles/Home.module.css";
import validator from "validator";
import React, { useState } from "react";
import BasicButton from "./components/basicbutton";
import About from "./components/companyabout";
import Products from "./components/products";
import axios from "axios";
import Position from "./components/positionqs";

export default function Home() {
  var valid = false;
  const [companyUrl, setCompanyUrl] = useState("");
  const [companyInfo, setCompanyInfo] = useState(null);
  const [productInfo, setProductInfo] = useState(null);
  const [file, setFile] = useState(null);
  const [positionUrl, setPositionUrl] = useState("");
  const [questionType, setQuestionType] = useState(""); 
  const [aboutQuestions, setAboutQuestions] = useState([]);
  const [productQuestions, setProductQuestions] = useState([]);

  const handleScrape = async () => {
    try {
      const response = await axios.get('http://localhost:2000/scrape', {
        params: { url: companyUrl },
      });
      setCompanyInfo(response.companyInfo);
    } catch (e) {}
  };

  const handleScrapeAbout = async (url) => {
    if (!validator.isURL(url)) {
      alert("Please enter a valid URL.");
      return;
    }

    try {
      const response = await axios.get('http://localhost:2000/about_scrape', {
        params: { url },
      });

      const { found, content } = response.data;

      if (found) {
        try {
          const tldrResponse = await axios.post(
            'http://127.0.0.1:2000/summarize_company',
            { content: content },
            { headers: { "Content-Type": "application/json" } }
          );
          const { summary } = tldrResponse.data;
          setCompanyInfo(summary);

          // Generate product questions using PRODUCT info
          if (productInfo) {
            const productQuestionsResponse = await axios.post(
              'http://localhost:2000/generate_questions',
              { content: productInfo },
              { headers: { "Content-Type": "application/json" } }
            );
            setProductQuestions(productQuestionsResponse.data.summary);
          }
        } catch (e) {
          console.log("this could be the error: ", e);
        }
      } else {
        setCompanyInfo("No about info found for the provided URL.");
      }
    } catch (e) {
      console.error("Error scraping about info:", e);
      const errorMessage = `An error occurred: ${e.message || "Unknown error"}`;
      setCompanyInfo((prevInfo) => `${prevInfo || ""}\n${errorMessage}`);
    }
  };

  const handleScrapeProducts = async () => {
    try {
      const response = await axios.get(
        'http://localhost:2000/products_scrape',
        {
          params: { url: companyUrl },
        }
      );
      const { found, content } = response.data;

      if (found) {
        try {
          const tldrResponse = await axios.post(
            'http://127.0.0.1:2000/summarize_products',
            { content: content },
            { headers: { "Content-Type": "application/json" } }
          );
          const { summary } = tldrResponse.data;
          setProductInfo(summary);

          // Generate about questions using COMPANY info
          if (companyInfo) {
            const aboutQuestionsResponse = await axios.post(
              'http://localhost:2000/generate_questions',
              { content: companyInfo },
              { headers: { "Content-Type": "application/json" } }
            );
            setAboutQuestions(aboutQuestionsResponse.data.summary);
          }
        } catch (e) {
          console.log("this could be the error: ", e);
        }
      } else {
        setProductInfo("No product info found for the provided URL.");
      }
    } catch (e) {
      console.error("Error scraping product info:", e);
      setProductInfo("An error occurred while fetching product information.");
    }
  };

  const handleCompanyUrlChange = (e) => {
    setCompanyUrl(e.target.value);
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handlePositionUrlChange = (e) => {
    setPositionUrl(e.target.value);
  };

  const handleQuestionTypeChange = (e) => {
    setQuestionType(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    let messages = [];

    if (companyUrl) {
      if (validator.isURL(companyUrl)) {
        valid = true;
        await handleScrapeAbout(companyUrl);
        await handleScrapeProducts(companyUrl);
        setCompanyUrl("");
      } else {
        valid = false;
      }
    }

    if (file) {
      if (file.type === "application/pdf") {
        messages.push(`file submitted: ${file.name}`);
        setFile(null);
        valid = true;
        alert(messages.join("\n"));
      } else {
        valid = false;
      }
    }

    if (positionUrl) {
      if (validator.isURL(positionUrl)) {
        setPositionUrl("");
        valid = true;
      } else {
        valid = false;
      }
    }

    if (!valid && messages.length === 0) {
      alert("please enter a valid url or resume!");
    }
  };

  return (
    <div style={{ padding: "10px" }}>
      <header className={styles.banner}>
        <h1>fairbetter</h1>
        <p style={{ fontSize: "14px", marginLeft: "10px" }}>
          By Abby G., Jade L., Vani R., Hetvi P.
        </p>
      </header>
      <header className={styles.desc}>
        <p style={{ textAlign: "center", padding: "10px" }}>
          Feel better and fairbetter at career fairs with our site! You can
          enter a company URL and/or your resume to generate questions to ask
          recruiters at events and in interviews!
        </p>
      </header>

      <div className={styles["column-container"]}>
        <div className={styles.column}>
          <form onSubmit={handleSubmit}>
            <input
              className={styles.urls}
              type="companyUrl"
              value={companyUrl}
              onChange={handleCompanyUrlChange}
              placeholder="enter company url:"
              style={{ marginLeft: "10px" }}
            />
            <BasicButton onclick={handleScrape} text="generate!" />
          </form>

          <section className={styles.sections} style={{ backgroundColor: "#4B97BB" }}>
            <h2>ABOUT THE COMPANY</h2>
            <p>
              {companyInfo ? <span>{companyInfo}</span> : "Enter a company URL to get general info about the company!"}
            </p>
          </section>

          <section className={styles.sections} style={{ backgroundColor: "rgb(26, 98, 87)" }}>
            <h2>PRODUCTS</h2>
            <p>
              {productInfo ? <div>{productInfo}</div> : "Enter a company URL to get info about the company's products"}
            </p>
          </section>

      <section className={styles.sections} style={{ backgroundColor: "#615A8C" }}>
        <h2>QUESTIONS</h2>
        <div style={{ display: "flex", alignItems: "center" }}>
          <select
            className={styles.dropdown}
            value={questionType}
            onChange={handleQuestionTypeChange}
            style={{ marginRight: "10px", padding: "5px" }}
          >
            <option value="">question type</option>
            <option value="about">About</option>
            <option value="products">Products</option>
          </select>
          <BasicButton text="generate!" />
        </div>
        
        {questionType === "about" && (
          <div>
            {aboutQuestions.length > 0 ? (
              aboutQuestions.map((question, index) => (
                <p key={index}>{question}</p>
              ))
            ) : (
              <p>Enter a company URL to get about questions</p>
            )}
          </div>
        )}
        
        {questionType === "products" && (
          <div>
            {productQuestions.length > 0 ? (
              productQuestions.map((question, index) => (
                <p key={index}>{question}</p>
              ))
            ) : (
              <p>Enter a company URL to get product questions</p>
            )}
          </div>
        )}
        
        <p>enter a company url to get example questions</p>
      </section>
              
        </div>

        <div className="column" style={{ marginLeft: "100px" }}>
          <form onSubmit={handleSubmit}>
            <input
              className={styles.urls}
              type="positionUrl"
              value={positionUrl}
              onChange={handlePositionUrlChange}
              placeholder="enter job position url:"
              style={{ marginLeft: "10px" }}
            />
            <BasicButton text="generate!" />
          </form>

          <Position />

          <section className={styles.sections} style={{ backgroundColor: "#606CA6" }}>
            <h2>SKILL ALIGNMENT</h2>
            <div>
              <label htmlFor="file" className={styles.resume}>
                {file ? file.name : "select resume file"}
              </label>
              <input
                id="file"
                type="file"
                onChange={handleFileChange}
                style={{ display: "none" }}
              />
              <BasicButton text="upload" />
            </div>
            <p>you match these qualifications: (enter a url to find out!!)</p>
          </section>
        </div>
      </div>
    </div>
  );
}
