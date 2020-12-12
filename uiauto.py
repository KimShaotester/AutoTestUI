import uiautomator2
import unittest
import subprocess
import time
import re

def run_shell_command(cmd):
    return subprocess.run(cmd, shell=True, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

class uiauto():
    def __init__(self):
        self.ip = ""

    def device_initialize(self):
        self.device = uiautomator2.connect(self.ip)

    def click_by_text(self, text, contains=False, timeout=2):
        if contains:
            return self.device(textcontains=text).click_exists(timeout)
        return self.device(text=text).click_exists(timeout)

    def click_by_resourceId(self, resourceId, timeout):
        return self.device(resourceId=resourceId).click_exists(timeout)

    def click_by_description(self, description, contains=False, timeout=2):
        if contains:
            return self.device(descriptionContains=description).click_exists(timeout)
        return self.device(description=description).click_exists(timeout)

    def click_by_packageName(self, packageName, timeout):
        return self.device(packageName=packageName).click_exists(timeout)

    def click_list_text(self, list, contains=False, timeout=2):
        for text in list:
            self.click_by_text(text, contains, timeout)
