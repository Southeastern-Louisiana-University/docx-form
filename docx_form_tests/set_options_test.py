from docx_form import DocxForm

def test_set_options():
    # Initialize docx-form instance
    path = "./docx_form_tests/test.docx"
    test = DocxForm(path)
    
    # Set element to a control with options
    element = test.content_control_forms_and_form_fields[8]

    # Display options
    element.print_options()

    # Select option and change text
    element.set_option(2)

    # Check for changes
    compare = "Optional-Test"
    assert element.text == compare
