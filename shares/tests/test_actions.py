import contextlib
from pathlib import Path
from unittest import mock

from django.test import TestCase

from shares import actions
from shares.exceptions import InvalidRequestPathException


def _create_test_scandir_result(is_file, name):
    mock_result = mock.MagicMock()
    mock_result.is_file.return_value = is_file
    mock_result.is_dir.return_value = not is_file
    mock_result.name = name
    return mock_result


class TestGetDirectoriesAndFiles(TestCase):

    def test_redirects_on_invalid_path(self):
        with self.settings(FL_FILES_PATH=Path(__file__).resolve().parent.parent):
            with self.assertRaises(InvalidRequestPathException):
                actions.get_directories_and_files(Path("/"))

            with self.assertRaises(InvalidRequestPathException):
                actions.get_directories_and_files(Path("../"))

            with self.assertRaises(InvalidRequestPathException):
                actions.get_directories_and_files(Path("../../../"))

    @mock.patch("os.scandir")
    def test_returns_sorted_directories_and_files(self, mock_scandir):
        mock_scandir.return_value = contextlib.nullcontext([
            _create_test_scandir_result(True, "file1"),
            _create_test_scandir_result(False, "dir2"),
            _create_test_scandir_result(True, "file3"),
            _create_test_scandir_result(True, "file2"),
            _create_test_scandir_result(False, "dir1"),
            _create_test_scandir_result(False, "dir3"),
        ])

        (directories, files, _) = actions.get_directories_and_files(Path("."))

        self.assertListEqual(directories, [
            dict(name="dir1/", path=Path("dir1")),
            dict(name="dir2/", path=Path("dir2")),
            dict(name="dir3/", path=Path("dir3")),
        ])
        self.assertListEqual(files, [
            dict(name="file1", path=Path("file1")),
            dict(name="file2", path=Path("file2")),
            dict(name="file3", path=Path("file3")),
        ])

    @mock.patch("os.scandir")
    def test_returns_paths_for_nested_directories(self, mock_scandir):
        mock_scandir.return_value = contextlib.nullcontext([
            _create_test_scandir_result(True, "file1"),
            _create_test_scandir_result(False, "dir2"),
            _create_test_scandir_result(True, "file3"),
            _create_test_scandir_result(True, "file2"),
            _create_test_scandir_result(False, "dir1"),
            _create_test_scandir_result(False, "dir3"),
        ])

        requested_path = Path("path")
        (directories, files, _) = actions.get_directories_and_files(requested_path)

        self.assertListEqual(directories, [
            dict(name="dir1/", path=requested_path / "dir1"),
            dict(name="dir2/", path=requested_path / "dir2"),
            dict(name="dir3/", path=requested_path / "dir3"),
        ])
        self.assertListEqual(files, [
            dict(name="file1", path=requested_path / "file1"),
            dict(name="file2", path=requested_path / "file2"),
            dict(name="file3", path=requested_path / "file3"),
        ])

    @mock.patch("os.scandir")
    def test_no_parent_path_for_main_path(self, mock_scandir):
        mock_scandir.return_value = contextlib.nullcontext([])

        requested_path = Path(".")
        (_, _, parent_path) = actions.get_directories_and_files(requested_path)
        self.assertIsNone(parent_path)

    @mock.patch("os.scandir")
    def test_parent_path_returned(self, mock_scandir):
        mock_scandir.return_value = contextlib.nullcontext([])

        requested_path = Path("child")
        (_, _, parent_path) = actions.get_directories_and_files(requested_path)
        self.assertEqual(parent_path, Path("."))

        requested_path = Path("child1/child2")
        (_, _, parent_path) = actions.get_directories_and_files(requested_path)
        self.assertEqual(parent_path, Path("child1"))
