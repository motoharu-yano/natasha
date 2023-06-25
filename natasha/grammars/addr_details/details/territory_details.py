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


TERRITORY_DETAILS = or_(
    rule(OPEN_PARENTHESIS, normalized('рыбсовхоз'), CLOSE_PARENTHESIS),
    rule(OPEN_PARENTHESIS, INT, '-', INT, normalized('поле'), CLOSE_PARENTHESIS),
    rule(OPEN_PARENTHESIS, INT, CLOSE_PARENTHESIS),
    rule(OPEN_PARENTHESIS, NOUN, INT, caseless('тер'), DOT.optional(), caseless('с'), CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, ADJF, caseless('района'), CLOSE_PARENTHESIS),
    rule(OPEN_PARENTHESIS, caseless('сибтяжмаш'), CLOSE_PARENTHESIS),
    rule(OPEN_PARENTHESIS, caseless('ЛДК'), DASH, INT,  CLOSE_PARENTHESIS),
)
