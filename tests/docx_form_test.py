from docx_form import __version__, DocxForm


def test_version():
    assert __version__ == "0.1.0"


def test_docx_form():
    docx_form = DocxForm("path")
    assert docx_form.path == "path"
