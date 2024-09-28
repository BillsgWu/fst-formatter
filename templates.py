class Template:
    cursor = None
    tfile = None
    filetype = None
    merges = None
class ThisTemplate(Template):
    cursor = (1,8)
    merges = {2:3,4:6,7:9}
    tfile = "./template.xlsx"
    filetype = "binary/xlsx"