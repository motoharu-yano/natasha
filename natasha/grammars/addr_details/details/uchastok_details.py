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

from ..settlement_name import SETTLEMENT_NAME


UCHASTOK_DETAILS_TER_WORDS1 = or_(
    rule(
            caseless('тер'),
            DOT.optional()
        )
)

UCHASTOK_DETAILS_TER_WORDS2 = or_(
    rule(caseless('СНТ')),
    rule(caseless('СН')),
    rule(caseless('ДНТ')),
    rule(caseless('ТСН')),
    rule(caseless('ГСК')),
)

UCHASTOK_DETAILS_TER = or_(
    rule(UCHASTOK_DETAILS_TER_WORDS1, UCHASTOK_DETAILS_TER_WORDS2),
    rule(UCHASTOK_DETAILS_TER_WORDS2, NOUN, UCHASTOK_DETAILS_TER_WORDS1, UCHASTOK_DETAILS_TER_WORDS2),
    rule(UCHASTOK_DETAILS_TER_WORDS2, NOUN, UCHASTOK_DETAILS_TER_WORDS1),
    rule(UCHASTOK_DETAILS_TER_WORDS2, NOUN, DASH, INT, UCHASTOK_DETAILS_TER_WORDS1),
    rule(UCHASTOK_DETAILS_TER_WORDS2, ADJF, DASH, ADJF, UCHASTOK_DETAILS_TER_WORDS1),

    rule(UCHASTOK_DETAILS_TER_WORDS1),
    rule(UCHASTOK_DETAILS_TER_WORDS1, UCHASTOK_DETAILS_TER_WORDS2),
    rule(UCHASTOK_DETAILS_TER_WORDS1, caseless('с')),
)

UCHASTOK_NAME_NUMERIC_PART = or_(
    rule(INT),
    rule('-', INT),
)

UCHASTOK_DETAILS = or_(
    rule(OPEN_PARENTHESIS, SETTLEMENT_NAME, NOUN, UCHASTOK_NAME_NUMERIC_PART.optional(), UCHASTOK_DETAILS_TER, CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, NOUN, UCHASTOK_NAME_NUMERIC_PART.optional(), UCHASTOK_DETAILS_TER, CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, ADJF, UCHASTOK_NAME_NUMERIC_PART.optional(), UCHASTOK_DETAILS_TER, CLOSE_PARENTHESIS.optional()),

    rule(OPEN_PARENTHESIS, NOUN, NOUN, UCHASTOK_NAME_NUMERIC_PART.optional(), UCHASTOK_DETAILS_TER, CLOSE_PARENTHESIS.optional()),

    rule(OPEN_PARENTHESIS, UCHASTOK_DETAILS_TER, CLOSE_PARENTHESIS.optional()),

    rule(OPEN_PARENTHESIS, NOUN, UCHASTOK_NAME_NUMERIC_PART.optional(), CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, ADJF, UCHASTOK_NAME_NUMERIC_PART.optional(), CLOSE_PARENTHESIS.optional()),
)