# -*- coding:utf-8 -*-
import os
import sys
import re
import subprocess
from moats import GlobalVar

env = GlobalVar.ENVIRONMENT
remoteAdbHost = env['remote_adb_host']
adbPort = env['adb_port']

class Adb(object):
    """Adb封装"""


    def __init__(self):
        self.remoteAdbHost = remoteAdbHost
        self.adbPort = adbPort

    def adb(self,command):
        return list(os.popen('adb ' + command).readlines())

    def adb_start_server(self):
        return list(os.popen('adb start-server').readlines())

    def adb_kill_server(self):
        return list(os.popen('adb kill-server').readlines())

    def adb_P(self,command):
        return list(os.popen('adb -P ' + self.adbPort + command).readlines())

    def adb_H(self,command):
        return list(os.popen('adb -H ' + self.remoteAdbHost + command).readlines())


    def adb_devices(self):
        readDeviceId = list(os.popen('adb devices').readlines())
        # 正则表达式匹配出 id 信息
        try:
            deviceId = re.findall(r'^\w*\b', readDeviceId[1])[0]
            return deviceId
        except BaseException:
            print(BaseException)

    def adb_H_devices(self):
        readDeviceId = list(os.popen('adb -H ' + self.remoteAdbHost + ' devices').readlines())
        # 正则表达式匹配出 id 信息
        try:
            deviceId = re.findall(r'^\w*\b', readDeviceId[1])[0]
            return deviceId
        except BaseException:
            print(BaseException)

    @staticmethod
    def adb_install(apkname):
        content = list(os.popen('adb install -r ' + apkname).readlines())
        print(content)
        if 'Success' in content:
            return True
        else:
            return False
        # return os.popen('adb install -r ' + apkname)

    @staticmethod
    def adb_uninstall(package):
        # return os.popen('adb uninstall ' + package)
        content = list(os.popen('adb uninstall ' + package).readlines())
        print(content)
        if 'Success' in content:
            return True
        else:
            return False
        
    def adb_shell_monkey(self, package, report_dir):
        return os.system('adb shell monkey -p ' + package + ' -v-v-v --pct-touch 10 --pct-motion 30 --pct-appswitch 20 --ignore-crashes --ignore-timeouts 100000 1 >> ' + report_dir + 'monkey.txt' + ' 2>> ' + report_dir + '/monkey_error.txt')
    
    @staticmethod
    def adb_is_app_installed(package_name):
        result = os.popen('adb shell pm list packages ' + package_name).readlines()
        if isinstance(result, list) and len(result) > 0:
            if package_name in result[0]:
                return True
        return False

    def phoneInfo(self):
        device = os.popen('adb shell getprop ro.product.model').read()
        pyInfo = sys.platform + "\n" + sys.version
        size_str = os.popen('adb shell wm size').read()
        return (device, pyInfo, size_str)

    def getAndroidVersion(self):

        sysInfo = subprocess.check_output('adb shell cat /system/build.prop')
        print(sysInfo)
        sysInfo = sysInfo.decode(encoding='utf-8')
        # 获取安卓版本号
        androidVersion = re.findall("version.release=(\d\.\d)*", sysInfo, re.S)[0]
        return androidVersion
