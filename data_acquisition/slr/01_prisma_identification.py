"""
PRISMA Stage 1 v2: Identification — Semantic Scholar + PubMed + manual web
Fallback since OpenAlex returns 503
"""
import requests
import pandas as pd
import time
from pathlib import Path
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

OUT = Path("data_acquisition/slr")
OUT.mkdir(parents=True, exist_ok=True)
MAX_RETRIES = 3

def s2_search(query, label, limit=100):
    """Semantic Scholar search (free, no API key needed)"""
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    all_results = []
    offset = 0
    while offset < limit:
        for attempt in range(MAX_RETRIES):
            try:
                params = {
                    "query": query,
                    "limit": min(100, limit - offset),
                    "offset": offset,
                    "year": "2020-2026",
                    "fieldsOfStudy": "Economics,Business",
                    "fields": "title,authors,year,externalIds,journal,citationCount,openAccessPdf",
                }
                r = requests.get(url, params=params, timeout=30)
                if r.status_code == 200:
                    data = r.json()
                    papers = data.get("data", [])
                    if not papers:
                        break
                    for p in papers:
                        all_results.append({
                            "query": label,
                            "title": p.get("title", ""),
                            "authors": ", ".join([a.get("name", "") for a in p.get("authors", [])][:5]),
                            "year": p.get("year", ""),
                            "doi": p.get("externalIds", {}).get("DOI", ""),
                            "journal": p.get("journal", {}).get("name", ""),
                            "cited_by": p.get("citationCount", 0),
                            "open_access": bool(p.get("openAccessPdf")),
                        })
                    progress = min(offset + len(papers), limit)
                    print(f"  {label}: {progress}/{limit}", end="\r")
                    offset += len(papers)
                    break
                elif r.status_code == 429:
                    time.sleep(5 * (attempt + 1))
                else:
                    time.sleep(2)
                    break
            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    print(f"\n  FAILED {label}: {e}")
                time.sleep(2)
        time.sleep(1.5)  # rate limit

    return all_results

# Search themes
searches = [
    ('"data descriptor" "stock market" OR "capital market" OR financial dataset', "Data Descriptor Financial"),
    ('"panel data" "stock exchange" "emerging" firm value OR firm performance fixed effects', "Panel Emerging Mkts"),
    ('ESG OR "environmental social" "firm value" OR "tobin q" Sharia OR Islamic stock ASEAN OR Indonesia', "ESG Sharia Firm Value"),
    ('"Indonesia Stock Exchange" OR IDX capital market panel OR dataset OR analysis', "IDX Studies"),
    ('"data in brief" OR "Scientific Data" Indonesia OR "emerging economy" finance OR economics', "Data Journals"),
]

all_papers = []
for query, label in searches:
    print(f"\nSearching: {label}")
    papers = s2_search(query, label, limit=100)
    all_papers.extend(papers)
    print(f"\n  => {len(papers)} papers for {label}")
    time.sleep(2)

df = pd.DataFrame(all_papers)
# Deduplicate
df = df.drop_duplicates(subset=["title"]).copy()
df = df[df["doi"].notna() | (df["title"] != "")].copy()
df.to_csv(OUT / "prisma_1_identification.csv", index=False)

print(f"\n{'='*50}")
print(f"PRISMA STAGE 1 COMPLETE")
print(f"Total unique papers: {len(df)}")
for q in sorted(df["query"].unique()):
    n = len(df[df["query"] == q])
    print(f"  {q}: {n}")
