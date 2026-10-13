# FairBetter
By Abby Gillham, Jade Lavallee, Vani Ramesh, and Hetvi Patel

## What is FairBetter?
This project is designed to help students in career fairs learn more about the companies at these fairs, and give them prompts to ask specific questions to recruiters in order to gain better insight on the company and its available positions. This project's main functionalities are:

- Users can upload their resume and then view a list of generated questions regarding relevant job positions
- Users can type in a company website URL and receive a list of questions pertaining to company values, their products, etc. to ask recruiters during career fairs or during interviews
- Users can filter generated question content by category and can choose between company values, past projects, products, and more
- Users can view a brief description of the company’s values, projects, etc., providing context for generated questions
- Users can view their skill alignment with a given company, as well as related available positions at that company

To view the full project proposal, click on [this link](https://docs.google.com/document/d/1mV1K5WPqCeogfCkUp8lAnDB-jo6Rp8Sw4jq6DSICiSY/edit?tab=t.0).

## Design
In our Frontend, we will make API calls to the backend to collect the necessary data, which will already be formatted and parsed on the backend side. Then we can simply deal with the display on the React side.
![image](https://github.com/user-attachments/assets/8464d5ba-5048-4a2a-960d-718052a1a9c5)

## Mockups/User Interface
![image](https://github.com/user-attachments/assets/2b04d616-02ce-4175-91c1-167fe0759ec9)

**Why this setup?**

By keeping the frontend and backend separate during development, we can avoid bottlenecks. React is perfect for creating an interactive interface, while Python and Gemini handle the heavy lifting on the backend. This setup also makes future updates, like adding new data sources or improving the response system, easier to manage.

## Developer Roles

- **Abby Gillham:** Web scraping, About/product info summaries
- **Jade Lavallee:** UI design, web scraping
- **Vani Ramesh:** Question generator, api, resume scraper
- **Hetvi Patel:** Resume scraper

## Tech Stack

- Frontend:
  - React (JavaScript, CSS, HTML)
  - TypeScript
- Backend
  - Gemini (for the AI)
  - Flask
  - Python

## Development Process
Overall, our project went fairly smoothly, with the biggest hurdles being the Gemini AI configuration and the integration of frontend and backend.

We ran into some issues with the Gemini AI as most of us weren't familiar with using it before, so there was a significant learning curve in learning to make calls to the AI. We also had trouble getting the AI to output the correct format as the generate_content function would output it as a GenerateContentResponse object, but we were able to use the to_dict function to output it as a JSON.

Additionally, we had a lot of trouble with the integration because of type mismatches, where the parameter being called into the function was not of type JSON and thus was throwing errors, but by changing the return types of the functions to be consistent we were able to get the integration to work.

## Running the Project

To open up the website, run

```
npm run dev
```

In order to process links entered into the website, make sure to run

```
cd web_scraping
```

to enter our web scraping file and then run the command

```
python app.py
```

to run the backend.
