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


from ..tokens import DASH, DOT, OPEN_PARENTHESIS, CLOSE_PARENTHESIS, SLASH
from ..tokens import ADJF, ADJS, PRTS, COMP, ADVB, NOUN, VERB, INT, TITLE, ANUM

from ..addr_name import ADDR_NAME


STREET_DETAILS_TER_WORDS1 = or_(
    rule(
            caseless('тер'),
            DOT.optional()
        )
)

STREET_DETAILS_TER_WORDS2 = or_(
    rule(caseless('СНТ')),
    rule(caseless('СН')),
    rule(caseless('ДНТ')),
    rule(caseless('ТСН')),
    rule(caseless('ГСК')),
    rule(caseless('ДНП')),
    rule(caseless('ОНТ')),
)

STREET_DETAILS_TER = or_(
    rule(STREET_DETAILS_TER_WORDS1, STREET_DETAILS_TER_WORDS2),
    rule(STREET_DETAILS_TER_WORDS2, NOUN, STREET_DETAILS_TER_WORDS1, STREET_DETAILS_TER_WORDS2),
    rule(STREET_DETAILS_TER_WORDS2, NOUN, STREET_DETAILS_TER_WORDS1),
    rule(STREET_DETAILS_TER_WORDS2, NOUN, DASH, INT, STREET_DETAILS_TER_WORDS1),
    rule(STREET_DETAILS_TER_WORDS2, ADJF, DASH, ADJF, STREET_DETAILS_TER_WORDS1),
    rule(STREET_DETAILS_TER_WORDS2, ADJF, NOUN, STREET_DETAILS_TER_WORDS1),
    rule(STREET_DETAILS_TER_WORDS2, ADJF, NOUN, DASH, INT, STREET_DETAILS_TER_WORDS1),
    rule(STREET_DETAILS_TER_WORDS2, ADJF, STREET_DETAILS_TER_WORDS1),

    rule(STREET_DETAILS_TER_WORDS2, NOUN, NOUN, STREET_DETAILS_TER_WORDS1),
    rule(STREET_DETAILS_TER_WORDS2, NOUN, INT, STREET_DETAILS_TER_WORDS1),

    rule(STREET_DETAILS_TER_WORDS1),
)

STREET_DETAILS_MKR_WORDS1 = or_(
    rule(
            caseless('мкр'),
            DOT.optional()
        )
)

STREET_DETAILS_MKR = or_(
    rule(NOUN, STREET_DETAILS_MKR_WORDS1),
    rule(ADJF, STREET_DETAILS_MKR_WORDS1),
    rule(ADJF, NOUN, STREET_DETAILS_MKR_WORDS1),
)

STREET_DETAILS_WORDS3 = or_(
    rule(OPEN_PARENTHESIS, normalized('рыбсовхоз'), CLOSE_PARENTHESIS),
    rule(OPEN_PARENTHESIS, INT, '-', INT, normalized('поле'), CLOSE_PARENTHESIS),
    rule(caseless('гск')),
)

STREET_NAME_NUMERIC_PART = or_(
    rule(INT),
    rule('-', INT),
)

STREET_DETAILS = or_(
    rule(OPEN_PARENTHESIS, ADDR_NAME, NOUN, STREET_NAME_NUMERIC_PART.optional(), STREET_DETAILS_WORDS3.optional(), STREET_DETAILS_TER, CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, NOUN, STREET_NAME_NUMERIC_PART.optional(), STREET_DETAILS_WORDS3.optional(), STREET_DETAILS_TER, CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, NOUN, NOUN, STREET_NAME_NUMERIC_PART.optional(), STREET_DETAILS_WORDS3.optional(), STREET_DETAILS_TER, CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, ADJF, STREET_NAME_NUMERIC_PART.optional(), STREET_DETAILS_WORDS3.optional(), STREET_DETAILS_TER, CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, NOUN, STREET_DETAILS_TER, CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, STREET_DETAILS_TER, CLOSE_PARENTHESIS.optional()),

    rule(OPEN_PARENTHESIS, NOUN, NOUN, ADJF, NOUN, caseless('т'), CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, STREET_DETAILS_TER_WORDS2, NOUN, DASH, NOUN, caseless('те'), CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, NOUN, NOUN, ADJF, NOUN, CLOSE_PARENTHESIS.optional()),

    rule(OPEN_PARENTHESIS, NOUN, STREET_NAME_NUMERIC_PART.optional(), STREET_DETAILS_WORDS3.optional(), CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, ADJF, STREET_NAME_NUMERIC_PART.optional(), STREET_DETAILS_WORDS3.optional(), CLOSE_PARENTHESIS.optional()),

    rule(OPEN_PARENTHESIS, INT, caseless('зона'), CLOSE_PARENTHESIS.optional()),

    rule(OPEN_PARENTHESIS, STREET_DETAILS_MKR, STREET_NAME_NUMERIC_PART.optional(), STREET_DETAILS_WORDS3.optional(), CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, STREET_DETAILS_MKR, STREET_NAME_NUMERIC_PART.optional(), STREET_DETAILS_WORDS3.optional(), CLOSE_PARENTHESIS.optional()),
)
