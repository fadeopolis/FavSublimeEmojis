
# Sublime Text 3 plugin for inserting emojis

The plugin adds an action `Insert emoji` to the sublime text 3 command palette.
The Emoji list is automatically generated from the official Emoji list from unicode.org.
To bootstrap the plugin to make it usable run the below commands.

## rebuild emoji DB

```bash
wget https://unicode.org/emoji/charts/emoji-list.html
python3 lib/build-emoji-db.py "Emoji List, v5.0.html" > emoji.db
```
