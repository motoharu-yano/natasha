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


##########
#
#  SETTLEMENT NAME
#
##########


SIMPLE = and_(
    or_(
        NOUN,  # Александровка, Заречье, Горки
        ADJS,  # Кузнецово
        ADJF,  # Никольское, Новая, Марьино
    ),
    TITLE,
    not_(normalized('линия')),
    not_(normalized('переулок')),
)

COMPLEX = rule(
    SIMPLE,
    DASH.optional(),
    SIMPLE
)

NAME = or_(
    rule(SIMPLE),
    COMPLEX
)

SETTLEMENT_NAME = or_(
    NAME,
    rule(NAME, '-', INT),
    rule(NAME, ANUM)
)

