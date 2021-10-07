with open('words_uppercase.txt', 'rt') as f:
    words_uppercase = f.read()

words_lowercase = ""
for word in words_uppercase:
    words_lowercase += word.lower()

with open('words.txt', 'wt') as f:
    f.write(words_lowercase)