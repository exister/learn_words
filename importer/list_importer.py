# -*- coding: utf-8 -*-

import urwid
import os
import string
import random

urwid.set_encoding("UTF-8")

file_label = urwid.Edit(u'Specify file location\n')
command = urwid.Edit(u'Enter command: ')
word_label = urwid.Text('')

words = None
used_words = {}
current = None

def handle_input(text):
    if text == 'enter':
        if command.edit_text:
            if command.edit_text == 'n':
                key, word = next_word()
                word_label.set_text(key)
            elif command.edit_text == 's' and current:
                word_label.set_text(unicode(u', '.decode('utf-8').join(current[1])))
            elif command.edit_text == 'q':
                raise urwid.ExitMainLoop()
            command.set_edit_text(u'')
            return True
        elif file_label.edit_text:
            if os.path.exists(file_label.edit_text) and os.path.isfile(file_label.edit_text):
                file_label.set_caption(u'{0}: {1}'.format(file_label.caption, file_label.edit_text))
                global words
                words = parse_file(file_label.edit_text)
                file_label.set_edit_text(u'')
            return True

def next_word():
    global words, used_words, current

    if words:
        key = random.choice(words.keys())
        word = words[key]
        del words[key]
        used_words[key] = word
        current = (key, word)
        return current
    else:
        return None, None

def parse_file(path):
    result = {}
    with file(path, 'r') as f:
        letters = string.ascii_letters + string.whitespace
        for line in f:
            if not line.strip():
                continue
            min_index = -1
            for i, c in enumerate(line.strip()):
                if c not in letters:
                    min_index = i
                    break
            if min_index > 0:
                en, ru = line[:min_index].strip().decode('utf-8'), line[min_index:].strip().decode('utf-8')
#                import ipdb; ipdb.set_trace()
                ru = ru.split(u',')
                result.setdefault(en.lower(), ru)

    return result

palette = [
    ('body', 'black', 'dark cyan', 'standout'),
    ('foot', 'light gray', 'black'),
    ('head', 'light gray', 'black'),
    ('key', 'light cyan', 'black', 'underline'),
    ('title', 'white', 'black',),
]

footer_text = [
    ('key', "n"), " - next word, ",
    ('key', "s"), " - show translation, ",
    ('key', "q"), " - exit",
]

listbox_content = [
    file_label, command, word_label
]

listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))
footer = urwid.AttrMap(urwid.Text(footer_text), 'foot')
header = urwid.AttrMap(urwid.Text(u'Learn words'), 'head')
view = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header, footer=footer)
loop = urwid.MainLoop(view, palette, unhandled_input=handle_input)
loop.run()
