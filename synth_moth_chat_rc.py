# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 6.7.2
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore

qt_resource_data = b"\
\x00\x00\x00i\
[\
Controls]\x0d\x0aStyle\
=Material\x0d\x0a\x0d\x0a[Un\
iversal]\x0d\x0aTheme=\
System\x0d\x0aAccent=R\
ed\x0d\x0a\x0d\x0a[Material]\
\x0d\x0aTheme=Dark\x0d\x0aAc\
cent=Red\
\x00\x00\x03\xdc\
i\
mport QtQuick 2.\
0\x0d\x0aimport QtQuic\
k.Layouts\x0d\x0aimpor\
t QtQuick.Contro\
ls.Material 2.1\x0d\
\x0a\x0d\x0aItem {\x0d\x0a    i\
d: msgRow\x0d\x0a    p\
roperty string c\
olorMsg: \x22#FFFFF\
F\x22\x0d\x0a    width: 8\
00\x0d\x0a    RowLayou\
t{\x0d\x0a        spac\
ing: 10\x0d\x0a       \
 Text {\x0d\x0a       \
     id: nick\x0d\x0a \
           horiz\
ontalAlignment: \
Text.AlignLeft\x0d\x0a\
            font\
.pointSize: 16\x0d\x0a\
            wrap\
Mode: Text.WordW\
rap\x0d\x0a           \
 textFormat: Tex\
t.StyledText\x0d\x0a  \
          text: \
\x22huesos:\x22\x0d\x0a     \
       font.fami\
ly: \x22Papyrus\x22\x0d\x0a \
           font.\
italic: true\x0d\x0a  \
          width:\
 395\x0d\x0a          \
  Material.accen\
t: Material.Gree\
n\x0d\x0a        }\x0d\x0a  \
      Text {\x0d\x0a  \
          id: ms\
g\x0d\x0a            h\
orizontalAlignme\
nt: Text.AlignLe\
ft\x0d\x0a            \
font.pointSize: \
16\x0d\x0a            \
wrapMode: Text.W\
ordWrap\x0d\x0a       \
     textFormat:\
 Text.StyledText\
\x0d\x0a            te\
xt: \x22ya huesos\x22\x0d\
\x0a            fon\
t.family: \x22Papyr\
us\x22\x0d\x0a           \
 font.italic: tr\
ue\x0d\x0a            \
width: 395\x0d\x0a    \
        Material\
.accent: Materia\
l.Green\x0d\x0a       \
     color: colo\
rMsg\x0d\x0a        }\x0d\
\x0a    }\x0d\x0a}\x0d\x0a\
"

qt_resource_name = b"\
\x00\x0d\
\x07\xe6\x08\xd3\
\x00q\
\x00m\x00l\x00C\x00o\x00m\x00p\x00o\x00n\x00e\x00n\x00t\x00s\
\x00\x15\
\x08\x1e\x16f\
\x00q\
\x00t\x00q\x00u\x00i\x00c\x00k\x00c\x00o\x00n\x00t\x00r\x00o\x00l\x00s\x002\x00.\
\x00c\x00o\x00n\x00f\
\x00\x0a\
\x09h\xc7\xbc\
\x00m\
\x00s\x00g\x00R\x00o\x00w\x00.\x00q\x00m\x00l\
"

qt_resource_struct = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x03\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00 \x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x90nU\x9e\xbc\
\x00\x00\x00P\x00\x00\x00\x00\x00\x01\x00\x00\x00m\
\x00\x00\x01\x91p(\xa5\xc4\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
