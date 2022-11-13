import sys
from time import time, sleep
from math import sin, cos, radians as rad
from languages import *

from PyQt5.QtCore import Qt, QRect, QPoint, QSize
from PyQt5.QtGui import QColor, QIcon, QFont, QPainter, QPixmap, QPen, QBrush
from PyQt5.QtWidgets import QWidget, QMainWindow, QMenu, QMenuBar, QAction
from PyQt5.QtWidgets import QHBoxLayout, QInputDialog, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QPushButton, QFileDialog, QSlider, QErrorMessage
from PyQt5.QtWidgets import QSpinBox, QColorDialog, QFontDialog, QDialog
from PyQt5.QtWidgets import QToolBar, QDialogButtonBox, QApplication

# Подключим функцию для задания
# значка приложения на панели задач
# Не на Виндовс она не сработает
try:
    from PyQt5.QtWinExtras import QtWin
    myappid = 'mycompany.myproduct.subproduct.version'
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

# Зададим полезные константы
BRUSH = 'Кисть'
PEN = 'Карандаш'
LINE = 'Прямая'
ELLIPSE = 'Овал'
RECTANGLE = 'Прямоугольник'
TRIANGLE = 'Треугольник'
ARC = 'Дуга'
HEART = 'Сердце'

RUSSIAN = 'Русский'
ENGLISH = 'English'
ITALIAN = 'Italiano'
CHINISE = '中文'
UCRAINE = 'Український'

'''
pyuic5 note.ui -o frog.py
pyuic5 dialog.ui -o frog.py
pyrcc5 -o res.py res.qrc
pyinstaller --onefile --noconsole --icon=icon.ico PyPaint.py
pyinstaller --onefile red.py
pyinstaller --onefile --noconsole red.py
'''


# Создадим классы фигур, которыми мы будем рисовать.
# Каждому добавим метод для вывода этой фигуры на фон окна

# Класс точек, нарисованных карандашом
class Point:
    def __init__(self, x, y, color):
        self.x, self.y, self.color = int(x), int(y), QColor(color)

    def __str__(self):
        # Этот метод нужен для записи объекта в файл.
        # Передает основную информацию об объекте
        m = '\t'.join([str(i) for i in [self.x, self.y, self.color.name()]])
        return self.__class__.__name__ + '\t' + m

    def draw(self, painter):
        set_pen_and_brush(painter, self.color)
        painter.drawPoint(self.x, self.y)


