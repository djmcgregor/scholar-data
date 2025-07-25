from os import getenv
from scholarly import scholarly
import pandas as pd
import matplotlib.pyplot as plt


def get_citation_data(author_id):
    # Function to get citation data using author ID
    # Retrieve the author using the author ID
    author = scholarly.search_author_id(author_id)

    # Fill in the author details
    author = scholarly.fill(author)
    print(f"Author: {author['name']}")

    # Extract citation metrics
    citations_per_year = author['cites_per_year']
    total_citations = author['citedby']
    h_index = author['hindex']
    i10_index = author['i10index']

    return citations_per_year, total_citations, h_index, i10_index


def save_to_csv(citations_per_year, total_citations, h_index, i10_index):
    # First, total metrics
    metrics = pd.DataFrame({
        'Metric': ['NaN', 'Citations:', 'h-index:', 'i10-index:'],
        'Value': ('NaN', total_citations, h_index, i10_index)
    }) # include NaN for the first row to accomodate google sheet format
    metrics.to_csv('data/total_metrics.csv', index=False, header=False)

    # Now Annual Metrics - convert to DataFrame
    df = pd.DataFrame(list(citations_per_year.items()), columns=['Year', 'Citations'])
    df.to_csv('data/annual_citations.csv', index=False)

def plot_citations(citations_per_year):
    # Function to generate bar plot
    df = pd.DataFrame(list(citations_per_year.items()), columns=['Year', 'Citations'])
    years = df.Year
    citations = df.Citations
    # years = list(citations_per_year.keys())
    # citations = list(citations_per_year.values())

    plt.bar(years, citations, color='gray', width=0.5)

    # Add data labels
    for i, citation in enumerate(citations):
        plt.text(years[i],
                 citation + 1,
                 str(citation),
                 ha='center',
                 va='bottom',
                 bbox=dict(facecolor='white',
                           edgecolor='none',
                           boxstyle='round,pad=0.2'))

    # Set axis labels and title
    plt.ylabel('Citations')
    plt.xlabel('Year')

    # Set y-axis limits to provide space above bars, add horizontal grid lines, and remove tick marks
    plt.ylim(-0.1, citations.max() + 10)
    plt.grid(axis='y', linestyle='-', color='gray', alpha=0.25)
    plt.tick_params(axis='both', which='both', length=0)

    # Remove the border (spines) of the plot
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    # Save the plot
    plt.savefig('data/citations_plot.png', dpi=300, bbox_inches='tight')


def main():
    author_id = getenv("AUTHOR_ID")
    citations_per_year, total_citations, h_index, i10_index = get_citation_data(author_id)

    # Save data to CSV
    save_to_csv(citations_per_year, total_citations, h_index, i10_index)

    # Plot citations
    plot_citations(citations_per_year)


if __name__ == "__main__":
    main()
