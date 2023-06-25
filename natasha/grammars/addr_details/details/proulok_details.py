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


PROULOK_DETAILS_WORDS1 = or_(
    rule(
            caseless('тер'),
            DOT.optional()
        )
)


PROULOK_DETAILS_WORDS2 = or_(
    rule(caseless('СНТ')),
    rule(caseless('ДНТ')),
    rule(caseless('ТСН')),
)

PROULOK_DETAILS = or_(
    rule(OPEN_PARENTHESIS, ADDR_NAME, NOUN, PROULOK_DETAILS_WORDS1, PROULOK_DETAILS_WORDS2, CLOSE_PARENTHESIS),
)
