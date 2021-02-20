# -*- coding: utf-8 -*-

import sublime
import sublime_plugin

from .lib import emoji_db
from .lib import hangul_db

# from typing import List, Optional

## list of all emojis
emojis           = None # type: Optional[List[emoji_db.Emoji]]
## list of items shown in drop-down list user selects from
emoji_list_items = None # type: Optional[List[str]]

class FavInsertEmojiCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    global emojis, emoji_list_items

    window = self.view.window()

    if emojis is None:
      assert emoji_list_items is None

      try:
        emoji_db_text = sublime.load_resource("/".join(("Packages", __package__, "emoji.db")))
      except OSError as e:
        self.view.show_popup('<b>error: Emoji DB file not found (' + repr(e) + '<b/>')
        return

      try:
        emojis = emoji_db.parse_db(emoji_db_text)
      except ValueError as e:
        self.view.show_popup('<b>error: Emoji DB file corrupted (' + repr(e) + '<b/>')
        return

      emoji_list_items = []

      for e in emojis:
        tags = [e.major_category, e.minor_category]
        tags.extend(e.tags)

        item = [e.name + ' (' + e.emoji + ')', ' | '.join(tags)]

        emoji_list_items.append(item)

    def callback(selection):
      ## called with selection == -1 if user cancels dialog

      if selection >= 0:
        try:
          txt = emojis[selection].emoji
        except IndexError:
          txt = '<emoji-error: invalid selection>'

        self.view.run_command("insert", {"characters": txt})

    window.show_quick_panel(emoji_list_items, callback)


class FavInsertJamoCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    window = self.view.window()

    txt = []
    gui = []

    for jamo in hangul_db.jamo_db():
      txt.append(jamo.unicode)
      gui.append(' '.join([
        jamo.unicode,
        '(' + ', '.join(jamo.romanizations) + ')'
      ]))

    def callback(selection):
      if selection >= 0:
        try:
          c = txt[selection]
        except IndexError:
          c = '<hangul-error: invalid selection>'

        self.view.run_command("insert", {"characters": c})

    window.show_quick_panel(gui, callback)


class FavInsertHangulCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    window = self.view.window()

    txt = []
    gui = []

    for sy in hangul_db.syllable_db():
      txt.append(sy.unicode)
      gui.append(sy.unicode + ' (' + sy.jamo_romanization + ')')

    def callback(selection):
      if selection >= 0:
        try:
          c = txt[selection]
        except IndexError:
          c = '<hangul-error: invalid selection>'

        self.view.run_command("insert", {"characters": c})

    window.show_quick_panel(gui, callback)



