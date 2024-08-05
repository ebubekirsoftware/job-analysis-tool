# Job Analysis Tool

## Overview

The Job Analysis Tool is a Python application designed to scrape job listings, analyze job descriptions using OpenAI's GPT model, and visualize technology trends. This tool allows you to efficiently extract and process job-related data and gain insights into technological requirements.

## Features

- **Scrape Job Listings**: Extract job listings from a specified country and job title.
- **Process Job Descriptions**: Use OpenAI's GPT model to analyze job descriptions.
- **Visualize Technology Trends**: Generate visualizations to understand technology trends in job descriptions.

## Requirements
- pandas==1.4.4
- plotly==5.9.0
- openai==1.35.13
- selenium==4.21.0
- beautifulsoup4==4.11.1

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/ebubekirsoftware/job-analysis-tool.git
    cd job-analysis-tool
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Ensure you have ChromeDriver installed and accessible in your PATH, or adjust the `driver_path` argument accordingly.

## Usage

To run the application, use the following command:

```bash
python app.py --api_key YOUR_API_KEY --title "Job Title" --country "Country" --number_of_jobs 100
```

Replace YOUR_API_KEY with your OpenAI API key, and adjust Job Title, Country, and number_of_jobs according to your needs.

Command-line Arguments
--api_key: Your OpenAI API key (required)
--title: Job title to analyze (required)
--country: Country to analyze job listings from (required)
--number_of_jobs: Number of job listings to scrape (required)
--driver_path: Path to the ChromeDriver executable (optional, default is "chromedriver.exe")

### Example

```bash
python app.py --api_key sk-abc123 --title "Data Scientist" --country "USA" --number_of_jobs 100
```

This will scrape 100 job listings for the title "Data Scientist" in the USA, process the job descriptions using OpenAI's API, and visualize the technology trends.
