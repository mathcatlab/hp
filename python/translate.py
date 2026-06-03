#%%
import csv
def define_translate_dict(file_name = "translate_dict.csv"):
    reader = csv.reader(open(file_name,"r"))
    d = {}
    for row in reader:
        k, v = row
        d[k] = v
    return d

def translate(html, LANG, dict):
    if LANG == "":
        pass
    else:
        for k, v in dict.items():
            html = html.replace(k, v)
    return html