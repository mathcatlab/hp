#%%
def format_date(date,n=8): # change format if n < 8
    date = str(date)
    formatted_date = date[:4]+"/"+date[4:6]+"/"+date[6:8]
    formatted_date = formatted_date.replace("X","")
    return formatted_date

def format_title(title):
    return title.replace(";",",")

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

def format_notes(notes):
    if notes == "":
        return ""
    else:
        return f" ({notes})"

