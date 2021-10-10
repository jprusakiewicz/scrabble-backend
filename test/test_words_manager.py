import unittest

from app.words import words_manager


class WordsManagerTest(unittest.TestCase):
    def test_checking_correct_word(self):
        # given
        locale = 'pl'
        correct_word = "unia"
        #when
        result = words_manager.check_word(correct_word, locale)
        #then
        self.assertEqual(True, result)  # add assertion here

        # def test_checking_word(self):
        # given
        locale = 'pl'
        incorrect_word = "aasdfds"
        #when
        result = words_manager.check_word(incorrect_word, locale)
        #then
        self.assertEqual(False, result)  # add assertion here


if __name__ == '__main__':
    unittest.main()
