
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


Index = fact(
    'Index',
    ['value']
)
Country = fact(
    'Country',
    ['name']
)
Region = fact(
    'Region',
    ['name', 'type']
)
Raion = fact(
    'Raion',
    ['name', 'type']
)
Settlement = fact(
    'Settlement',
    ['name', 'type']
)
Street = fact(
    'Street',
    ['name', 'type']
)
Building = fact(
    'Building',
    ['number', 'type']
)
Room = fact(
    'Room',
    ['number', 'type']
)
AddrPart = fact(
    'AddrPart',
    ['value']
)


def value(key):
    @property
    def field(self):
        return getattr(self, key)
    return field


class Index(Index):
    type = 'индекс'


# correlates with kladr position 0
class Country(Country):
    type = 'страна'
    value = value('name')


# correlates with kladr position 1
class Region(Region):
    value = value('name')


# correlates with kladr position 2
class Raion(Raion):
    value = value('name')


# correlates with kladr position 3
class Settlement(Settlement):
    value = value('name')


# correlates with kladr position 4
class Street(Settlement):
    value = value('name')


# correlates with kladr position 5
class Building(Building):
    value = value('number')


class Room(Room):
    value = value('number')


class AddrPart(AddrPart):
    @property
    def obj(self):
        from natasha import obj

        part = self.value
        return obj.AddrPart(part.value, part.type)


DASH = eq('-')
DOT = eq('.')
OPEN_PARENTHESIS = eq('(')
CLOSE_PARENTHESIS  = eq(')')
SLASH  = eq('/')

ADJF = gram('ADJF')
NOUN = gram('NOUN')
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


#########
#
#  STRANA
#
##########


# TODO
COUNTRY_VALUE = dictionary({
    'россия',
    'украина'
})

ABBR_COUNTRY_VALUE = in_caseless({
    'рф'
})

COUNTRY = or_(
    COUNTRY_VALUE,
    ABBR_COUNTRY_VALUE
).interpretation(
    Country.name
).interpretation(
    Country
)


#############
#
#  FED OKRUGA
#
############


FED_OKRUG_NAME = or_(
    rule(
        dictionary({
            'дальневосточный',
            'приволжский',
            'сибирский',
            'уральский',
            'центральный',
            'южный',
        })
    ),
    rule(
        caseless('северо'),
        DASH.optional(),
        dictionary({
            'западный',
            'кавказский'
        })
    )
).interpretation(
    Region.name
)

FED_OKRUG_WORDS = or_(
    rule(
        normalized('федеральный'),
        normalized('округ')
    ),
    rule(caseless('фо'))
).interpretation(
    Region.type.const('федеральный округ')
)

FED_OKRUG = rule(
    FED_OKRUG_WORDS,
    FED_OKRUG_NAME
).interpretation(
    Region
)


#########
#
#   RESPUBLIKA
#
############


RESPUBLIKA_WORDS = or_(
    rule(caseless('респ'), DOT.optional()),
    rule(normalized('республика'))
).interpretation(
    Region.type.const('республика')
)

RESPUBLIKA_ADJF = or_(
    rule(
        dictionary({
            'удмуртский',
            'чеченский',
            'чувашский',
        })
    ),
    rule(
        caseless('карачаево'),
        DASH.optional(),
        normalized('черкесский')
    ),
    rule(
        caseless('кабардино'),
        DASH.optional(),
        normalized('балкарский')
    )
).interpretation(
    Region.name
)

RESPUBLIKA_NAME = or_(
    rule(
        dictionary({
            'адыгея',
            'алтай',
            'башкортостан',
            'бурятия',
            'дагестан',
            'ингушетия',
            'калмыкия',
            'карелия',
            'коми',
            'крым',
            'мордовия',
            'татарстан',
            'тыва',
            'удмуртия',
            'хакасия',
            'саха',
            'якутия',
        })
    ),
    rule(caseless('марий'), caseless('эл')),
    rule(
        normalized('северный'), normalized('осетия'),
        rule('-', normalized('алания')).optional()
    )
).interpretation(
    Region.name
)

RESPUBLIKA_ABBR = in_caseless({
    'кбр',
    'кчр',
    'рт',  # Татарстан
}).interpretation(
    Region.name  # TODO type
)

RESPUBLIKA = or_(
    rule(RESPUBLIKA_ADJF, RESPUBLIKA_WORDS),
    rule(RESPUBLIKA_WORDS, RESPUBLIKA_NAME),
    rule(RESPUBLIKA_ABBR)
).interpretation(
    Region
)


##########
#
#   KRAI
#
########


KRAI_WORDS = normalized('край').interpretation(
    Region.type.const('край')
)

KRAI_NAME = dictionary({
    'алтайский',
    'забайкальский',
    'камчатский',
    'краснодарский',
    'красноярский',
    'пермский',
    'приморский',
    'ставропольский',
    'хабаровский',
}).interpretation(
    Region.name
)

KRAI = rule(
    KRAI_NAME, KRAI_WORDS
).interpretation(
    Region
)


############
#
#    OBLAST
#
############


OBLAST_WORDS = or_(
    rule(normalized('область')),
    rule(
        caseless('обл'),
        DOT.optional()
    )
).interpretation(
    Region.type.const('область')
)

OBLAST_NAME = dictionary({
    'амурский',
    'архангельский',
    'астраханский',
    'белгородский',
    'брянский',
    'владимирский',
    'волгоградский',
    'вологодский',
    'воронежский',
    'горьковский',
    'ивановский',
    'ивановский',
    'иркутский',
    'калининградский',
    'калужский',
    'камчатский',
    'кемеровский',
    'кировский',
    'костромской',
    'курганский',
    'курский',
    'ленинградский',
    'липецкий',
    'магаданский',
    'московский',
    'мурманский',
    'нижегородский',
    'новгородский',
    'новосибирский',
    'омский',
    'оренбургский',
    'орловский',
    'пензенский',
    'пермский',
    'псковский',
    'ростовский',
    'рязанский',
    'самарский',
    'саратовский',
    'сахалинский',
    'свердловский',
    'смоленский',
    'тамбовский',
    'тверской',
    'томский',
    'тульский',
    'тюменский',
    'ульяновский',
    'челябинский',
    'читинский',
    'ярославский',
}).interpretation(
    Region.name
)

