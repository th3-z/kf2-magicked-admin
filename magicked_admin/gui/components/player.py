from gui.components.widgets import BlinkLabel
from PySide2.QtCore import QPropertyAnimation, Slot
from PySide2.QtGui import QColor, QPixmap
from PySide2.QtWidgets import (QHBoxLayout, QLabel, QProgressBar, QPushButton,
                               QVBoxLayout, QWidget)
from utils import find_data_file
from web_admin.constants import PlayerUpdateData

STYLE_HP = """
QProgressBar {
    border-radius: 0;
    background-color: #f00;
    height: 0.3em;
    text-align: center;
}

QProgressBar::chunk {
    border-radius: 0;
    background-color: #0f0;
}
"""


class PlayerWidget(QWidget):
    def __init__(self, player):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.player = player

        perk_icon = QLabel()
        pm_perk_icon = QPixmap(find_data_file('gui/res/logo.png'))
        pm_perk_icon = pm_perk_icon.scaledToHeight(32)
        perk_icon.setPixmap(pm_perk_icon)
        layout.addWidget(perk_icon)

        center_left = QWidget()
        center_left_layout = QVBoxLayout(center_left)
        center_left_layout.setContentsMargins(0, 0, 0, 0)

        line_name = QWidget()
        line_name_layout = QHBoxLayout(line_name)
        line_name_layout.setContentsMargins(0, 0, 0, 0)
        line_name_layout.addWidget(QLabel(player.country))
        line_name_layout.addWidget(QLabel(player.username))
        self.perk = QLabel((player.perk or "") + " lv. " + str(player.perk_level))
        line_name_layout.addWidget(self.perk)
        self.ping = QLabel(str(player.ping) + " ms")
        line_name_layout.addWidget(self.ping)

        center_left_layout.addWidget(line_name)

        self.hp = QProgressBar()
        self.hp.setStyleSheet(STYLE_HP)
        self.hp.setMaximum(player.max_health)
        self.hp.setValue(player.health)
        self.hp.setFormat("{} / {}".format(player.health, player.max_health))
        center_left_layout.addWidget(self.hp)

        layout.addWidget(center_left)

        center_right = QWidget()
        center_right.setMinimumWidth(80)
        center_right_layout = QVBoxLayout(center_right)
        center_right_layout.setContentsMargins(0, 0, 0, 0)

        self.dosh = BlinkLabel(str(player.dosh) + "£", blink_color=QColor(0, 255, 0))
        center_right_layout.addWidget(self.dosh)
        self.kills = BlinkLabel(str(player.kills) + " Kills", blink_color=QColor(255, 0, 0))
        center_right_layout.addWidget(self.kills)

        layout.addWidget(center_right)

        buttons = QWidget()
        buttons_layout = QVBoxLayout(buttons)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.addWidget(QPushButton("Kick"))
        buttons_layout.addWidget(QPushButton("Stats"))
        layout.addWidget(buttons)

        player.signals.player_update.connect(self.update)

        self.kills_prev = player.kills
        self.dosh_prev = player.dosh

        self.hp_anim = None

    @Slot(PlayerUpdateData)
    def update(self, player_update_data):
        self.hp.setMaximum(self.player.max_health)
        self.hp_anim = QPropertyAnimation(self.hp, b"value")
        self.hp_anim.setDuration(200)
        self.hp_anim.setStartValue(self.hp.value())
        self.hp_anim.setEndValue(player_update_data.health)
        self.hp_anim.start()
        self.hp.setFormat("{} / {}".format(player_update_data.health, self.player.max_health))

        self.kills.setText(str(player_update_data.kills) + " Kills")
        self.dosh.setText("£" + str(player_update_data.dosh))
        self.perk.setText(player_update_data.perk + " lv. " + str(self.player.perk_level))
        self.ping.setText(str(player_update_data.ping) + " ms")

        if player_update_data.kills > self.kills_prev:
            self.kills.blink()
        if player_update_data.dosh > self.dosh_prev:
            self.dosh.blink()

        self.kills_prev = player_update_data.kills
        self.dosh_prev = player_update_data.dosh
