import ast
from pathlib import Path

from chepochem.metadata import MetadataFlags
from chepochem.python import PythonDocumentLoader


def test__generate_function_metadata__on_success__returns_correct_metadata():
    document_loader = PythonDocumentLoader(
        python_file=Path("sample.py"),
        metadata_flags=MetadataFlags(file_name=True, position=True, calls=True),
    )
    python_function = ast.parse(
        """
def sample_function():
    some_var = 1 + 1
    call_another_function()
    module.call()
    return
"""
    ).body[0]

    result = document_loader._generate_function_metadata(python_function).body[0]

    assert result == {
        "file_name": "sample.py",
        "line_number": 1,
        "calls": ["call_another_function", "module.call"],
    }
