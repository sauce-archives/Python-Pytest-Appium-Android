import base_test

@base_test.on_platforms(base_test.browsers)
class SubTest1(base_test.BaseTest):

    # verify google title
        # click to make a new note in the app
    def test_note(self):
        self.driver.find_element_by_accessibility_id('New note').click()
        self.driver.find_element_by_class_name('android.widget.EditText').send_keys('Here is a new note from Python')
        self.driver.find_element_by_accessibility_id('Save').click()
        notes = self.driver.find_elements_by_class_name('android.widget.TextView')
        self.assertEqual(notes[2].text,'Here is a new note from Python')