
# Sublime Text 3 plugin for inserting emojis

The plugin adds an action `Insert emoji` to the sublime text 3 command palette.
The Emoji list is automatically generated from the official Emoji list from unicode.org.
To bootstrap the plugin to make it usable run the below commands.

## rebuild emoji DB

```bash
wget -O emoji-list.html https://unicode.org/emoji/charts/emoji-list.html
python3 lib/build-emoji-db.py emoji-list.html > emoji.db
```
