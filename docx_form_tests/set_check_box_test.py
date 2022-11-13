from docx_form import DocxForm


def test_set_check_box():
    # initialize docx-form instance
    path = "./docx_form_tests/test.docx"
    test = DocxForm(path)

    # Set element to an unchecked check box
    element = test.content_control_forms_and_form_fields[4]

    # Store the original state of the check box
    original_state = element.text

    # Change the check box
    element.set_check_box(True)

    # Store the new state of the check box
    new_state = element.text

    # Check For Change
    assert original_state == "☐"
    assert new_state == "☒"
