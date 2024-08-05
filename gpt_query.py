import os
import re
import pandas as pd
from openai import OpenAI


def initialize_openai_client(api_key):
    return OpenAI(api_key=api_key)


def extract_technologies(description, client):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a skilled assistant, adept at extracting technologies from job descriptions."
            },
            {
                "role": "user",
                "content": f"Given the following job description, extract a list of tools, programming languages and frameworks mentioned. Identify all mentioned tools, programming languages, frameworks. Pay special attention to sections like 'Requirements,' 'Qualifications,' or 'What You'll Need,' but also look for relevant information throughout the entire description. Exclude general phrases like 'ability to work in a team' unless they are specifically emphasized as a key requirement. List them separated by commas.\n\nJob Description: {description}\n\nTechnologies and Skills:"
            }
        ],
        max_tokens=100,
        n=1,
        stop="\n",
        temperature=0.5,
    )
    technologies = response.choices[0].message
    return technologies


def extract_content(text):
    text = str(text)
    match = re.search(r"content='(.*?)'", text)
    return match.group(1) if match else text


def process_job_descriptions(jobs_df, client):
    jobs_df['Technologies'] = jobs_df['Job Description'].apply(lambda desc: extract_technologies(desc, client))
    jobs_df['Technologies'] = jobs_df['Technologies'].apply(extract_content)
    jobs_df['Technologies'] = jobs_df['Technologies'].apply(lambda x: x.split(', '))
    #jobs_df.to_csv('jobs.csv', index=False)
    return jobs_df


def main():
    api_key = load_openai_api_key()
    client = initialize_openai_client(api_key)
    jobs_df = pd.read_csv('jobs.csv')
    jobs_df = process_job_descriptions(jobs_df, client)
    print(jobs_df.head())


if __name__ == "__main__":
    main()
