

def get_desired_capabilities(devices_name, app_package, app_activity,  adb_port='5037', remote_adb_host='127.0.0.1'):
    desired_caps = {'platformName': 'Android',
                    'deviceName': devices_name,
                    'appPackage': app_package,
                    'appActivity': app_activity,
                    'udid': devices_name,
                    'unicodeKeyboard': True,
                    'resetKeyboard': True,
                    'newCommandTimeout': 7200,
                    'ignoreUnimportantViews': True,
                    'noReset': True,
                    'adbPort': adb_port,
                    'remoteAdbHost': remote_adb_host}
    return desired_caps


def get_desired_capabilities_install_app(devices_name, app, adb_port='5037', remote_adb_host='127.0.0.1'):
    desired_caps = {'platformName': 'Android',
                    'deviceName': devices_name,
                    'app': app,
                    'udid': devices_name,
                    'unicodeKeyboard': True,
                    'resetKeyboard': True,
                    'newCommandTimeout': 7200,
                    'ignoreUnimportantViews': True,
                    'noReset': True,
                    'adbPort': adb_port,
                    'remoteAdbHost': remote_adb_host
                    }
    return desired_caps
