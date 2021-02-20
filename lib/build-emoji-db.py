# -*- coding: utf-8 -*-

################################################################################
## build Emoji DB file from official HTML list of Emoji

import ast
import bs4
import emoji_db
import sys
import typing as ty


def main(args):

  if args:
    emoji_file = open(args[0])
  else:
    emoji_file = sys.stdin

  soup = bs4.BeautifulSoup(emoji_file, "lxml")

  emoji_table = soup.find('table')
  assert emoji_table

  ## drop unused <img> tags
  for img in soup.find_all('img'):
    img.decompose()

  major_category = None
  minor_category = None

  emojis = []

  for tr in emoji_table.find_all('tr'):
    major = get_major_category(tr)
    if major is not None:
      major_category = major
      minor_category = None
      continue

    minor = get_minor_category(tr)
    if minor is not None:
      minor_category = minor
      continue

    if is_legend(tr):
      continue

    emoji = get_emoji(tr, major_category, minor_category)
    if emoji:
      emojis.append(emoji)
      continue

    print('error: malformed line:', file=sys.stderr)
    print(tr.prettify(), file=sys.stderr)
    exit(1)

  ## FIXME: discard multi character emojis (neither the shell nor sublime can handle them)
  emojis = [e for e in emojis if len(e.emoji) == 1]

  db = emoji_db.encode_db(emojis)
  print(db)


def get_major_category(tr: bs4.Tag) -> str:
  """
    Checks if a <tr> tag is a major category line

    Example:
    ```html
      <tr>
        <th class="bighead" colspan="5">
          <a href="#smileys_&amp;_people" name="smileys_&amp;_people">
            Smileys &amp; People
          </a>
        </th>
      </tr>
    ```
    If the structures matches extract text of <tr>, otherwise return None
  """
  if tr.th and tr.th.get('class') == ['bighead']:
    assert tr.text
    return tr.text

  return


def get_minor_category(tr: bs4.Tag) -> str:
  """
    Checks if a <tr> tag is a minor category line

    Example:
    ```html
      <tr>
        <th class="mediumhead" colspan="5">
          <a href="#face-positive" name="face-positive">
            face-positive
          </a>
        </th>
      </tr>
    ```
    If the structures matches extract text of <tr>, otherwise return None
  """
  if tr.th and tr.th.get('class') == ['mediumhead']:
    assert tr.text
    return tr.text

  return


def is_legend(tr: bs4.Tag) -> bool:
  """
    Checks if a <tr> tag is a legend line.

    Example:
    ```html
      <tr>
       <th class="rchars">
        <a href="../format.html#col-num" target="text">
         №
        </a>
       </th>
       <th class="rchars">
        <a href="../format.html#col-code" target="text">
         Code
        </a>
       </th>
       <th class="center">
        <a href="../format.html#col-vendor" target="text">
         Sample
        </a>
       </th>
       <th>
        <a href="../format.html#col-name" target="text">
         CLDR Short Name
        </a>
       </th>
       <th>
        <a href="../format.html#col-annotations" target="text">
         Other Keywords
        </a>
       </th>
      </tr>
    ```
    If this matches, ignore this line.
  """

  return tr.text == '№\nCode\nSample\nCLDR Short Name\nOther Keywords\n'


def get_emoji(tr, major_category: str, minor_category: str) -> ty.Optional[emoji_db.Emoji]:
  """
    Example:
    ```html
      <tr>
        <td class="rchars">1</td>
        <td class="code">
          <a href="#1f600" name="1f600">U+1F600</a>
        </td>
        <td class="andr">
          <a href="full-emoji-list.html#1f600" target="full">
          <img alt="😀" class="imga" src="data:image/png;base64,..." title="U+1F600 😀 grinning face"/>
          </a>
        </td>
        <td class="name">grinning face</td>
        <td class="name">face | grin | grinning face</td>
      </tr>
    ```
    If this matches, ignore this line.
  """

  tds = tr.find_all('td')

  if len(tds) != 5:
    return

  number, code, image, name, categories = tds

  if number.get('class') != ['rchars']:
    return
  if code.get('class') != ['code']:
    return
  if image.get('class') != ['andr']:
    return
  if name.get('class') != ['name']:
    return
  if categories.get('class') != ['name']:
    return

  try:
    number = int(number.text)
  except ValueError:
    return

  # turn list unicode codepoints in format 'U\+[0-9A-F]{1,5}' into python bytes objects
  # input example:   'U+1F469 U+1F3FF U+200D U+1F33E'
  # expected output: '👩🏿u200d🌾'
  code = code.text.split(' ')
  code = [c.lstrip('U+') for c in code]
  code = ["'\\U" + c.rjust(8, '0') + "'" for c in code]
  code = [ast.literal_eval(c) for c in code]
  code = ''.join(code)

  name = name.text
  ## 'new' emojis are prefixed with '⊛'. remove that prefix
  name = name.lstrip('⊛ ')

  categories = [c.strip() for c in categories.text.split('|')]

  return emoji_db.Emoji(
    id             = number,
    emoji          = code,
    name           = name,
    major_category = major_category,
    minor_category = minor_category,
    tags           = categories
  )


if __name__ == '__main__':
  main(sys.argv[1:])