OBLAST = rule(
    OBLAST_NAME,
    OBLAST_WORDS
).interpretation(
    Region
)


##########
#
#    AUTO OKRUG
#
#############


AUTO_OKRUG_NAME = or_(
    rule(
        dictionary({
            'чукотский',
            'эвенкийский',
            'корякский',
            'ненецкий',
            'таймырский',
            'агинский',
            'бурятский',
        })
    ),
    rule(caseless('коми'), '-', normalized('пермяцкий')),
    rule(caseless('долгано'), '-', normalized('ненецкий')),
    rule(caseless('ямало'), '-', normalized('ненецкий')),
).interpretation(
    Region.name
)

AUTO_OKRUG_WORDS = or_(
    rule(
        normalized('автономный'),
        normalized('округ')
    ),
    rule(caseless('ао'))
).interpretation(
    Region.type.const('автономный округ')
)

HANTI = rule(
    caseless('ханты'), '-', normalized('мансийский')
).interpretation(
    Region.name
)

BURAT = rule(
    caseless('усть'), '-', normalized('ордынский'),
    normalized('бурятский')
).interpretation(
    Region.name
)

AUTO_OKRUG = or_(
    rule(AUTO_OKRUG_NAME, AUTO_OKRUG_WORDS),
    or_(
        rule(
            HANTI,
            AUTO_OKRUG_WORDS,
            '-', normalized('югра')
        ),
        rule(
            caseless('хмао'),
        ).interpretation(Region.name),
        rule(
            caseless('хмао'),
            '-', caseless('югра')
        ).interpretation(Region.name),
    ),
    rule(
        BURAT,
        AUTO_OKRUG_WORDS
    )
).interpretation(
    Region
)


##########
#
#  RAION
#
###########


RAION_WORDS = or_(
    rule(caseless('р'), '-', in_caseless({'он', 'н'}), DOT.optional()),
    rule(normalized('район'))
).interpretation(
    Raion.type.const('район')
)

RAION_SIMPLE_NAME = and_(
    ADJF,
    TITLE
)

RAION_MODIFIERS = rule(
    in_caseless({
        'усть',
        'северо',
        'александрово',
        'гаврилово',
    }),
    DASH.optional(),
    TITLE
)

RAION_COMPLEX_NAME = rule(
    RAION_MODIFIERS,
    RAION_SIMPLE_NAME
)

RAION_NAME = or_(
    rule(RAION_SIMPLE_NAME),
    RAION_COMPLEX_NAME
).interpretation(
    Raion.name
)

RAION = or_(
    rule(RAION_NAME, RAION_WORDS),
    rule(RAION_WORDS, RAION_NAME)
).interpretation(
    Raion
)

###########
#
#   GOROD
#
###########


# Top 200 Russia cities, cover 75% of population

COMPLEX = morph_pipeline([
    'санкт-петербург',
    'нижний новгород',
    'н.новгород',
    'ростов-на-дону',
    'набережные челны',
    'улан-удэ',
    'нижний тагил',
    'комсомольск-на-амуре',
    'йошкар-ола',
    'старый оскол',
    'великий новгород',
    'южно-сахалинск',
    'петропавловск-камчатский',
    'каменск-уральский',
    'орехово-зуево',
    'сергиев посад',
    'новый уренгой',
    'ленинск-кузнецкий',
    'великие луки',
    'каменск-шахтинский',
    'усть-илимск',
    'усолье-сибирский',
    'кирово-чепецк',
])

SIMPLE = dictionary({
    'москва',
    'новосибирск',
    'екатеринбург',
    'казань',
    'самара',
    'омск',
    'челябинск',
    'уфа',
    'волгоград',
    'пермь',
    'красноярск',
    'воронеж',
    'саратов',
    'краснодар',
    'тольятти',
    'барнаул',
    'ижевск',
    'ульяновск',
    'владивосток',
    'ярославль',
    'иркутск',
    'тюмень',
    'махачкала',
    'хабаровск',
    'оренбург',
    'новокузнецк',
    'кемерово',
    'рязань',
    'томск',
    'астрахань',
    'пенза',
    'липецк',
    'тула',
    'киров',
    'чебоксары',
    'калининград',
    'брянск',
    'курск',
    'иваново',
    'магнитогорск',
    'тверь',
    'ставрополь',
    'симферополь',
    'белгород',
    'архангельск',
    'владимир',
    'севастополь',
    'сочи',
    'курган',
    'смоленск',
    'калуга',
    'чита',
    'орёл',
    'волжский',
    'череповец',
    'владикавказ',
    'мурманск',
    'сургут',
    'вологда',
    'саранск',
    'тамбов',
    'стерлитамак',
    'грозный',
    'якутск',
    'кострома',
    'петрозаводск',
    'таганрог',
    'нижневартовск',
    'братск',
    'новороссийск',
    'дзержинск',
    'шахта',
    'нальчик',
    'орск',
    'сыктывкар',
    'нижнекамск',
    'ангарск',
    'балашиха',
    'благовещенск',
    'прокопьевск',
    'химки',
    'псков',
    'бийск',
    'энгельс',
    'рыбинск',
    'балаково',
    'северодвинск',
    'армавир',
    'подольск',
    'королёв',
    'сызрань',
    'норильск',
    'златоуст',
    'мытищи',
    'люберцы',
    'волгодонск',
    'новочеркасск',
    'абакан',
    'находка',
    'уссурийск',
    'березники',
    'салават',
    'электросталь',
    'миасс',
    'первоуральск',
    'рубцовск',
    'альметьевск',
    'ковровый',
    'коломна',
    'керчь',
    'майкоп',
    'пятигорск',
    'одинцово',
    'копейск',
    'хасавюрт',
    'новомосковск',
    'кисловодск',
    'серпухов',
    'новочебоксарск',
    'нефтеюганск',
    'димитровград',
    'нефтекамск',
    'черкесск',
    'дербент',
    'камышин',
    'невинномысск',
    'красногорск',
    'мур',
    'батайск',
    'новошахтинск',
    'ноябрьск',
    'кызыл',
    'октябрьский',
    'ачинск',
    'северск',
    'новокуйбышевск',
    'елец',
    'евпатория',
    'арзамас',
    'обнинск',
    'каспийск',
    'элиста',
    'пушкино',
    'жуковский',
    'междуреченск',
    'сарапул',
    'ессентуки',
    'воткинск',
    'ногинск',
    'тобольск',
    'ухта',
    'серов',
    'бердск',
    'мичуринск',
    'киселёвск',
    'новотроицк',
    'зеленодольск',
    'соликамск',
    'раменский',
    'домодедово',
    'магадан',
    'глазов',
    'железногорск',
    'канск',
    'назрань',
    'гатчина',
    'саров',
    'новоуральск',
    'воскресенск',
    'долгопрудный',
    'бугульма',
    'кузнецк',
    'губкин',
    'кинешма',
    'ейск',
    'реутов',
    'железногорск',
    'чайковский',
    'азов',
    'бузулук',
    'озёрск',
    'балашов',
    'юрга',
    'кропоткин',
    'клин'
})

