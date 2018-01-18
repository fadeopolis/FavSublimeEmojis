# -*- coding: utf-8 -*-

import ast
import collections

__all__ = [
  'Emoji',
  'parse_db',
  'encode_db',
  'load',
  'save',
]


Emoji = collections.namedtuple(
  'Emoji',
  [
    'id',              # : int, numeric ID of emoji
    'emoji',           # : str, unicode as str
    'name',            # : str, name and description
    # 'major_category',  # : str, descriptive category
    # 'minor_category',  # : str, descriptive category
    # 'tags',            # : [str], descriptive tags
  ],
)


def parse_db(db: str) -> [Emoji]:
  """
    Parse emoji DB from a string
  """

  db = db.splitlines()
  db = [ast.literal_eval(e) for e in db]
  db = [Emoji(**e) for e in db]

  return db


def encode_db(db: [Emoji]) -> str:
  """
    Encode emoji DB into a string
  """

  db = [e._asdict() for e in db]
  db = [dict(e) for e in db]
  db = [repr(e) for e in db]
  db = '\n'.join(db)

  # db = json.dumps(db, indent=2, ensure_ascii=True)
  # db = pprint.pformat(db, width=120)

  return db


def load(path: str) -> [Emoji]:
  """
    Load emoji DB from file path
  """
  db = open(path, 'r').read()
  db = parse_db(db)

  return db


def save(db: [Emoji], path: str):
  """
    Store emoji DB to file
  """

  txt = encode_db(db)

  with open(path, 'w') as file:
    file.write(txt)
