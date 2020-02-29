#You can import and rename things to work with them internally,
# without exposing them publicly or to avoid naming conflicts!
from contextlib import contextmanager
from pathlib import Path

from atomicwrites import atomic_write as _backend_writer, AtomicWriter

# You probably need to inspect and override some internals of the package


class SuffixWriter(AtomicWriter):
    def __init__(self, path, mode='w', overwrite=False,
                 **open_kwargs):
        self._path = path
        # self._open_kwargs = open_kwargs
        # self._path = path
        # self._mode = mode
        # self._overwrite = overwrite
        super().__init__(path, mode, overwrite, **open_kwargs)

    def get_fileobject(self, dir=None, **kwargs):
        def __enter__(gf_self):
            return gf_self

        temp_suffix = ''.join(Path(self._path).suffixes)
        super().get_fileobject(suffix=temp_suffix, **kwargs)



# Override functions like this


@contextmanager
def atomic_write(file, mode='w', as_file=True, new_default='asdf', **kwargs):
    try:
        # You can override things just fine...
        with _backend_writer(file, writer_cls=AtomicWriter, **kwargs) as f:
            # Don't forget to handle the as_file logic!
            if not as_file:
                yield f.name
            else:
                yield f

    except (OSError, IOError):
        # remove_temp_file(temp_file)
        raise

    finally:
        # remove_temp_file(temp_file)
        pass


