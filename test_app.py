import os
import unittest
import sys
import new
from appium import webdriver
from sauceclient import SauceClient

browsers = [{
    'appiumVersion':    '1.3.4',
    'platformName':     'Android',
    'platformVersion':  '4.3',
    'deviceName':       'Android Emulator',
    'app':              'http://appium.s3.amazonaws.com/NotesList.apk',
    'name':             'Python Appium Android 4.3 example'
}, {
    'appiumVersion':    '1.3.4',
    'platformName':     'Android',
    'platformVersion':  '5.0',
    'deviceName':       'Android Emulator',
    'app':              'http://appium.s3.amazonaws.com/NotesList.apk',
    'name':             'Python Appium Android 5.0 example'
}]

username = os.environ['SAUCE_USERNAME']
access_key = os.environ['SAUCE_ACCESS_KEY']

# This decorator is required to iterate over browsers
def on_platforms(platforms):
    def decorator(base_class):
        module = sys.modules[base_class.__module__].__dict__
        for i, platform in enumerate(platforms):
            d = dict(base_class.__dict__)
            d['desired_capabilities'] = platform
            name = "%s_%s" % (base_class.__name__, i + 1)
            module[name] = new.classobj(name, (base_class,), d)
    return decorator

@on_platforms(browsers)
class FirstSampleTest(unittest.TestCase):

    # setUp runs before each test case
    def setUp(self):
        self.desired_capabilities['name'] = self.id()
        self.driver = webdriver.Remote(
           command_executor="http://%s:%s@ondemand.saucelabs.com:80/wd/hub" % (username, access_key),
           desired_capabilities=self.desired_capabilities)

    # click to make a new note in the app
    def test_note(self):
        self.driver.find_element_by_accessibility_id('New note').click()
        self.driver.find_element_by_class_name('android.widget.EditText').send_keys('Here is a new note from Python')
        self.driver.find_element_by_accessibility_id('Save').click()
        notes = self.driver.find_elements_by_class_name('android.widget.TextView')
        self.assertEqual(notes[2].text,'Here is a new note from Python')

    # tearDown runs after each test case
    def tearDown(self):
        self.driver.quit()
        sauce_client = SauceClient(username, access_key)
        status = (sys.exc_info() == (None, None, None))
        sauce_client.jobs.update_job(self.driver.session_id, passed=status)
