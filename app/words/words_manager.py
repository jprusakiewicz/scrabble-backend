class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class WordsManager(metaclass=SingletonMeta):
    def __init__(self):
        self.supported_locales = ['pl', 'en']
        self.words = self.load_words()

    def load_words(self):
        words = {}
        for locale in self.supported_locales:
            try:
                words[locale] = self.read_words(locale)
            except FileNotFoundError:
                print(f"File not found for locale: {locale}")
        return words

    def read_words(self, locale: str):
        print(f"reading locale: {locale}")
        path = ""
        if locale == 'pl':
            path = '../app/words/slowa.txt'
        elif locale == 'en':
            path = "../app/words/words.txt"
        # elif locale == '...':
        #     path = "... .txt"

        with open(path) as f:
            words = f.read().split('\n')

        return words

    def is_locale_supported(self, locale: str) -> bool:
        if locale in self.words:
            return True
        return False

    def check_word(self, word, locale):
        if word in self.words[locale]:
            return True
        return False


words_manager = WordsManager()

