from lxml import etree
from functools import reduce
from os.path import basename, splitext
from jinja2 import Template
from forms_templates import REGULAR_FORM_TEMPLATE

"""
reads jinja2 template and compiles forms from its markup.

example markup in `doli-templates/`.
"""

"""
TO-DO
- [ ] add logging http://docs.python-guide.org/en/latest/writing/logging/
- [ ] check if there is clash in var_names
"""

# XPATH to elements marked up with DOli form information
DOLI_XPATH = "//span[@class='doli-elem']"

# field separator in data-validator attribute
VALIDATOR_LIST_SEP = "|"

# maps human-friendly string to WTForms validator function string
VALIDATOR_MAP = {"not-empty": "DataRequired()", "is-number":
                 "Number()", "": None}
# maps human-friendly string to WTForms class
FORM_TYPE_MAP = {"long": "HTMLField", "date": "DateField", "text":
                 "StringField", "": None}


def elem_valid(elem):
    """checks if <span> element is valid form markup."""
    assert elem.get("class") == "doli-elem"
    assert elem.get("data-label") is not None
    assert elem.get("data-validator") is not None
    assert elem.get("data-type") in FORM_TYPE_MAP.keys()
    return True


def elem_varname(elemtext):
    """transforms '\n {{_var_name}} \n ' into _var_name."""
    return elemtext.partition("{{")[2].partition("}}")[0].strip()


def elem2field(elem):
    """
    transforms <span> element into formulary data dictionary.
    """
    if elem_valid(elem):
        return {"var_name": elem_varname(elem.text),
                "type": to_form_type(elem.get("data-type")),
                "label": elem.get("data-label"),
                "validators": elem_validators(elem.get("data-validator"))}
    else:
        return None


def to_form_type(type_str):
    """maps human-friendly string to WTForms class"""
    return FORM_TYPE_MAP[type_str]


def to_val(validator_str):
    """maps human-friendly string to WTForms validator function
    string."""
    return VALIDATOR_MAP[validator_str]


def elem_validators(val_field):
    """transforms list of human-friendly strings to list of WTForms
    validator functions strings."""
    val_field = val_field.strip()
    if val_field == "":
        return []
    else:
        val_elems = val_field.split(VALIDATOR_LIST_SEP)
        return list(map(to_val, val_elems))

    
def filenameWOext(fp):
    return splitext(basename(fp))[0]


def make_form(form_name, form_fields):
    return {"name": form_name, "fields": form_fields}


def compile_form_in_file(fp, p):
    """
    reads form markup in file using parser p to tuple. we might have
    to manually feed the parser an enclosing `div` element, else it
    won't consider the markdown file valid HTML.

    """
    #p.feed('<div class="doli-publication" id="doli-{}">\n\n'.format(basename(fp)))
    html = etree.parse(fp, parser=p)
    #p.feed('\n</div>')
    #p.close()
    elems = html.findall(DOLI_XPATH)
    return make_form(filenameWOext(fp), list(map(elem2field, elems)))


def parse_files(fps):
    """reads markup in files using parser p and compiles them to python
    functions."""
    html_parser = etree.HTMLParser(encoding="utf8", recover=False)
    return {"forms": list(reduce(lambda fields, fp:
                                 fields.append(compile_form_in_file(fp, html_parser)) or fields,
                                 fps, []))}


def render_forms(forms):
    form_template = Template(REGULAR_FORM_TEMPLATE)
    return form_template.render(forms)


def compile_forms(files):
    """
    compiles files to python module containing WTForms.
    :files: [filepath]
    """
    forms = parse_files(files)
    return render_forms(forms)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="This utility is part of the DOliberto project (see github.com/DOliberto/DOliberto.")
    subparsers = parser.add_subparsers(title="subcommands",
                                       help="sub-command help")
    
    # test
    description_help = "parses publication templates in the appropriate format and outputs their AST."
    parser_tt = subparsers.add_parser("test-template",
                                      description=description_help,
                                      help=description_help, aliases=["tt"])
    parser_tt.add_argument("filepaths", nargs="+", type=str,
                           help="paths to template file.")
    parser_tt.set_defaults(func=lambda x: print(parse_files(x.filepaths)))

    # compile
    description_help = "parses publication templates in the appropriate format and compiles them to WTForms."
    parser_tt = subparsers.add_parser("compile-form",
                                      description=description_help,
                                      help=description_help, aliases=["cf"])
    parser_tt.add_argument("filepaths", nargs="+", type=str,
                           help="paths to template file.")
    parser_tt.set_defaults(func=lambda x: print(compile_forms(x.filepaths)))

    # parse args
    args = parser.parse_args()
    args.func(args)
