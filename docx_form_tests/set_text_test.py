from docx_form import DocxForm

def test_set_text():
    # initialize docx-form instance
    path = "./docx_form_tests/test.docx"
    test = DocxForm(path)
    element = test.content_control_forms_and_form_fields[3]
    new_text = "That New New Plain text"
    element.set_text(new_text)
    assert element.text == new_text
