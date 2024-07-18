// Copyright (C) 2021 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial


import QtQuick 2.0
import QtQuick.Layouts 1.11
import QtQuick.Controls 2.1
import QtQuick.Window 2.1
import QtQuick.Controls.Material 2.1
import QtQml

import io.qt.textproperties 1.0

ApplicationWindow {
    id: page
    width: 800
    height: 800
    visible: true
    Material.theme: Material.Dark
    Material.accent: Material.Red
    title: "SynthMoth"
    property string colorNick: "#FFFFFF"
    property string colorMsg: "#FFFFFF"
    property string colEnd: "</font>"

    Bridge {
        id: bridge
    }

    property QtObject chat

    GridLayout {
        id: grid
        columns: 2
        Item{
            Layout.alignment: Qt.AlignLeft
            width: 400
            height: 800
            Timer {
                id: timerchat
                interval: 4000
                onTriggered: opacityAnimation.start()
            }
            Flickable{
                id: flick
                anchors.fill:parent
                clip: true
                contentHeight: leftlabel.contentHeight
                contentY : contentHeight-height
                ScrollBar.vertical: ScrollBar {
                    parent: flick.parent
                    anchors.top: flick.top
                    anchors.left: flick.right
                    anchors.bottom: flick.bottom
                    Material.accent: Material.BlueGrey
                }
                NumberAnimation {
                    id: opacityAnimation
                    target: flick
                    property: "opacity"
                    to: 0
                    duration: 2000
                }
                Text {
                    id: leftlabel
                    horizontalAlignment: Text.AlignLeft
                    font.pointSize: 16
                    wrapMode: Text.WordWrap
                    textFormat: Text.StyledText
                    text: ""
                    font.family: "Papyrus"
                    font.italic: true
                    width: 400
                    Material.accent: Material.Green
                }
            }
        }

        ColumnLayout {
            id: rightcolumn
            spacing: 2
            Layout.columnSpan: 1
            Layout.preferredWidth: 400
            Layout.preferredHeight: 400
            Layout.fillWidth: true

            RowLayout {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter

                /*Button {
                    id: green
                    text: "Green"
                    highlighted: true
                    Material.accent: Material.Green
                    onClicked: {
                        leftlabel.color = bridge.getColor(green.text)
                        leftlabel.text = leftlabel.text + "test text <br>"
                    }
                }*/
                Button {
                    id: blue
                    text: "Turn On"
                    highlighted: true
                    Material.accent: Material.Green
                    onClicked: {
                        bridge.turnOn()
                    }
                }
                Button {
                    id: nonebutton
                    text: "Turn Off"
                    highlighted: true
                    Material.accent: Material.Red
                    onClicked: {
                        bridge.turnOff()
                    }
                }
            }
            RowLayout {
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                Text {
                    id: rightlabel
                    color: "white"
                    Layout.alignment: Qt.AlignLeft
                    text: "Font size"
                    Material.accent: Material.White
                }
                Slider {
                    width: rightcolumn.width*0.6
                    Layout.alignment: Qt.AlignRight
                    id: slider
                    value: 0.5
                    onValueChanged: {
                        leftlabel.font.pointSize = bridge.getSize(value)
                    }
                }
            }
            RowLayout {
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                Text {
                    id:sredlabel
                    color: "white"
                    Layout.alignment: Qt.AlignLeft
                    text: "sred"
                    Material.accent: Material.White
                }
                Slider {
                    width: rightcolumn.width*0.6
                    Layout.alignment: Qt.AlignRight
                    id: sred
                    value: 0.5
                    onValueChanged: {
                        var colors = (bridge.getTextColor(sredlabel.text, value, colorMsg)).split("|")
                        colorMsg = colors[0]
                        colorNick = colors[1]
                    }
                }
            }
            RowLayout {
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                Text {
                    id: sgreenlabel
                    color: "white"
                    Layout.alignment: Qt.AlignLeft
                    text: "sgreen"
                    Material.accent: Material.White
                }
                Slider {
                    width: rightcolumn.width*0.6
                    Layout.alignment: Qt.AlignRight
                    id: sgreen
                    value: 0.5
                    onValueChanged: {
                        var colors = bridge.getTextColor(sgreenlabel.text, value, colorMsg).split("|")
                        colorMsg = colors[0]
                        colorNick = colors[1]
                    }
                }
            }
            RowLayout {
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                Text {
                    id: sbluelabel
                    color: "white"
                    Layout.alignment: Qt.AlignRight
                    text: "sblue"
                    Material.accent: Material.White
                }
                Slider {
                    width: rightcolumn.width*0.6
                    Layout.alignment: Qt.AlignLeft
                    id: sblue
                    value: 0.5
                    onValueChanged: {
                        var colors = bridge.getTextColor(sbluelabel.text, value, colorMsg).split("|")
                        colorMsg = colors[0]
                        colorNick = colors[1]
                    }
                }
            }
            RowLayout {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter

                Button {
                    id: visiblechat
                    text: flick.opacity == 1 ? "Hide" : "Show"
                    highlighted: true
                    Material.accent: Material.BlueGrey
                    onClicked: {
                        opacityAnimation.stop()
                        flick.opacity = flick.opacity == 1 ? 0 : 1
                    }
                }
            }
        }
    }

    Connections {
        target: chat

        function onNewChatMessage(msgF) {
            var tmpArr = msgF.split(":")
            var user = "<font color=\"" + colorNick + "\"><b>" + tmpArr[0] + "</b>" + colEnd
            var msg = "<font color=\"" + colorMsg +"\">"
            for (var i = 1; i < tmpArr.length; i++){
                msg = msg + ":" + tmpArr[i]
            }
            msg = msg + colEnd
            flick.opacity = 1
            opacityAnimation.stop()
            leftlabel.text = leftlabel.text + user + msg + "<br>"
            timerchat.restart()
        }
    }
}
