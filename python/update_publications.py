#%%
"""
To update the publication list, the Publications.bib file should be updated manually.
Then, the bib will be converted to csv and then written to html
"""

import pandas as pd
from update_date import update_date
from translate import translate
from formatting import format_date, format_title, format_authors
# from languages import translate
"""
def format_title(title):
    return title.replace(";",",")
def format_date(date,n=8): # change format if n < 8
    date = str(date)
    formatted_date = date[:4]+"/"+date[4:6]+"/"+date[6:8]
    formatted_date = formatted_date.replace("X","")
    return formatted_date
def format_authors(authors):
    sorted_authors = ""
    for a in authors.split(" and "):
        try:
            last,first  = a.split(", ")
            sorted_authors += first + " " + last + ", "
        except ValueError:
            sorted_authors += a + ", "
    sorted_authors = sorted_authors[:-2]        
    return sorted_authors
"""

from CV_utils import write_csv_from_bib


def reorder_publications(publications):
    priority = publications.author.str.count("Ooka\*")
    priority += publications.author.str.startswith("Ooka")
    priority += 2*publications.journal.str.count("Nature")
    priority += 2*publications.journal.str.count("Science")
    priority += publications.journal.str.count("Nat.")
    publications["priority"] = priority
    publications = publications.sort_values(by = ["type", "year", "priority","status"], ascending = [True, False, False, False]).fillna("")
    return publications


def write_publications_html(LANG, translate_dict):
    ### first update the csv file
    write_csv_from_bib("../achievements/publications.bib") 

    #### Main Articles #####
    publications = pd.read_csv(f"../achievements/Publications.csv", index_col = 0) # {LANG}
    publications = reorder_publications(publications)


    original = publications[publications["type"]=="Original"]
    review = publications[publications["type"]=="Review"]
    editorial = publications[publications["type"]=="Editorial"]


    num_corresponding = publications["author"].str.contains("Ooka\*").sum() # Must write Ooka*+, not Ooka+*
    num_first = publications["ID"].str.contains("Ooka").sum() + publications["author"].str.contains("Ooka+",regex=False).sum() + publications["author"].str.contains("Ooka*+",regex=False).sum()
    # out_html = f"<br>(Corresponding Author: {num_corresponding}, First Author: {num_first}, +: Dual First Author)<br>\n\n"
    out_html = ""

    df_list =[original, review, editorial]
    for i, df in enumerate(df_list):
        if i == 0:
            out_html += f"\n\t<h2>Original Articles</h2><ol>\n"
        elif i == 1:
            out_html += f"\n\t<h2>Reviews</h2><ol>\n"
        elif i == 2:
            out_html += f"\n\t<h2>Editorials and Perspectives</h2><ol>\n"
        year_header = 2030
        N = df.shape[0]
        for j in range(N):
            data = df.iloc[j]# .astype(str)
            type,notes,status,url,preprint,bib_key,j_key,title,pages,volume,year,fullname,abbrv,journal,authors,ENTRYTYPE,ID,priority  = data
            year = int(year)
            if year < year_header:
                year_header = year
                out_html += f"\t<h2>{year_header}</h2>\n"
            if authors != "":
                authors = format_authors(authors)
                out_html += f"\t\t<li>{authors}"
            if title != "":
                out_html += f" <b>\"{title}\"</b>" 
            if journal != "":
                out_html += f", <i>{journal}</i>"
            if year != "":
                out_html += f", <b>{year}</b>"
            if volume != "":
                volume = int(volume)
                out_html += f", <i>{volume}</i>"
            if pages != "": 
                out_html += f", {pages}"
            if status != "":
                out_html += f" (<i>{status}</i>)"
            out_html += "."
            if url != "":
                out_html += f"    <a href=\"{url}\" target=\"_blank\">link</a>"
            if preprint != "":
                out_html += f"    <a href=\"{preprint}\" target=\"_blank\">preprint</a>"            
            out_html += f"<br>\n\n" 
        out_html += "\t</ol>\n\n"
    #### Other Articles (Non Peer Reviewed) #####
    out_html += f"<h2>Other Articles (Non Peer Reviewed)</h2><ol>\n"
    df = pd.read_csv(f"../achievements/Non_Peer_Reviewed{LANG}.csv")
    df = df.sort_values(by = ["Year"], ascending = [False]).fillna("")
    N = df.shape[0]
    for i in range(N):
        data = df.iloc[i].astype(str)
        title, authors, journal, year, volume, pages, URL, type, date, doi, notes = data
        year = int(year)
        volume = int(volume)
        title = format_title(title)
        authors = format_authors(authors)
        if pages != "": # it has "proper" bibliography information:
            out_html += f"\t\t<li>{authors} \"{title}\", <i>{journal}</i>, <b>{year}</b>, <i>{volume}</i>, {pages}.<br>\n\n"
        if pages == "": # it must have a URL
            out_html += f"\t\t<li>{authors} \"{title}\", <i>{journal}</i>, <b>{year}</b> (<a href={URL}>URL</a>).<br>\n\n"
    out_html += "\t</ol>\n\n"
    out_html = out_html.replace("MoS$_2$", "MoS<sub>2</sub>").replace("CO$_2$", "CO<sub>2</sub>").replace("{\`e}","&egrave").replace("MnO$_2$", "MnO<sub>2</sub>")
    out_html = out_html.replace("--"," - ")
    out_html = out_html.replace("<i></i>, ","").replace(", .", ".")
    out_html = translate(out_html, LANG, translate_dict) 

    with open(f"../publications{LANG}.html", "r", encoding="utf-8") as f:
        original_html = f.read()
    original_contents = original_html.split("<!-- PAGE SPECIFICS -->")[1].split("<!-- END PAGE SPECIFICS -->")[0]
    new_html = original_html.replace(original_contents, out_html)
    new_html = update_date(new_html)
    with open(f"../publications{LANG}.html", "w", encoding="utf-8") as f:
        f.write(new_html)
