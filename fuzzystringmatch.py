import re
from thefuzz import fuzz


def fuzzy_approx_match_string(query_string, sentence):
    strings = query_string.split(' ')
    strings = [string.strip() for string in strings if string != '']

    ret = []
    for string in strings:
        match_ratio = fuzz.partial_token_sort_ratio(string, sentence)
        if match_ratio >= 70.0:
            ret.append(sentence)
            break

    return len(ret) > 0, ret


def fuzzy_approx_match_string_list(query_string, sentence_list):
    matched_sentence = []
    for sentence in sentence_list:
        matched, match_info = fuzzy_approx_match_string(query_string, sentence)
        if matched:
            matched_sentence.append(sentence)

    return matched_sentence


def fuzzy_regex_match_string(query_string, sentence):
    strings = query_string.split(' ')
    strings = [string.strip() for string in strings if string != '']

    ret = []
    for string in strings:
        match = re.search(string, sentence, re.IGNORECASE)
        if match is not None:
            ret.append(match)

    return len(ret) > 0, ret


def fuzzy_regex_match_string_list(query_string, sentence_list):
    matched_sentence = []
    for sentence in sentence_list:
        matched, match_info = fuzzy_regex_match_string(query_string, sentence)
        if matched:
            matched_sentence.append((match_info, sentence))

    return matched_sentence


def fuzzy_regex_match_window_list(query_string, window_list):
    matched_sentence = []
    for window in window_list:
        matched, match_info = fuzzy_regex_match_string(query_string, window.title)
        if matched:
            matched_sentence.append((match_info, window))

    return matched_sentence


if __name__ == '__main__':
    ret = fuzzy_regex_match_string("win open", "Windows list open windows")
    print(ret)
