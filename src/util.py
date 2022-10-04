import os
import shlex
import subprocess
import sys
import threading
import traceback

from PyQt5.QtGui import QIcon, QPixmap

version = {
    "curr": "0.6.12",
    "history": {
        "0.0.1": "实现基本功能:\n"
                 "  1、查词界面\n"
                 "  2、翻译界面\n"
                 "  3、剪贴板取词",
        "0.1.1": "支持本地词典",
        "0.2.2": "1、防止多次运行\n"
                 "2、支持OCR取词",
        "0.2.3": "1、设置改变实时生效\n"
                 "2、完善关于窗口\n"
                 "3、解决BUG",
        "0.3.4": "1、支持更改OCR取词热键\n"
                 "2、完善OCR取词服务\n"
                 "3、优化界面\n"
                 "4、解决中文输入问题",
        "0.5.5": "支持谷歌翻译",
        "0.6.6": "支持生词本",
        "0.6.7": "优化性能",
        "0.6.8": "1、完善OCR取词服务的安装与启动逻辑。\n"
                 "2、优化性能。\n"
                 "3、更换程序图标。",
        "0.6.9": "1、优化设置界面。\n"
                 "2、解决Ubuntu系统中的兼容问题。\n"
                 "3、优化OCR取词，提升成功概率。\n",
        "0.6.10": "1、解决上个版本安装OCR服务失败的问题。\n"
                  "2、优化设置界面。\n",
        "0.6.11": "1、完善剪贴板取词设置。\n",
        "0.6.12": "1、完善无托盘区域的兼容性。\n"
                  "2、提高archlinux、centos的兼容性。\n",
    }
}


def get_version():
    return version["curr"]


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception as err:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def load_icon(name):
    return QIcon(QPixmap(resource_path("./res/{}.png".format(name))))


def log_line(log_function, line):
    try:
        log_function(line.decode('utf-8'))
    except Exception as ex:
        log_function("{}".format(traceback.format_exc()))
        print(ex, traceback.format_exc())


def run_app(cmd, log_function=print, passwd=None) -> int:
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    log_function("{} run app: {}".format(threading.currentThread().getName(), ' '.join(cmd)))
    try:
        env = os.environ
        if passwd:
            env["PASSWD"] = passwd
        p = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            env=env
        )
        # log_function("running app: {}".format(' '.join(cmd)))
        while p.poll() is None:
            line = p.stdout.readline()
            log_line(log_function, line)

        for line in p.stdout.readlines():
            log_line(log_function, line)
        log_function("{} runn app finish. returncode={}".format(threading.currentThread().getName(), p.returncode))
        return p.returncode
    except Exception as ex:
        print(ex)
        log_function(traceback.format_exc())
        return -2
