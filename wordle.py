from nltk.corpus import words
import copy

word_set = set(words.words())
for word in copy.deepcopy(word_set):
    if (len(word) != 5 or word[0].isupper()):
        word_set.remove(word)

found = False
confirmed = []

def getRemovals(word, word_set):
    removals = 0
    word_set_copy = copy.deepcopy(word_set)
    for letter in set(word):
        for word in copy.deepcopy(word_set_copy):
            if letter in word:
                word_set_copy.remove(word)
                removals += 1
    
    return removals

def getBest(word_set):
    print("Calculating...")
    top_words = []
    for word in copy.deepcopy(word_set):
        removals = getRemovals(word, word_set)
        if len(top_words) < 10:
            top_words.append([word, removals])
        elif removals > top_words[len(top_words) - 1][1]:
            top_words[len(top_words) - 1] = [word, removals]

        top_words = sorted(top_words, key=lambda x: x[1])
        top_words.reverse()
    return top_words

def update(word_rec, word_set, confirmed):
    print(f"The word is: {word_rec}")
    input(f"Attempt the word then press enter to continue.")

    unaccounted_positions = [x for x in range(len(word_rec))]
    confirming_phase = True
    print("Are any letters in the correct location? If so, please enter their positions.")
    while confirming_phase:
        option = int(input("Enter Position (0 to continue): "))
        if option == 0:
            confirming_phase = False

        elif option < 0 or option > 5:
            print("Error! Invalid option. Please try again.")
        
        else:
            index = option - 1
            letter = word_rec[index]
            confirmed.append([letter, index])
            unaccounted_positions.remove(index)
            for word in copy.deepcopy(word_set):
                if word[index] != letter:
                    word_set.remove(word)
        
    misplaced_phase = True
    misplaced = []
    print("Are any letters correct but misplaced? If so, please enter their positions.")
    while misplaced_phase:
        option = int(input("Enter Position (0 to continue): "))
        if option == 0:
            misplaced_phase = False

        elif option < 0 or option > 5 or (option - 1) not in unaccounted_positions:
            print("Error! Invalid option. Please try again.")
            
        else:
            index = option - 1
            letter = word_rec[index]
            misplaced.append([letter, index])
            unaccounted_positions.remove(index)
            for word in copy.deepcopy(word_set):
                temp = word
                for rule in confirmed:
                    temp = temp[0:rule[1]] + '*' + temp[rule[1] + 1:len(temp)]
                if word[index] == letter or letter not in temp:
                    word_set.remove(word)
        
    for index in unaccounted_positions:
        letter = word_rec[index]
        expected = 0
        for x in misplaced + confirmed:
            if x == letter:
                expected += 1

        for word in copy.deepcopy(word_set):
            if word.count(letter) != expected:
                word_set.remove(word)

while not found:
    word_list = getBest(word_set)
    print("Recommendations: ")
    counter = 1
    for word in word_list:
        print(f"{counter}: {word}")
        counter += 1

    print()
    word_rec = input("Please select a word: ")
    update(word_rec, word_set, confirmed)
    if len(word_set) < 10:
        print(word_set)
        found = True

print(word_set)