# Класс точек, нарисованных кистью
class BrushPoint:
    def __init__(self, x, y, width, color):
        self.x, self.y = int(x), int(y)
        self.width, self.color = int(width), QColor(color)

    def __str__(self):
        # Этот метод нужен для записи объекта в файл.
        # Передает основную информацию об объекте
        m = [str(i) for i in [self.x, self.y, self.width, self.color.name()]]
        return self.__class__.__name__ + '\t' + '\t'.join(m)

    def draw(self, painter):
        width = self.width
        set_pen_and_brush(painter, self.color)
        painter.drawEllipse(self.x - width // 2, self.y - width // 2, width, width)


# Родительский класс для будущих фигур
class Shape:
    def __init__(self, x1, y1, x2, y2, width, color):
        self.x1, self.y1, self.x2, self.y2 = int(x1), int(y1), int(x2), int(y2)
        self.width, self.color = int(width), QColor(color)

    def __str__(self):
        # Этот метод нужен для записи объекта в файл.
        # Передает основную информацию об объекте
        m = [self.x1, self.y1, self.x2, self.y2, self.width, self.color.name()]
        m = list(map(lambda i: str(i), m))
        return self.__class__.__name__ + '\t' + '\t'.join(m)


# Класс фигуры "Прямая линия"/"Линия кисти"
class Line(Shape):
    def draw(self, painter):
        set_pen_and_brush(painter, self.color, self.width)
        painter.drawLine(self.x1, self.y1, self.x2, self.y2)


# Класс фигуры "Овал/Круг"
class Ellipse(Shape):
    def draw(self, painter):
        set_pen_and_brush(painter, self.color)
        dx, dy = self.x2 - self.x1, self.y2 - self.y1
        painter.drawEllipse(self.x1, self.y1, dx, dy)


# Класс фигуры "Прямоугольник"
class Rectangle(Shape):
    def draw(self, painter):
        set_pen_and_brush(painter, self.color)
        dx, dy = self.x2 - self.x1, self.y2 - self.y1
        painter.drawRect(self.x1, self.y1, dx, dy)


# Класс фигуры "Треугольник"
class Triangle(Shape):
    def draw(self, painter):
        set_pen_and_brush(painter, self.color)
        dx, dy = self.x2 - self.x1, self.y2 - self.y1
        painter.drawPolygon(QPoint(self.x1, self.y2),
                            QPoint(self.x1 + dx // 2, self.y1),
                            QPoint(self.x2, self.y2))


# Класс фигуры "Дуга"
class Arc(Shape):
    def draw(self, painter):
        set_pen_and_brush(painter, self.color, self.width)
        dx, dy = self.x2 - self.x1, self.y2 - self.y1
        if dy > 0:
            painter.drawArc(self.x1, self.y1, dx, dy * 2, 0, 16 * 180)
        else:
            painter.drawArc(self.x1, self.y1, dx, dy * 2, 16 * 180, 16 * 180)


# Класс фигуры "Сердце"
class Heart(Shape):
    def draw(self, painter):
        set_pen_and_brush(painter, self.color, 5)
        # Рекурсивная функция рисования залитых сердец
        draw_heart(painter, self.x1, self.y1, self.x2, self.y2, 5)


# Создадим класс окна, на котором будем рисовать
class Canvas(QMainWindow):
    def __init__(self):
        super().__init__()
        # Изначальное имя
        self.filename = 'Безымянный'
        # Изначальный язык
        self.language = RUSSIAN
        # Не изменялся
        self.changed = False
        self.rect = QRect(0, 21, 1200, 800)
        self.objects = []
        self.deleted_objects = []
        self.brushLines = False
        self.x1, self.y1 = -1, -1
        # Инструмент по умолчанию кисть и ширина 10
        self.tool = BRUSH
        self.width = 10
        # Цвета по умолчанию
        self.color = QColor(0, 0, 0)
        self.color2 = QColor(255, 255, 255)
        self.shift_pressed = False
        self.help_window = None
        self.L_systems = None
        self.polygons = None
        self.struct()
        self.set_shortcuts()
        self.connecting()
        canvas_set_language(self, RUSSIAN)
        self.coords = self.toolBar.geometry()

    # Задаём внешний вид окна, в большинстве нарисованного в QtDesigner'e
    # Создаём действия и тулбар
    def struct(self):
        self.setTitle()
        self.resize(1200, 800)
        self.label = QLabel(self)

        try:
            self.setWindowIcon(QIcon('icon.png'))
        except Exception:
            pass
        self.setMinimumSize(720, 400)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.menu_bar = QMenuBar(self)
        self.file = QMenu(self.menu_bar)
        self.edit = QMenu(self.menu_bar)
        self.tools = QMenu(self.menu_bar)
        self.jokes = QMenu(self.menu_bar)
        self.help = QMenu(self.menu_bar)
        self.setMenuBar(self.menu_bar)
        self.toolBar = QToolBar(self)
        self.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.btnCancel = QAction(self)
        self.btnReturn = QAction(self)
        self.btnLanguage = QAction(self)
        self.btnChangeFont = QAction(self)
        self.btnReturnToolBar = QAction(self)
        self.btnChange_canvas_size = QAction(self)

        self.btnToolPen = QAction(self)
        self.btnToolBrush = QAction(self)
        self.btnToolLine = QAction(self)
        self.btnToolEllipse = QAction(self)
        self.btnToolRectangle = QAction(self)
        self.btnToolTriangle = QAction(self)
        self.btnToolArc = QAction(self)
        self.btnToolHeart = QAction(self)
        self.btnToolWidtn = QAction(self)

        self.btnPen = QAction(self)
        self.btnBrush = QAction(self)
        self.btnLine = QAction(self)
        self.btnEllipse = QAction(self)
        self.btnRectangle = QAction(self)
        self.btnTriangle = QAction(self)
        self.btnArc = QAction(self)
        self.btnHeart = QAction(self)
        self.btnWidtn = QAction(self)

        self.btnColor1 = QAction(self)
        pixmap = QPixmap(17, 17)
        pixmap.fill(self.color)
        self.btnColor1.setIcon(QIcon(pixmap))
        self.btnColor2 = QAction(self)
        pixmap = QPixmap(17, 17)
        pixmap.fill(self.color2)
        self.btnColor2.setIcon(QIcon(pixmap))
        self.btnPolygons = QAction(self)
        self.btnSystems = QAction(self)
        self.btnNew = QAction(self)
        self.btnOpen = QAction(self)
        self.btnSave = QAction(self)
        self.btnExport = QAction(self)
        self.btnExit = QAction(self)
        self.btnHelp = QAction(self)

        self.tools.addAction(self.btnPen)
        self.tools.addAction(self.btnBrush)
        self.tools.addAction(self.btnLine)
        self.tools.addAction(self.btnEllipse)
        self.tools.addAction(self.btnRectangle)
        self.tools.addAction(self.btnTriangle)
        self.tools.addAction(self.btnArc)
        self.tools.addAction(self.btnHeart)
        self.tools.addSeparator()
        self.tools.addAction(self.btnWidtn)
        self.tools.addAction(self.btnColor1)
        self.tools.addAction(self.btnColor2)
        self.jokes.addAction(self.btnPolygons)
        self.jokes.addAction(self.btnSystems)
        self.jokes.addSeparator()
        self.jokes.addAction(self.btnChangeFont)
        self.jokes.addAction(self.btnLanguage)
        self.edit.addAction(self.btnCancel)
        self.edit.addAction(self.btnReturn)
        self.edit.addSeparator()
        self.edit.addAction(self.btnChange_canvas_size)
        self.edit.addAction(self.btnReturnToolBar)
        self.file.addAction(self.btnNew)
        self.file.addAction(self.btnOpen)
        self.file.addAction(self.btnSave)
        self.file.addAction(self.btnExport)
        self.file.addSeparator()
        self.file.addAction(self.btnExit)
        self.help.addAction(self.btnHelp)
        self.menu_bar.addAction(self.file.menuAction())
        self.menu_bar.addAction(self.edit.menuAction())
        self.menu_bar.addAction(self.tools.menuAction())
        self.menu_bar.addAction(self.jokes.menuAction())
        self.menu_bar.addAction(self.help.menuAction())
        self.toolBar.addAction(self.btnToolPen)
        self.toolBar.addAction(self.btnToolBrush)
        self.toolBar.addAction(self.btnToolLine)
        self.toolBar.addAction(self.btnToolEllipse)
        self.toolBar.addAction(self.btnToolRectangle)
        self.toolBar.addAction(self.btnToolTriangle)
        self.toolBar.addAction(self.btnToolArc)
        self.toolBar.addAction(self.btnToolHeart)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.btnToolWidtn)
        self.toolBar.addAction(self.btnColor1)
        self.toolBar.addAction(self.btnColor2)
        self.toolBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

    # Установка сочетаний клавиш
    def set_shortcuts(self):
        self.btnPen.setShortcut('Alt+1')
        self.btnBrush.setShortcut('Alt+2')
        self.btnLine.setShortcut('Alt+3')
        self.btnEllipse.setShortcut('Alt+4')
        self.btnRectangle.setShortcut('Alt+5')
        self.btnTriangle.setShortcut('Alt+6')
        self.btnArc.setShortcut('Alt+7')
        self.btnHeart.setShortcut('Alt+8')
        self.btnWidtn.setShortcut('Alt+9')
        self.btnColor1.setShortcut('Alt+0')
        self.btnColor2.setShortcut('Alt+-')
        self.btnCancel.setShortcut('Ctrl+Z')
        self.btnReturn.setShortcuts(('Ctrl+Y', 'Ctrl+Shift+Z'))
        self.btnNew.setShortcut('Ctrl+N')
        self.btnOpen.setShortcut('Ctrl+O')
        self.btnSave.setShortcut('Ctrl+S')
        self.btnExport.setShortcut('Ctrl+E')
        self.btnExit.setShortcut('Ctrl+Q')
        self.btnHelp.setShortcut('F1')

    # Соединение кнопок с их функциями-действиями
    def connecting(self):
        list_btns = [self.btnPen, self.btnBrush, self.btnLine, self.btnEllipse,
                     self.btnRectangle, self.btnTriangle, self.btnArc, self.btnHeart]

        list_tool_btns = [self.btnToolPen, self.btnToolBrush, self.btnToolLine,
                          self.btnToolEllipse, self.btnToolRectangle, self.btnToolTriangle,
                          self.btnToolArc, self.btnToolHeart]

        list_funcs = [self.set_pen, self.set_brush, self.set_line, self.set_ellipse,
                      self.set_rectangle, self.set_triangle, self.set_arc, self.set_heart]
        for n, btn in enumerate(list_btns):
            btn.triggered.connect(list_funcs[n])
            list_tool_btns[n].triggered.connect(list_funcs[n])

        self.change_font(QFont('Consolas', 9))

        all_actions = self.file.actions() + self.edit.actions() + self.help.actions()
        all_actions += self.tools.actions() + self.jokes.actions()
        for i in all_actions:
            i.setFont(QFont('Consolas', 9))

        btns = [self.btnWidtn, self.btnToolWidtn, self.btnColor1, self.btnColor2,
                self.btnPolygons, self.btnSystems, self.btnCancel, self.btnReturn,
                self.btnLanguage, self.btnChangeFont, self.btnReturnToolBar,
                self.btnChange_canvas_size, self.btnNew, self.btnOpen, self.btnSave,
                self.btnExport, self.btnExit, self.btnHelp]
        funcs = [self.set_width, self.set_width, self.set_color1, self.set_color2,
                 self.call_polygons, self.call_l_systems, self.add_deleted_object,
                 self.return_last_deleted_object, self.change_language, self.change_font,
                 self.return_tool_bar, self.change_canvas_size, self.new, self.open,
                 self.save, self.export_picture, self.close, self.call_help]

        for n, btn in enumerate(btns):
            btn.triggered.connect(funcs[n])

    # Переопределим функцию рисования окна.
    # Добавим показ объектов, нарисованных пользователем
    def paintEvent(self, event):
        self.toolBar.setContextMenuPolicy(Qt.NoContextMenu)
        painter = QPainter(self)
        painter.begin(self)

        # Нарисуем белый фон с тенью
        # В этом варианте область вне листа не закрашивается
        # set_pen_and_brush(painter, QColor(245, 245, 245))
        # painter.drawRect(0, 0, self.rect.width() + 4, self.rect.height() + 4)
        # set_pen_and_brush(painter, QColor(200, 200, 200))
        # painter.drawRect(0, 0, self.rect.width() + 3, self.rect.height() + 3)
        # set_pen_and_brush(painter, QColor(150, 150, 150))
        # painter.drawRect(0, 0, self.rect.width() + 2, self.rect.height() + 2)
        # set_pen_and_brush(painter, QColor(10, 10, 10))
        # painter.drawRect(0, 0, self.rect.width() + 1, self.rect.height() + 1)

        set_pen_and_brush(painter, QColor(255, 255, 255))
        painter.drawRect(self.rect)
        for i in self.objects:
            if i not in ('[', ']'):
                i.draw(painter)

        # Закрасим объекты вне листа
        # И нарисуем тень из кучи прямоугольников
        # В этом варианте область вне листа закрашивается
        cs = [20, 50, 120, 180, 220]
        for n, c in enumerate(cs):
            set_pen_and_brush(painter, QColor(c, c, c))
            painter.drawRect(self.rect.width() + n, 0, 1, self.rect.height() + 5 - n)
            painter.drawRect(0, self.rect.height() + n, self.rect.width() + 1 + n, 1)
        c = 240
        set_pen_and_brush(painter, QColor(c, c, c))
        painter.drawRect(self.rect.width() + 5, 0, 1000, self.rect.height() + 1000)
        painter.drawRect(0, self.rect.height() + 5, self.rect.width() + 6, 1000)

        # Сделаем белый фон за панелью инструментов,
        # если она зафиксирована в основном окне
        # Если этого не сделать, пользователь сможет закрашивать кнопки,
        # а это неудобно
        c = 245
        set_pen_and_brush(painter, QColor(c, c, c))
        if not self.toolBar.isWindow():
            painter.drawRect(self.toolBar.geometry())
        painter.end()

    # Переопределим функцию, вызывающуюся при нажатии на клавиши мыши
    def mousePressEvent(self, event):
        # Запомним координаты тул бара
        self.coords = self.toolBar.geometry()
        self.toolBar.move(10000, 0)
        x, y = event.x(), event.y()
        self.x1, self.y1 = x, y
        if event.button() == 1:
            # Одна кнопка мыши вызывает один цвет, другая другой
            standart = (x, y, x, y, self.width, self.color)
        else:
            standart = (x, y, x, y, self.width, self.color2)
        # На каждый инструмент свой класс вызываемых фигур
        if self.tool == BRUSH:
            if self.width == 1:
                if event.button() == 1:
                    self.add_object(Point(x, y, self.color))
                else:
                    self.add_object(Point(x, y, self.color2))
            else:
                if event.button() == 1:
                    self.add_object(BrushPoint(x, y, self.width, self.color))
                else:
                    self.add_object(BrushPoint(x, y, self.width, self.color2))
        elif self.tool == PEN:
            if event.button() == 1:
                self.add_object(Point(x, y, self.color))
            else:
                self.add_object(Point(x, y, self.color2))
        elif self.tool == LINE:
            self.add_object(Line(*standart))
        elif self.tool == ELLIPSE:
            self.add_object(Ellipse(*standart))
        elif self.tool == RECTANGLE:
            self.add_object(Rectangle(*standart))
        elif self.tool == TRIANGLE:
            self.add_object(Triangle(*standart))
        elif self.tool == ARC:
            self.add_object(Arc(*standart))
        elif self.tool == HEART:
            self.add_object(Heart(*standart))
        self.clear_deleted_objects()
        self.update()

    # Переопределим функцию, вызывающуюся при перемещении мыши с зажатой клавишей
    def mouseMoveEvent(self, event):
        x, y = event.x(), event.y()
        if self.x1 == -1 and self.y1 == -1:
            self.x1, self.y1 = x, y
            self.toolBar.move(10000, 0)
            self.add_object(BrushPoint(x, y, self.width, self.color))
        if self.tool == BRUSH:
            if not self.brushLines:
                # Скобочки нужны, чтобы при отмене действия
                # удалялась сразу вся линия, а не отдельные её части
                self.objects.insert(-1, '[')
                self.brushLines = True
            # Чтобы в линии не было пробелов,
            # будем рисовать линии, если расстояние между точками слишком большое
            if ((self.x1 - x) ** 2 + (self.y1 - y) ** 2) ** 0.5 > self.width / 2:
                try:
                    self.add_object(Line(self.x1, self.y1, x, y,
                                         self.width, self.objects[-1].color))
                except AttributeError:
                    self.add_object(Line(self.x1, self.y1, x, y, self.width, self.color))
            else:
                try:
                    self.add_object(BrushPoint(x, y, self.width, self.objects[-1].color))
                except AttributeError:
                    self.add_object(BrushPoint(x, y, self.width, self.color))
            self.update()
        elif self.tool == PEN:
            if not self.brushLines:
                self.objects.insert(-1, '[')
                self.brushLines = True
            try:
                self.add_object(Line(self.x1, self.y1, x, y, 1, self.objects[-1].color))
            except AttributeError:
                self.add_object(Line(self.x1, self.y1, x, y, 1, self.color))
            self.update()
        elif self.tool == LINE:
            if self.shift_pressed:
                # Рисуем линию, параллельную одной из осей координат
                # Параллельно какой выбираем тем, по какой оси проекция линии больше
                dx = x - self.objects[-1].x1
                dy = y - self.objects[-1].y1
                if abs(dx) < abs(dy):
                    if dx * dy < 0:
                        dx, dy = 0, dy
                    else:
                        dx, dy = 0, dy
                else:
                    if dx * dy < 0:
                        dx, dy = dx, 0
                    else:
                        dx, dy = dx, 0
                self.objects[-1].x2 = self.objects[-1].x1 + dx
                self.objects[-1].y2 = self.objects[-1].y1 + dy
            else:
                self.objects[-1].x2 = x
                self.objects[-1].y2 = y
            self.update()
        # Остальные фигуры редактируются одинаково,
        # так что можно записать их в одно условие
        elif self.tool in [ELLIPSE, RECTANGLE, TRIANGLE, ARC, HEART]:
            if self.shift_pressed:
                # Если нажат шифт,
                # Рисуем фигуру, у которой размер по х равен размеру по у
                dx = x - self.objects[-1].x1
                dy = y - self.objects[-1].y1
                if abs(dx) < abs(dy):
                    if dx * dy < 0:
                        dx, dy = dx, -dx
                    else:
                        dx, dy = dx, dx
                else:
                    if dx * dy < 0:
                        dx, dy = -dy, dy
                    else:
                        dx, dy = dy, dy
                self.objects[-1].x2 = self.objects[-1].x1 + dx
                self.objects[-1].y2 = self.objects[-1].y1 + dy
            else:
                self.objects[-1].x2 = x
                self.objects[-1].y2 = y
            self.update()
        # Поспим немного, чтобы увеличить расстояние между точками
        sleep(0.01)
        self.x1, self.y1 = x, y

    # Переопределим функцию отжатия клавиши мыши,
    # чтобы добавлять точку в конце нарисованной кистью или карандашом линии
    # Потому что если линия заканчивается на прямую, то конец словно отрубленный
    # А так же добавлять скобочку после свободных линий
    def mouseReleaseEvent(self, event):
        # Вернём тулбар
        self.toolBar.setGeometry(self.coords)
        if self.brushLines:
            if event.button() == 1:
                if self.tool == BRUSH:
                    self.add_object(BrushPoint(self.x1, self.y1,
                                                   self.width - 1, self.color))
                else:
                    self.add_object(Point(self.x1, self.y1, self.color))
            else:
                if self.tool == BRUSH:
                    self.add_object(BrushPoint(self.x1, self.y1,
                                                   self.width - 1, self.color2))
                else:
                    self.add_object(Point(self.x1, self.y1, self.color2))
            # Закончим рисование линии
            self.add_object(']')
            self.brushLines = False
        self.x1, self.y1 = -1, -1

    # Сделаем обработку нажатия клавиши Shift,
    # Чтобы можно было рисовать ровные фигуры и линии
    def keyPressEvent(self, event):
        if int(event.modifiers()) == Qt.ShiftModifier:
            self.shift_pressed = True
        self.update()

    # Отжатие шифта
    def keyReleaseEvent(self, event):
        if int(event.key()) == 16777248:
            self.shift_pressed = False
        self.update()

    # Если открыта справка, закроем её вместе с приложением
    # Также предложим сохранить файл
    def closeEvent(self, event):
        if self.want_you_save():
            self.save()
        if self.help_window and self.help_window.opened:
            self.help_window.close()

    def import_picture(self):
        text = "PNG (*.png);;JPEG (*.jpg);;All Files (*)"
        filename, *ok = QFileDialog.getOpenFileName(self, self.text_open,
                                                    '', text)
        if filename:
            self.filename = filename
            self.setTitle()
            self.pixmap = QPixmap(filename)
            self.label.setPixmap(self.pixmap)
            self.label.resize(self.pixmap.size())
            self.rect.setSize(self.pixmap.size())

    # Импорт изображения в нормальный формат
    def export_picture(self):
        coords = self.toolBar.geometry()
        coords2 = self.geometry()
        self.setGeometry(self.rect)
        # Убираем тулбар
        self.toolBar.move(10000, 0)
        x1, y1, x2, y2 = self.rect.getCoords()
        image = self.grab().copy(x1, y1 + 1, x2 + 1, y2 - 40)
        self.setGeometry(coords2)
        # Возвращаем тулбар
        self.toolBar.setGeometry(coords)
        text = "PNG (*.png);;JPEG (*.jpg);;All Files (*)"
        filename, *ok = QFileDialog.getSaveFileName(self, self.tsave,
                                                    self.filename, text)
        if filename:
            image.save(filename)

    # Функция создания нового файла
    def new(self):
        if self.want_you_save():
            # Предложим сохранение закрываемого файла
            self.save()
        ok = self.change_canvas_size()
        if ok:
            self.filename = 'Безымянный'
            self.setTitle()
            self.clear()
        self.update()

    # Очистить холст
    def clear(self):
        self.changed = False
        self.x1, self.y1 = 0, 0
        self.tool = BRUSH
        self.width = 10
        self.color = QColor(0, 0, 0)
        self.color2 = QColor(255, 255, 255)

        pixel_map = QPixmap(17, 17)
        pixel_map.fill(self.color)
        self.btnColor1.setIconText(self.tcolor + ' 1 (' + self.color.name() + ')')
        self.btnColor1.setIcon(QIcon(pixel_map))
        pixel_map = QPixmap(17, 17)
        pixel_map.fill(self.color2)
        self.btnColor2.setIconText(self.tcolor + ' 2 (' + self.color2.name() + ')')
        self.btnColor2.setIcon(QIcon(pixel_map))

        self.objects.clear()
        self.clear_deleted_objects()

    # Изменить размер листа
    def change_canvas_size(self):
        size_dialog = SizeDialog(self, self.tsizes[0], self.tsizes[1],
                                 self.tsizes[2], 1200, 800)
        size_dialog.exec()
        # Обрабатываем только диалог
        if size_dialog.accepted:
            self.rect.setWidth(size_dialog.width.value())
            self.rect.setHeight(size_dialog.height.value())
            return True
        return False

    # Создадим функцию сохранения рисунка в текстовом файле.
    # Записываем информацию о каждом нарисованном объекте,
    # чтобы потом можно было восстановить объекты по этой информации
    def save(self):
        s = self.bigtsave
        filename = QFileDialog.getSaveFileName(self, self.tsave, self.filename, s)[0]
        if filename:
            try:
                file = open(filename, 'w')
                self.changed = False
                self.filename = filename
                self.setTitle()
                file.write(str(self.rect.size().width()) + ', ' +
                           str(self.rect.size().height()))
                file.write('\n' + str(self.width))
                file.write('\n' + str(self.color.name()))
                file.write('\n' + str(self.color2.name()))
                file.write('\n' + '\n'.join([str(i) for i in self.objects]))
                file.close()
            except Exception:
                # Показываем ошибку если что-то не так и очищаем объекты
                error = QErrorMessage(self)
                error.showMessage(self.text_error)
                error.exec()
                self.clear()
                return

    def want_you_save(self):
        if self.changed:
            s = self.want_save_text
            self.dialog = UserConfirmationDialog(self, '', s)
            self.dialog.exec()
            if self.dialog.accepted:
                return True
        return False

    # Открываем ранее созданный в этой программе текстовый файл
    # Создаем каждый объект, передавая в класс информацию о нём
    # Все объекты добавляем в список нарисованных пользователем объектов
    def open(self):
        if self.want_you_save():
            self.save()
        # Выбор файла с рисунком
        s = self.bigtsave
        filename = QFileDialog.getOpenFileName(self, self.text_open, '', s)[0]
        if filename:
            try:
                self.changed = False
                self.filename = filename
                self.setTitle()
                file = open(filename, 'r')
                self.clear()
                self.update()
                data = file.read().split('\n')

                # Для удобства установим кисти и размер окна,
                # которые использовались при сохранении рисунка
                self.rect.setSize(QSize(*map(int, data[0].split(', '))))
                self.width = int(data[1])
                self.color = QColor(data[2])
                self.color2 = QColor(data[3])

                pixmap = QPixmap(17, 17)
                pixmap.fill(self.color)
                self.btnColor1.setIconText(self.tcolor + ' 1 (' +
                                           self.color.name() + ')')
                self.btnColor1.setIcon(QIcon(pixmap))
                pixmap = QPixmap(17, 17)
                pixmap.fill(self.color2)
                self.btnColor2.setIconText(self.tcolor + ' 2 (' +
                                           self.color2.name() + ')')
                self.btnColor2.setIcon(QIcon(pixmap))

                # Создаём каждый объект
                for i in data[4:]:
                    c, *args = i.split('\t')
                    if c in ('[', ']'):
                        self.add_object(c)
                    elif c == 'Point':
                        self.add_object(Point(*args))
                    elif c == 'BrushPoint':
                        self.add_object(BrushPoint(*args))
                    elif c == 'Line':
                        self.add_object(Line(*args))
                    elif c == 'Ellipse':
                        self.add_object(Ellipse(*args))
                    elif c == 'Rectangle':
                        self.add_object(Rectangle(*args))
                    elif c == 'Triangle':
                        self.add_object(Triangle(*args))
                    elif c == 'Arc':
                        self.add_object(Arc(*args))
                    elif c == 'Heart':
                        self.add_object(Heart(*args))
                    else:
                        raise ValueError
                file.close()
                self.changed = False
            except Exception:
                error = QErrorMessage(self)
                error.showMessage(self.text_error)
                error.exec()
                self.clear()
                return

    # Удобная функция
    def setTitle(self):
        self.setWindowTitle(self.filename + ' - PyPaint')

    def add_object(self, object):
        self.changed = True
        self.objects.append(object)

    # Функция отмены последнего действия
    def add_deleted_object(self):
        if self.objects:
            # Вытащим последний элемент из нарисованных объектов
            # и добавим его в удаленные объекты
            if self.objects[-1] == ']':
                # Если мы встречаем скобочку, то удаляем все объекты
                # до закрывающей скобочки, так мы удалим всю линию
                self.deleted_objects.append(self.objects.pop())
                while True:
                    elem = self.objects.pop()
                    self.deleted_objects.append(elem)
                    if elem == '[':
                        break
            else:
                self.deleted_objects.append(self.objects.pop())
        if not self.objects:
            self.changed = False
        self.update()

    # Функция очистки отменённых действий
    # Вызывается при создании любого объекта
    def clear_deleted_objects(self):
        self.deleted_objects.clear()

    # Функция возврата отменённого действия
    def return_last_deleted_object(self):
        if self.deleted_objects:
            # Вытащим последний элемент из списка удалённых
            # и добавим в нарисованные объекты
            if self.deleted_objects[-1] == '[':
                # Если мы встречаем скобочку, до следующей скобочки
                # возвращаем элементы. Так мы вернём всю линию
                self.add_object(self.deleted_objects.pop())
                while True:
                    elem = self.deleted_objects.pop()
                    self.add_object(elem)
                    if elem == ']':
                        break
            else:
                self.add_object(self.deleted_objects.pop())
        if self.objects:
            self.changed = True
        self.update()

    def change_language(self):
        # Список возможных языков
        m = [RUSSIAN, ENGLISH, ITALIAN, CHINISE, UCRAINE]
        s1, s2 = self.choose_language_text
        s, ok = QInputDialog.getItem(self, s1, s2, m)
        # Диалог с выбором языка
        if ok:
            self.language = s
            canvas_set_language(self, self.language)

    # Вызов окна со справкой
    def call_help(self):
        self.help_window = HelpWindow()
        self.help_window.show()

    # Вызов окна с многоугольниками
    def call_polygons(self):
        self.polygons = PolygonEditorWindow(self.language)
        self.polygons.setWindowTitle(self.btnPolygons.text())
        self.polygons.color = self.color
        self.polygons.show()

    # Вызов окна с L-системами
    def call_l_systems(self):
        self.L_systems = LSystemsEditorWindow(self.language)
        self.L_systems.setWindowTitle(self.btnSystems.text())
        # если имя верно и окно создалось
        if self.L_systems:
            self.L_systems.color = self.color
            self.L_systems.show()

    def change_font(self, font=None):
        if font:
            for i in self.toolBar.actions():
                i.setFont(font)
        else:
            # Диалог выбора шрифта
            font, ok_pressed = QFontDialog.getFont(self)
            if ok_pressed:
                for i in self.toolBar.actions():
                    i.setFont(font)

    # Если по ошибке тулбар куда-то исчез, его можно вернуть
    def return_tool_bar(self):
        self.toolBar.setGeometry(0, 21, self.size().width(), 35)

    # Функция изменения 1 цвета кисти/фигур
    def set_color1(self):
        color = QColorDialog.getColor(self.color)
        if color.isValid():
            self.color = color
            pixmap = QPixmap(17, 17)
            pixmap.fill(self.color)
            self.btnColor1.setIcon(QIcon(pixmap))
            self.btnColor1.setIconText(self.tcolor + ' 1 (' + self.color.name() + ')')

    # Функция изменения 2 цвета кисти/фигур
    def set_color2(self):
        color = QColorDialog.getColor(self.color2)
        if color.isValid():
            self.color2 = color
            pixmap = QPixmap(17, 17)
            pixmap.fill(self.color2)
            self.btnColor2.setIcon(QIcon(pixmap))
            self.btnColor2.setIconText(self.tcolor + ' 2 (' + self.color2.name() + ')')

    # Функция изменения размера кисти/толщины линий
    def set_width(self):
        s1, s2 = self.choose_size_brush_text
        width, ok_pressed = QInputDialog.getInt(self, s1, s2, self.width, 1, 500)
        if width and ok_pressed:
            self.width = width

    # Функции изменения инструмента, которым рисует пользователь
    # Вызывается кнопками изменения инструмента на панели инструментов
    def set_pen(self):
        self.tool = PEN

    def set_brush(self):
        self.tool = BRUSH

    def set_line(self):
        self.tool = LINE

    def set_ellipse(self):
        self.tool = ELLIPSE

    def set_rectangle(self):
        self.tool = RECTANGLE

    def set_triangle(self):
        self.tool = TRIANGLE

    def set_arc(self):
        self.tool = ARC

    def set_heart(self):
        self.tool = HEART


# Класс окна справки, создающегося при вызове справки
# Я сделал его для красоты,
# чтоб было похоже на настоящее приложение
class HelpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.opened = True
        self.setWindowTitle('О приложении "PyPaint"')

        self.layout = QVBoxLayout(self)
        # Для красоты добавим картинку с иконки приложения
        self.image_lable = QLabel()
        try:
            self.image_lable.setPixmap(QPixmap('icon.png'))
        except Exception:
            pass

        self.text_lable = QLabel()
        self.text_lable.setFont(QFont('Consolas', 10, QFont.Light))
        # Вставим текст из файла ReadMe в папке с приложением
        try:
            file = open('ReadMe.txt', 'r')
            data = file.read()
            self.text_lable.setText(data)
        except FileNotFoundError:
            s = 'Здесь должен быть текст из файла ReadMe.txt,\nно файл отсутствует в папке.'
            s += '\nСкачайте, пожалуйста, этот файл там,\nгде вы взяли это приложение.'
            self.text_lable.setText(s)
        self.layout_1 = QHBoxLayout()
        self.layout_1.addWidget(self.image_lable, 0, Qt.AlignRight)
        self.layout.addLayout(self.layout_1)
        self.layout.addWidget(self.text_lable)
        self.layout.setSpacing(10)

        self.setFixedSize(self.minimumSize())

    # Чтобы замаскировать то, что картинка немного меньше текста,
    # Мы сделаем фон идеально белым
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        set_pen_and_brush(qp, QColor(255, 255, 255))
        # set_pen_and_brush(qp, QColor(235, 235, 235))
        qp.drawRect(0, 0, self.size().width(), self.size().height())
        qp.end()

    def closeEvent(self, event):
        self.opened = False


# Небольшое окошко, в котором можно строить многоугольники.
# и экспортировать на главный холст
# Я взял его из классной задачи, немного переделав
class PolygonEditorWindow(QWidget):
    def __init__(self, language):
        super().__init__()
        polygons_set_language(self, language)

        # Структура
        self.objects = []
        self.resize(400, 520)
        self.setMinimumHeight(400)
        self.color = QColor(0, 155, 0)

        self.main_hor = QHBoxLayout(self)
        self.main_hor.setSpacing(20)
        self.vert_1 = QVBoxLayout()
        self.vert_1.setSpacing(5)
        self.btn = QPushButton(self.btn_text, self)
        self.btn.setMinimumSize(50, 25)
        self.btn.setMaximumSize(5000, 30)
        self.btn.clicked.connect(self.export)

        self.hor_1 = QHBoxLayout()
        self.cbtn = QPushButton(self.cbtn_text, self)
        self.cbtn.clicked.connect(self.change_color)

        self.lab = QLabel(self)
        self.lab.setText(self.tcolor + ': ' + str(self.color.name()).upper())
        self.lab.setMaximumSize(5000, 25)
        self.hor_1.addWidget(self.cbtn)
        self.hor_1.addWidget(self.lab)

        self.hor_2 = QHBoxLayout()
        self.lab1 = QLabel(self)
        self.lab1.setText(self.text_size)
        self.lab1.setMaximumSize(5000, 25)

        self.line_size = QSpinBox(self)
        self.line_size.setMinimum(1)
        self.line_size.setMaximum(30)
        self.line_size.valueChanged.connect(self.update)
        self.hor_2.addWidget(self.lab1)
        self.hor_2.addWidget(self.line_size)
        self.vert_1.addWidget(QLabel())
        self.vert_1.addWidget(self.btn)
        self.vert_1.addLayout(self.hor_1)
        self.vert_1.addLayout(self.hor_2)

        self.vert_2 = QVBoxLayout()
        self.vert_2.setSpacing(15)
        self.hor_3 = QHBoxLayout()
        self.angles_number = QSpinBox(self)
        self.angles_number.setValue(4)
        self.angles_number.setMinimum(3)
        self.angles_number.setMaximum(100)
        self.angles_number.valueChanged.connect(self.update)
        self.label1 = QLabel(self)
        self.label1.setText(self.text_number)
        self.hor_3.addWidget(self.label1)
        self.hor_3.addWidget(self.angles_number)

        self.hor_4 = QHBoxLayout()
        self.coefficient = QSpinBox(self)
        self.coefficient.setValue(90)
        self.coefficient.setMinimum(0)
        self.coefficient.setMaximum(100)
        self.coefficient.valueChanged.connect(self.update)
        self.label2 = QLabel(self)
        self.label2.setText(self.text_koef + ", %:")
        self.hor_4.addWidget(self.label2)
        self.hor_4.addWidget(self.coefficient)

        self.hor_5 = QHBoxLayout()
        self.shapes_number = QSpinBox(self)
        self.shapes_number.setValue(1)
        self.shapes_number.setMinimum(0)
        self.shapes_number.setMaximum(2000)
        self.shapes_number.valueChanged.connect(self.update)
        self.label3 = QLabel(self)
        self.label3.setText(self.text_kol + ':')
        self.hor_5.addWidget(self.label3)
        self.hor_5.addWidget(self.shapes_number)
        self.vert_2.addWidget(QLabel())
        self.vert_2.addLayout(self.hor_3)
        self.vert_2.addLayout(self.hor_4)
        self.vert_2.addLayout(self.hor_5)
        self.main_hor.addLayout(self.vert_1)
        self.main_hor.addLayout(self.vert_2)

    # Функция, которая рисует все прямоугольники
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        flag = bool(self.shapes_number.text()) * bool(self.coefficient.text())

        if flag * self.angles_number.text():
            self.objects = self.append_objects()
            for i in self.objects:
                try:
                    i.draw(qp)
                    # Если значение слишком больше окна
                except OverflowError:
                    pass
        qp.end()

    # Функция, которая создаёт многоугольники и складывает в список
    def append_objects(self):
        objects = []
        koef = float(self.coefficient.text()) / 100 % 1
        angels = self.angles_number.value()

        n = int(self.shapes_number.text())
        l1, l2 = self.size().width() // 2, self.size().height() // 2 - 45
        r = int(0.4 * min(self.size().height() - 50, self.size().width()))

        m = []
        angle = 360 / angels
        if angels % 2 == 1:
            a = 0
        else:
            a = angle / 2
        for i in range(angels):
            m.append((l1 - r * sin(rad(a)), l2 - r * cos(rad(a))))
            a += angle

        for i in range(n):
            m1 = []
            for j in range(angels):
                h1, h2 = m[j - 1]
                h3, h4 = m[j]
                if ((h2 - h1) ** 2 + (h4 - h3) ** 2) ** 0.5 > 1:
                    objects.append(Line(h1, h2, h3, h4,
                                        self.line_size.value(), self.color))
            for j in range(angels):
                x1, y1 = m[j - 1]
                x2, y2 = m[j]
                m1.append((x1 + (x2 - x1) * koef, y1 + (y2 - y1) * koef))
            m = m1[:]
        return objects

    # Функция переноса построенной фигуры на холст
    def export(self):
        # Координаты от левого верхнего угла
        dialog = SizeDialog(self, self.coords, self.left,
                            self.right, 50, 50, self.big_text)
        dialog.exec()
        if dialog.accepted:
            global canvas
            width = dialog.width.value()
            height = dialog.height.value() + 20
            canvas.objects.append('[')
            # Добавляет скобки, чтоб экспортированный объект был целым в списке объектов
            for i in self.objects:
                i.x1 += width
                i.y1 += height
                i.x2 += width
                i.y2 += height
                canvas.objects.append(i)
            canvas.objects.append(']')
            canvas.show()
            canvas.update()

    # Смена цвета фигуры
    def change_color(self):
        color = QColorDialog.getColor(self.color)
        if color.isValid():
            self.color = color
            self.lab.setText(self.tcolor + ": " + str(self.color.name()).upper())
            self.update()


# Класс дополнительного окна с L-системами
# Тоже из классной задачи
# Оно также сделано на основе ПаинтИвента
# и мне показалось оно сюда подходит
class LSystemsEditorWindow(QWidget):
    def __init__(self, language):
        super().__init__()
        systems_set_language(self, language)

        self.flag_x_menshe = False
        self.flag_x_bolshe = False
        self.flag_y_menshe = False
        self.flag_y_bolshe = False
        self.flag = False
        self.objects = []
        self.color = QColor(0, 155, 0)

        # Открытие файла
        f = QFileDialog.getOpenFileName(self, self.text_1, '', self.text)
        # Если название неверно
        if not f[0]:
            self.flag = True
            return

        try:
            s = open(f[0], 'r').read().split('\n')

            self.name, self.angles, self.axsioma, *t = s
            # Устанавливаем имя окна на имя системы плюс название Л-система
            self.setWindowTitle(self.windowTitle() + ' - ' + self.name)
            self.angles = float(str(self.angles).replace(',', '.'))
            self.teorems = {}
            for i in t:
                if i:
                    self.teorems[i.split()[0]] = i.split()[1]

            # Структура
            self.resize(400, 500)
            self.vert = QVBoxLayout(self)
            self.vert.addWidget(QLabel(self))
            self.slider = QSlider(Qt.Horizontal, self)
            self.slider.setMaximum(6)
            self.slider.sliderMoved.connect(self.update)
            self.slider.valueChanged.connect(self.update)
            self.slider.sliderReleased.connect(self.update)
            self.slider.sliderPressed.connect(self.update)
            self.slider.setValue(0)
            self.step = 0
            self.slider.resize(360, 20)
            self.tip_label = QLabel(self.tip1)
            self.vert.addWidget(self.tip_label)

            self.hor_1 = QHBoxLayout()
            self.hor_2 = QHBoxLayout()
            self.btn = QPushButton(self.btn1, self)
            self.btn.setMinimumWidth(100)
            self.btn.clicked.connect(self.export)

            self.cbtn = QPushButton(self.btn2, self)
            self.cbtn.clicked.connect(self.change_color)

            self.color_label = QLabel(self)
            self.color_label.setText(self.tcolor + str(self.color.name()).upper())
            self.color_label.setMaximumSize(5000, 25)
            self.color_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)

            self.lab1 = QLabel(self)
            self.lab1.setText(self.lab1_text)
            self.lab1.setMaximumSize(5000, 25)

            self.line_size = QSpinBox(self)
            self.line_size.setMinimum(1)
            self.line_size.setMaximum(30)
            self.line_size.valueChanged.connect(self.update)

            self.lab2 = QLabel(self)
            self.lab2.setText(self.lab2_text)
            self.lab2.setMaximumSize(5000, 25)

            self.line_len = QSpinBox(self)
            self.line_len.setMinimum(1)
            self.line_len.setMaximum(30)
            self.line_len.setValue(10)
            self.line_len.valueChanged.connect(self.update)

            self.hor_1.addWidget(self.btn)
            self.hor_1.addWidget(self.color_label)
            self.hor_1.addWidget(self.cbtn)
            self.hor_2.addWidget(self.lab1)
            self.hor_2.addWidget(self.line_size)
            self.hor_2.addWidget(self.lab2)
            self.hor_2.addWidget(self.line_len)

            self.vert.addLayout(self.hor_1)
            self.vert.addLayout(self.hor_2)
            self.vert.addWidget(self.slider)
            # Если файл неправильный
        except AssertionError:
            error = QErrorMessage(self)
            error.showMessage(self.error_message)
            error.exec()
            self.flag = True

    def paintEvent(self, event):
        if self.flag:
            self.close()
            return

        self.nx, self.ny = self.size().width() // 2, self.size().height() // 2
        if self.flag_x_bolshe * self.flag_x_menshe:
            pass
        elif self.flag_x_menshe:
            self.nx = self.size().width() - 40
        elif self.flag_x_bolshe:
            self.nx = 40

        if self.flag_y_menshe * self.flag_y_bolshe:
            pass
        elif self.flag_y_menshe:
            self.ny = self.size().height() - 80
        elif self.flag_y_bolshe:
            self.ny = 40

        # На случай, если что-то пойдет не так
        saved_axsioma = self.axsioma

        try:
            delta = self.step - self.slider.value()
            if delta:
                self.tip_label.setText('')
            self.axsioma = recount(self.axsioma, delta, self.teorems)
            self.step = self.slider.value()
            self.append_tree(self.axsioma)
        except TimeoutError:
            # Если слишком долго будет строиться аксиома на данном шаге
            self.axsioma = saved_axsioma
            self.slider.setValue(self.step)
            self.tip_label.setText(self.tip2)

        qp = QPainter()
        qp.begin(self)
        for i in self.objects:
            i.draw(qp)
        qp.end()

    # создание дерева и добавление его в список
    def append_tree(self, s):
        self.objects = []
        x, y = self.nx, self.ny
        angle = 0
        m = []

        for i in s:
            if i in 'FGBA':
                x1, y1 = x + self.line_len.value() * cos(rad(angle)), \
                         y + self.line_len.value() * sin(rad(angle))
                line = Line(x, y, x1, y1, self.line_size.value(), self.color.name())
                self.objects.append(line)

                x, y = x + self.line_len.value() * cos(rad(angle)),  \
                       y + self.line_len.value() * sin(rad(angle))
                if x1 < 0:
                    self.flag_x_menshe = True
                elif x1 > self.size().width():
                    self.flag_x_bolshe = True
                if y1 < 0:
                    self.flag_y_menshe = True
                elif y1 > self.size().height():
                    self.flag_y_bolshe = True
            elif i in 'fb':
                x, y = x + self.line_len.value() * cos(rad(angle)), \
                       y + self.line_len.value() * sin(rad(angle))

            elif i in 'J+':
                angle = (angle + self.angles) % 360
            elif i in 'H-−':
                angle = (angle - self.angles + 360) % 360

            elif i == '[':
                m.append((x, y, angle))
            elif i == ']':
                if m:
                    x, y, angle = m.pop()
            elif i == '|':
                angle += 180
                angle %= 360

    # Функция экспорта на главный холст
    def export(self):
        dialog = SizeDialog(self, self.coords, self.left,
                            self.right, 50, 50, self.big_text)
        dialog.exec()
        if dialog.accepted:
            global canvas
            width = dialog.width.value()
            height = dialog.height.value() + 20
            canvas.objects.append('[')
            for i in self.objects:
                i.x1 += width
                i.y1 += height
                i.x2 += width
                i.y2 += height
                canvas.objects.append(i)
            canvas.objects.append(']')
            canvas.show()
            canvas.update()

    # Изменить цвет
    def change_color(self):
        color = QColorDialog.getColor(self.color)
        if color.isValid():
            self.color = color
            self.lab.setText(self.tcolor + str(self.color.name()).upper())
            self.update()


