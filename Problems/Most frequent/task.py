from collections import Counter

n = int(input())
text = ("all I want is a proper cup of coffee made in a proper copper coffee pot. "
        "I may be off my dot but I want a cup of coffee from a proper coffee pot.")

for word, c in Counter(text.split()).most_common(n):
    print(word, c)
