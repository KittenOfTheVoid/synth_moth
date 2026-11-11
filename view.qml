// Copyright (C) 2021 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial


import QtQuick 2.0
import QtQuick.Layouts 1.11
import QtQuick.Controls 2.1
import QtQuick.Window 2.1
import QtQuick.Controls.Material 2.1
import QtQml

import "qrc:/qmlComponents" as Components

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
    property int counter: 0

    Bridge {
        id: bridge
    }

    Components.ChatContextMenu {
        id: chatMenu
    }

    property QtObject chat

    GridLayout {
        id: grid
        columns: 2
        Item{
            Layout.alignment: Qt.AlignLeft
            width: 500
            height: 800

            Rectangle {
                id: chatBackground
                anchors.fill: parent
                radius: 14
                opacity: chatView.opacity
                
                // Тёмный полупрозрачный фон
                color: "#B30D0D12"                    // чуть с синевой, выглядит дороже
                
                border.color: "#33FFFFFF"
                border.width: 1

                // Очень лёгкий внутренний градиент (опционально)
                gradient: Gradient {
                    GradientStop { position: 0.0; color: "#C9101018" }
                    GradientStop { position: 1.0; color: "#A00A0A10" }
                }
            }

            Timer {
                id: timerchat
                interval: 4000
                onTriggered: opacityAnimation.start()
            }

            ListView {
                id: chatView
                anchors.fill: parent
                model: chatList
                delegate: chatDelegate
                clip: true
                spacing: 4
                contentHeight: chatView.contentHeight

                ScrollBar.vertical: ScrollBar {
                    parent: chatView.parent
                    anchors.top: chatView.top
                    anchors.left: chatView.right
                    anchors.bottom: chatView.bottom
                    Material.accent: Material.BlueGrey
                }
            
                onCountChanged: {
                    if (count > 0) {
                        Qt.callLater(function() {
                            positionViewAtEnd()
                        })
                    }
                }
            }
            NumberAnimation {
                id: opacityAnimation
                target: chatView
                property: "opacity"
                to: 0
                duration: 2000
            }

            ListModel {
                id: chatList
            }

            Component {
                id: chatDelegate
                Item {
                    width: chatView.width
                    height: chatMsg.implicitHeight + 8

                    property string nick: model.nick

                    Rectangle { // фон при наведении
                        anchors.fill: parent
                        color: mouseArea.containsMouse ? "#22ffffff" : "transparent"
                        radius: 4
                    }

                    Text {
                        id: chatMsg
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.verticalCenter: parent.verticalCenter
                        leftPadding: 8
                        rightPadding: 8
                        text: model.msg
                        textFormat: Text.StyledText
                        wrapMode: Text.WordWrap
                        font.pointSize: 15
                        font.family: "Papyrus"
                        font.italic: true
                        color: colorMsg
                    }

                    MouseArea {
                        id: mouseArea
                        anchors.fill: parent
                        acceptedButtons: Qt.LeftButton | Qt.RightButton
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor

                        onClicked: (mouse) => {
                            if (mouse.button === Qt.RightButton || mouse.button === Qt.LeftButton) {
                                chatMenu.user = nick
                                chatMenu.popup()
                            }
                        }
                    }
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
                    enabled: !twitchBot.isWorking
                    onClicked: {
                        twitchBot.startBot()
                    }
                }
                Button {
                    id: nonebutton
                    text: "Turn Off"
                    highlighted: true
                    Material.accent: Material.Red
                    enabled: twitchBot.isWorking
                    onClicked: {
                        twitchBot.stopBot()
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
                    text: chatView.opacity === 1 ? "Hide" : "Show"
                    highlighted: true
                    Material.accent: Material.BlueGrey
                    onClicked: {
                        opacityAnimation.stop()
                        chatView.opacity = chatView.opacity === 1 ? 0 : 1
                    }
                }
                Button {
                    id: test
                    text: "Test"
                    highlighted: true
                    Material.accent: Material.BlueGrey
                    onClicked: {
                        chatList.append({"nick": "huesos", "msg": "huesos: ya hochu pizzu" + chatView.count})
                        page.counter += 1
                    }
                }
            }
        }
    }

    Connections {
        target: twitchBot

        function onMessageReceived(user_name, message, user_color) {
            console.log(user_name.length)
            var userLen = user_name.length - 36
            var msg = "<font color=\"" + user_color + "\"><b>" + user_name + "</b></font><font>:" + message + "</font>"
            chatList.append({"nick": user_name, "msg": msg})
            chatView.opacity = 1
            opacityAnimation.stop()
            timerchat.restart()
        }
    }
}
