import os
import shutil
import psutil
import time
from tqdm import tqdm

class Copy2Usb:
    def __init__(self):
        self.origin_devices = psutil.disk_partitions()
        self.current_woking_directory = os.getcwd()
        self.new_device = []
        self.finished_devices = []

    def check_new_device(self):
        result = False
        for each in psutil.disk_partitions():
            if 'removable' in each.opts and each not in self.finished_devices:
                result = True
        return result

    def get_new_device(self):
        new_device = []
        for each in psutil.disk_partitions():
            if 'removable' in each.opts and each not in self.finished_devices:
                new_device.append(each)
        self.new_device = new_device
        return str(new_device)

    def get_cwd_files(self):
        self.files =  []
        for each in os.listdir(self.current_woking_directory):
            if '.' in each:
                self.files.append(each)


    def copy2usb(self):
        self.labels = os.popen("wmic VOLUME GET Label").read().split('\n')
        self.captions = os.popen("wmic VOLUME GET Caption").read().split('\n')
        print('\n------------------\nCopy Process Start:\n{} files in total\n{} devices in total'.format(str(len(self.files)), str(len(self.new_device))))
        for each in self.new_device:
            self.finished_devices.append(each)
            for l in range(len(self.captions)):
                if each.device in self.captions[l]:
                    device_label = self.labels[l]

            for f in tqdm(self.files, ncols=70, desc='Progress at {}'.format(device_label)):
                try:
                    shutil.copy2(self.current_woking_directory+'\\'+f, each.device)
                except:
                    try:
                        shutil.copy(self.current_woking_directory+'\\'+f, each.device)
                    except PermissionError as e:
                        pass

if __name__ == '__main__':
    index = '''This program is programmed by @tony_syz, used for copying
copy2usb.py - How To Use:

Environment
    To run this program, tqdm, psutil and shutil is required.
    You can install tqdm with the command 'pip install tqdm' etc..

Use
    Some files will be copy to usb devices which is removable.
    Open the source code with Python3, or use the command 'python C:\\path\\to\\copy2usb.py'.
    Insert your USB Disk and wait for a few seconds until the progress bar finish.'''
    print(index)
    c = Copy2Usb()
    while True:
        time.sleep(0.5)
        if c.check_new_device() == True:
            n = c.get_new_device()
            c.get_cwd_files()
            c.copy2usb()