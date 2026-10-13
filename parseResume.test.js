const fs = require("fs");
const PDFParser = require("pdf2json");

jest.mock("pdf2json", () => {
  return jest.fn().mockImplementation(() => {
    return {
      on: jest.fn(),
      loadPDF: jest.fn(),
    };
  });
});

describe("PDF Resume Parser", () => {
  let pdfParser;

  beforeEach(() => {
    PDFParser.mockClear();
    pdfParser = new PDFParser();
  });

  const parseResume = (text) => {
    const resumeData = {};

    const nameRegex = /^Name:\s*(.*)$/im;
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
  };

  it("should correctly parse resume text from a PDF", () => {
    const samplePDFData = {
      formImage: {
        Pages: [
          {
            Texts: [
              { R: [{ T: encodeURIComponent("Name: John Doe") }] },
              { R: [{ T: encodeURIComponent("Email: john.doe@example.com") }] },
              { R: [{ T: encodeURIComponent("Phone: +1234567890") }] },
              { R: [{ T: encodeURIComponent("Skills: JavaScript, Node.js, React") }] },
              { R: [{ T: encodeURIComponent("Education: BSc Computer Science") }] },
              { R: [{ T: encodeURIComponent("Experience: 5 years in web development") }] },
            ],
          },
        ],
      },
    };
  
    const rawText = samplePDFData.formImage.Pages.map((page) =>
      page.Texts.map((text) => decodeURIComponent(text.R[0].T)).join("\n")
    ).join("\n");
  
    const result = parseResume(rawText);
  
    expect(result.name).toBe("John Doe");
    expect(result.contacts).toEqual(["john.doe@example.com", "+1234567890"]);
    expect(result.skills).toEqual(["JavaScript", "Node.js", "React"]);
    expect(result.education).toBe("BSc Computer Science");
    expect(result.experience).toBe("5 years in web development");
  });
});