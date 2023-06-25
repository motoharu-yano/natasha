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


ALLEY_DETAILS_TER_WORDS1 = or_(
    rule(
            caseless('тер'),
            DOT.optional()
        )
)

ALLEY_DETAILS_TER_WORDS2 = or_(
    rule(caseless('СНТ')),
    rule(caseless('СН')),
    rule(caseless('ДНТ')),
    rule(caseless('ТСН')),
    rule(caseless('ГСК')),
)

ALLEY_DETAILS_TER = or_(
    rule(ALLEY_DETAILS_TER_WORDS1, ALLEY_DETAILS_TER_WORDS2),
    rule(ALLEY_DETAILS_TER_WORDS2, NOUN, ALLEY_DETAILS_TER_WORDS1, ALLEY_DETAILS_TER_WORDS2),
    rule(ALLEY_DETAILS_TER_WORDS2, NOUN, ALLEY_DETAILS_TER_WORDS1),
    rule(ALLEY_DETAILS_TER_WORDS2, NOUN, DASH, INT, ALLEY_DETAILS_TER_WORDS1),
    rule(ALLEY_DETAILS_TER_WORDS2, ADJF, DASH, ADJF, ALLEY_DETAILS_TER_WORDS1),
    rule(ALLEY_DETAILS_TER_WORDS2, ADJF, NOUN, ALLEY_DETAILS_TER_WORDS1),
    rule(ALLEY_DETAILS_TER_WORDS2, ADJF, NOUN, DASH, INT, ALLEY_DETAILS_TER_WORDS1),
    rule(ALLEY_DETAILS_TER_WORDS2, ADJF, ALLEY_DETAILS_TER_WORDS1),

    rule(ALLEY_DETAILS_TER_WORDS1),
)

ALLEY_NAME_NUMERIC_PART = or_(
    rule(INT),
    rule('-', INT),
)


ALLEY_DETAILS = or_(
    rule(OPEN_PARENTHESIS, ADDR_NAME, NOUN, ALLEY_NAME_NUMERIC_PART.optional(), ALLEY_DETAILS_TER, CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, NOUN, ALLEY_NAME_NUMERIC_PART.optional(), ALLEY_DETAILS_TER, CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, NOUN, NOUN, ALLEY_NAME_NUMERIC_PART.optional(), ALLEY_DETAILS_TER, CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, ADJF, ALLEY_NAME_NUMERIC_PART.optional(), ALLEY_DETAILS_TER, CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, NOUN, ALLEY_DETAILS_TER, CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, ALLEY_DETAILS_TER, CLOSE_PARENTHESIS.optional()),

    rule(OPEN_PARENTHESIS, NOUN, ALLEY_NAME_NUMERIC_PART.optional(), CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, ADJF, ALLEY_NAME_NUMERIC_PART.optional(), CLOSE_PARENTHESIS.optional()),
)