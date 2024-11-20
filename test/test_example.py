import pytest

def test_equal_or_not():
    assert 3==3
    assert 3!=1

def test_is_instance():
    assert isinstance('this is a string', str)
    assert not isinstance('10', int)


class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.year = years


# def test_person_initialisation():
#     # Arrange: create a student instance
#     first_name = "John"
#     last_name = "Doe"
#     major = "Computer Science"
#     years = 3
#
#     # Act: initialize the Student
#     student = Student(first_name, last_name, major, years)
#
#     # Assert: check that each attribute was set correctly
#     assert student.first_name == first_name
#     assert student.last_name == last_name
#     assert student.major == major
#     assert student.year == years


# Define the pytest fixture
@pytest.fixture
def student():
    # Arrange: create a student instance
    first_name = "John"
    last_name = "Doe"
    major = "Computer Science"
    years = 3

    # Return the student instance to be used in tests
    return Student(first_name, last_name, major, years)


# Test function that uses the fixture
def test_person_initialisation(student):
    # Assert: check that each attribute was set correctly
    assert student.first_name == "John"
    assert student.last_name == "Doe"
    assert student.major == "Computer Science"
    assert student.year == 3