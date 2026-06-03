#%%
import pandas as pd
from update_date import update_date
from formatting import format_date
from translate import translate
import datetime


format_list = ["Upcoming Presentations","Invited","Oral","Poster"]
today = int(datetime.date.today().strftime("%Y%m%d"))

def presentation_df_to_html(df, out_html, format):
    df = df.sort_values(by = "Date", ascending = False)
    N = df.shape[0]

    if N == 0:
        return ""
    else:
        out_html += f"\t<h2>{format} ({N})</h2>\n\t<ol>\n"
        for i in range(N):
            data = df.iloc[i].astype(str)
            date,conference,venue,country_or_city,title,authors,format,notes = data
            date = format_date(date)
            out_html += f'\t\t<li>{authors}, <b>"{title}"</b>, {conference}, {venue}, {country_or_city} ({date}).</li><br>\n\n'
        out_html += "\t</ol>\n\n"
        return out_html

def write_presentations_html(LANG, translate_dict):
    file_name = f"../achievements/Presentations{LANG}.csv"
    all_df = pd.read_csv(file_name, encoding_errors = "backslashreplace")
    all_df.Date.astype(int)
    # try: 
    #     all_df == all_df.sort_values(by=["Date"])
    # except ValueError:
    #     all_df.to_csv(file_name, index = False)
    # This part probably not working
    out_html = ""
    for j,format in enumerate(format_list):
        if format == "Upcoming Presentations":
            df = all_df[all_df.Date >= today]
        else:
            df = all_df[all_df.Date < today]
            df = df[df.Format == format_list[j]]
        out_html = presentation_df_to_html(df, out_html, format)
        # out_html = write_presentation_html(df, out_html, format)
    out_html = translate(out_html, LANG, translate_dict)            
        
            
    with open(f"../presentations{LANG}.html", "r", encoding="utf-8") as f:
        original_html = f.read()
        original_contents = original_html.split("<!-- PAGE SPECIFICS -->\n")[1].split("<!-- END PAGE SPECIFICS -->")[0]
    with open(f"../presentations{LANG}.html", "w", encoding="utf-8") as f:
        new_html = original_html.replace(original_contents, out_html)
        new_html = update_date(new_html)
        f.write(new_html)