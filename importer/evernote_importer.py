# -*- coding: utf-8 -*-

from xml.etree.ElementTree import ElementTree, fromstring
import re
import sys
import os

# Usage
# osascript /path/to/export_note.scpt note_name /path/to/export.xml

def parse_evernote_exported_file(source_path, result_path):
    regex = re.compile(u"^([A-Za-z!',.:?\s/-]+)(\([A-Za-z!',.:?\s/-]+\))?(.*)$", re.IGNORECASE|re.UNICODE)

    result = {}
    f = ElementTree()
    try:
        note = f.parse(os.path.abspath(os.path.expanduser(source_path)))
    except SystemError, e:
        return False

    xml = fromstring(note.find('note/content').text.encode('utf-8'))
    divs = xml.findall('div')

    for line in divs:
        if not line.text or not line.text.strip():
            continue

        text = line.text.strip()

        en = None
        en_alternative = None
        ru = None

        if u';' in text:
            en, ru = text.split(u';')
        else:
            match = regex.match(text)
            if match:
                ru = match.groups()[2]
                if not ru.strip() and match.groups()[1] and len(match.groups()[1]) > 2:
                    en_alternative = match.groups()[1][1:-1]
                    en = match.groups()[0]
                else:
                    en = u' '.join([x for x in match.groups()[:2] if x])

        if en:
            if ru.strip():
                result.setdefault(en.lower().strip(), ru.strip())
            elif en_alternative and len(en_alternative.strip()) > 2:
                result.setdefault(en.lower().strip(), en_alternative.strip())

    with file(os.path.abspath(os.path.expanduser(result_path)), "w") as fp:
        for k, v in result.iteritems():
            fp.write((u"{0}; {1}\n".format(k, v)).encode('utf-8'))

if __name__ == "__main__":
    parse_evernote_exported_file(sys.argv[1], sys.argv[2])