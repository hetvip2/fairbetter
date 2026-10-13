import fs from "fs";
import PDFParser from "pdf2json";

const pdfParser = new PDFParser();

const filename = "./uploads/table.pdf";

pdfParser.on("pdfParser_dataError", (errData) =>
  console.error("Error parsing PDF:", errData.parserError)
);

pdfParser.on("pdfParser_dataReady", (pdfData) => {
  // Convert the raw PDF JSON data to text
  const rawText = samplePDFData.formImage.Pages.map((page) =>
  page.Texts.map((text) => decodeURIComponent(text.R[0].T)).join("\n")
).join("\n");

  // Extract resume sections
  const resumeData = parseResume(rawText);

  console.log("Parsed Resume Data:", resumeData);
});

pdfParser.loadPDF(filename);

// Function to parse specific resume sections from the text
function parseResume(text) {
  const resumeData = {};

  const nameRegex = /^Name:\s*(.+)$/im; // Fixed regex
  const contactRegex = /(?:Email|E-mail|Phone|Mobile):?\s*([\w@.\-+() ]+)/gi;
  const skillsRegex = /Skills:\s*(.*)/i;
  const educationRegex = /Education:\s*(.*)/i;
  const experienceRegex = /Experience:\s*(.*)/i;

  const nameMatch = text.match(nameRegex);
  const contactMatches = Array.from(text.matchAll(contactRegex));
  const skillsMatch = text.match(skillsRegex);
  const educationMatch = text.match(educationRegex);
  const experienceMatch = text.match(experienceRegex);

  resumeData.name = nameMatch ? nameMatch[1].trim() : "Not found";
  resumeData.contacts = contactMatches.map((match) => match[1].trim());
  resumeData.skills = skillsMatch ? skillsMatch[1].split(",").map((s) => s.trim()) : [];
  resumeData.education = educationMatch ? educationMatch[1].trim() : "Not found";
  resumeData.experience = experienceMatch ? experienceMatch[1].trim() : "Not found";

  return resumeData;
}