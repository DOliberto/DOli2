from lxml import etree
from functools import filter, reduce

"""
- [] add logging http://docs.python-guide.org/en/latest/writing/logging/

- [] use typing https://docs.python.org/3/library/typing.html
"""

# XPATH to elements marked up with DOli form information
DOLI_XPATH = "//span[@class='preprocdoli']"

def finfo_is_valid(finfo):
    return True

def compile_forms_in_file(fp, p):
    html = etree.parse(fp, parser=p)
    fs_infos = html.findall(DOLI_XPATH)
    return filter(finfo_is_valid, fs_infos)

def compile_files(fps, p):
    return reduce(lambda finfos, fp: compile_forms_in_file(fp, p) + finfos, fps, [])

def compile_forms(files):
    html_parser = etree.HTMLParser()
    return compile_files(fps, html_parser)
        
