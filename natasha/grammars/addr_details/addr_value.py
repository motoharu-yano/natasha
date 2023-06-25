from yargy import (
    rule,
    or_, and_, not_
)
from yargy.interpretation import fact
from yargy.predicates import (
    eq, lte, gte, gram, type, tag,
    length_eq,
    in_, in_caseless, dictionary,
    normalized, caseless,
    is_title
)
from yargy.pipelines import morph_pipeline
from yargy.tokenizer import QUOTES


from .tokens import DASH, DOT, OPEN_PARENTHESIS, CLOSE_PARENTHESIS, SLASH
from .tokens import ADJF, ADJS, PRTS, COMP, ADVB, NOUN, VERB, INT, TITLE, ANUM


##############
#
#   ADDR VALUE
#
#############


LETTER = in_caseless(set('абвгдежзиклмнопрстуфхцчшщэюя'))

QUOTE = in_(QUOTES)

LETTER = or_(
    rule(LETTER),
    rule(QUOTE, LETTER, QUOTE)
)

IDENTIFICATION_ELEMENT_OF_ADDRESSED_OBJECT_PREFIX = or_(
    rule(
        caseless('двлд'),  # домовладение
    ),
    rule(
        caseless('влд'),  # владение
    ),
    rule(
        caseless('зд'),  # здание
    ),
    rule(
        caseless('влд'),  # владение
    ),
    rule(
        caseless('г'), '-', caseless('ж'), # гараж
    ),
)

LITER_RULE = or_(
    rule(caseless('литер')),
    rule(caseless('литерБ')),
    rule(caseless('литерВ')),
    rule(caseless('литерД')),
)

IDENTIFICATION_ELEMENT_OF_ADDRESSED_OBJECT_POSTFIX = or_(
    rule(
        caseless('соор'),  # сооружение
    ),
    rule(
        caseless('стр'),  # строение
    ),
    rule(
        LITER_RULE
    ),
)

HOUSE_ROOM = or_(
    rule(SLASH, INT)
)

DOM_VALUE_EXCEPTIONS = or_(
    rule(INT, caseless('Естр'), INT),  # multiple problems here 1Е considered as первое like Село Ивановское 1е
                                       # another problem that it can not distinguish first letter of house Е and lower case letters стр
                                       # it thinks that this is one word
    rule(INT, caseless('Астр'), INT),
    rule(INT, caseless('Бстр'), INT),
    rule(INT, caseless('Встр'), INT),
    rule(INT, caseless('Гстр'), INT),
    rule(INT, caseless('Дстр'), INT),
    rule(INT, caseless('Жстр'), INT),
    rule(INT, caseless('Истр'), INT),
    rule(INT, caseless('Пстр'), INT),
    rule(INT, caseless('Рстр'), INT),
    rule(INT, caseless('Устр'), INT),

    rule(INT, caseless('Асоор'), INT),

    rule(INT, caseless('ка')),  # not sure what is going on here, maybe rule for only 1 letter after number is interfering, or корпус or word ending ка
    rule(INT, caseless('кб')),
    rule(INT, caseless('кв'), HOUSE_ROOM.optional()),
    rule(INT, caseless('кг')),
    rule(INT, caseless('кд')),
    rule(INT, caseless('ке')),
    rule(INT, caseless('кж')),
    rule(INT, caseless('ки')),
    rule(INT, caseless('вс')),

    rule(INT, caseless('ат')),
    rule(INT, caseless('гп')),
    rule(INT, caseless('тп')),
    rule(INT, caseless('эс')),
    rule(INT, caseless('пс')),
    rule(INT, caseless('ак'), INT),
    rule(INT, caseless('кк')),

    rule(INT, caseless('гкв')),
)

HOUSE_PART_NUMBER = or_(
    rule(INT),
)

HOUSE_PART = or_(
    rule(SLASH, HOUSE_PART_NUMBER.optional(), 'РП'),
    rule(SLASH, HOUSE_PART_NUMBER.optional(), 'ТП'),
    rule(SLASH, INT),
)

# house number with optional letter in the end
VALUE = or_(
    DOM_VALUE_EXCEPTIONS,
    rule(INT, caseless('к'), INT),  # корпус
    rule(INT, LETTER, HOUSE_PART.optional()),
    rule(INT, HOUSE_PART.optional()),
    rule(INT)
)

SEP = in_(r'/\-_')

VALUE = or_(
    rule(IDENTIFICATION_ELEMENT_OF_ADDRESSED_OBJECT_PREFIX, VALUE),
    rule(VALUE, IDENTIFICATION_ELEMENT_OF_ADDRESSED_OBJECT_POSTFIX, VALUE),
    rule(IDENTIFICATION_ELEMENT_OF_ADDRESSED_OBJECT_POSTFIX, VALUE),
    rule(IDENTIFICATION_ELEMENT_OF_ADDRESSED_OBJECT_POSTFIX, VALUE, SEP, VALUE),
    rule(IDENTIFICATION_ELEMENT_OF_ADDRESSED_OBJECT_PREFIX, VALUE, IDENTIFICATION_ELEMENT_OF_ADDRESSED_OBJECT_POSTFIX),
    rule(IDENTIFICATION_ELEMENT_OF_ADDRESSED_OBJECT_PREFIX, VALUE, IDENTIFICATION_ELEMENT_OF_ADDRESSED_OBJECT_POSTFIX, VALUE),
    rule(IDENTIFICATION_ELEMENT_OF_ADDRESSED_OBJECT_PREFIX, VALUE, SEP, VALUE),
    rule(IDENTIFICATION_ELEMENT_OF_ADDRESSED_OBJECT_PREFIX, VALUE, SEP, VALUE, SEP, VALUE),
    rule(VALUE),  # house number with optional letter
    rule(VALUE, SEP, VALUE),  # house number with optional letter, sep, another house number with optional letter
    rule(VALUE, SEP, LETTER)  # house number with optional letter, sep, letter
)

ADDR_VALUE = rule(
    eq('№').optional(),
    VALUE
)
