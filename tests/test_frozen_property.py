import pytest
from inspyre_toolbox.syntactic_sweets.classes.decorators.freeze import freeze_property

class TestClass:
    def __init__(self):
        self._value = None

    @freeze_property
    def value(self, val):
        self._value = val

    @property
    def value(self):
        return self._value

@pytest.fixture
def test_instance():
    return TestClass()

@pytest.mark.parametrize(
    "initial_value, new_value",
    [
        (10, 20),
        ("initial", "new"),
        (None, "new"),
    ],
    ids=["int_values", "string_values", "none_to_string"]
)
def test_freeze_property_happy_path(test_instance, initial_value, new_value):
    # Act
    test_instance.value = initial_value

    # Assert
    assert test_instance.value == initial_value

    # Act & Assert
    with pytest.raises(AttributeError):
        test_instance.value = new_value

@pytest.mark.parametrize(
    "initial_value, new_value",
    [
        (10, 10),
        ("same", "same"),
        (None, None),
    ],
    ids=["int_same_values", "string_same_values", "none_same_values"]
)
def test_freeze_property_same_value(test_instance, initial_value, new_value):
    # Act
    test_instance.value = initial_value

    # Assert
    assert test_instance.value == initial_value

    # Act & Assert
    with pytest.raises(AttributeError):
        test_instance.value = new_value

@pytest.mark.parametrize(
    "initial_value, new_value",
    [
        (10, 20),
        ("initial", "new"),
        (None, "new"),
    ],
    ids=["int_values", "string_values", "none_to_string"]
)
def test_freeze_property_error_cases(test_instance, initial_value, new_value):
    # Act
    test_instance.value = initial_value

    # Assert
    assert test_instance.value == initial_value

    # Act & Assert
    with pytest.raises(AttributeError):
        test_instance.value = new_value

def test_freeze_property_get_without_instance():
    # Arrange
    class TestClassWithoutInstance:
        def __init__(self):
            self._value = None

        @freeze_property
        def value(self, val):
            self._value = val

        @property
        def value(self):
            return self._value

    # Act
    instance = TestClassWithoutInstance()
    # Accessing the value property to check if it has been set up correctly
    prop = instance.value

    # Assert
    assert isinstance(prop, freeze_property)  # Ensure that prop is a property descriptor

    # Optional: Test setting and getting the value
    instance.value = 42
    assert instance.value == 42
