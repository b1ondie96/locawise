import os
import shutil
import tempfile
from pathlib import Path

import pytest

from threepio.envutils import find_file_by_basename


class TestFindFileByBasename:

    @pytest.fixture
    def temp_directory(self):
        """Create a temporary directory structure for testing."""
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        try:
            # Create some files in the temp directory
            with open(os.path.join(temp_dir, "test1.txt"), "w") as f:
                f.write("test content")

            # Create a subdirectory
            subdir = os.path.join(temp_dir, "subdir")
            os.makedirs(subdir)

            # Create files in the subdirectory
            with open(os.path.join(subdir, "test2.pdf"), "w") as f:
                f.write("test content")

            with open(os.path.join(subdir, "test3.txt"), "w") as f:
                f.write("test content")

            # Create a deeper subdirectory
            deep_subdir = os.path.join(subdir, "deep")
            os.makedirs(deep_subdir)

            # Create a file in the deeper subdirectory
            with open(os.path.join(deep_subdir, "test4.jpg"), "w") as f:
                f.write("test content")

            # Create a file with the same basename but different extension
            with open(os.path.join(deep_subdir, "test1.pdf"), "w") as f:
                f.write("test content")

            yield temp_dir

        finally:
            # Clean up the temporary directory
            shutil.rmtree(temp_dir)

    def test_find_file_in_root_directory(self, temp_directory):
        """Test finding a file in the root directory."""
        result = find_file_by_basename("test1", temp_directory)
        assert result == os.path.join(temp_directory, "test1.txt")

    def test_find_file_in_subdirectory(self, temp_directory):
        """Test finding a file in a subdirectory."""
        result = find_file_by_basename("test2", temp_directory)
        assert result == os.path.join(temp_directory, "subdir", "test2.pdf")

    def test_find_file_in_deep_subdirectory(self, temp_directory):
        """Test finding a file in a deeper subdirectory."""
        result = find_file_by_basename("test4", temp_directory)
        assert result == os.path.join(temp_directory, "subdir", "deep", "test4.jpg")

    def test_multiple_files_with_same_basename(self, temp_directory):
        """Test that the function returns the first file found with the basename."""
        # This depends on os.walk order, which typically returns directories in lexicographic order
        # In our case, it should find test1.txt in the root directory first
        result = find_file_by_basename("test1", temp_directory)
        assert result == os.path.join(temp_directory, "test1.txt")

    def test_file_not_found(self, temp_directory):
        """Test behavior when the file is not found."""
        result = find_file_by_basename("nonexistent", temp_directory)
        assert result is None

    def test_empty_directory(self):
        """Test behavior with an empty directory."""
        with tempfile.TemporaryDirectory() as empty_dir:
            result = find_file_by_basename("test", empty_dir)
            assert result is None

    def test_case_sensitivity(self, temp_directory):
        """Test case sensitivity."""
        # This should not find "Test1.txt" because we created "test1.txt"
        result = find_file_by_basename("Test1", temp_directory)
        assert result is None

    def test_with_path_objects(self, temp_directory):
        """Test with Path objects instead of strings."""
        # Convert string paths to Path objects
        path_obj = Path(temp_directory)
        result = find_file_by_basename("test1", path_obj)
        assert result == os.path.join(temp_directory, "test1.txt")
