from lxml import etree
from functools import reduce

"""
- [] add logging http://docs.python-guide.org/en/latest/writing/logging/

- [] use typing https://docs.python.org/3/library/typing.html
"""

# XPATH to elements marked up with DOli form information
DOLI_XPATH = "//span[@class='preprocdoli']"
VALIDATOR_LIST_SEP = "|"
VALIDATOR_MAP = {"not-empty": "DataRequired()", "is-number": "Number()"}

def elem_valid(elem):
    try:
        assert elem.get("class") == "preprocdoli"
        assert elem.get("data-label") is not None
        assert elem.get("data-validator") is not None
        assert elem.get("data-long") in [None, "true", "false"]
        return True
    except AssertionError:
        return False

def is_long(val):
    if val is None:
        return False
    val = val.lower()
    if val == "true":
        return True
    elif val == "false":
        return False

def elem2finfo(elem):
    if elem_valid(elem):
        return (is_long(elem.get("data-long")), elem.get("data-label"), elem_validators(elem.get("data-validator")))
    else:
        return None

def to_val(validator_str):
    return VALIDATOR_MAP[validator_str]

def elem_validators(val_field):
    val_elems = val_field.split(VALIDATOR_LIST_SEP)
    return list(map(to_val, val_elems))

def compile_forms_in_file(fp, p):
    html = etree.parse(fp, parser=p)
    fs_infos = html.findall(DOLI_XPATH)
    return list(map(elem2finfo, fs_infos))

def compile_files(fps, p):
    return reduce(lambda finfos, fp: compile_forms_in_file(fp, p) + finfos, fps, [])

def compile_forms(files):
    html_parser = etree.HTMLParser(encoding="utf8", recover=False)
    return compile_files(files, html_parser)
