#%%

import pandas as pd
from update_date import update_date
from translate import translate
from formatting import format_date, format_title, format_authors

        
def write_funding_html(LANG, translate_dict):
    df = pd.read_csv(f"../achievements/Funding{LANG}.csv")
    df = df.sort_values(by = "Start", ascending = False).fillna("")
    N = df.shape[0]

    out_html = "\n\n\t<h2>Funding</h2>\n\t<ol>\n"
    for i in range(N):
        data = df.iloc[i].astype(str)
        start,finish,title,name,funding_source,PI,amount,unit = data
        if PI != "PI":
            PI = "collaborator"
        if LANG == "_JP":
            PI = PI.replace("PI", "代表").replace("collaborator","分担")

        out_html += f'\t\t<li><b>{name}</b> "{title}" ({PI}), {amount} {unit} ({start}--{finish}).</li><br>\n\n'
    out_html +="\t</ol>\n\n"
    with open(f"../funding{LANG}.html", "r", encoding="utf-8") as f:
        original_html = f.read()
    original_contents = original_html.split("<!-- PAGE SPECIFICS -->")[1].split("<!-- END PAGE SPECIFICS -->")[0]
    new_html = original_html.replace(original_contents, out_html)
    new_html = update_date(new_html)
    with open(f"../funding{LANG}.html", "w", encoding="utf-8") as f:
        f.write(new_html)