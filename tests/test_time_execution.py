import unittest
from time_execution import time_execution


class TestRaiseForMaintenance(unittest.TestCase):
    def test_time_execution_call_executes_normally(self):
        class Mock:
            def __init__(self):
                self.func_has_been_called = False

            @time_execution('Mock')
            def func(self):
                self.func_has_been_called = True

        mock = Mock()
        mock.func()

        self.assertEqual('tests.test_time_execution.Mock.func', Mock.func.__fqn__)
        self.assertTrue(mock.func_has_been_called)
