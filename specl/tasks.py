"""Luigi task for running specl"""

from luigi import LocalTarget, Task, Parameter, ExternalTask, build

from specl import execute as specl_execute
from specl import write_data as specl_write


class SpeclSpec(ExternalTask):
    # where the spec lives on disk
    spec = Parameter(default='samples/specs/sample_spec.yml')

    def output(self):
        return LocalTarget(self.spec)


class SpeclData(ExternalTask):
    # where the data lives on disk
    data = Parameter(default='samples/data/sample1.csv')

    def output(self):
        return LocalTarget(self.data)


class CleanData(Task):

    spec = Parameter(default='samples/specs/sample_spec.yml')
    data = Parameter(default='samples/data/sample1.csv')

    def requires(self):
        return {'spec': SpeclSpec(self.spec),
                'data': SpeclData(self.data)
                }

    def output(self):
        return LocalTarget('samples/output/out.csv')

    def run(self):
        with self.input()['spec'].open() as s:
            spec, df = specl_execute(s.name)
            specl_write(spec, df)


if __name__ == "__main__":
    """
    Run CleanData task.
    """
    build([
        CleanData(
            spec='samples/specs/sample_spec.yml',
            data='samples/data/sample1.csv'
        )], local_scheduler=True)
