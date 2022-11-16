# docx-form

![API Documentation Status](https://github.com/Southeastern-Louisiana-University/docx-form/actions/workflows/publish_api_documentation.yml/badge.svg) ![PyPi Deployment Status](https://github.com/Southeastern-Louisiana-University/docx-form/actions/workflows/deploy.yml/badge.svg) ![Unit Test Status](https://github.com/Southeastern-Louisiana-University/docx-form/actions/workflows/run_unit_tests.yml/badge.svg)

### [API Documentation](https://southeastern-louisiana-university.github.io/docx-form/ 'API Documentation') | [PyPi Page](https://pypi.org/project/docx-form/ 'PyPi Page')

### Description

This package allows you to easily modify the values of content controls & form fields in `.docx` files with Python.

### Supported Content Controls

- [x] Plain Text
- [x] Rich Text
- [x] Drop Down List
- [x] Combo Box
- [x] Date Picker
- [x] Check Box

### Supported Form Fields (To-Do)

- [ ] Text
- [ ] Drop Down
- [ ] Check Box

## Installation

1. Install [Python](https://www.python.org/downloads/ 'Python') (**minimum version: 3.10.6**)
   1. **Warning: Python 3.11 breaks some dependencies as of 10/28/2022. This warning will be removed when this is no longer the case.**
2. In a terminal, run: `pip install docx-form`

## Usage

The file `./docx_form_tests/test.docx` wil be used for the following guide.

1. Create a new python file `example.py`
2. Import docx-form:

```python
from docx_form import DocxForm
```

3. Initialize a `DocxForm` instance:

```python
...
full_path = 'path/to/docx/file/test.docx'
document = DocxForm(full_path)
```

4. Print the content controls:

```python
...
document.print_all_content_controls_and_form_fields()
```

5. View the console output & make note of the indexes:

```
0: RichTextContentControl | id: -1012910137 | text: Rich Text Content Control
1: RichTextContentControl | id: -1135860421 | text: Another Rich Text Content Control
2: PlainTextContentControl | id: -132710284 | text: Plain Text Content Control
3: PlainTextContentControl | id: 28152470 | text: Another Plain Text Content Control
4: CheckBoxContentControl | id: -1942055255 | text: ☐
5: CheckBoxContentControl | id: -635946620 | text: ☒
6: ComboBoxContentControl | id: 199831773 | text: Combo t Option 1
7: ComboBoxContentControl | id: -1984237200 | text: Choose an item.
8: DropDownListContentControl | id: -827207619 | text: Drop-Down Content Control
9: DropDownListContentControl | id: 2026666311 | text: Another Drop-Down Content Control
10: DatePickerContentControl | id: 645172330 | text: 9/6/2022
11: DatePickerContentControl | id: 539787165 | text: 9/7/2022
```

**Note: The Content Controls are listed starting from the top-left of the document going from left to right on each line of the document all the way to the bottom.**

6. Edit the second Rich Text Content Control:

```python
...
# Import type for proper intellisense in your editor/IDE
from docx_form.content_controls import RichTextContentControl
...
rich_text_control: RichTextContentControl = document.content_control_forms_and_form_fields[1]
rich_text_control.set_text("The example worked!")
```

7. Save the file:

```python
...
# Note: This will overwrite the original file
document.save()
```

8. If `document.list_all_content_controls_and_form_fields()` is run again:

```
...
1: RichTextContentControl | id: -1135860421 | text: The example worked!
...
```

9. Full File:

```python
from docx_form import DocxForm
from docx_form.content_controls import RichTextContentControl

# Create a DocxForm instance
full_path = "path/to/docx/file/test.docx"
document = DocxForm(full_path)

# Kept for reference
# document.list_all_content_controls_and_form_fields()

# Edit the second Rich Text content control
rich_text_control: RichTextContentControl = (
    document.content_control_forms_and_form_fields[1]
)
rich_text_control.set_text("The example worked!")

# Note: This will overwrite the original file
document.save()
```

## Examples

The file `./docx_form_tests/test.docx` wil be used for the following examples.

### Plain Text

```python
from docx_form import DocxForm
from docx_form.content_controls import PlainTextContentControl

# Create a DocxForm instance
full_path = "path/to/docx/file/test.docx"
document = DocxForm(full_path)

# Kept for reference
# document.list_all_content_controls_and_form_fields()

# Edit the content control (remember the console output)
content_control: PlainTextContentControl = (
    document.content_control_forms_and_form_fields[2]
)
content_control.set_text("Plain text edit")

# Note: This will overwrite the original file
document.save()
```

### Check Box

```python
from docx_form import DocxForm
from docx_form.content_controls import CheckBoxContentControl

# Create a DocxForm instance
full_path = "path/to/docx/file/test.docx"
document = DocxForm(full_path)

# Kept for reference
# document.list_all_content_controls_and_form_fields()

# Edit the content control (remember the console output)
content_control: CheckBoxContentControl = (
    document.content_control_forms_and_form_fields[4]
)
content_control.set_check_box(True)

# Note: This will overwrite the original file
document.save()
```

### Combo Box

```python
from docx_form import DocxForm
from docx_form.content_controls import ComboBoxContentControl

# Create a DocxForm instance
full_path = "path/to/docx/file/test.docx"
document = DocxForm(full_path)

# Kept for reference
# document.list_all_content_controls_and_form_fields()

# Edit the content control (remember the console output)
content_control: ComboBoxContentControl = (
    document.content_control_forms_and_form_fields[6]
)
content_control.print_options()
"""
Output:
0: Display Value = "None" || Value = "Choose an item."
1: Display Value = "Combo Box Option 1" || Value = "Combo Box Option 1"
2: Display Value = "Combo Box Option 2" || Value = "Combo Box Option 2"
"""
content_control.set_text(2)

# Note: This will overwrite the original file
document.save()
```

### Drop Down List

```python
from docx_form import DocxForm
from docx_form.content_controls import DropDownListContentControl

# Create a DocxForm instance
full_path = "path/to/docx/file/test.docx"
document = DocxForm(full_path)

# Kept for reference
# document.list_all_content_controls_and_form_fields()

# Edit the content control (remember the console output)
content_control: DropDownListContentControl = (
    document.content_control_forms_and_form_fields[8]
)
content_control.print_options()
"""
Output:
0: Display Value = "None" || Value = "Choose an item."
1: Display Value = "Drop-Down Content Control" || Value = "Drop-Down Content Control"
"""
content_control.set_option(0)

# Note: This will overwrite the original file
document.save()
```

### Date Picker

```python
from datetime import datetime
from docx_form import DocxForm
from docx_form.content_controls import DatePickerContentControl

# Create a DocxForm instance
full_path = "path/to/docx/file/test.docx"
document = DocxForm(full_path)

# Kept for reference
# document.list_all_content_controls_and_form_fields()

# Edit the content control (remember the console output)
content_control: DatePickerContentControl = (
    document.content_control_forms_and_form_fields[10]
)
print(content_control.date_format) # Output: "M/d/yyyy"
new_date = datetime(1999, 12, 31)
content_control.set_date(new_date)

# Note: This will overwrite the original file
document.save()
```

## Setup For Contribution

### Requirements:

- [Python](https://www.python.org/downloads/ 'Python') (**minimum version: 3.10.6**)
  - **Warning: Python 3.11 breaks some dependencies as of 10/28/2022. This warning will be removed when this is no longer the case.**
- [Poetry](https://python-poetry.org/docs/)
  - **DO NOT** forget to add Poetry to your `PATH` (step 3)

#### Environment Setup

The following will be done in Visual Studio Code on a Windows machine:

1. Open a terminal in the repository's root
2. Run `poetry install`
3. Run `poetry env info`
   1. Copy the path listed under `Virtualenv > Executable:`
4. Change the Python interpreter to the newly created Poetry virtual environment:
   1. `CTRL + SHIFT + P` to open the command menu
   2. Type `interpreter` and hit `ENTER`
   3. Select `+ Enter interpreter path...`
   4. Paste the path to the virtual environment
   5. Hit `ENTER`
5. Open `./docx_form/docx_form.py` (This is the root file, so do any local testing within the `if __name__ == "__main__":` scope)
6. Click the `Run` button in the top-right of the editor (assuming the [Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) is installed)
   1. If no errors are thrown, you are ready to execute locally and using poetry!
7. Open a `Git Bash` terminal in the repository's root
   1. Run `curl -o- https://raw.githubusercontent.com/tapsellorg/conventional-commits-git-hook/master/scripts/install.sh | sh`
      1. Here is the repository for the git hook: [conventional-commits-git-hook](https://github.com/BrianGilbert/conventional-commits-git-hook)
   2. Run `git init`
   3. You now have the git hook installed to ensure proper commit messages
      1. Follow [these guidelines](https://www.conventionalcommits.org/en/v1.0.0/) for commit messages

#### Code Style Guide

1. Do your best to follow [PEP8 Guidelines](https://pep8.org/ 'PEP8 Guidelines')
2. **ALL** code must have [Type Hints](https://peps.python.org/pep-0484/ 'Type Hints')
   1. If a variable, parameter, or function return has a type of `Any`, it **WILL NOT** be accepted
