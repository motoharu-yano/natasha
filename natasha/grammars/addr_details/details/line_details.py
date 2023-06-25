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


LINE_DETAILS_WORDS1 = or_(
    rule(
            caseless('тер'),
            DOT.optional()
        )
)

LINE_DETAILS_WORDS2 = or_(
    rule(caseless('СНТ')),
    rule(caseless('ДНТ')),
    rule(caseless('ТСН')),
)

LINE_DETAILS = or_(
    rule(OPEN_PARENTHESIS, NOUN, LINE_DETAILS_WORDS1, LINE_DETAILS_WORDS2, CLOSE_PARENTHESIS),
    rule(OPEN_PARENTHESIS, caseless('хах'), LINE_DETAILS_WORDS1, LINE_DETAILS_WORDS2, CLOSE_PARENTHESIS),
)
