# -*- coding: utf-8 -*-

import abc
import struct
import itertools

__all__ = [
  'Jamo',
  'Consonant',
  'Vowel',
  'Syllable',
  'jamo_db',
  'syllable_db',
]

#  https://en.wikipedia.org/wiki/Korean_language_and_computers#Hangul_in_Unicode
#
#  Hangul Syllables block
#


class Jamo:
  """
    A jamo, a hangul character

    attributes:
      *name*    : str ... name
      *RR_name* : str ... name in revised romanization
      *unicode* : str ... unicode str for jamo
  """
  __slots__ = ('_unicode', '_name', '_RR_name')

  def __init__(self, unicode: str, name: str, RR_name: str):
    self._unicode = unicode
    self._name    = name
    self._RR_name = RR_name

  @property
  def name(self):
    return self._name

  @property
  def RR_name(self):
    return self._RR_name

  @property
  def unicode(self):
    return self._unicode

  @abc.abstractproperty
  def romanizations(self):
    """ self -> tuple[str] """

  def __repr__(self):
    return type(self).__name__ + '(' + repr(self.unicode) + ')'


class Consonant(Jamo):
  """
    attributes:
      *initial* ... romanization when appearing in initial position
      *final* ..... romanization when appearing in final position.
  """
  __slots__ = Jamo.__slots__ + ('_initial', '_final',)

  def __init__(self, unicode: str,
               initial_romanization: str, final_romanization: str,
               RR_name: str, name: str):
    super().__init__(unicode, name, RR_name)

    self._initial     = initial_romanization
    self._final       = final_romanization

  @property
  def initial(self):
    return self._initial

  @property
  def final(self):
    return self._final

  @property
  def romanizations(self):
    r = ()
    if self.initial:
      r += (self.initial,)
    if self.final:
      r += (self.final,)
    return r


class Vowel(Jamo):
  """
    attributes:
      *romanization* : str ... romanization
  """
  __slots__ = Jamo.__slots__ + ()

  def __init__(self, unicode, RR_name, name):
    super().__init__(unicode, name, RR_name)

  @property
  def romanizations(self):
    return (self.RR_name,)


class Special_Batchim(Jamo):
  """
    Special jamo that can only appear as batchim.
    They aren't really real jamo (well, according to unicode they kina are)
  """
  __slots__ = Jamo.__slots__ + ('jamo',)

  def __init__(self, unicode, *jamo):
    super().__init__(
      unicode,
      ''.join(j.name for j in jamo),
      '-'.join(j.RR_name for j in jamo),
    )
    self.jamo = jamo

  @property
  def final(self):
    return '-'.join(filter(bool, (j.final for j in self.jamo)))

  @property
  def romanizations(self):
    return (self.RR_name,)


ᄀ = Consonant('ᄀ', 'g',  'k',  'giyoek',      '기역')
ㄲ = Consonant('ㄲ', 'kk', 'k',  'ssangiyoek',  '쌍기역')
ㄴ = Consonant('ㄴ', 'n',  'n',  'nieun',       '니은')
ㄷ = Consonant('ㄷ', 'd',  't',  'dieud',       '디귿')
ㄸ = Consonant('ㄸ', 'tt', None, 'ssangdigeut', '쌍디귿')
ㄹ = Consonant('ㄹ', 'r',  'l',  'rieul',       '리을')
ㅁ = Consonant('ㅁ', 'm',  'm',  'mieum',       '미음')
ㅂ = Consonant('ㅂ', 'b',  'p',  'bieup',       '비읍')
ㅃ = Consonant('ㅃ', 'pp', None, 'ssangbieup',  '쌍비읍')
ㅅ = Consonant('ㅅ', 's',  't',  'siot',        '시옷')
ㅆ = Consonant('ㅆ', 'ss', 't',  'ssangsiot',   '쌍시옷')
ㅇ = Consonant('ㅇ', None, 'ng', 'ieung',       '이응')
ㅈ = Consonant('ㅈ', 'j',  't',  'jieut',       '지읒')
ㅉ = Consonant('ㅉ', 'jj', None, 'ssangjieut',  '쌍지읒')
ㅊ = Consonant('ㅊ', 'ch', 't',  'chieut',      '치읓')
ㅋ = Consonant('ㅋ', 'k',  'k',  'kieuk',       '키읔')
ㅌ = Consonant('ㅌ', 't',  't',  'tieut',       '티읕')
ㅍ = Consonant('ㅍ', 'p',  'p',  'pieup',       '피읖')
ㅎ = Consonant('ㅎ', 'h',  'h',  'hieut',       '히읗')

ㅏ = Vowel('ㅏ', 'a',   '아')
ㅐ = Vowel('ㅐ', 'ae',  '애')
ㅑ = Vowel('ㅑ', 'ya',  '야')
ㅒ = Vowel('ㅒ', 'yae', '얘')
ㅓ = Vowel('ㅓ', 'eo',  '어')
ㅔ = Vowel('ㅔ', 'e',   '에')
ㅕ = Vowel('ㅕ', 'yeo', '여')
ㅖ = Vowel('ㅖ', 'ye',  '예')
ㅗ = Vowel('ㅗ', 'o',   '오')
ㅘ = Vowel('ㅘ', 'wa',  '와')
ㅙ = Vowel('ㅙ', 'wae', '왜')
ㅚ = Vowel('ㅚ', 'oe',  '외')
ㅛ = Vowel('ㅛ', 'yo',  '요')
ㅜ = Vowel('ㅜ', 'u',   '우')
ㅝ = Vowel('ㅝ', 'wo',  '워')
ㅞ = Vowel('ㅞ', 'we',  '웨')
ㅟ = Vowel('ㅟ', 'wi',  '위')
ㅠ = Vowel('ㅠ', 'yu',  '유')
ㅡ = Vowel('ㅡ', 'eu',  '으')
ㅢ = Vowel('ㅢ', 'ui',  '의')
ㅣ = Vowel('ㅣ', 'i',   '이')

