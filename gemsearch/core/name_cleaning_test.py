import unittest

from gemsearch.core.name_cleaning import clean_playlist_name, clean_tag_name, clean_tag

class NameCleaningTest(unittest.TestCase):

    def test_tag_cleaning(self):
        self.assertEqual(clean_tag_name('  hello  '), 'hello')
        self.assertEqual(clean_tag_name('  hello --- '), 'hello')
        self.assertEqual(clean_tag_name('BlaaaDD'), 'blaaadd')
        self.assertEqual(clean_tag_name(' BlaaaDD'), 'blaaadd')

        self.assertFalse(clean_tag({'count': 1, 'tag': 'test'}))
        self.assertFalse(clean_tag_name('  '))
        self.assertFalse(clean_tag_name(' 12 '))
        self.assertFalse(clean_tag_name(''))

    def test_playlist_trim(self):
        self.assertEqual(clean_playlist_name('  hello  '), 'hello')
        self.assertEqual(clean_playlist_name('  hello 12 '), 'hello 12')

        self.assertFalse(clean_playlist_name('  ---  '))
        self.assertFalse(clean_playlist_name('---'))

if __name__ == '__main__':
    unittest.main()
