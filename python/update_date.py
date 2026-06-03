#%%	
import datetime
import re

def update_date(html):
    today = datetime.date.today().strftime('%Y/%m/%d')
    update_date = "(Last Update: [\d+\/]+\d+)"
    old_str = re.findall(update_date, html)[-1]
    new_str = rf"Last Update: {today}"
    html = html.replace(old_str, new_str)
    return html