from configparser import ConfigParser
from moats import GlobalVar
import subprocess
import time
import os


class Config:
    def __init__(self, config_file, argvs):
        # 读取配置文件中的参数
        self.time_stamp = time.strftime("%Y%m%d%H%M%S")
        self.config_file = config_file
        self.argvs = argvs[0:]
        self.project_path = os.path.dirname(config_file)
        self.test_data_file = os.path.join(self.project_path,'test_data/test_data.conf')
        self.appium_v = Config.invoke('appium -v').splitlines()[0].strip()
        self.apk = self.get_config('app', 'apk')
        self.apk_download_url = self.get_config('app', 'apk_download_url')
        self.apk_path = os.path.join('.', self.apk)
        self.app_activity = self.get_config('app', 'app_activity')
        self.app_package = self.get_config('app', 'app_package')
        self.smtp_server = self.get_config('email', 'smtp_server')
        self.smtp_user = self.get_config('email', 'smtp_user')
        self.smtp_password = self.get_config('email', 'smtp_password')
        self.subject = self.get_config('email', 'subject')
        self.receivers = self.get_config('email', 'receivers')
        self.remote_adb_host = self.get_config('devices', 'remote_adb_host')
        self.adb_port = self.get_config('devices', 'adb_port')
        self.appium_host = self.get_config('appium', 'appium_host')
        self.appium_port = self.get_config('appium', 'appium_port')
        self.debug = False
        if not self.get_config('report', 'report_path'):
            self.report_path = './test_report'
        else:
            self.report_path = os.path.join(self.get_config('report', 'report_path'),'test_report')
        self.report_dir = os.path.join(self.report_path,self.time_stamp)
        self.report_name = os.path.join(self.report_dir,self.time_stamp + '_report.html')
        self.report_zip_name = os.path.join(self.report_path, self.time_stamp + 'report.zip')
        if self.get_config('debug', 'debug') == 'True':
            self.debug = True
        # 读取命令行参数
        if len(self.argvs) > 0:
            self.remote_adb_host = self.get_config('devices', 'remote_adb_host')
        if len(self.argvs) > 1:
            self.adb_port = self.argvs[1]
        self.devices = self.get_android_devices()
        self.check_environment()
        self.set_environment()
        self.make_report_dir()

    def make_report_dir(self):
        self.mkdir(self.report_path)
        self.mkdir(self.report_dir)

    def get_config(self, section, option):
        cp = ConfigParser()
        cp.read(self.config_file, encoding='utf-8')
        return cp.get(section, option)

    def check_environment(self):
        if not self.devices:
            print('没有设备连接')
            exit()
        else:
            print('已连接设备:', self.devices)
        if not self.appium_v:
            print('appium 有问题')
            exit()
        else:
            print('appium version {}'.format(self.appium_v))

    def set_environment(self):
        GlobalVar.ENVIRONMENT = self.__dict__

    def output_environment(self):
        print('运行时环境变量：')
        for each in GlobalVar.ENVIRONMENT.items():
            print(each)

    @staticmethod
    def invoke(cmd):
        # shell设为true，程序将通过shell来执行
        # stdin, stdout, stderr分别表示程序的标准输入、输出、错误句柄。
        # 他们可以是PIPE，文件描述符或文件对象，也可以设置为None，表示从父进程继承。
        # subprocess.PIPE实际上为文本流提供一个缓存区
        output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        o = output.decode("utf-8")
        return o

    @staticmethod
    def get_android_devices():
        android_devices_list = []
        for device in Config.invoke('adb devices').splitlines():
            if 'device' in device and 'devices' not in device:
                device = device.split('\t')[0]
                android_devices_list.append(device)
        return android_devices_list

    def mkdir(self,target_path):
        """
        创建目录
        :param target_path: 将要创建的目录路径
        :return: True or False
        """
        target_path = target_path.strip()
        target_path = target_path.rstrip("\\")
        isExists = os.path.exists(target_path)
        if not isExists:
            os.makedirs(target_path)
            print(target_path + ' 创建成功')
            return True
        else:
            print(target_path + ' 目录已存在')
            return False


if __name__ == '__main__':
    c = Config('config.conf', 'aa')
    env =GlobalVar.ENVIRONMENT
    print(env['receivers'])
