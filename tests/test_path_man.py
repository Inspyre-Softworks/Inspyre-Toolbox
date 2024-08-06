from pathlib import Path

import pytest

from inspyre_toolbox.path_man import check_path


@pytest.mark.parametrize(
        "path, do_not_expand, do_not_resolve, do_not_convert, do_not_provision, expected, test_id",
        [
                # Happy path tests
                (Path("/valid/path"), False, False, False, False, True, "valid_path"),
                ("/valid/path", False, False, False, False, True, "valid_path_str"),
                (Path("/valid/path"), True, True, True, True, True, "valid_path_no_provision"),

                # Edge cases
                (Path("/non/existent/path"), False, False, False, False, False, "non_existent_path"),
                ("/non/existent/path", False, False, False, False, False, "non_existent_path_str"),
                (Path("/valid/path"), True, True, True, False, True, "valid_path_no_expand_resolve_convert"),

                # Error cases
                (123, False, False, False, False, False, "invalid_path_type_int"),
                (None, False, False, False, False, False, "invalid_path_type_none"),
                (Path("/valid/path"), "invalid", False, False, False, False, "invalid_do_not_expand_type"),
                ],
        ids=lambda x: x[-1]
        )
def test_check_path(path, do_not_expand, do_not_resolve, do_not_convert, do_not_provision, expected, test_id):
    # Act
    result = check_path(path, do_not_expand, do_not_resolve, do_not_convert, do_not_provision)

    # Assert
    assert result == expected
