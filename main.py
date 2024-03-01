import sys
import time

from PySide6.QtCore import Qt, QEasingCurve, QPropertyAnimation, QTimer, QRectF, QEvent, QThread, Property, QPoint, \
    QPointF, QSize, QSizeF
from PySide6.QtGui import QPainter, QImage, QBrush
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QGraphicsOpacityEffect, QLabel, QWidget, QHBoxLayout, QApplication, QPushButton, \
    QAbstractButton
import resources_rc


class JukeBox(QAbstractButton):

    def __init__(self, image: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(300, 300)
        self.image: QImage = None
        self.juke_image = QImage(":/images/images/juke.png")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.set_image(image)
        self._doing = True
        self._angle = 0

        self.rotate_animation = QPropertyAnimation(self, b"rotate", self)
        self.rotate_animation.setDuration(3000)
        self.rotate_animation.setLoopCount(-1)
        self.clicked.connect(self.control)

        self.restart()

    def control(self):
        if self.rotate_animation.state() == QPropertyAnimation.State.Paused:
            self.rotate_animation.resume()
        else:
            self.rotate_animation.pause()

    def restart(self):
        self.rotate_animation.setStartValue(0)
        self.rotate_animation.setEndValue(360)
        self.rotate_animation.start()

    def angle(self):
        return self._angle

    def set_angle(self, angle):
        self._angle = angle
        self.update()

    def set_image(self, filepath: str):
        self.image = QImage(filepath)
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        painter.setPen(Qt.PenStyle.NoPen)

        juke_side = min(self.width(), self.height())
        image_side = juke_side * 2 / 3
        target_x = self.width() / 2 - juke_side / 2
        target_y = self.height() / 2 - juke_side / 2
        sub = juke_side / 2 - image_side / 2
        juke_rect = QRectF(target_x, target_y, juke_side, juke_side)
        image_rect = juke_rect.adjusted(sub, sub, -sub, -sub)
        juke_image = self.juke_image.scaled(QSize(juke_side, juke_side), Qt.AspectRatioMode.KeepAspectRatio,
                                            Qt.TransformationMode.SmoothTransformation)
        image = self.image.scaled(image_rect.size().toSize(), Qt.AspectRatioMode.KeepAspectRatio,
                                  Qt.TransformationMode.SmoothTransformation)
        painter.setBrush(QBrush(image))
        painter.translate(image_rect.center())
        painter.rotate(self._angle)
        painter.translate(-image_side / 2, -image_side / 2)
        painter.drawEllipse(QRectF(0, 0, image_side, image_side))
        painter.translate(image_side / 2, image_side / 2)
        painter.rotate(-self._angle)
        painter.translate(-image_rect.center())
        painter.drawImage(juke_rect, juke_image)

    rotate = Property(int, angle, set_angle)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = JukeBox()
    w.set_image("images/q.jpg")
    w.show()
    sys.exit(app.exec())
