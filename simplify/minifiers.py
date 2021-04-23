from python_minifier import minify as _py_minify
from css_html_js_minify import css_minify as _css_minify
from .rjsmin import jsmin as _js_minify
from htmlmin import minify as _html_minify
import json
from xmlformatter import Formatter as _XmlFormatter
import mimetypes

mimetypes.add_type("text/python", ".py")
mimetypes.add_type("text/python", ".pyw")

_xml_minify = _XmlFormatter(compress=True, selfclose=True)


def json_minify(data: str):
    data = json.loads(data)
    data = json.dumps(data, separators=(',', ":"))
    return data


def xml_minify(data: str):
    data = _xml_minify.format_string(data)
    return data.decode()


def html_minify(data: str):
    data = _html_minify(data)
    return data


def js_minify(data: str):
    data = _js_minify(data)
    return data


def css_minify(data: str):
    data = _css_minify(data)
    return data


def py_minify(data: str):
    data = _py_minify(data, rename_locals=False, convert_posargs_to_args=False)
    return data


def no_minify(data: str):
    return data


def get_minifier(filename: str):
    extension = mimetypes.guess_extension(mimetypes.guess_type(filename)[0])[1:]
    if extension == "html":
        return html_minify
    elif extension == "py":
        return py_minify
    elif extension == "js":
        return js_minify
    elif extension == "json":
        return json_minify
    elif extension == "xml":
        return xml_minify
    elif extension == "css":
        return no_minify
