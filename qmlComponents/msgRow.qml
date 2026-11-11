import QtQuick 2.0
import QtQuick.Layouts
import QtQuick.Controls.Material 2.1

Item {
    id: msgItem
    property string colorMsg: "#FFFFFF"
    width: 800
    RowLayout{
        spacing: 10
        Text {
            id: nick
            horizontalAlignment: Text.AlignLeft
            font.pointSize: 16
            wrapMode: Text.WordWrap
            textFormat: Text.StyledText
            text: ""
            font.family: "Papyrus"
            font.italic: true
            width: 395
            Material.accent: Material.Green
        }
        Text {
            id: msg
            horizontalAlignment: Text.AlignLeft
            font.pointSize: 16
            wrapMode: Text.WordWrap
            textFormat: Text.StyledText
            text: ""
            font.family: "Papyrus"
            font.italic: true
            width: 395
            Material.accent: Material.Green
            color: colorMsg
        }
    }
}
