// Copyright (C) 2021 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial


import QtQuick 2.0
import QtQuick.Layouts 1.11
import QtQuick.Controls 2.1
import QtQuick.Window 2.1
import QtQuick.Controls.Material 2.1
import QtQml

import "qmlComponents"

import io.qt.textproperties 1.0

ApplicationWindow {
    id: page
    width: 900
    height: 800
    visible: true
    Material.theme: Material.Dark
    Material.accent: Material.Red
    title: "SynthMoth"
    property string colorMsg: "#FFFFFF"
    property string colEnd: "</font>"
    property int counter: 0

    Bridge {
        id: bridge
    }

    property QtObject chat

    GridLayout {
        id: grid
        columns: 2
        Item{
            Layout.alignment: Qt.AlignLeft
            width: 500
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
                contentHeight: chatView.contentHeight
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
                ListModel {
                    id: chatList
                }

                Component {
                    id: chatDelegate
                    Row{
                        Rectangle {
                            height: chatMsg.contentHeight
                            width: 500
                            color: "transparent"
                            Text {
                                id: chatNick
                                horizontalAlignment: Text.AlignLeft
                                font.pointSize: 16
                                wrapMode: Text.WordWrap
                                textFormat: Text.StyledText
                                text: nick
                                font.family: "Papyrus"
                                font.italic: true
                                Material.accent: Material.Green
                            }
                            Text {
                                id: chatMsg
                                horizontalAlignment: Text.AlignLeft
                                font.pointSize: 16
                                wrapMode: Text.WordWrap
                                textFormat: Text.StyledText
                                text: msg
                                font.family: "Papyrus"
                                font.italic: true
                                Material.accent: Material.Green
                                color: colorMsg
                            }
                        }
                    }
                }

                ListView {
                    id: chatView
                    anchors.fill: parent
                    model: chatList
                    delegate: chatDelegate
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
                        //leftlabel.font.pointSize = bridge.getSize(value)
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
                        colorMsg = bridge.getTextColor(sredlabel.text, value, colorMsg)
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
                        colorMsg = bridge.getTextColor(sgreenlabel.text, value, colorMsg)
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
                        colorMsg = bridge.getTextColor(sbluelabel.text, value, colorMsg)
                    }
                }
            }
            RowLayout {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter

                Button {
                    id: visiblechat
                    text: flick.opacity === 1 ? "Hide" : "Show"
                    highlighted: true
                    Material.accent: Material.BlueGrey
                    onClicked: {
                        opacityAnimation.stop()
                        flick.opacity = flick.opacity === 1 ? 0 : 1
                    }
                }
                Button {
                    id: test
                    text: "Test"
                    highlighted: true
                    Material.accent: Material.BlueGrey
                    onClicked: {
                        chatList.append({"nick": "huesos", "msg": "‎‎‎   ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ya hochu pizzu " + page.counter})
                        page.counter += 1
                    }
                }
            }
        }
    }

    Connections {
        target: chat

        function onNewChatMessage(msgF) {
            var tmpArr = msgF.split(":")
            var user = tmpArr[0]
            console.log(user.length)
            var userLen = user.length - 36
            var msg = "<font>"
            for (var i = 0; i < userLen*2; i++){
                msg = msg + "‎‎‎ "
            }
            for (var i = 1; i < tmpArr.length; i++){
                msg = msg + ": " + tmpArr[i]
            }
            msg = msg + colEnd
            chatList.append({"nick": user, "msg": msg})
            flick.opacity = 1
            opacityAnimation.stop()
            //leftlabel.text = leftlabel.text + user + msg + "<br>"
            timerchat.restart()
        }
    }
}