# Я сделал этот класс для получения размера
# изображения при создании нового холста
# Или координат
class SizeDialog(QDialog):
    def __init__(self, parent, title, title_1, title_2, v1, v2, text=''):
        super().__init__(parent)
        self.accepted = False
        self.setWindowTitle(title)
        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout_3 = QHBoxLayout()
        self.label = QLabel(self)

        if text:
            self.text = QLabel(self)
            self.text.setText(text)
            self.verticalLayout.addWidget(self.text)
            self.setFixedSize(300, 150)
        else:
            self.setFixedSize(180, 100)

        self.width = QSpinBox(self)
        self.width.setMinimum(0)
        self.width.setMaximum(3000)
        self.width.setValue(v1)
        self.width.setSingleStep(10)

        self.label_2 = QLabel(self)
        self.horizontalLayout_3.addWidget(self.label)
        self.horizontalLayout_3.addWidget(self.width)
        self.horizontalLayout_3.addWidget(QLabel(self))
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.addWidget(self.label_2)

        self.height = QSpinBox(self)
        self.height.setMinimum(0)
        self.height.setMaximum(2500)
        self.height.setValue(v2)
        self.height.setSingleStep(10)

        self.horizontalLayout_2.addWidget(self.height)
        self.horizontalLayout_2.addWidget(QLabel(self))
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QHBoxLayout()
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label.setText(title_1)
        self.label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.label_2.setText(title_2)
        self.label_2.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.buttonBox.accepted.connect(self.my_accept)
        self.buttonBox.rejected.connect(self.reject)

    def my_accept(self):
        self.accepted = True
        self.accept()


