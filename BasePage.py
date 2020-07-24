# -*- coding:utf-8 -*-
from appium.webdriver.common.touch_action import TouchAction
from moats.Log import Log as L
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from moats import GlobalVar
from time import sleep
import time


class Page:
    """页面基础类，定位方法封装，通用操作封装"""

    def __init__(self, driver):
        """初始化"""
        self.driver = driver

    def swipe_to_up(self):
        """上滑屏幕"""
        L.d('操作：上滑屏幕')
        resolution = self.driver.get_window_size()
        width = resolution['width']
        height = resolution['height']
        self.driver.swipe(width / 2, height * 3 / 4, width / 2, height / 4)

    def swipe_to_down(self):
        """下滑屏幕"""
        L.d('操作：下滑屏幕')
        resolution = self.driver.get_window_size()
        width = resolution['width']
        height = resolution['height']
        self.driver.swipe(width / 2, height / 4, width / 2, height * 3 / 4)

    def swipe_to_notifications(self):
        """下滑屏幕"""
        L.d('操作：下滑到通知栏')
        resolution = self.driver.get_window_size()
        width = resolution['width']
        height = resolution['height']
        self.driver.swipe(width / 2, height / 1000, width / 2, height * 3 / 4)

    def swipe_to_side(self, y=None):
        '''右滑到侧边栏，经过实测发现有时候点击头像到侧边栏无效'''
        resolution = self.driver.get_window_size()
        width = resolution['width']
        height = resolution['height']
        if y is None:
            y = height / 2
        self.driver.swipe(width / 1080, y, width * 5 / 6, y)  # 1080p

    def swipe_to_left(self, y=None):
        """左滑屏幕
        y: 左滑的y坐标"""
        L.d('操作：左滑屏幕')
        resolution = self.driver.get_window_size()
        width = resolution['width']
        height = resolution['height']
        if y is None:
            y = height / 2
        self.driver.swipe(width * 3 / 4, y, width / 4, y)

    def swipe_to_right(self, y=None):
        """右滑屏幕
        y: 右滑的y坐标"""
        L.d('操作：右滑屏幕')
        resolution = self.driver.get_window_size()
        width = resolution['width']
        height = resolution['height']
        if y is None:
            y = height / 2
        self.driver.swipe(width / 4, y, width * 3 / 4, y)

    def is_exist(self, loc, timeout=10):
        """
        判定元素是否存在
        args:
        *loc:元素定位参数
        """
        try:
            L.d('查找：' + str(loc[0]) + ' = ' + '\"' + str(loc[1]) + '\"' + ' 的控件')
            widgets = WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(loc))

            if isinstance(widgets, list):
                if len(widgets) > 0:
                    return True
            else:
                return False

        except TimeoutException:
            return False

    def press_back(self):
        """通用返回按钮"""
        L.d('操作：点击通用返回按钮')
        self.driver.press_keycode(4)
        sleep(GlobalVar.short)

    def double_click(self, element):
        """双击操作

        element：执行该操作的控件

        举例：
        | Double Click | myElement |
        """
        L.d('操作：双击控件 ' + str(element.text))
        action = TouchAction(self.driver)
        action.press(element).release().press(element).release().perform()

    def check_contain_text(self, text):
        """查找手机屏幕上是否存在指定的字符串
        """
        L.d('操作：查找屏幕上是否存在：' + text)
        if not isinstance(text, str):
            text = str(text)
        try:
            page_source = self.driver.page_source
            text_repeat = str(page_source).count(text)
            if text_repeat != 0:
                return True
            else:
                return False
        except Exception as e:
            return False

    def check_is_current_activity(self, target_activity, timeout=10):
        """

        :param target_activity: 目标activity
        :param timeout: 超时时间
        :return: True or False
        """
        L.d('检查当前activity是否是：' + target_activity)
        return self.driver.wait_activity(target_activity, timeout)

    def check_is_current_package(self, app_package):
        """
        :param app_package: 当前测试的APP包名
        :return: True or False
        """
        L.d('检查当前package是否是：' + app_package)
        if self.driver.current_package() == app_package:
            return True
        else:
            return False

    def switch_to_activity(self, app_package, activity_name):
        """
        启动某个app的某个activity
        :param app_package: APP package name
        :param activity_name: activity name
        :return: 无
        """
        L.d('转换到' + app_package + '的' + activity_name)
        self.driver.start_activity(app_package, activity_name, )

    def switch_to_main_activity(self, main_activity_name, timeout=30):

        """
        启动某个APP的主activity
        :param app_package: APP package name
        :param main_activity_name: main activity name
        :param timeout: 超时时间
        :return: True or False
        """

        L.d('转换到主activity')
        end_time = time.time() + timeout
        while not self.driver.wait_activity(main_activity_name, timeout=2):
            self.allow_permission()
            self.driver.press_keycode(4)
            self.driver.close_app()
            self.driver.launch_app()
            if time.time() > end_time:
                return None
        else:
            if not self.is_exist(loc=('-android uiautomator', 'new UiSelector().text("新世界")')):
                self.driver.close_app()
                self.driver.launch_app()

    @property
    def window_width(self):
        return self.driver.get_window_size()['width']

    @property
    def window_height(self):
        return self.driver.get_window_size()['height']

    def allow_permission(self):
        while self.is_exist(loc=('-android uiautomator', 'new UiSelector().text("允许")'), timeout=1):
            self.driver.find_element_by_android_uiautomator('new UiSelector().text("允许")').click()
