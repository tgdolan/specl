"""Luigi task for running specl"""

from luigi import LocalTarget, Task, Parameter, ExternalTask, build

from . import specl

class SpeclSpec(ExternalTask):
    # where the spec lives on disk
    spec = Parameter(default='./samples/specs/sample_spec.yml')

    def output(self):
        return LocalTarget(self.spec)

class SpeclData(ExternalTask):
    # where the data lives on disk
    data = Parameter(default='./samples/data/sample1.csv')

    def output(self):
        return LocalTarget(self.data)


class CleanData(Task):

    spec = Parameter(default='./samples/specs/sample_spec.yml')
    data = Parameter(default='./samples/data/sample1.csv')

    def requires(self):
        return {'spec': SpeclSpec(self.spec),
                'data': SpeclData(self.data)
                }

    def output(self):
        return LocalTarget('./samples/output/out.csv')

    def run(self):
        with self.input()['spec'].open() as s:
            print("running luigi")
            spec, df = specl.execute(s.name)
            specl.write_data(spec, df)

class SpeclTask(Task):

    def requires(self):
        return CleanData();



if __name__ == "__main__":
    """
    Run SpeclTask task.
    """
    build([
        SpeclTask()
    ], local_scheduler=True)
