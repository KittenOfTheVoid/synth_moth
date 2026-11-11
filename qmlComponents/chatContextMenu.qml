import QtQuick 2.0
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1

Menu {
    Material.theme: Material.Dark
    Material.accent: Material.Red
    id: contextMenu
    property string user: ""

    MenuItem {
        text: qsTr("Ban 1 sec")
        onClicked: {
            twitchBot.banUser(user, 1)
        }
    }
    MenuItem {
        text: qsTr("Ban 10 min")
        onClicked: {
            twitchBot.banUser(user, 600)
        }
    }
    MenuItem {
        text: qsTr("Permanent ban")
        onClicked: {
            twitchBot.banUser(user, -1)
        }
    }
}
