import luigi
import os.path
from luigi.mock import MockTarget
from specl.tasks import CleanData

mock_spec_target = MockTarget("spec", mirror_on_stderr=False)
mock_output_target = MockTarget("output", mirror_on_stderr=False)


class MockCleanData(CleanData):
    def requires(self):
        return mock_spec_target

    def output(self):
        return mock_output_target


def test_that_clean_data_task_runs():
    """ This is really more like an integration test, but wanted to get at least
        something in place to test CleanData Luigi task.
    """
    luigi.build([
        CleanData(
            spec='../samples/specs/sample_spec.yml',
            data='../samples/data/sample1.csv'
        )], local_scheduler=True)
    assert os.path.exists('../samples/output/out.csv')