GOROD_ABBR = in_caseless({
    'спб',
    'мск',
    'нск'   # Новосибирск
})

GOROD_NAME = or_(
    rule(SIMPLE),
    COMPLEX,
    rule(GOROD_ABBR)
).interpretation(
    Settlement.name
)

SIMPLE = and_(
    TITLE,
    or_(
        NOUN,
        ADJF  # Железнодорожный, Юбилейный
    )
)

COMPLEX = or_(
    rule(
        SIMPLE,
        DASH.optional(),
        SIMPLE
    ),
    rule(
        TITLE,
        DASH.optional(),
        caseless('на'),
        DASH.optional(),
        TITLE
    )
)

NAME = or_(
    rule(SIMPLE),
    COMPLEX
)

MAYBE_GOROD_NAME = or_(
    NAME,
    rule(NAME, '-', INT)
).interpretation(
    Settlement.name
)

GOROD_WORDS = or_(
    rule(normalized('город')),
    rule(
        caseless('г'),
        DOT.optional()
    )
).interpretation(
    Settlement.type.const('город')
)

GOROD = or_(
    rule(GOROD_WORDS, MAYBE_GOROD_NAME),
    rule(GOROD_WORDS.optional(), GOROD_NAME
    )
).interpretation(
    Settlement
)


##########
#
#  SETTLEMENT NAME
#
##########


