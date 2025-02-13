#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Read all the test files.
"""

import os
import tempfile
import unittest

import libsbgnpy.libsbgn as libsbgn


##############################################
# Test files
##############################################
current_dir = os.path.dirname(os.path.realpath(__file__))
testfile_dir = os.path.join(current_dir, "test-files")


def find_sbgn_files(directory):
    sbgn_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".sbgn"):
                f = os.path.join(root, file)
                sbgn_files.append(f)
    return sbgn_files


sbgn_files = find_sbgn_files(directory=testfile_dir)
##############################################


class TestSBGNFile(unittest.TestCase):
    """
    Dummy test class. Test methods are attached.
    """

    pass


def create_method(f):
    """Test function generator.

    :param f:
    :return:
    """

    def f_expected(self):
        print("*" * 80)
        print(f)
        print("*" * 80)
        sbgn = libsbgn.parse(f)
        self.assertTrue(sbgn is not None)

        # write everything to tempfile
        f_tmp = tempfile.NamedTemporaryFile(suffix=".sbgn")
        sbgn.write_file(f_tmp.name)

    return f_expected


# Add test functions for files
for k, f in enumerate(sbgn_files):
    test_method = create_method(f)
    test_method.__name__ = "test_%s" % k
    setattr(TestSBGNFile, test_method.__name__, test_method)
    del test_method

if __name__ == "__main__":
    unittest.main()
