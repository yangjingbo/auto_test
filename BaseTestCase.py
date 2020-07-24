# -*- coding:utf-8 -*-
import unittest
from appium import webdriver
from moats.function import screenshot_for_report
from moats.desired_capabilities import get_desired_capabilities
import datetime
from moats.BasePage import Page
from moats import GlobalVar
DEVICES_NAME = GlobalVar.ENVIRONMENT['devices'][0]
APP_PACKAGE = GlobalVar.ENVIRONMENT['app_package']
APP_ACTIVITY = GlobalVar.ENVIRONMENT['app_activity']
ADB_PORT = GlobalVar.ENVIRONMENT['adb_port']
REMOTE_ADB_HOST = GlobalVar.ENVIRONMENT['remote_adb_host']
APPIUM_HOST = GlobalVar.ENVIRONMENT['appium_host']
APPIUM_PORT = GlobalVar.ENVIRONMENT['appium_port']


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.start = datetime.datetime.now()
        desired_caps = get_desired_capabilities(DEVICES_NAME, APP_PACKAGE, APP_ACTIVITY, ADB_PORT, REMOTE_ADB_HOST)
        self.driver = webdriver.Remote('http://{}:{}/wd/hub'.format(APPIUM_HOST, APPIUM_PORT), desired_caps)
        self.driver.implicitly_wait(10)
        page = Page(self.driver)
        page.switch_to_main_activity(APP_ACTIVITY)

    def tearDown(self):
        screenshot_for_report(self.driver)
        self.driver.quit()
        self.end = datetime.datetime.now()
        duration_time = str(self.end - self.start)
        print('durationTime:' + duration_time)


if __name__ == '__main__':
    unittest.main()
