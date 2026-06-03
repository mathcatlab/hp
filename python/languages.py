
translate_dict = {"Scientific Publications":"論文",
                  "Corresponding Author":"責任著者",
                  "First Author":"筆頭著者",
                  "Last Author":"最終著者",
                  "Patents":"知財・特許",
                  "Dual ":"共同"}    

def translate(txt):
    for k,v in translate_dict.items():
        txt = txt.replace(k,v)
    return txt