ADJS = gram('ADJS')
SIMPLE = and_(
    or_(
        NOUN,  # Александровка, Заречье, Горки
        ADJS,  # Кузнецово
        ADJF,  # Никольское, Новая, Марьино
    ),
    TITLE,
    not_(caseless('линия')),
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


###########
#
#   SELO
#
#############


SELO_WORDS = or_(
    rule(
        caseless('с'),
        DOT.optional()
    ),
    rule(normalized('село'))
).interpretation(
    Settlement.type.const('село')
)

SELO_NAME = SETTLEMENT_NAME.interpretation(
    Settlement.name
)

SELO = rule(
    SELO_WORDS, SELO_NAME
).interpretation(
    Settlement
)


###########
#
#   AUL
#
#############


AUL_WORDS = or_(
    rule(normalized('аул'))
).interpretation(
    Settlement.type.const('аул')
)

AUL_NAME = SETTLEMENT_NAME.interpretation(
    Settlement.name
)

AUL = rule(
    AUL_WORDS, AUL_NAME
).interpretation(
    Settlement
)


###########
#
#   SNT
#
#############


SNT_WORDS = or_(
    rule(
        caseless('снт'),
        DOT.optional()
    ),
    rule(normalized('садовое'), normalized('неком'), '-', caseless('е'), normalized('товарищество'))
).interpretation(
    Settlement.type.const('cнт')
)

SNT_DETAILS_WORDS1 = or_(
    rule(
            caseless('тер'),
            DOT.optional()
        )
)

SNT_DETAILS_WORDS2 = or_(
    rule(caseless('СНТ')),
    rule(caseless('СН')),
    rule(caseless('ДНТ')),
    rule(caseless('ТСН')),
)

SNT_DETAILS = or_(
    rule(OPEN_PARENTHESIS, normalized('рыбсовхоз'), CLOSE_PARENTHESIS),
    rule(OPEN_PARENTHESIS, INT, caseless('лет'), NOUN, SNT_DETAILS_WORDS1, SNT_DETAILS_WORDS2, CLOSE_PARENTHESIS),
    rule(OPEN_PARENTHESIS, NOUN, SNT_DETAILS_WORDS1, SNT_DETAILS_WORDS2, CLOSE_PARENTHESIS),
    rule(OPEN_PARENTHESIS, normalized('энем'), normalized('пгт'), CLOSE_PARENTHESIS),
    rule(OPEN_PARENTHESIS, normalized('энем'), CLOSE_PARENTHESIS),
)

SNT_NUMERIC_PART = or_(
    rule(INT),
    rule('-', INT),
)

SNT_NAME_VALUE = or_(
    rule(SETTLEMENT_NAME, NOUN, SNT_NUMERIC_PART.optional(), SNT_DETAILS.optional()),
    rule(SETTLEMENT_NAME, SNT_NUMERIC_PART.optional(), SNT_DETAILS.optional()),
    rule(INT, caseless('лет'), 'СА', caseless('и'), 'ВМФ'),
    rule(INT, caseless('лет'), NOUN),
    rule(caseless('хах')),
    rule(SNT_DETAILS_WORDS2, 'N', INT, 'ОСТ', 'ОАО', 'УМПО'),
    rule(SNT_DETAILS_WORDS2, NOUN, SNT_NUMERIC_PART.optional()),
    rule(SNT_DETAILS_WORDS2, ADJF, SNT_NUMERIC_PART.optional()),
)

SNT_NAME = SNT_NAME_VALUE.interpretation(
    Settlement.name
)

SNT = or_(
    rule(SNT_WORDS, SNT_NAME),
).interpretation(
    Settlement
)


###########
#
#   HUTOR
#
#############


HUTOR_WORDS = or_(
    rule(
        caseless('х'),
        DOT.optional()
    ),
    rule(normalized('хутор'))
).interpretation(
    Settlement.type.const('хутор')
)

HUTOR_NAME = SETTLEMENT_NAME.interpretation(
    Settlement.name
)

HUTOR = rule(
    HUTOR_WORDS, HUTOR_NAME
).interpretation(
    Settlement
)


###########
#
#   STANTSIA
#
#############


STANTSIA_WORDS = or_(
    rule(
        caseless('ст'),
        DOT.optional()
    ),
    rule(normalized('станция'))
).interpretation(
    Settlement.type.const('станция')
)

STANTSIA_NAME = SETTLEMENT_NAME.interpretation(
    Settlement.name
)

STANTSIA = rule(
    STANTSIA_WORDS, STANTSIA_NAME
).interpretation(
    Settlement
)

###########
#
#   TERRITORY
#
#############

TERRITORY_ABBREVIATIONS = dictionary({'ДНТ', 'СНТ', 'ТСН'})

TERRITORY_WORDS = or_(
    rule(caseless('тер'), DOT.optional(), TERRITORY_ABBREVIATIONS.optional()),
    rule(normalized('территория'), TERRITORY_ABBREVIATIONS.optional())
).interpretation(
    Settlement.type.const('территория')
)

TERRITORY_DETAILS = or_(
    rule(OPEN_PARENTHESIS, normalized('рыбсовхоз'), CLOSE_PARENTHESIS),
)

TERRITORY_SUB_RULE = and_(
    NOUN,
    not_(caseless('дом'))
)

TERRITORY_NUMERIC_PART = or_(
    rule(INT),
    rule('-', INT),
)

TERRITORY_NAME_VALUE = or_(
    rule(NOUN, TERRITORY_SUB_RULE, TERRITORY_NUMERIC_PART.optional(), TERRITORY_DETAILS.optional()),
    rule(ADJF, TERRITORY_SUB_RULE, TERRITORY_NUMERIC_PART.optional(), TERRITORY_DETAILS.optional()),
    rule(NOUN, TERRITORY_NUMERIC_PART.optional(), TERRITORY_DETAILS.optional()),
    rule(ADJF, TERRITORY_NUMERIC_PART.optional(), TERRITORY_DETAILS.optional()),
    rule(caseless('хах'), TERRITORY_NUMERIC_PART.optional(), TERRITORY_DETAILS.optional()),
    rule(INT, caseless('лет'), NOUN, TERRITORY_DETAILS.optional()),
)

TERRITORY_NAME = TERRITORY_NAME_VALUE.interpretation(
    Settlement.name
)

TERRITORY = rule(
    TERRITORY_WORDS, TERRITORY_NAME
).interpretation(
    Settlement
)


###########
#
#   POSELENIE
#
#############


POSELENIE_WORDS = or_(
    rule(
        caseless('п'),
        DOT.optional()
    ),
    rule(normalized('поселение'))
).interpretation(
    Settlement.type.const('поселение')
)

POS_SUB_RULE = and_(
    NOUN,
    not_(caseless('улица'))
)

POSELENIE_NAME_VALUE = or_(
    rule(NOUN, POS_SUB_RULE),
    rule(NOUN),
    rule(SETTLEMENT_NAME),
)

POSELENIE_NAME = POSELENIE_NAME_VALUE.interpretation(
    Settlement.name
)

POSELENIE = rule(
    POSELENIE_WORDS, POSELENIE_NAME
).interpretation(
    Settlement
)


###########
#
#   SELSKOE POSELENIE
#
#############


SELSKOE_POSELENIE_WORDS = or_(
    rule(
        caseless('с'),
        '/',
        caseless('п'),
        DOT.optional()
    ),
    rule(normalized('сельское'), normalized('поселение'))
).interpretation(
    Settlement.type.const('сельское поселение')
)

POS_SUB_RULE = and_(
    NOUN,
    not_(caseless('улица'))
)

SELSKOE_POSELENIE_NAME_VALUE = or_(
    rule(NOUN, POS_SUB_RULE),
    rule(NOUN),
    rule(SETTLEMENT_NAME),
)

SELSKOE_POSELENIE_NAME = SELSKOE_POSELENIE_NAME_VALUE.interpretation(
    Settlement.name
)

SELSKOE_POSELENIE = rule(
    SELSKOE_POSELENIE_WORDS, SELSKOE_POSELENIE_NAME
).interpretation(
    Settlement
)


###########
#
#   STANITSA
#
#############


STANITSA_WORDS = or_(
    rule(
        caseless('ст'),
        '-',
        caseless('ца'),
    ),
    rule(normalized('станица'))
).interpretation(
    Settlement.type.const('станица')
)

STANITSA_NAME_VALUE = or_(
    rule(NOUN, SETTLEMENT_NAME),
    rule(NOUN),
    rule(SETTLEMENT_NAME),
)

STANITSA_NAME = STANITSA_NAME_VALUE.interpretation(
    Settlement.name
)

STANITSA = rule(
    STANITSA_WORDS, STANITSA_NAME
).interpretation(
    Settlement
)


###########
#
#   DEREVNYA
#
#############


DEREVNYA_WORDS = or_(
    rule(
        caseless('д'),
        DOT.optional()
    ),
    rule(normalized('деревня'))
).interpretation(
    Settlement.type.const('деревня')
)

DEREVNYA_NAME = SETTLEMENT_NAME.interpretation(
    Settlement.name
)

DEREVNYA = rule(
    DEREVNYA_WORDS,
    DEREVNYA_NAME
).interpretation(
    Settlement
)


###########
#
#   POSELOK
#
#############


POSELOK_WORDS = or_(
    rule(
        in_caseless({'п', 'пос'}),
        DOT.optional()
    ),
    rule(normalized('посёлок')),
    rule(
        caseless('р'),
        DOT.optional(),
        caseless('п'),
        DOT.optional()
    ),
    rule(
        normalized('рабочий'),
        normalized('посёлок')
    ),
    rule(
        caseless('пгт'),
        DOT.optional()
    ),
    rule(
        caseless('п'), DOT, caseless('г'), DOT, caseless('т'),
        DOT.optional()
    ),
    rule(
        normalized('посёлок'),
        normalized('городского'),
        normalized('типа'),
    ),
).interpretation(
    Settlement.type.const('посёлок')
)

POSELOK_NAME = SETTLEMENT_NAME.interpretation(
    Settlement.name
)

POSELOK = rule(
    POSELOK_WORDS,
    POSELOK_NAME
).interpretation(
    Settlement
)


##############
#
#   ADDR PERSON
#
############


ABBR = and_(
    length_eq(1),
    is_title()
)

PART = and_(
    TITLE,
    or_(
        gram('Name'),
        gram('Surn')
    )
)

MAYBE_FIO = or_(
    rule(TITLE, PART),
    rule(PART, TITLE),

    rule(TITLE, TITLE, TITLE),

    rule(ABBR, '.', TITLE),
    rule(ABBR, '.', ABBR, '.', TITLE),
    rule(TITLE, ABBR, '.', ABBR, '.')
)

POSITION_WORDS_ = or_(
    rule(
        dictionary({
            'мичман',
            'геолог',
            'подводник',
            'краевед',
            'снайпер',
            'штурман',
            'бригадир',
            'учитель',
            'политрук',
            'военком',
            'ветеран',
            'историк',
            'пулемётчик',
            'авиаконструктор',
            'адмирал',
            'академик',
            'актер',
            'актриса',
            'архитектор',
            'атаман',
            'врач',
            'воевода',
            'генерал',
            'губернатор',
            'хирург',
            'декабрист',
            'разведчик',
            'граф',
            'десантник',
            'конструктор',
            'скульптор',
            'писатель',
            'поэт',
            'капитан',
            'князь',
            'комиссар',
            'композитор',
            'космонавт',
            'купец',
            'лейтенант',
            'лётчик',
            'майор',
            'маршал',
            'матрос',
            'подполковник',
            'полковник',
            'профессор',
            'сержант',
            'старшина',
            'танкист',
            'художник',
            'герой',
            'княгиня',
            'строитель',
            'дружинник',
            'диктор',
            'прапорщик',
            'артиллерист',
            'графиня',
            'большевик',
            'патриарх',
            'сварщик',
            'офицер',
            'рыбак',
            'брат',
        })
    ),
    rule(normalized('генерал'), normalized('армия')),
    rule(normalized('герой'), normalized('россия')),
    rule(
        normalized('герой'),
        normalized('российский'), normalized('федерация')),
    rule(
        normalized('герой'),
        normalized('советский'), normalized('союз')
    ),
)

ABBR_POSITION_WORDS = rule(
    in_caseless({
        'адм',
        'ак',
        'акад',
    }),
    DOT.optional()
)

POSITION_WORDS = or_(
    POSITION_WORDS_,
    ABBR_POSITION_WORDS
)

MAYBE_PERSON = or_(
    MAYBE_FIO,
    rule(POSITION_WORDS, MAYBE_FIO),
    rule(POSITION_WORDS, TITLE)
)


###########
#
#   IMENI
#
##########


IMENI_WORDS = or_(
    rule(
        caseless('им'),
        DOT.optional()
    ),
    rule(caseless('имени'))
)

IMENI = or_(
    rule(
        IMENI_WORDS.optional(),
        MAYBE_PERSON
    ),
    rule(
        IMENI_WORDS,
        TITLE
    )
)

##########
#
#   LET
#
##########


LET_WORDS = or_(
    rule(caseless('лет')),
    rule(
        DASH.optional(),
        caseless('летия')
    )
)

LET_NAME = in_caseless({
    'влксм',
    'ссср',
    'алтая',
    'башкирии',
    'бурятии',
    'дагестана',
    'калмыкии',
    'колхоза',
    'комсомола',
    'космонавтики',
    'москвы',
    'октября',
    'пионерии',
    'победы',
    'приморья',
    'района',
    'совхоза',
    'совхозу',
    'татарстана',
    'тувы',
    'удмуртии',
    'улуса',
    'хакасии',
    'целины',
    'чувашии',
    'якутии',
})

LET = rule(
    INT,
    LET_WORDS,
    LET_NAME
)


##########
#
#    ADDR DATE
#
#############


MONTH_WORDS = dictionary({
    'январь',
    'февраль',
    'март',
    'апрель',
    'май',
    'июнь',
    'июль',
    'август',
    'сентябрь',
    'октябрь',
    'ноябрь',
    'декабрь',
})

DAY = and_(
    INT,
    gte(1),
    lte(31)
)

YEAR = and_(
    INT,
    gte(1),
    lte(2100)
)

YEAR_WORDS = normalized('год')

DATE = or_(
    rule(DAY, MONTH_WORDS),
    rule(YEAR, YEAR_WORDS)
)


#########
#
#   MODIFIER
#
############


MODIFIER_WORDS_ = rule(
    dictionary({
        'большой',
        'малый',
        'средний',

        'верхний',
        'центральный',
        'нижний',
        'северный',
        'дальний',

        'первый',
        'второй',

        'старый',
        'новый',

        'красный',
        'лесной',
        'тихий',
    }),
    DASH.optional()
)

ABBR_MODIFIER_WORDS = rule(
    in_caseless({
        'б', 'м', 'н'
    }),
    DOT.optional()
)

SHORT_MODIFIER_WORDS = rule(
    in_caseless({
        'больше',
        'мало',
        'средне',

        'верх',
        'верхне',
        'центрально',
        'нижне',
        'северо',
        'дальне',
        'восточно',
        'западно',

        'перво',
        'второ',

        'старо',
        'ново',

        'красно',
        'тихо',
        'горно',
    }),
    DASH.optional()
)

MODIFIER_WORDS = or_(
    MODIFIER_WORDS_,
    ABBR_MODIFIER_WORDS,
    SHORT_MODIFIER_WORDS,
)


##########
#
#   ADDR NAME
#
##########


ROD = gram('gent')

SIMPLE = and_(
    or_(
        ADJF,  # Школьная
        and_(NOUN, ROD),  # Ленина, Победы
    ),
    TITLE
)

COMPLEX = or_(
    rule(
        and_(ADJF, TITLE),
        NOUN
    ),
    rule(
        TITLE,
        DASH.optional(),
        TITLE
    ),
)

# TODO
EXCEPTION = dictionary({
    'арбат',
    'варварка'
})

MAYBE_NAME = or_(
    rule(SIMPLE),
    COMPLEX,
    rule(EXCEPTION)
)

NAME = or_(
    MAYBE_NAME,
    LET,
    DATE,
    IMENI
)

NAME = rule(
    MODIFIER_WORDS.optional(),
    NAME
)

ADDR_CRF = tag('I').repeatable()

NAME = or_(
    NAME,
    ANUM,
    rule(NAME, ANUM),
    rule(ANUM, NAME),
    rule(INT, DASH.optional(), NAME),
    rule(NAME, DASH, INT),
    ADDR_CRF
)

ADDR_NAME = NAME


########
#
#    STREET
#
#########


STREET_WORDS = or_(
    rule(normalized('улица')),
    rule(
        caseless('ул'),
        DOT.optional()
    )
).interpretation(
    Street.type.const('улица')
)

STREET_DETAILS_WORDS1 = or_(
    rule(
            caseless('тер'),
            DOT.optional()
        )
)

STREET_DETAILS_WORDS2 = or_(
    rule(caseless('СНТ')),
    rule(caseless('СН')),
    rule(caseless('ДНТ')),
    rule(caseless('ТСН'))
)

STREET_DETAILS_WORDS3 = or_(
    rule(OPEN_PARENTHESIS, normalized('рыбсовхоз'), CLOSE_PARENTHESIS),
)

STREET_NAME_NUMERIC_PART = or_(
    rule(INT),
    rule('-', INT),
)

STREET_DETAILS = or_(
    rule(OPEN_PARENTHESIS, ADDR_NAME, NOUN, STREET_NAME_NUMERIC_PART.optional(), STREET_DETAILS_WORDS3.optional(), STREET_DETAILS_WORDS1, STREET_DETAILS_WORDS2, CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, NOUN, STREET_NAME_NUMERIC_PART.optional(), STREET_DETAILS_WORDS3.optional(), STREET_DETAILS_WORDS1, STREET_DETAILS_WORDS2, CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, NOUN, NOUN, STREET_NAME_NUMERIC_PART.optional(), STREET_DETAILS_WORDS3.optional(), STREET_DETAILS_WORDS1, STREET_DETAILS_WORDS2, CLOSE_PARENTHESIS.optional()),
    rule(OPEN_PARENTHESIS, ADJF, STREET_NAME_NUMERIC_PART.optional(), STREET_DETAILS_WORDS3.optional(), STREET_DETAILS_WORDS1, STREET_DETAILS_WORDS2, CLOSE_PARENTHESIS.optional()),
)

STREET_NAME_VALUE = or_(
    rule(NOUN, ADDR_NAME, STREET_DETAILS.optional()),
    rule(NOUN, STREET_DETAILS.optional()),
    rule(ADDR_NAME, STREET_DETAILS.optional()),
    rule(INT, NOUN, STREET_DETAILS.optional()),
)

STREET_NAME = STREET_NAME_VALUE.interpretation(
    Street.name
)

STREET = or_(
    rule(STREET_WORDS, STREET_NAME),
    rule(STREET_NAME, STREET_WORDS)
).interpretation(
    Street
)


########
#
#    PROULOK
#
#########


PROULOK_WORDS = or_(
    rule(normalized('проулок')),
).interpretation(
    Street.type.const('проулок')
)

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

PROULOK_NAME_VALUE = or_(
    rule(INT.optional(), NOUN, ADDR_NAME, PROULOK_DETAILS.optional()),
    rule(INT.optional(), NOUN, PROULOK_DETAILS.optional()),
    rule(INT.optional(), ADDR_NAME, PROULOK_DETAILS.optional()),
)

PROULOK_NAME = PROULOK_NAME_VALUE.interpretation(
    Street.name
)

PROULOK = or_(
    rule(PROULOK_WORDS, PROULOK_NAME),
    rule(PROULOK_NAME, PROULOK_WORDS)
).interpretation(
    Street
)


########
#
#    DACHNY POSELOK
#
#########


DACHNY_POSELOK_WORDS = or_(
    rule(normalized('дачный'), normalized('поселок')),
    rule(
        caseless('дп'),
        DOT.optional()
    )
).interpretation(
    Street.type.const('дачный поселок')
)

DACHNY_POSELOK_DETAILS_WORDS1 = or_(
    rule(
            caseless('тер'),
            DOT.optional()
        )
)

DACHNY_POSELOK_DETAILS_WORDS2 = or_(
    rule(caseless('СНТ')),
    rule(caseless('ДНТ')),
    rule(caseless('ТСН')),
)

DACHNY_POSELOK_DETAILS = or_(
    rule(OPEN_PARENTHESIS, ADDR_NAME, NOUN, DACHNY_POSELOK_DETAILS_WORDS1, DACHNY_POSELOK_DETAILS_WORDS2, CLOSE_PARENTHESIS),
)

DACHNY_POSELOK_NAME_VALUE = or_(
    rule(INT.optional(), NOUN, ADDR_NAME, DACHNY_POSELOK_DETAILS.optional()),
    rule(INT.optional(), NOUN, DACHNY_POSELOK_DETAILS.optional()),
    rule(INT.optional(), ADDR_NAME, DACHNY_POSELOK_DETAILS.optional()),
)

DACHNY_POSELOK_NAME = DACHNY_POSELOK_NAME_VALUE.interpretation(
    Street.name
)

DACHNY_POSELOK = or_(
    rule(DACHNY_POSELOK_WORDS, DACHNY_POSELOK_NAME),
    rule(DACHNY_POSELOK_NAME, DACHNY_POSELOK_WORDS)
).interpretation(
    Street
)

########
#
#    LINE
#
#########


LINE_WORDS = or_(
    rule(normalized('линия')),
).interpretation(
    Street.type.const('линия')
)

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

LINE_NAME_VALUE = or_(
    rule(INT, '-', caseless('я'), LINE_DETAILS.optional()),
)

LINE_NAME = LINE_NAME_VALUE.interpretation(
    Street.name
)

LINE = or_(
    rule(LINE_WORDS, LINE_NAME),
    rule(LINE_NAME, LINE_WORDS)
).interpretation(
    Street
)

########
#
#    DOROGA
#
#########


DOROGA_WORDS = or_(
    rule(
        caseless('дор'),
        DOT.optional()
    ),
    rule(normalized('дорога'))
).interpretation(
    Street.type.const('дорога')
)

SEP = in_(r'/')

DOROGA_PREFIX = or_(
    rule(caseless('а'), SEP, caseless('д')),
)

LETTER = in_caseless(set('абвгдежзиклмнопрстуфхшщэюя'))

DOROGA_NAME_COMPLEX = or_(
    rule(ADDR_NAME, LETTER, ADDR_NAME),
    # first word is not ADJF which is specified in ADDR_NAME and ADDR_NAME does not allow single lowercase letters, so wrote another rule
    rule(NOUN, LETTER, ADDR_NAME),  # Дорога А/Д Подъезд к Гавердовскому
    rule(NOUN, LETTER, dictionary({'п', 'с'}), DOT.optional(), ADDR_NAME), #  Дорога А/Д Подъезд к п. Удобный
    rule(NOUN, '-', NOUN, '-', NOUN),
    rule(ADDR_NAME),
)

DOROGA_NAME_VALUE = or_(
    rule(DOROGA_PREFIX, DOROGA_NAME_COMPLEX),
    rule(DOROGA_NAME_COMPLEX),
)

DOROGA_VALUE = DOROGA_NAME_VALUE.interpretation(
    Street.name
)

DOROGA = or_(
    rule(DOROGA_WORDS, DOROGA_VALUE),
    rule(DOROGA_VALUE, DOROGA_WORDS)
).interpretation(
    Street
)


##########
#
#    PROSPEKT
#
##########


PROSPEKT_WORDS = or_(
    rule(
        in_caseless({'пр', 'просп'}),
        DOT.optional()
    ),
    rule(
        caseless('пр'),
        '-',
        in_caseless({'кт', 'т'}),
        DOT.optional()
    ),
    rule(normalized('проспект'))
).interpretation(
    Street.type.const('проспект')
)

PROSPEKT_NAME = ADDR_NAME.interpretation(
    Street.name
)

PROSPEKT = or_(
    rule(PROSPEKT_WORDS, PROSPEKT_NAME),
    rule(PROSPEKT_NAME, PROSPEKT_WORDS)
).interpretation(
    Street
)


############
#
#    PROEZD
#
#############


PROEZD_WORDS = or_(
    rule(caseless('пр'), DOT.optional()),
    rule(
        caseless('пр'),
        '-',
        in_caseless({'зд', 'д'}),
        DOT.optional()
    ),
    rule(normalized('проезд'))
).interpretation(
    Street.type.const('проезд')
)

PROEZD_NAME = ADDR_NAME.interpretation(
    Street.name
)

PROEZD = or_(
    rule(PROEZD_WORDS, PROEZD_NAME),
    rule(PROEZD_NAME, PROEZD_WORDS)
).interpretation(
    Street
)


###########
#
#   PEREULOK
#
##############


PEREULOK_WORDS = or_(
    rule(
        caseless('п'),
        DOT
    ),
    rule(
        caseless('пер'),
        DOT.optional()
    ),
    rule(normalized('переулок'))
).interpretation(
    Street.type.const('переулок')
)

PEREULOK_DETAILS_WORDS1 = or_(
    rule(
            caseless('тер'),
            DOT.optional()
        )
)

PEREULOK_DETAILS_WORDS2 = or_(
    rule(caseless('СНТ')),
    rule(caseless('ДНТ')),
    rule(caseless('ТСН')),
)

PEREULOK_DETAILS = or_(
    rule(OPEN_PARENTHESIS, NOUN, PEREULOK_DETAILS_WORDS1, PEREULOK_DETAILS_WORDS2, CLOSE_PARENTHESIS),
)

PEREULOK_NAME_VALUE = or_(
    rule(ADDR_NAME, PEREULOK_DETAILS.optional()),
    rule(NOUN, PEREULOK_DETAILS.optional()),
)

PEREULOK_NAME = PEREULOK_NAME_VALUE.interpretation(
    Street.name
)

PEREULOK = or_(
    rule(PEREULOK_WORDS, PEREULOK_NAME),
    rule(PEREULOK_NAME, PEREULOK_WORDS)
).interpretation(
    Street
)


########
#
#  PLOSHAD
#
##########


PLOSHAD_WORDS = or_(
    rule(
        caseless('пл'),
        DOT.optional()
    ),
    rule(normalized('площадь'))
).interpretation(
    Street.type.const('площадь')
)

PLOSHAD_NAME = ADDR_NAME.interpretation(
    Street.name
)

PLOSHAD = or_(
    rule(PLOSHAD_WORDS, PLOSHAD_NAME),
    rule(PLOSHAD_NAME, PLOSHAD_WORDS)
).interpretation(
    Street
)


############
#
#   SHOSSE
#
###########


# TODO
# Покровское 17 км.
# Сергеляхское 13 км
# Сергеляхское 14 км.


SHOSSE_WORDS = or_(
    rule(
        caseless('ш'),
        DOT.optional()
    ),
    rule(normalized('шоссе'))
).interpretation(
    Street.type.const('шоссе')
)

SHOSSE_NAME_VALUE = or_(
    rule(ADDR_NAME),
)

SHOSSE_NAME = SHOSSE_NAME_VALUE.interpretation(
    Street.name
)

SHOSSE = or_(
    rule(SHOSSE_WORDS, SHOSSE_NAME),
    rule(SHOSSE_NAME, SHOSSE_WORDS)
).interpretation(
    Street
)


########
#
#  NABEREG
#
##########


NABEREG_WORDS = or_(
    rule(
        caseless('наб'),
        DOT.optional()
    ),
    rule(normalized('набережная'))
).interpretation(
    Street.type.const('набережная')
)

NABEREG_NAME = ADDR_NAME.interpretation(
    Street.name
)

NABEREG = or_(
    rule(NABEREG_WORDS, NABEREG_NAME),
    rule(NABEREG_NAME, NABEREG_WORDS)
).interpretation(
    Street
)


########
#
#  BULVAR
#
##########


BULVAR_WORDS = or_(
    rule(
        caseless('б'),
        '-',
        caseless('р')
    ),
    rule(
        caseless('б'),
        DOT
    ),
    rule(
        caseless('бул'),
        DOT.optional()
    ),
    rule(normalized('бульвар'))
).interpretation(
    Street.type.const('бульвар')
)

BULVAR_NAME = ADDR_NAME.interpretation(
    Street.name
)

BULVAR = or_(
    rule(BULVAR_WORDS, BULVAR_NAME),
    rule(BULVAR_NAME, BULVAR_WORDS)
).interpretation(
    Street
)


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
        caseless('г'), '-', caseless('ж'), # гараж
    ),
)

