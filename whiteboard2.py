from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from video2 import make_hz_videos
import sys


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("painter")
        self.resize(1920, 1080)
        self.setStyleSheet("background:#A8A8A8;")

        self.last_x, self.last_y = None, None
        self.penSize = 10

        self.canvasColor = "#ffffff"

        self.color_dict = {
            "black": "#1C1C1C",
            "red": "#CB1B45",
            "blue": "#0D5661",
            "yellow": "#F9BF45",
        }

        self.currentColor = QColor(self.color_dict["black"])

        self.img_dict = {
            "pen": "img/pen.png",
            "eraser": "img/eraser.png",
            "black": "img/black.png",
            "arrow-top": "img/arrow/top.png",
            "arrow-down": "img/arrow/down.png",
            "arrow-left": "img/arrow/left.png",
            "arrow-right": "img/arrow/right.png",
        }
        self.initUI()

    def initUI(self):
        side_width = 480

        self.canvas = QPixmap(1920 - side_width, 1080)
        self.canvas.fill(self.canvasColor)

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(side_width, 0, 1520, 1080)
        self.label.setPixmap(self.canvas)

        btn_gap = 50
        btn_width = 150

        self.penBtn = QtWidgets.QPushButton(self)
        self.penBtn.setStyleSheet(
            """
                QPushButton{
                    background:rgba( 255, 255, 255, 100% );
                    border-image:url('img/pen.png')
                }
                """
        )
        self.penBtn.setGeometry(65, 65, btn_width, btn_width)
        self.penBtn.clicked.connect(lambda: self.setColor(self.color_dict["black"]))

        # self.eraserBtn = QtWidgets.QPushButton(self)
        # self.eraserBtn.setStyleSheet(
        #     """
        #         QPushButton{
        #             background:rgba( 255, 255, 255, 100% );
        #             border-image:url('img/eraser.png')
        #         }
        #         """
        # )
        # self.eraserBtn.setGeometry(
        #     65 + btn_width * 1 + btn_gap, 65, btn_width, btn_width
        # )
        # self.eraserBtn.clicked.connect(lambda: self.setColor(self.canvasColor))

        self.eraser_btn = self.hz_img(
            "img/eraser",
            hz=6,
            x=(65 + btn_width * 1 + btn_gap),
            y=65,
            w=btn_width,
            h=btn_width,
        )

        self.colorBtn1 = QtWidgets.QPushButton(self)
        self.colorBtn1.setStyleSheet(
            """
                QPushButton{
                    background:"""
            + self.color_dict["black"]
            + """;
                }
                """
        )
        self.colorBtn1.setGeometry(
            65, 65 + btn_width * 1 + btn_gap, btn_width, btn_width
        )
        self.colorBtn1.clicked.connect(lambda: self.setColor(self.color_dict["black"]))

        self.colorBtn2 = QtWidgets.QPushButton(self)
        self.colorBtn2.setStyleSheet(
            """
                QPushButton{
                    background:"""
            + self.color_dict["red"]
            + """;;
                }
                """
        )
        self.colorBtn2.setGeometry(
            65 + btn_width * 1 + btn_gap,
            65 + btn_width * 1 + btn_gap,
            btn_width,
            btn_width,
        )
        self.colorBtn2.clicked.connect(lambda: self.setColor(self.color_dict["red"]))

        self.colorBtn3 = QtWidgets.QPushButton(self)
        self.colorBtn3.setStyleSheet(
            """
                QPushButton{
                    background:"""
            + self.color_dict["blue"]
            + """;;
                }
                """
        )
        self.colorBtn3.setGeometry(
            65,
            65 + btn_width * 2 + btn_gap * 2,
            btn_width,
            btn_width,
        )
        self.colorBtn3.clicked.connect(lambda: self.setColor(self.color_dict["blue"]))

        self.colorBtn4 = QtWidgets.QPushButton(self)
        self.colorBtn4.setStyleSheet(
            """
                QPushButton{
                    background:"""
            + self.color_dict["yellow"]
            + """;;
                }
                """
        )
        self.colorBtn4.setGeometry(
            65 + btn_width * 1 + btn_gap,
            65 + btn_width * 2 + btn_gap * 2,
            btn_width,
            btn_width,
        )
        self.colorBtn4.clicked.connect(lambda: self.setColor(self.color_dict["yellow"]))

        self.confirmBtn = QtWidgets.QPushButton(self, "Confirm")
        self.confirmBtn.setStyleSheet(
            """
                QPushButton{
                    background: #ffffff;
                }
                """
        )
        self.confirmBtn.setGeometry(
            65,
            1080 - 65 - 150,
            350,
            150,
        )
        self.confirmBtn.clicked.connect(
            lambda: self.setColor(self.color_dict["yellow"])
        )

    def mousePressEvent(self, event):
        mx = int(QEnterEvent.position(event).x() - 480)
        my = int(QEnterEvent.position(event).y())
        qpainter = QPainter()
        qpainter.begin(self.canvas)
        qpainter.setPen(
            QPen(
                self.currentColor,
                self.penSize,
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
            )
        )
        qpainter.drawPoint(mx, my)
        qpainter.end()
        self.label.setPixmap(self.canvas)
        self.update()

    def mouseMoveEvent(self, event):
        mx = int(QEnterEvent.position(event).x() - 480)
        my = int(QEnterEvent.position(event).y())
        if self.last_x is None:
            self.last_x = mx
            self.last_y = my
            return
        qpainter = QPainter()
        qpainter.begin(self.canvas)
        qpainter.setPen(
            QPen(
                self.currentColor,
                self.penSize,
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
            )
        )
        qpainter.drawLine(self.last_x, self.last_y, mx, my)
        qpainter.end()
        self.label.setPixmap(self.canvas)
        self.update()
        self.last_x = mx
        self.last_y = my

    def mouseReleaseEvent(self, event):
        self.last_x, self.last_y = None, None

    def setColor(self, color):
        self.currentColor = QColor(color)

    def confirmEvent(self):
        pass

    def hz_img(self, img_path, hz, x, y, w=150, h=150):
        video = make_hz_videos(w, h, hz, img_path)
        player = QMediaPlayer(self)
        player.setSource(QUrl(img_path + "_video_" + str(hz) + ".mp4"))
        videoWidget = QVideoWidget(self)
        videoWidget.setGeometry(x, y, w, h)
        player.setVideoOutput(videoWidget)
        videoWidget.show()
        player.setLoops(-1)
        player.play()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec())
