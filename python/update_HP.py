#%%
from update_publications import write_publications_html
from update_presentations import write_presentations_html
from update_awards import write_awards_html
from update_funding import write_funding_html
from CV_utils import write_csv_from_bib

# from python.archived.clean_bib import save_cleaned_bib
from translate import define_translate_dict

translate_dict = define_translate_dict("translate_dict.csv")

write_csv_from_bib("../achievements/Publications.bib")       
# save_cleaned_bib()
for LANG in ["","_JP"]:
    write_publications_html(LANG, translate_dict)
    write_presentations_html(LANG, translate_dict)
    # check hyphens in page numbers are OK if there is a cp932 error
    write_awards_html(LANG)
    write_funding_html(LANG,translate_dict)
    # update funding, add hyphen japanese
