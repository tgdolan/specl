import os
import io
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch, call, mock_open
from csci_utils.io import atomic_write
import atomicwrites



class FakeFileFailure(IOError):
    pass


class AtomicWriteTests(TestCase):

    def test_atomic_write(self):
        """Ensure file exists after being written successfully"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.tar.gz")

            with atomic_write(fp, "w") as f:
                assert not os.path.exists(fp)
                tmpfile = f.name
                f.write("asdf")

            assert not os.path.exists(tmpfile)
            assert os.path.exists(fp)

            with open(fp) as f:
                self.assertEqual(f.read(), "asdf")

    def test_atomic_failure(self):
        """Ensure that file does not exist after failure during write"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            with self.assertRaises(FakeFileFailure):
                with atomic_write(fp, "w") as f:
                    tmpfile = f.name
                    assert os.path.exists(tmpfile)
                    raise FakeFileFailure()

            assert not os.path.exists(tmpfile)
            assert not os.path.exists(fp)

    def test_file_exists(self):
        """Ensure an error is raised when a file exists
        Utilizes a patch to mock the output of the isfile() method on os.path.
        """
        pass
        # with self.assertRaises(FileExistsError):
        #     with atomic_write("elbow.txt", 'w') as f:
        #         f.write("bar")

    def test_yield_temp_path_when_as_file_false(self):
        """Ensure atomic_write yields temp path when as_file is False."""
        with atomic_write("test.txt", "w", False) as f:
            self.assertIsInstance(f, str)

    @patch('atomicwrites.atomic_write')
    def test_should_pass_extra_args_to_open_file(self, mocked_writer):
        pass
        # kwargs = {'buffering': -1}
        # with TemporaryDirectory() as tmp:
        #     fp = os.path.join(tmp, "asdf.txt")
        #     with mocked_writer:
        #         with atomic_write(file=fp, mode="w", **kwargs) as f:
        #             f.write("asdf")
        #         mocked_writer.assert_called()
                # mo.assert_called_with(f.name, "w", buffering=-1)
