from typing import Any

from PyQt6.QtCore import QPointF, QRectF, QSize, Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QPixmap, QWheelEvent
from PyQt6.QtWidgets import (
    QFrame, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView
)


class ImageViewer(QGraphicsView):
    """ImageViewer"""

    imageClicked = pyqtSignal(QPointF)

    def __init__(self, qsize: QSize):
        super(ImageViewer, self).__init__()
        self._qsize = qsize
        self._zoom = 0
        self._empty = True
        self._scene = QGraphicsScene(self)
        self._image = QGraphicsPixmapItem()
        self._scene.addItem(self._image)
        self.setScene(self._scene)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.Shape.NoFrame)

    def fitInView(self, scale: bool = True, **kwargs: Any) -> None:
        """
        Overrides fitInView of the QGraphicsView superclass

        :param scale:
        :param kwargs:
        :return:
        """
        rect = QRectF(self._image.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if not self._empty:
                scene_rect = self.transform().mapRect(
                    rect
                )  # Dimensions of th image and applies transformation
                factor = min(
                    self._qsize.width() / scene_rect.width(),
                    self._qsize.height() / scene_rect.height(),
                )
                self.scale(factor, factor)
            self._zoom = 0

    def wheelEvent(self, event: QWheelEvent) -> None:
        """
        Overrides wheelEvent of the QGraphicsView superclass

        :param event:
        :return:
        """
        if not self._empty:
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Overrides mousePressEvent of the QGraphicsView superclass

        :param event:
        :return:
        """
        if self._image.isUnderMouse():
            self.imageClicked.emit(self.mapToScene(event.position().toPoint()))

        super(ImageViewer, self).mousePressEvent(event)

    def set_image(self, pixmap: QPixmap = None) -> None:
        """
        Initialize image to the ImageViewer

        :param pixmap:
        :return:
        """
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
            self._image.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
            self._image.setPixmap(QPixmap())
        self.fitInView()
