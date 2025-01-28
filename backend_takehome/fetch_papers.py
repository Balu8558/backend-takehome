import requests
import pandas as pd
from typing import List, Dict, Any

def fetch_papers(query: str) -> List[Dict[str, Any]]:
    """
    Fetch research papers from PubMed API based on the query.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 10  # Fetch up to 10 papers
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    paper_ids = response.json()["esearchresult"]["idlist"]
    
    paper_details = []
    for paper_id in paper_ids:
        details = fetch_paper_details(paper_id)
        if details:
            paper_details.append(details)
    
    return paper_details

def fetch_paper_details(paper_id: str) -> Dict[str, Any]:
    """
    Fetch details of a paper given its PubMed ID.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {
        "db": "pubmed",
        "id": paper_id,
        "retmode": "json"
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    paper_info = response.json()["result"][paper_id]
    
    return {
        "PubmedID": paper_id,
        "Title": paper_info.get("title", "N/A"),
        "Publication Date": paper_info.get("pubdate", "N/A"),
    }

def save_to_csv(papers: List[Dict[str, Any]], filename: str = "papers.csv"):
    """
    Save the fetched papers to a CSV file.
    """
    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")
