import unittest

import os
from influxdb.influxdb08.client import InfluxDBClientError
from time_execution import time_execution, configure
from time_execution.backends.influxdb import InfluxBackend


@time_execution
def fqn_test():
    pass


@time_execution
class Dummy(object):
    @time_execution
    def go(self):
        pass


class TestTimeExecution(unittest.TestCase):
    def setUp(self):
        super(TestTimeExecution, self).setUp()

        self.database = 'unittest'
        self.backend = InfluxBackend(
            host=os.environ.get('INFLUX_PORT_4444_UDP_ADDR', 'localhost'),
            database=self.database,
            use_udp=False
        )

        try:
            self.backend.client.create_database(self.database)
        except InfluxDBClientError:
            # Something blew up so ignore it
            pass

        configure(backends=[self.backend])

    def tearDown(self):
        self.backend.client.delete_database(self.database)

    def test_fqn(self):
        self.assertEqual(fqn_test.fqn, 'tests.test_time_execution.fqn_test')
        self.assertEqual(Dummy.fqn, 'tests.test_time_execution.Dummy')
        self.assertEqual(Dummy().go.fqn, 'tests.test_time_execution.Dummy.go')

    def test_time_execution(self):

        count = 4

        @time_execution
        def go():
            return True

        for i in range(count):
            go()

        query = 'select * from {}'.format(go.fqn)
        metrics = self.backend.client.query(query)
        self.assertEqual(len(metrics[0]['points']), count)

    def test_time_execution_hook(self):

        @time_execution
        def go():
            return True

        go()