IDENTIFICATION_ELEMENT_OF_ADDRESSED_OBJECT_POSTFIX = or_(
    rule(
        caseless('соор'),  # сооружение
    ),
    rule(
        caseless('стр'),  # строение
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

    rule(INT, caseless('ат')),
    rule(INT, caseless('гп')),
    rule(INT, caseless('тп')),
    rule(INT, caseless('эс')),
    rule(INT, caseless('пс')),
    rule(INT, caseless('ак'), INT),
)

HOUSE_PART = or_(
    rule(SLASH, 'РП'),
    rule(SLASH, 'ТП'),
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

SEP = in_(r'/\-')

VALUE = or_(
    rule(IDENTIFICATION_ELEMENT_OF_ADDRESSED_OBJECT_PREFIX, VALUE),
    rule(VALUE, IDENTIFICATION_ELEMENT_OF_ADDRESSED_OBJECT_POSTFIX, VALUE),
    rule(IDENTIFICATION_ELEMENT_OF_ADDRESSED_OBJECT_POSTFIX, VALUE),
    rule(VALUE),  # house number with optional letter
    rule(VALUE, SEP, VALUE),  # house number with optional letter, sep, another house number with optional letter
    rule(VALUE, SEP, LETTER)  # house number with optional letter, sep, letter
)

ADDR_VALUE = rule(
    eq('№').optional(),
    VALUE
)


############
#
#    DOM
#
#############


DOM_WORDS = or_(
    rule(normalized('дом')),
    rule(
        caseless('д'),
        DOT
    )
).interpretation(
    Building.type.const('дом')
)

DOM_VALUE = ADDR_VALUE.interpretation(
    Building.number
)

DOM = rule(
    DOM_WORDS,
    DOM_VALUE
).interpretation(
    Building
)


###########
#
#  KORPUS
#
##########


KORPUS_WORDS = or_(
    rule(
        in_caseless({'корп', 'кор'}),
        DOT.optional()
    ),
    rule(normalized('корпус'))
).interpretation(
    Building.type.const('корпус')
)

KORPUS_VALUE = ADDR_VALUE.interpretation(
    Building.number
)

KORPUS = or_(
    rule(
        KORPUS_WORDS,
        KORPUS_VALUE
    ),
    rule(
        KORPUS_VALUE,
        KORPUS_WORDS
    )
).interpretation(
    Building
)


###########
#
#  STROENIE
#
##########


STROENIE_WORDS = or_(
    rule(
        caseless('стр'),
        DOT.optional()
    ),
    rule(normalized('строение'))
).interpretation(
    Building.type.const('строение')
)

STROENIE_VALUE = ADDR_VALUE.interpretation(
    Building.number
)

STROENIE = rule(
    STROENIE_WORDS,
    ADDR_VALUE
).interpretation(
    Building
)


###########
#
#   OFIS
#
#############


OFIS_WORDS = or_(
    rule(
        caseless('оф'),
        DOT.optional()
    ),
    rule(normalized('офис'))
).interpretation(
    Room.type.const('офис')
)

OFIS_VALUE = ADDR_VALUE.interpretation(
    Room.number
)

OFIS = rule(
    OFIS_WORDS,
    OFIS_VALUE
).interpretation(
    Room
)


###########
#
#   KVARTIRA
#
#############


KVARTIRA_WORDS = or_(
    rule(
        caseless('кв'),
        DOT.optional()
    ),
    rule(normalized('квартира'))
).interpretation(
    Room.type.const('квартира')
)

KVARTIRA_VALUE = ADDR_VALUE.interpretation(
    Room.number
)

KVARTIRA = rule(
    KVARTIRA_WORDS,
    KVARTIRA_VALUE
).interpretation(
    Room
)


###########
#
#   INDEX
#
#############


INDEX = and_(
    INT,
    gte(100000),
    lte(999999)
).interpretation(
    Index.value
).interpretation(
    Index
)


#############
#
#   ADDR PART
#
############


ADDR_PART = or_(
    INDEX,
    COUNTRY,
    FED_OKRUG,

    RESPUBLIKA,
    KRAI,
    OBLAST,
    AUTO_OKRUG,

    RAION,

    GOROD,
    HUTOR,
    STANTSIA,
    TERRITORY,
    POSELENIE,
    SELSKOE_POSELENIE,
    STANITSA,
    DEREVNYA,
    SELO,
    AUL,
    SNT,
    POSELOK,

    STREET,
    PROULOK,
    DACHNY_POSELOK,
    LINE,
    DOROGA,
    PROSPEKT,
    PROEZD,
    PEREULOK,
    PLOSHAD,
    SHOSSE,
    NABEREG,
    BULVAR,

    DOM,
    KORPUS,
    STROENIE,
    OFIS,
    KVARTIRA
).interpretation(
    AddrPart.value
).interpretation(
    AddrPart
)
