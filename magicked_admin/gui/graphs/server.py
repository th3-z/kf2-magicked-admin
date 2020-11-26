import time

from PySide2.QtCore import Slot, QMargins, QDateTime
from PySide2.QtWidgets import QWidget, QHBoxLayout
from PySide2.QtCharts import QtCharts
from PySide2.QtGui import QPainter, Qt

from database.queries.graphs import players_time, kills_time
from gui.graphs.factory import axis_x_week, axis_x_day


class PlayersGraph(QWidget):
    def __init__(self, parent, server):
        super().__init__(parent)

        layout = QHBoxLayout(self)

        self.server = server

        self.setMinimumWidth(580)
        self.setMinimumHeight(230)

        self.chart = QtCharts.QChart()
        self.chart.setAnimationOptions(QtCharts.QChart.AllAnimations)
        self.chart.legend().setVisible(False)
        self.chart.setMargins(QMargins(0, 0, 0, 0))

        self.series = QtCharts.QLineSeries()
        self.series.setName("Players")
        self.add_data(players_time(self.server.server_id))
        self.chart.addSeries(self.series)

        axis_x = axis_x_day()
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        self.series.attachAxis(axis_x)

        axis_y = QtCharts.QValueAxis()
        axis_y.setTickCount(7)
        axis_y.setLabelFormat("%d")
        axis_y.setTitleText("Players")
        axis_y.setMax(6)
        axis_y.setMin(0)
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        self.series.attachAxis(axis_y)

        chart_view = QtCharts.QChartView(self.chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(chart_view)

    def add_data(self, data):
        self.series.clear()

        for row in data:
            self.series.append(row['date'] * 1000, int(row['players']))


class KillsGraph(QWidget):
    def __init__(self, parent, server):
        super().__init__(parent)

        layout = QHBoxLayout(self)

        self.server = server

        self.setMinimumWidth(580)
        self.setMinimumHeight(230)

        self.chart = QtCharts.QChart()
        self.chart.setAnimationOptions(QtCharts.QChart.AllAnimations)
        self.chart.legend().setVisible(False)
        self.chart.setMargins(QMargins(0, 0, 0, 0))

        self.series = QtCharts.QLineSeries()
        self.series.setName("Kills")
        self.add_data(kills_time(self.server.server_id))
        self.chart.addSeries(self.series)

        axis_x = axis_x_day()
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        self.series.attachAxis(axis_x)

        axis_y = QtCharts.QValueAxis()
        axis_y.setTickCount(7)
        axis_y.setLabelFormat("%d")
        axis_y.setTitleText("Kills")
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        self.series.attachAxis(axis_y)

        chart_view = QtCharts.QChartView(self.chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(chart_view)

    def add_data(self, data):
        self.series.clear()

        for row in data:
            self.series.append(row['time'] * 1000, int(row['kills']))