import logging

from PySide2.QtCore import Signal, Slot, QObject, QUrl
from PySide2.QtWidgets import QVBoxLayout, QPlainTextEdit, QPushButton, QWidget, QLabel, QSpacerItem, QSizePolicy
from PySide2.QtGui import QPixmap, Qt, QFont, QDesktopServices, QPainter
from PySide2.QtCharts import QtCharts

from utils import find_data_file
from database.queries.graphs import players_time, kills_time

logger = logging.getLogger(__name__)


class WelcomeWi(QWidget):
    def __init__(self, parent, magicked_admin):
        super().__init__(parent)

        self.header = QLabel()
        self.header.setText("Killing Floor 2 Magicked Admin")
        self.header.setFont(QFont('nosuchfont', 24))
        self.header.setAlignment(Qt.AlignHCenter)

        self.version = QLabel()
        self.version.setText(magicked_admin.version)
        self.version.setAlignment(Qt.AlignHCenter)

        self.logo = QLabel()
        pm_logo = QPixmap(find_data_file('gui/res/logo.png'))
        pm_logo.scaledToHeight(64)
        self.logo.setPixmap(pm_logo)
        self.logo.setAlignment(Qt.AlignHCenter)

        self.guide = QLabel()
        self.guide.setText("<em>No server selected, add or select a server at the top-right.</em>")
        self.guide.setAlignment(Qt.AlignHCenter)

        self.docs = QLabel()
        doclink = "https://kf2-ma.th3-z.xyz"
        self.docs.setText("<a href='{}'>Documentation</a>".format(doclink))
        self.docs.setAlignment(Qt.AlignHCenter)
        self.docs.linkActivated.connect(self.link)

        layout = QVBoxLayout(self)
        layout.addWidget(self.header)
        layout.addWidget(self.version)
        layout.addWidget(self.logo)
        layout.addWidget(self.guide)
        layout.addWidget(self.docs)
        layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

    def link(self, url):
        QDesktopServices.openUrl(QUrl(url))


class ServerWi(QWidget):
    def __init__(self, parent, server):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(server.name))

        self.chart = QtCharts.QChart()
        self.chart.setAnimationOptions(QtCharts.QChart.AllAnimations)
        self.add_series(players_time())

        self.chart_view = QtCharts.QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.chart_kills = QtCharts.QChart()
        self.chart_kills.setAnimationOptions(QtCharts.QChart.AllAnimations)
        self.add_series_kills(kills_time())

        self.kills_chart_view = QtCharts.QChartView(self.chart_kills)
        self.kills_chart_view.setRenderHint(QPainter.Antialiasing)

        layout.addWidget(self.chart_view)
        layout.addWidget(self.kills_chart_view)


    def add_series(self, data):
        series = QtCharts.QLineSeries()
        series.setName("Players")

        for row in data:
            series.append(row['time']*1000, row['players'])

        self.chart.addSeries(series)

        axis_x = QtCharts.QDateTimeAxis()
        axis_x.setTickCount(8)
        axis_x.setFormat("MM/dd")
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QtCharts.QValueAxis()
        axis_y.setTickCount(7)
        axis_y.setLabelFormat("%d")
        axis_y.setTitleText("Players")
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

    def add_series_kills(self, data):
        series = QtCharts.QLineSeries()
        series.setName("Kills")

        for row in data:
            series.append(row['time']*1000, row['kills'])

        self.chart_kills.addSeries(series)

        axis_x = QtCharts.QDateTimeAxis()
        axis_x.setTickCount(8)
        axis_x.setFormat("MM/dd")
        self.chart_kills.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QtCharts.QValueAxis()
        axis_y.setTickCount(10)
        axis_y.setLabelFormat("%d")
        axis_y.setTitleText("Kills")
        self.chart_kills.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)


class TabServer(QWidget):

    def __init__(self, parent, magicked_admin):
        super().__init__(parent)

        self._server = None

        self.welcome_widget = WelcomeWi(self, magicked_admin)
        self.server_widget = None

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(
            self.welcome_widget
        )

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, server):
        if server == self._server:
            return

        if not server:
            self.server_widget.deleteLater()
            self.server_widget = None
            self.welcome_widget.show()
        else:
            self.welcome_widget.hide()
            self.server_widget = ServerWi(self, server)
            self.layout.addWidget(self.server_widget)
        self._server = server


