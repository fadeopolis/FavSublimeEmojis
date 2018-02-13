# -*- coding: utf-8 -*-

import sublime
import sublime_plugin

from .lib import emoji_db
from .lib import hangul_db


class FavInsertEmojiCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    window = self.view.window()

    emojis = sublime.load_resource("/".join(("Packages", __package__, "emoji.db")))

    try:
      emojis = emoji_db.parse_db(emojis)
    except ValueError as e:
      self.view.show_popup('<b>error: Emoji DB file corrupted (' + repr(e) + '<b/>')
      return

    items = [e.name + ' (' + e.emoji + ')' for e in emojis]

    def callback(selection):
      if selection >= 0:
        try:
          txt = emojis[selection].emoji
        except IndexError:
          txt = '<emoji-error: invalid selection>'

        self.view.run_command("insert", {"characters": txt})

    window.show_quick_panel(items, callback)


class FavInsertHangulCommand(sublime_plugin.TextCommand):
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
