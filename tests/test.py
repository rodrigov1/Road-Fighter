# # tests/test_my_class.py
#
# import pytest
# from unittest.mock import Mock
# from src.my_class import MyClass, Dependency
#
# def test_my_class_execute():
#     # Create a mock dependency
#     mock_dependency = Mock(spec=Dependency)
#     # Define the return value for the mock's perform_action method
#     mock_dependency.perform_action.return_value = "Mocked action"
#
#     # Create an instance of MyClass with the mock dependency
#     my_class_instance = MyClass(mock_dependency)
#
#     # Execute the method
#     result = my_class_instance.execute()
#
#     # Assert that the result is as expected
#     assert result == "Result: Mocked action"
#
#     # Assert that the perform_action method was called once
#     mock_dependency.perform_action.assert_called_once()
