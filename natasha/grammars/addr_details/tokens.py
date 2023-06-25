
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


DASH = eq('-')
DOT = eq('.')
OPEN_PARENTHESIS = eq('(')
CLOSE_PARENTHESIS  = eq(')')
SLASH  = eq('/')

ADJF = gram('ADJF')
ADJS = gram('ADJS')
PRTS = gram('PRTS')
COMP = gram('COMP')
ADVB = gram('ADVB')
NOUN = gram('NOUN')
VERB = gram('VERB')
INT = type('INT')
TITLE = is_title()

ANUM = rule(
    INT,
    DASH.optional(),
    in_caseless({
        'я', 'й', 'е',
        'ое', 'ая', 'ий', 'ой'
    })
)
