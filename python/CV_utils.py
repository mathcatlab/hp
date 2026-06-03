#%%
import pandas as pd
import bibtexparser

def sort_authors(authors):
    sorted_authors = ""
    for a in authors.split(" and "):
        last,first  = a.split(", ")
        sorted_authors += first + " " + last + ", "
    sorted_authors = sorted_authors[:-2]        
    return sorted_authors

def write_csv_from_bib(bib_file, sort = True):
    with open(bib_file) as f:
        bib = bibtexparser.load(f)
    df = pd.DataFrame(bib.entries)    
    # cols = ["ID", "author","journal","year","volume","pages", "doi", "notes", "ENTRYTYPE"]
    # missing_cols = [item for item in df.columns if item not in cols]
    # cols += missing_cols
    df = df.sort_values(by=["year"], ascending = False)   
    df = df.fillna("")
    num_publications =df.shape[0]
    corresponding_authors = df.author.str.contains(r"Ooka\*").sum()
    first_authors = df.ID.str.contains("Ooka").sum()
    print(num_publications, corresponding_authors, first_authors)
    df.to_csv("../achievements/publications.csv")
if __name__ == "__main__":
    write_csv_from_bib("../achievements/publications.bib")
