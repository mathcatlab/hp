#%%
import pandas as pd
from formatting import format_date, format_notes
from update_date import update_date
def awards_df_to_html(LANG):
    df = pd.read_csv(f"../achievements/Awards{LANG}.csv")
    df = df.sort_values(by = "Date", ascending = False).fillna("")
    N = df.shape[0]
    out_html = f"\n\t<ol>\n"
    for i in range(N):
        data = df.iloc[i].astype(str)
        date,prize, from_where, notes = data
        date = format_date(date)
        notes = format_notes(notes)
        out_html += f'\t\t<li><b>{prize}</b>{notes}, {date}.</li><br>\n\n'
    out_html += "\t</ol>\n\n"
    return out_html



def write_awards_html(LANG):
    out_html = awards_df_to_html(LANG)
    with open(f"../awards{LANG}.html", "r", encoding="utf-8") as f:
        original_html = f.read()
        original_contents = original_html.split("<!-- PAGE SPECIFICS -->\n")[1].split("<!-- END PAGE SPECIFICS-->")[0]
    with open(f"../awards{LANG}.html", "w", encoding="utf-8") as f:
        new_html = original_html.replace(original_contents, out_html)
        new_html = update_date(new_html)
        f.write(new_html)