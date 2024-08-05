# Job Analysis Tool

## Overview

The Job Analysis Tool is a Python application designed to scrape job listings, analyze job descriptions using OpenAI's GPT model, and visualize technology trends. This tool allows you to efficiently extract and process job-related data and gain insights into technological requirements.

## Features

- **Scrape Job Listings**: Extract job listings from a specified country and job title.
- **Process Job Descriptions**: Use OpenAI's GPT model to analyze job descriptions.
- **Visualize Technology Trends**: Generate visualizations to understand technology trends in job descriptions.

## Requirements

- Python 3.x
- `pandas`
- `argparse`
- `requests` (for making API calls)
- `selenium` (for web scraping)
- `matplotlib` (for visualizations)
- `openai` (for GPT processing)
- ChromeDriver (or another WebDriver for Selenium)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/job-analysis-tool.git
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
