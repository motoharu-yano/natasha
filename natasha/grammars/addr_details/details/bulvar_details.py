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


BULVAR_DETAILS_TER_WORDS1 = or_(
    rule(
            caseless('тер'),
            DOT.optional()
        )
)

BULVAR_DETAILS_TER_WORDS2 = or_(
    rule(caseless('СНТ')),
    rule(caseless('СН')),
    rule(caseless('ДНТ')),
    rule(caseless('ТСН')),
    rule(caseless('ГСК')),
)

BULVAR_DETAILS_TER = or_(
    rule(BULVAR_DETAILS_TER_WORDS1, BULVAR_DETAILS_TER_WORDS2),
    rule(BULVAR_DETAILS_TER_WORDS2, NOUN, BULVAR_DETAILS_TER_WORDS1, BULVAR_DETAILS_TER_WORDS2),
    rule(BULVAR_DETAILS_TER_WORDS2, NOUN, BULVAR_DETAILS_TER_WORDS1),
    rule(BULVAR_DETAILS_TER_WORDS2, NOUN, DASH, INT, BULVAR_DETAILS_TER_WORDS1),
    rule(BULVAR_DETAILS_TER_WORDS2, ADJF, DASH, ADJF, BULVAR_DETAILS_TER_WORDS1),
    rule(BULVAR_DETAILS_TER_WORDS2, ADJF, NOUN, BULVAR_DETAILS_TER_WORDS1),
    rule(BULVAR_DETAILS_TER_WORDS2, ADJF, NOUN, DASH, INT, BULVAR_DETAILS_TER_WORDS1),
    rule(BULVAR_DETAILS_TER_WORDS2, ADJF, BULVAR_DETAILS_TER_WORDS1),

    rule(BULVAR_DETAILS_TER_WORDS1),
)

BULVAR_NAME_NUMERIC_PART = or_(
    rule(INT),
    rule('-', INT),
)

BULVAR_DETAILS = or_(
    rule(OPEN_PARENTHESIS, ADDR_NAME, NOUN, BULVAR_NAME_NUMERIC_PART.optional(), BULVAR_DETAILS_TER, CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, NOUN, BULVAR_NAME_NUMERIC_PART.optional(), BULVAR_DETAILS_TER, CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, NOUN, NOUN, BULVAR_NAME_NUMERIC_PART.optional(), BULVAR_DETAILS_TER, CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, ADJF, BULVAR_NAME_NUMERIC_PART.optional(), BULVAR_DETAILS_TER, CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, NOUN, BULVAR_DETAILS_TER, CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, BULVAR_DETAILS_TER, CLOSE_PARENTHESIS.optional()),

    rule(OPEN_PARENTHESIS, NOUN, BULVAR_NAME_NUMERIC_PART.optional(), CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, ADJF, BULVAR_NAME_NUMERIC_PART.optional(), CLOSE_PARENTHESIS.optional()),
)