# Создал диалог для получения согласия/несогласия от пользователя
class UserConfirmationDialog(QDialog):
    def __init__(self, parent, title, title_1):
        super().__init__(parent)
        self.accepted = False
        self.resized = False
        self.setWindowTitle(title)
        self.verticalLayout = QVBoxLayout(self)
        self.label = QLabel(self)
        self.label.setText(title_1)
        self.label.setAlignment(Qt.AlignLeft)

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.No)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.my_accept)
        self.buttonBox.rejected.connect(self.reject)

    def paintEvent(self, event):
        if not self.resized:
            self.setFixedSize(self.minimumSize().width() + 10, self.minimumSize().height() + 20)
            self.resized = True

    def my_accept(self):
        self.accepted = True
        self.accept()


# Функция для рисования сердца
def draw_heart(painter, x1, y1, x2, y2, width):
    dx, dy = x2 - x1, y2 - y1
    half = dx // 2
    part_x = dx / 20
    part_y = dy / 20
    # Пришлось помучиться с координатами
    # Оно всё ещё криво, но дальше я не вижу смысла изменять
    if dy > 0:
        if dx > 0:
            painter.drawArc(x1 + half - part_x // 2, y1,
                            half + part_x // 2, dy * 2 // 3, 16 * -45, 16 * 200)
            painter.drawArc(x1, y1, half + part_x // 2,
                            dy * 2 // 3, 16 * 25, 16 * 200)
            painter.drawLine(x1 + part_x * 1.54, y1 + part_y * 11.38,
                             x1 + half, y2)
            painter.drawLine(x1 + part_x * 18.45, y1 + part_y * 11.39,
                             x1 + half, y2)
        else:
            painter.drawArc(x1 + half - part_x // 2, y1,
                            half + part_x // 2, dy * 2 // 3, 16 * 25, 16 * 200)
            painter.drawArc(x1, y1, half + part_x // 2,
                            dy * 2 // 3, 16 * -45, 16 * 200)
            painter.drawLine(x1 + part_x * 1.54, y1 + part_y * 11.38,
                             x1 + half, y1 + dy)
            painter.drawLine(x1 + part_x * 18.45, y1 + part_y * 11.39,
                             x1 + half, y1 + dy)
    else:
        if dx > 0:
            painter.drawArc(x1 + half - part_x // 2, y1,
                            half + part_x // 2, dy * 2 // 3, 16 * 205, 16 * 200)
            painter.drawArc(x1, y1, half + part_x // 2,
                            dy * 2 // 3, 16 * 135, 16 * 200)
            painter.drawLine(x1 + part_x * 1.54, y1 + part_y * 11.38,
                             x1 + half, y1 + dy)
            painter.drawLine(x1 + part_x * 18.45, y1 + part_y * 11.39,
                             x1 + half, y1 + dy)
        else:
            painter.drawArc(x1 + half - part_x // 2, y1,
                            half + part_x // 2, dy * 2 // 3, 16 * 135, 16 * 200)
            painter.drawArc(x1, y1, half + part_x // 2,
                            dy * 2 // 3, 16 * 205, 16 * 200)
            painter.drawLine(x1 + part_x * 1.54, y1 + part_y * 11.38,
                             x1 + half, y1 + dy)
            painter.drawLine(x1 + part_x * 18.45, y1 + part_y * 11.39,
                             x1 + half, y1 + dy)

    # Так как это не цельная фигура, painter не заливает её.
    # Так что мы будем рисовать много таких же сердец,
    # чуть меньших по размеру, пока не достигнем центра

    change = width // 2
    if dx > width:
        if dy > width:
            draw_heart(painter, x1 + change, y1 + change, x2 - change, y2 - change, width)
        elif dy < -width:
            draw_heart(painter, x1 + change, y1 - change, x2 - change, y2 + change, width)
    elif dx < -width:
        if dy > width:
            draw_heart(painter, x1 - change, y1 + change, x2 + change, y2 - change, width)
        elif dy < -width:
            draw_heart(painter, x1 - change, y1 - change, x2 + change, y2 + change, width)


# Расчёт аксиомы по данной аксиоме, изменению шага и теоремам
def recount(axsioma, delta, teorems):
    # delta = self.step - self.slider.value()
    time1 = time()
    if delta < 0:
        for _ in range(-delta):
            n = 0
            while 1:
                if time() - time1 > 5:
                    raise TimeoutError

                j = axsioma[n:n + 1]
                if j in teorems.keys():
                    axsioma = axsioma[:n] + teorems[j] + axsioma[n + 1:]
                    n += len(teorems[j]) - 1
                if n >= len(axsioma) - 1:
                    break
                n += 1

    elif delta > 0:
        for _ in range(delta):
            for j in teorems.keys():
                if teorems[j] in axsioma:
                    axsioma = axsioma.replace(teorems[j], j)
    return axsioma


# Функция для удобства присвоения инструметов painter'у
def set_pen_and_brush(painter, color, width=1):
    painter.setPen(QPen(QColor(color), width))
    painter.setBrush(QBrush(QColor(color)))


# Функция, создающая "линию" из точек кисти, чтобы не нужно было рисовать её прямой
def creat_point_line(objects, x1, y1, x2, y2, color, width):
    if width == 1:
        objects.append(Line(x1, y1, x2, y2, width, color))
    else:
        w = width / 3
        dx, dy = x2 - x1, y2 - y1
        times = ((dx ** 2 + dy ** 2) ** 0.5) / w
        mini_dx = dx / times
        mini_dy = dy / times
        objects.append(BrushPoint(x1, y1, width, color))
        objects.append(Line(x1 + mini_dx, y1 + mini_dy, x2 - mini_dx,
                            y2 - mini_dy, width, color))
        objects.append(BrushPoint(x2, y2, width, color))


# Запуск обработки окна
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Установим иконку приложения на панели задач
    app.setWindowIcon(QIcon('icon.png'))
    canvas = Canvas()

    canvas.show()
    sys.exit(app.exec())
