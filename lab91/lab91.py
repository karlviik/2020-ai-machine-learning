import os
import math


def stopword(wstr):
	w = wstr.strip()
	if len(w) < 4:
		return True
	return False


def read_dir(dirn):
	cont_l = []
	for fn in os.listdir(dirn):
		with open(os.path.join(dirn, fn), encoding="latin-1") as f:
			words = [w.strip()
			         for w in f.read().replace("\n", " ").split(" ")
			         if not stopword(w)]
			cont_l.append(words)
	return cont_l


if __name__ == '__main__':
	ham_l = read_dir(os.path.join("enron6", "ham"))
	spam_l = read_dir(os.path.join("enron6", "spam"))

	ham_dict = {}
	for thing in ham_l:
		for word in thing:
			ham_dict[word] = ham_dict.setdefault(word, 0) + 1

	spam_dict = {}
	for thing in spam_l:
		for word in thing:
			spam_dict[word] = spam_dict.setdefault(word, 0) + 1

	p_spam = len(spam_l) / (len(ham_l) + len(spam_l))
	p_ham = len(ham_l) / (len(ham_l) + len(spam_l))
	all_unique_words = set(ham_dict.keys()).union(set(spam_dict.keys()))
	unique_word_count = len(all_unique_words)
	all_spam_words = sum(spam_dict.values())
	all_ham_words = sum(ham_dict.values())

	files = read_dir(os.path.join("testing"))
	for i, file in enumerate(files):
		actual_words = set([word for word in set(file) if word in all_unique_words])
		hspamln = sum([math.log((spam_dict.setdefault(word, 0) + 1) / (all_spam_words + unique_word_count)) for word in
		               actual_words]) + math.log(p_spam)
		hhamln = sum([math.log((ham_dict.setdefault(word, 0) + 1) / (all_ham_words + unique_word_count)) for word in
		              actual_words]) + math.log(p_ham)
		spam_chance = 1 / (1 + math.pow(math.e, hhamln - hspamln))
		ham_chance = 1 / (1 + math.pow(math.e, hspamln - hhamln))
		print(f"Probability of file {i + 1} being spam: {round(spam_chance * 10000) / 100}%")
		print(f"Probability of file {i + 1} being ham: {round(ham_chance * 10000) / 100}%")
		print()
