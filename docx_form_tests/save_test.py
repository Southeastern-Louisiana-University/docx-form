from docx_form import DocxForm
from zipfile import ZipFile


def test_save():
    # initialize docx-form instance
    path = "./docx_form_tests/test.docx"
    test = DocxForm(path)
    with ZipFile(test.file_path) as document:
        old_contents = document.read("word/document.xml")
    test.list_all_content_controls_and_form_fields()
    element = test.content_control_forms_and_form_fields[2]
    element.set_text("Hello World")
    test_changes = test.save("./docx_form_tests/test-m.docx")
    with ZipFile("./docx_form_tests/test-m.docx") as compare:
        new_contents = compare.read("word/document.xml")

    assert (new_contents != old_contents)
