import argparse
from scrap import Scraper
from gpt_query import initialize_openai_client, process_job_descriptions
from visual import prepare_technology_data, visualize_technologies


def main(api_key, title, country, number_of_jobs, driver_path):
    # Scraping jobs
    scraper = Scraper(driver_path)
    jobs_df = scraper.get_job_listings(title, country, number_of_jobs)
    descriptions = scraper.get_job_descriptions(jobs_df)
    clean_descriptions = scraper.clean_html(descriptions)
    jobs_df['Job Description'] = clean_descriptions

    # Processing job descriptions
    client = initialize_openai_client(api_key)
    jobs_df = process_job_descriptions(jobs_df, client)
    print(jobs_df.head())

    # Visualization
    top_technologies_df = prepare_technology_data(jobs_df)
    count = len(jobs_df)
    visualize_technologies(top_technologies_df, title, country, count)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Job Analysis Tool")
    parser.add_argument('--api_key', type=str, required=True, help="OpenAI API key")
    parser.add_argument('--title', type=str, required=True, help="Job title to analyze")
    parser.add_argument('--country', type=str, required=True, help="Country to analyze job listings from")
    parser.add_argument('--number_of_jobs', type=int, required=True, help="Number of job listings to scrape")
    parser.add_argument('--driver_path', type=str, default="chromedriver.exe",
                        help="Path to the ChromeDriver executable")

    args = parser.parse_args()

    main(args.api_key, args.title.upper(), args.country.upper(), args.number_of_jobs, args.driver_path)
