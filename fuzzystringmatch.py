import re


def fuzz_match_string(query_string, sentence):
    strings = query_string.split(' ')
    strings = [string.strip() for string in strings if string != '']

    ret = []
    for string in strings:
        match = re.search(string, sentence, re.IGNORECASE)
        if match is not None:
            ret.append(match)

    return len(ret) > 0, ret


def fuzzy_match_string_list(query_string, sentence_list):
    matched_sentence = []
    for sentence in sentence_list:
        matched, match_info = fuzz_match_string(query_string, sentence)
        if matched:
            matched_sentence.append((match_info, sentence))

    return matched_sentence


if __name__ == '__main__':
    ret = fuzz_match_string("win open", "Windows list open windows")
    print(ret)