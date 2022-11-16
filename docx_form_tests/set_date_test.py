from docx_form import DocxForm, content_controls
from datetime import datetime


def test_set_date():
    """
    Test the set_date method of the DatePickerContentControl class.
    """

    # initialize docx-form instance
    path = "./docx_form_tests/test.docx"
    test = DocxForm(path)

    # Set element to a date picker
    element: content_controls.DatePickerContentControl = (
        test.content_control_forms_and_form_fields[10]
    )

    # Store the original state of the date picker
    original_date_formatted = element.text
    original_date_utc = element.full_date

    # Change the date picker to a new date
    new_date = datetime(2020, 1, 1)
    element.set_date(new_date)

    # Store the new state of the check box
    new_date_formatted = element.text
    new_date_utc = element.full_date

    # Check For Change
    assert new_date_formatted != original_date_formatted
    assert new_date_utc != original_date_utc
