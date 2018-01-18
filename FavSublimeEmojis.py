# -*- coding: utf-8 -*-

import sublime
import sublime_plugin

from .lib import emoji_db


class FavInsertEmojiCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    window = self.view.window()

    emojis = sublime.load_resource("/".join(("Packages", __package__, "emoji.db")))

    try:
      emojis = emoji_db.parse_db(emojis)
    except ValueError as e:
      self.view.show_popup('<b>error: Emoji DB file corrupted (' + repr(e) + '<b/>')
      return

    items = [e.name + ' (' + e.emoji + ')' for e in emojis] + ['hi'] + ['ho']

    def callback(selection):
      if selection >= 0:
        try:
          txt = emojis[selection].emoji
        except IndexError:
          txt = '<emoji-error: invalid selection>'

        self.view.run_command("insert", {"characters": txt})

    window.show_quick_panel(items, callback)
