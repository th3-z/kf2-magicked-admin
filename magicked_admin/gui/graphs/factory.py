import time

from PySide2.QtCore import QDateTime
from PySide2.QtCharts import QtCharts


def axis_x_week():
    axis = QtCharts.QDateTimeAxis()
    axis.setTickCount(8)
    axis.setFormat("MM/dd")
    axis.setMin(QDateTime.fromSecsSinceEpoch(
        int(time.time() - (60 * 60 * 24 * 7)))
    )
    axis.setMax(QDateTime.fromSecsSinceEpoch(
        int(time.time()))
    )

    return axis


def axis_x_day():
    axis = QtCharts.QDateTimeAxis()
    axis.setTickCount(12)
    axis.setFormat("hh:mm")
    axis.setMin(QDateTime.fromSecsSinceEpoch(
        int(time.time() - (60 * 60 * 1)))
    )
    axis.setMax(QDateTime.fromSecsSinceEpoch(
        int(time.time()))
    )

    return axis
