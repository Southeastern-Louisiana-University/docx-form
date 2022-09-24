from docx_form import DocxForm


def test_docx_form():
    path: str = "./docx_form_tests/test.docx"  # Note: Poetry executes tests from the root directory, so account for this with file paths
    docx_form = DocxForm(path)
    assert docx_form.file_path == path
    assert len(docx_form.content_control_forms) == 12
