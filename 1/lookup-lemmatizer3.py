### This program is a very simple lemmatizer, which learns a
### lemmatization function from an annotated corpus. The function is
### so basic I wouldn't even consider it machine learning: it's
### basically just a big lookup table, which maps every word form
### attested in the training data to the most common lemma associated
### with that form. At test time, the program checks if a form is in
### the lookup table, and if so, it gives the associated lemma; if the
### form is not in the lookup table, it gives the form itself as the
### lemma (identity mapping).

### The program performs training and testing in one run: it reads the
### training data, learns the lookup table and keeps it in memory,
### then reads the test data, runs the testing, and reports the
### results.

### The program takes two command line arguments, which are the paths
### to the training and test files. Both files are assumed to be
### already tokenized, in Universal Dependencies format, that is: each
### token on a separate line, each line consisting of fields separated
### by tab characters, with word form in the second field, and lemma
### in the third field. Tab characters are assumed to occur only in
### lines corresponding to tokens; other lines are ignored.

import sys
import re

### Global variables

# Paths for data are read from command line
train_file = sys.argv[1]
test_file = sys.argv[2]

# Counters for lemmas in the training data: word form -> lemma -> count
lemma_count = {}

# Lookup table learned from the training data: word form -> lemma
lemma_max = {}

# Variables for reporting results
training_stats = ['Wordform types' , 'Wordform tokens' , 'Unambiguous types' , 'Unambiguous tokens' , 'Ambiguous types' , 'Ambiguous tokens' , 'Ambiguous most common tokens' , 'Identity tokens']
training_counts = dict.fromkeys(training_stats , 0)

test_outcomes = ['Total test items' , 'Found in lookup table' , 'Lookup match' , 'Lookup mismatch' , 'Not found in lookup table' , 'Identity match' , 'Identity mismatch']
test_counts = dict.fromkeys(test_outcomes , 0)

accuracies = {}

### Training: read training data and populate lemma counters

train_data = open(train_file, 'r')
i = 0
for line in train_data:

    # Tab character identifies lines containing tokens
    if re.search('\t', line):

        # Tokens represented as tab-separated fields
        field = line.strip().split('\t')

        # Word form in second field, lemma in third field
        form = field[1]
        lemma = field[2]
        lemma_added = False

        if form in lemma_count.keys():
            list_lemma = lemma_count[form]
            for i in range(len(list_lemma)): #see if lemma is already in lemma_count for the current form
                if list_lemma[i][0] == lemma:
                    list_lemma[i][1] += 1
                    lemma_added = True
            if lemma_added == False:
                list_lemma.append([lemma, 1])

        else:
           lemma_count[form] = [[lemma, 1]]

### lemma_count looks something like this now
### {form1, [[lemma1, 4]], form2, [[lemma1, 4], [lemma2, 5] ... and so on for entire train data


### Model building and training statistics
wordform_tokens = 0
ambi_types = 0
ambi_tokens = 0
ambi_most_common_tokens = 0
identity_tokens = 0 # form has lemma that is the same
count_lemma_tokens = 0
tie = 0
for form in lemma_count.keys():


        ######################################################
        ### Insert code for building the lookup table      ###
        ######################################################
        # fill up lemma max key: word form Value: lemma
    counts = lemma_count[form]
    max_count = -1
    max_lemma = ''
    for c in counts:  # c is a 2d list each index is [lemma, count of lemma]
        wordform_tokens += c[1]

        if len(counts) > 1:
            ambi_tokens += c[1]

        if form == c[0]:
            identity_tokens += c[1]

        if c[1] > max_count: # the previous lemma with the max_count stay as max_lemma. New lemma must have a greater count to become max.
            max_count = c[1]
            max_lemma = c[0]

        if c[1] == max_count:
            tie += 1

    if len(counts) > 1:
        ambi_types += 1
        ambi_most_common_tokens += max_count

    count_lemma_tokens += max_count  # use to calculate lookup accuracy
    lemma_max[form] = max_lemma

training_counts['Wordform types'] = len(lemma_max)
training_counts['Wordform tokens'] = wordform_tokens
training_counts['Unambiguous types'] = len(lemma_max) - ambi_types
training_counts['Unambiguous tokens'] = wordform_tokens - ambi_tokens
training_counts['Ambiguous types'] = ambi_types
training_counts['Ambiguous tokens'] = ambi_tokens
training_counts['Ambiguous most common tokens'] = ambi_most_common_tokens
training_counts['Identity tokens'] = identity_tokens

# for k in training_counts.keys():
#     print(k, ":", training_counts[k])

accuracies['Expected lookup'] = count_lemma_tokens / wordform_tokens  ### Calculate expected accuracy if we used lookup on all items ###
accuracies['Expected identity'] = identity_tokens / wordform_tokens  ### Calculate expected accuracy if we used identity mapping on all items ###

# for k in accuracies.keys():
#     print(k, ":", accuracies[k])

### Testing: read test data, and compare lemmatizer output to actual lemma

test_data = open (test_file , 'r')

total_test_items = 0
found_lookup_table = 0
lookup_match= 0
lookup_mismatch = 0
not_found_lookup_table = 0
identity_match = 0
identity_mismatch = 0

for line in test_data:

    # Tab character identifies lines containing tokens
    if re.search ('\t' , line):

        # Tokens represented as tab-separated fields
        field = line.strip().split('\t')

        # Word form in second field, lemma in third field
        form = field[1]
        lemma = field[2]
        total_test_items += 1

        if form in lemma_max.keys():
            found_lookup_table += 1

            if lemma == lemma_max[form]:
                lookup_match += 1
            else:
                lookup_mismatch += 1

        else:
            if form == lemma:
                identity_match += 1
            else:
                identity_mismatch += 1
            not_found_lookup_table += 1

test_counts['Total test items'] = total_test_items
test_counts['Found in lookup table'] = found_lookup_table
test_counts['Lookup match'] = lookup_match
test_counts['Lookup mismatch'] = lookup_mismatch  # same as found_lookup_table - lookup_match
test_counts['Not found in lookup table'] = not_found_lookup_table
test_counts['Identity match'] = identity_match
test_counts['Identity mismatch'] = identity_mismatch

# for k in test_counts.keys():
#     print(k, ":", test_counts[k])

accuracies['Lookup'] = lookup_match / found_lookup_table  ### Calculate accuracy on the items that used the lookup table ###

accuracies['Identity'] = identity_match / not_found_lookup_table  ### Calculate accuracy on the items that used identity mapping ###

accuracies['Overall'] = found_lookup_table / total_test_items  ### Calculate overall accuracy ###

### Report training statistics and test results

output = open ('lookup-output.txt' , 'w')

output.write ('Training statistics\n')

for stat in training_stats:
    output.write (stat + ': ' + str(training_counts[stat]) + '\n')

for model in ['Expected lookup' , 'Expected identity']:
    output.write (model + ' accuracy: ' + str(accuracies[model]) + '\n')

output.write ('Test results\n')

for outcome in test_outcomes:
    output.write (outcome + ': ' + str(test_counts[outcome]) + '\n')

for model in ['Lookup' , 'Identity' , 'Overall']:
    output.write (model + ' accuracy: ' + str(accuracies[model]) + '\n')

output.close