"""
Preprocessing utilities for text/sentence embedding.

Note that the following functions are not computationally optimized yet.
"""


from re import sub as re_sub

from spacy import load as spacy_load

from emoji import demojize


IRRELEVANT_PART_OF_SPEECH_TAGS = [
    # universal part-of-speech tags defined as irrelevant:
    # (reference: https://universaldependencies.org/docs/u/pos/)
    'ADP',  # adposition
    'AUX',  # auxiliary verb
    'CONJ',  # coordinating conjunction
    "EOL",  # end of line
    'PUNCT',  # punctuation
    'SCONJ',  # subordinating conjunction
    'SPACE',  # space
    # English-specific part-of-speech tags defined as irrelevant:
    # (references: https://www.ling.upenn.edu/courses/Fall_2003/ling001/
    # penn_treebank_pos.html,
    # https://github.com/explosion/spaCy/blob/master/spacy/glossary.py#L43)
    ".",  # punctuation mark, sentence closer
    ",",  # punctuation mark, comma
    "-LRB-",  # left round bracket
    "-RRB-",  # right round bracket
    "``",  # opening quotation mark
    '""',  # closing quotation mark
    "''",  # closing quotation mark
    ":",  # punctuation mark, colon or ellipsis
    "CC",  # conjunction, coordinating
    "HYPH",  # punctuation mark, hyphen
    "IN",  # conjunction, subordinating or preposition
    "LS",  # list item marker
    "POS",  # possessive ending
    "TO",  # infinitival "to"
    "SP",  # space (English), sentence-final particle (Chinese)
    "NFP",  # superfluous punctuation
    "BES",  # auxiliary "be"
]


# loading the model handling lexical properties:
lexical_model = spacy_load('en_core_web_sm')


def preprocess(sentence_text: str) -> str:
    """
    Preprocess in and end-to-end fashion the input text for later accurate
    sentence embedding computation by, in order:
        1) replacing emojis with the respective words in their official names,
        2) removing the irrelevant parts of speech,
        3) removing punctuation and special characters,
        4) turning any alphabetic character to lowercase,
        5) removing duplicate whitespaces.
    """
    return re_sub(
        ' +',
        ' ',
        remove_punctuation_and_special_characters(
            remove_irrelevant_pos(
                replace_emojis_with_words(sentence_text)
            )
        ).lower()
    )


def remove_irrelevant_pos(sentence_text: str) -> str:
    """
    Remove only the irrelevant words, depending on their part-of-speech tags.
    """
    # removing possible extreme whitespaces and newlines:
    sentence_text = sentence_text.strip()

    # tokenizing the sentence into words (with lexical content):
    global lexical_model
    sentence = lexical_model(sentence_text)

    # selecting only the relevant words based on their part-of-speech tags:
    global IRRELEVANT_PART_OF_SPEECH_TAGS
    only_relevant_words_sentence_text = ""
    for word in sentence:
        if word.pos_ not in IRRELEVANT_PART_OF_SPEECH_TAGS\
                and word.tag_ not in IRRELEVANT_PART_OF_SPEECH_TAGS:
            only_relevant_words_sentence_text += " " + word.text

    return only_relevant_words_sentence_text


def remove_punctuation_and_special_characters(sentence_text: str) -> str:
    """
    Remove punctuation and special characters.
    """
    return re_sub('[^A-Za-z0-9\s]+', ' ', sentence_text)


def replace_emojis_with_words(sentence_text: str) -> str:
    """
    Replace emojis with the respective words in their official names.
    """
    return demojize(sentence_text, delimiters=(" ", " "), ).replace("_", " ")
