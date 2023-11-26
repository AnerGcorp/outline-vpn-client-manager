
import sys
import time
import psutil
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon


def runcatCPU():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    icon = QSystemTrayIcon()
    icon.setIcon(QIcon('icons/0.png'))
    icon.setVisible(True)
    cpu_percent = psutil.cpu_percent(interval=1) / 100
    cpu_percent_update_fps = 20
    fps_count = 0
    while True:
        fps_count += 1
        if fps_count > cpu_percent_update_fps:
            cpu_percent = psutil.cpu_percent(interval=1) / 100
            fps_count = 0
        time_interval = (cpu_percent * cpu_percent - 2 * cpu_percent + 2) / 20
        for i in range(5):
            icon.setIcon(QIcon('icons/%d.png' % i))
            icon.setToolTip('cpu: %.2f' % cpu_percent)
            time.sleep(time_interval)
    app.exec_()


def runcatMemory():
    app = QApplication(sys.argv)

    app.setQuitOnLastWindowClosed(False)
    icon = QSystemTrayIcon()
    icon.setIcon(QIcon('icons/0.png'))
    icon.setVisible(True)
    memory_percent = psutil.virtual_memory().percent / 100
    memory_percent_update_fps = 20
    fps_count = 0
    while True:
        fps_count += 1
        if fps_count > memory_percent_update_fps:
            memory_percent = psutil.virtual_memory().percent / 100
            fps_count = 0

        time_interval = (memory_percent * memory_percent - 2 * memory_percent + 2) / 20
        for i in range(5):
            icon.setIcon(QIcon('icons/%d.png' % i))
            icon.setToolTip('memory: %.2f' % memory_percent)
            time.sleep(time_interval)
    app.exec_()


'''run'''
if __name__ == '__main__':
    resource_type = ['cpu', 'memory'][0]
    if resource_type == 'cpu':
        runcatCPU()
    elif resource_type == 'memory':
        runcatMemory()
    else:
        raise ValueError('Unknow resource_type <%s>...' % resource_type)