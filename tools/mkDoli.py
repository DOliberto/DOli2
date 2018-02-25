from lxml import etree
from functools import reduce
from os.path import basename, splitext

"""
reads jinja2 template and compiles forms from its markup.

example markup:
```
<span class="preprocdoli" data-label="texto" data-validator="not-empty" data-long="true">
  {{_texto}}
</span>
```

means that the variable `_texto` will be captured by a form with 'texto' as
label, and with validator that assures it is not empty. the data-long='true'
means that the form should actually be an HTML input box.
"""

"""
TO-DO
- [] add terminal call
- [] add logging http://docs.python-guide.org/en/latest/writing/logging/
"""

# XPATH to elements marked up with DOli form information
DOLI_XPATH = "//span[@class='preprocdoli']"

# field separator in data-validator attribute
VALIDATOR_LIST_SEP = "|"

# maps human-friendly string to WTForms validator function string
VALIDATOR_MAP = {"not-empty": "DataRequired()", "is-number": "Number()"}

def elem_valid(elem):
    """checks if <span> element is valid form markup."""
    try:
        assert elem.get("class") == "preprocdoli"
        assert elem.get("data-label") is not None
        assert elem.get("data-validator") is not None
        assert elem.get("data-long") in ["true", "false"]
        return True
    except AssertionError:
        return False

def elem_varname(elemtext):
    """transforms '\n {{_var_name}} \n ' into _var_name."""
    return elemtext.partition("{{")[2].partition("}}")[0]

def is_long(val):
    val = val.lower()
    if val == "true":
        return True
    elif val == "false":
        return False

def elem2finfo(elem):
    """
    transforms <span> element into formulary data tuple:
    
    (variable-name, is long form?, form-label, form-validators)
    """
    if elem_valid(elem):
        return (elem_varname(elem.text), is_long(elem.get("data-long")), elem.get("data-label"), elem_validators(elem.get("data-validator")))
    else:
        return None

def to_val(validator_str):
    """maps human-friendly string to WTForms validator function
    string."""
    return VALIDATOR_MAP[validator_str]

def elem_validators(val_field):
    """transforms list of human-friendly strings to list of WTForms
    validator functions strings."""
    val_elems = val_field.split(VALIDATOR_LIST_SEP)
    return list(map(to_val, val_elems))

def filenameWOext(fp):
    return splitext(basename(fp))[0]

def compile_forms_in_file(fp, p):
    """reads form markup in file using parser p to tuple."""
    html = etree.parse(fp, parser=p)
    fs_infos = html.findall(DOLI_XPATH)
    return (filenameWOext(fp), list(map(elem2finfo, fs_infos)))

def compile_files(fps, p):
    """reads markup in files using parser p and compiles them to python
    functions."""
    return reduce(lambda finfos, fp: finfos.append(compile_forms_in_file(fp, p)) or finfos, fps, [])

def compile_forms(files):
    """compiles files to python module containing WTForms."""
    html_parser = etree.HTMLParser(encoding="utf8", recover=False)
    return compile_files(files, html_parser)
