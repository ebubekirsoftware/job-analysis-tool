import pandas as pd
import warnings
from collections import Counter
import plotly.express as px
import plotly.offline as pyo
warnings.filterwarnings('ignore')

def extract_technologies(jobs_df):
    """Extracts and cleans the list of technologies from job descriptions."""
    technologies_list = jobs_df['Technologies'].dropna()
    all_technologies = [tech.strip() for sublist in technologies_list for tech in sublist]
    all_technologies = [tech.upper() for tech in all_technologies]
    return all_technologies

def count_technologies(all_technologies):
    """Counts the frequency of each technology."""
    tech_counter = Counter(all_technologies)
    return tech_counter.most_common(15)

def prepare_technology_data(jobs_df):
    """Prepares the data for visualization."""
    all_technologies = extract_technologies(jobs_df)
    top_technologies = count_technologies(all_technologies)
    top_technologies_df = pd.DataFrame(top_technologies, columns=['Technology', 'Count'])
    total_technologies = len(jobs_df['Technologies'].dropna())
    top_technologies_df['Percentage'] = round((top_technologies_df['Count'] / total_technologies) * 100, 3)
    return top_technologies_df.sort_values(by='Percentage', ascending=True)

def visualize_technologies(top_technologies_df, title, country, count):
    """Generates and displays a bar chart of the most demanded technologies."""
    fig = px.bar(
        top_technologies_df,
        x='Percentage',
        y='Technology',
        orientation='h',
        title=f"{title} İş İlanlarında En Çok Talep Edilen 15 Teknoloji ({country})",
        labels={'Percentage': 'Talep Yüzdesi (%)', 'Technology': 'Teknoloji'},
        text='Percentage',
        color='Percentage',
        color_continuous_scale='viridis'
    )

    fig.update_layout(
        title_font_size=16,
        title_font_family='Arial',
        title_font_color='black',
        xaxis_title_font_size=14,
        yaxis_title_font_size=14,
        xaxis_tickfont_size=12,
        yaxis_tickfont_size=12
    )

    fig.add_annotation(
        text=f"{count} adet iş ilanı baz alınmıştır.",
        xref="paper", yref="paper",
        x=0.99, y=0.01,
        showarrow=False,
        font=dict(size=12, color="black")
    )

    pyo.plot(fig)
