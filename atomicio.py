# You can import and rename things to work with them internally,
# without exposing them publicly or to avoid naming conflicts!
from contextlib import contextmanager
from pathlib import Path
import os
import tempfile
import io

from atomicwrites import atomic_write as _backend_writer, AtomicWriter


# You probably need to inspect and override some internals of the package


class SuffixWriter(AtomicWriter):
    def __init__(self, path, mode='w', overwrite=False,
                 **open_kwargs):
        self._path = path
        super().__init__(path, mode, overwrite, **open_kwargs)

    def get_fileobject(self, mydir=None, **kwargs):
        # def __enter__(self):
        #     return self

        temp_suffix = ''.join(Path(self._path).suffixes)
        # super().get_fileobject(suffix=temp_suffix, **kwargs)
        '''Return the temporary file to use.'''
        prefix = 'tmp'
        if mydir is None:
            mydir = os.path.normpath(os.path.dirname(self._path))
        descriptor, name = tempfile.mkstemp(suffix=temp_suffix, prefix=prefix,
                                            dir=mydir)

        # io.open() will take either the descriptor or the name, but we need
        # the name later for commit()/replace_atomic() and couldn't find a way
        # to get the filename from the descriptor.
        os.close(descriptor)
        kwargs['mode'] = self._mode
        kwargs['file'] = name
        return io.open(**kwargs)


# Override functions like this

@contextmanager
def atomic_write(file, mode='w', as_file=True, new_default='asdf', **kwargs):
    # You can override things just fine...
    with _backend_writer(file, writer_cls=SuffixWriter, **kwargs) as f:
        try:
            # Don't forget to handle the as_file logic!
            if not as_file:
                yield f.name
            else:
                yield f

        except (OSError, IOError):
            remove_temp_file(f.name)
            raise

        finally:
            pass
            # print("in atomic_write_finally")
            # remove_temp_file(file)


def remove_temp_file(file_path):
    """ Removes the file designated by the 'file_path' param if it exists.
    :param file_path: The file system path to the file to be removed.
    """
    if os.path.exists(file_path):
        os.remove(file_path)


if __name__ == '__main__':
    kwargs = {'buffering': -1}
    with atomic_write("bar.tar.gz", "w", **kwargs) as f:
        assert not os.path.exists("bar.tar.gz")
        tmpfile = f.name
        f.write("asdf")
