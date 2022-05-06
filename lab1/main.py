from nltk import download
from nltk.tokenize import sent_tokenize, word_tokenize
from pymorphy2 import MorphAnalyzer
from pymorphy2.tagset import OpencorporaTag
from enum import Enum


part_of_sentence = {
    'subject': 'NOUN nomn,NPRO',
    'predicate': 'VERB',
    'definition': 'ADJF,ADJS,NUMR',
    'addition': 'NOUN,NPRO',
    'circumstance': 'INFN,ADVB,GRND,PRTF,PRTS',
}


class RuPartOfSent(Enum):
    SUBJECT = 'Подлежащее'
    PREDICATE = 'Сказуемое'
    DEFINITION = 'Определение'
    ADDITION = 'Дополнение'
    CIRCUMSTANCE = 'Обстоятельство'
    UNKNOWN = ''


class Lexeme:
    lexeme = ''
    tags = None
    part_of_sent = None

    def __lt__(self, other):
        return True if self.lexeme < other.lexeme else False

    def __le__(self, other):
        return True if self.lexeme <= other.lexeme else False

    def __eq__(self, other):
        return True if self.lexeme == other.lexeme else False

    def __ne__(self, other):
        return True if self.lexeme != other.lexeme else False

    def __gt__(self, other):
        return True if self.lexeme > other.lexeme else False

    def __ge__(self, other):
        return True if self.lexeme >= other.lexeme else False


def get_words_from_text(text: str) -> list:
    sentences = sent_tokenize(text)
    words = []
    for sentence in sentences:
        for word in word_tokenize(sentence):
            if word != '.':
                words.append(word.lower())
    return words


def get_lexemes_from_text(text: str) -> list:
    lexemes = []
    words = get_words_from_text(text)
    morph = MorphAnalyzer()
    has_subject = False
    for word in words:
        le = morph.parse(word)[0]
        lexeme = Lexeme()
        lexeme.lexeme = word
        lexeme.tags = le.tag.cyr_repr
        lexeme.part_of_sent = get_part_of_sent(le.tag, has_subject).value
        if lexeme.part_of_sent == 'Подлежащее':
            has_subject = True
        lexemes.append(lexeme)
    return lexemes


def get_part_of_sent(tags: OpencorporaTag, has_subject: bool) -> RuPartOfSent:
    if tags.POS == 'NOUN' and tags.case == 'nomn':
        return RuPartOfSent.SUBJECT
    elif tags.POS == 'NOUN':
        return RuPartOfSent.ADDITION
    elif tags.POS == 'NPRO' and has_subject:
        return RuPartOfSent.ADDITION
    elif tags.POS == 'NPRO':
        return RuPartOfSent.SUBJECT
    for i in part_of_sentence.items():
        if tags.POS in i[1]:
            return RuPartOfSent[i[0].upper()]
    return RuPartOfSent.UNKNOWN


if __name__ == '__main__':
    download('punkt', quiet=True)
    te = input('Enter text: ')
    les = get_lexemes_from_text(te)
    for i in enumerate(les):
        print(i[1].lexeme, i[1].tags, i[1].part_of_sent)
