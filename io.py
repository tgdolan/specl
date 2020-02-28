#You can import and rename things to work with them internally,
# without exposing them publicly or to avoid naming conflicts!
from contextlib import contextmanager

from atomicwrites import atomic_write as _backend_writer, AtomicWriter

# You probably need to inspect and override some internals of the package


class SuffixWriter(AtomicWriter):

    def get_fileobject(self, dir=None, **kwargs):
        pass


# Override functions like this


@contextmanager
def atomic_write(file='some_path', mode='w', as_file=True, new_default='asdf', **kwargs):

    # You can override things just fine...
    with _backend_writer(file, writer_cls=AtomicWriter, **kwargs) as f:
        # Don't forget to handle the as_file logic!
        yield f
