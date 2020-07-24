import unittest


def get_all_testcases(test_file):
    suite = unittest.defaultTestLoader.discover(test_file, pattern='*test')
    return suite


def get_testcases_from_module(test_module):
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_module)
    return suite


def get_testcases_from_class(testcase_class):
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(testcase_class)
    return suite


def get_suite(test_case):
    """
    :param test_case: 测试用例或测试用例列表
    :return: 测试用例集
    """
    suite = unittest.TestSuite()
    for case in test_case:
        suite.addTest(case)
    return suite
