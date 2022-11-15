from docx_form import DocxForm

def test_set_options():
    # Initialize docx-form instance
    path = "C:/Users/rherb/OneDrive/Desktop/test.docx"
    test = DocxForm(path)
    
    # Set element to a control with options
    element = test.content_control_forms_and_form_fields[8]

    # Display options
    element.print_options()
    print(element.text)

    # Select option and change text
    element.set_option(1)
    print(element.text)

    # Check for changes
    assert element.text == ""
