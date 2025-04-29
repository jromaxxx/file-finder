import unittest
import os
import tempfile
import pandas as pd
from pathlib import Path
from finder.scanner import compute_hash, scan_directory, find_duplicates, find_large_files


class TestScanner(unittest.TestCase):
    def setUp(self):
        """Set up a temporary directory with test files."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_path = Path(self.test_dir.name)

        # Create test files
        self.file1 = self.test_path / "file1.txt"
        self.file2 = self.test_path / "file2.txt"
        self.file3 = self.test_path / "file3.txt"
        self.duplicate_file = self.test_path / "duplicate.txt"

        self.file1.write_text("This is file 1.")
        self.file2.write_text("This is file 2.")
        self.file3.write_text("This is file 3.")
        self.duplicate_file.write_text("This is file 1.")  # Duplicate content of file1

    def tearDown(self):
        """Clean up the temporary directory."""
        self.test_dir.cleanup()

    def test_compute_hash(self):
        """Test the compute_hash function."""
        hash1 = compute_hash(self.file1)
        hash_duplicate = compute_hash(self.duplicate_file)
        hash2 = compute_hash(self.file2)

        self.assertIsNotNone(hash1)
        self.assertIsNotNone(hash2)
        self.assertEqual(hash1, hash_duplicate)  # Duplicate files should have the same hash
        self.assertNotEqual(hash1, hash2)  # Different files should have different hashes

    def test_scan_directory(self):
        """Test the scan_directory function."""
        df = scan_directory(self.test_path)
        self.assertEqual(len(df), 4)  # Ensure all 4 files are scanned
        self.assertIn("path", df.columns)
        self.assertIn("size", df.columns)
        self.assertIn("name", df.columns)
        self.assertIn("hash", df.columns)

    def test_find_duplicates(self):
        """Test the find_duplicates function."""
        df = scan_directory(self.test_path)
        duplicates = find_duplicates(df)
        self.assertEqual(len(duplicates), 2)  # file1 and duplicate.txt should be duplicates
        self.assertTrue((duplicates["name"] == "file1.txt").any())
        self.assertTrue((duplicates["name"] == "duplicate.txt").any())

    def test_find_large_files(self):
        """Test the find_large_files function."""
        df = scan_directory(self.test_path)
        large_files = find_large_files(df, top_n=2)

        # Verify the number of files returned
        self.assertEqual(len(large_files), 2)

        # Verify the file names based on their sizes
        # Sort the DataFrame by size to determine the expected order
        sorted_df = df.sort_values(by="size", ascending=False).head(2)
        expected_files = sorted_df["name"].tolist()
        actual_files = large_files["name"].tolist()

        self.assertListEqual(expected_files, actual_files)


if __name__ == "__main__":
    unittest.main()