empty = Special_Batchim('')
ㄳ    = Special_Batchim('ㄳ', ᄀ, ㅅ)
ㄵ    = Special_Batchim('ㄵ', ㄴ, ㅈ)
ㄶ    = Special_Batchim('ㄶ', ㄴ, ㅎ)
ㄺ    = Special_Batchim('ㄺ', ㄹ, ᄀ)
ㄻ    = Special_Batchim('ㄻ', ㄹ, ㅁ)
ㄼ    = Special_Batchim('ㄼ', ㄹ, ㅂ)
ㄽ    = Special_Batchim('ㄽ', ㄹ, ㅅ)
ㄾ    = Special_Batchim('ㄾ', ㄹ, ㅌ)
ㄿ    = Special_Batchim('ㄿ', ㄹ, ㅍ)
ㅀ    = Special_Batchim('ㅀ', ㄹ, ㅎ)
ㅄ    = Special_Batchim('ㅄ', ㅂ, ㅅ)


_CONSONANTS = (
  ᄀ, ㄲ, ㄴ, ㄷ, ㄸ, ㄹ, ㅁ, ㅂ, ㅃ, ㅅ, ㅆ, ㅇ, ㅈ, ㅉ, ㅊ, ㅋ, ㅌ, ㅍ, ㅎ,
)

_VOWELS = (
  ㅏ, ㅐ, ㅑ, ㅒ, ㅓ, ㅔ, ㅕ, ㅖ, ㅗ, ㅘ, ㅙ, ㅚ, ㅛ, ㅜ, ㅝ, ㅞ, ㅟ, ㅠ, ㅡ, ㅢ, ㅣ,
)

_INITIAL = {
  ᄀ: 0, ㄲ: 1, ㄴ: 2, ㄷ: 3, ㄸ: 4, ㄹ: 5, ㅁ: 6, ㅂ: 7, ㅃ: 8, ㅅ: 9, ㅆ: 10,
  ㅇ: 11, ㅈ: 12, ㅉ: 13, ㅊ: 14, ㅋ: 15, ㅌ: 16, ㅍ: 17, ㅎ: 18,
}

_MEDIAL = {
  ㅏ: 0, ㅐ: 1, ㅑ: 2, ㅒ: 3, ㅓ: 4, ㅔ: 5, ㅕ: 6, ㅖ: 7, ㅗ: 8, ㅘ: 9, ㅙ: 10,
  ㅚ: 11, ㅛ: 12, ㅜ: 13, ㅝ: 14, ㅞ: 15, ㅟ: 16, ㅠ: 17, ㅡ: 18, ㅢ: 19, ㅣ: 20,
}

_FINAL = {
  empty: 0,
  ㄱ: 1, ㄲ: 2, ㄳ: 3, ㄴ: 4, ㄵ: 5, ㄶ: 6, ㄷ: 7, ㄹ: 8, ㄺ: 9, ㄻ: 10, ㄼ: 11,
  ㄽ: 12, ㄾ: 13, ㄿ: 14, ㅀ: 15, ㅁ: 16, ㅂ: 17, ㅄ: 18, ㅅ: 19, ㅆ: 20, ㅇ: 21,
  ㅈ: 22, ㅊ: 23, ㅋ: 24, ㅌ: 25, ㅍ: 26, ㅎ: 27
}


class Syllable:
  __slots__ = ('unicode', 'jamo')

  def __init__(self, jamo: (Jamo)):
    self.unicode = compose_syllable(*jamo)
    self.jamo    = jamo

  @property
  def initial(self):
    return self.jamo[0]

  @property
  def medial(self):
    return self.jamo[1]

  @property
  def final(self):
    return self.jamo[2]

  @property
  def jamo_romanization(self):
    txt = []

    initial, medial, final = self.jamo
    assert isinstance(initial, Jamo)
    assert isinstance(medial, Jamo)
    assert isinstance(final, Jamo)

    if self.initial.initial is not None:
      txt.append(self.initial.initial)

    txt.append(self.medial.RR_name)

    if self.final.final:
      txt.append(self.final.final)

    return '-'.join(txt)


def compose_syllable(initial: Jamo, medial: Jamo, final: Jamo) -> str:
  """
    Compose up to three Jamo to a syllable
  """

  #  The precomposed hangul syllables in the Hangul Syllables block in Unicode
  #  are algorithmically defined, using the following formula:
  #    [(initial) × 588 + (medial) × 28 + (final)] + 44032

  assert initial in _INITIAL, initial

  i = _INITIAL[initial]
  m = _MEDIAL[medial]
  f = _FINAL[final]

  codepoint = (i * 588 + m * 28 + f) + 44032
  utf_bytes = struct.pack('<i', codepoint)
  txt       = utf_bytes.decode('utf_32_le')
  return txt


def jamo_db():
  yield from _VOWELS
  yield from _CONSONANTS


def syllable_db():
  for I, M, F in itertools.product(_INITIAL, _MEDIAL, _FINAL):
    yield Syllable((I, M, F))
