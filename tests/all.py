#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from unittest.runner import TextTestRunner

from tests.fromJsonToHdl_test import FromJsonToHdlTC


def main_test_suite():
    tcs = [
        FromJsonToHdlTC,
    ]
    loader = unittest.TestLoader()
    loadedTcs = [loader.loadTestsFromTestCase(tc) for tc in tcs]
    suite = unittest.TestSuite(loadedTcs)

    return suite


suite = main_test_suite()

if __name__ == "__main__":
    runner = TextTestRunner(verbosity=3)
    runner.run(suite)
