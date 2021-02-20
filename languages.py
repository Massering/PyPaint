RUSSIAN = 'Русский'
ENGLISH = 'English'
ITALIAN = 'Italiano'
CHINISE = '中文'
UCRAINE = 'Український'


def canvas_set_language(self, language):
    if language == RUSSIAN:
        self.tcolor = ' Цвет'
        self.file.setTitle('Файл')
        self.edit.setTitle('Правка')
        self.tools.setTitle('Инструменты')
        self.jokes.setTitle('Прикольчики')
        self.help.setTitle('Справка')
        self.btnPen.setText('Карандаш')
        self.btnToolPen.setToolTip('Инструмент: Произвольная линия с толщиной 1 пиксель')
        self.btnBrush.setText('Кисть')
        self.btnToolBrush.setToolTip('Инструмент: Произвольная линия')
        self.btnLine.setText('Прямая')
        self.btnToolLine.setToolTip('Инструмент: Прямая линия')
        self.btnEllipse.setText('Овал')
        self.btnToolEllipse.setToolTip('Инструмент: Овал (круг)')
        self.btnRectangle.setText('Прямоугольник')
        self.btnToolRectangle.setToolTip('Инструмент: Прямоугольник (квадрат)')
        self.btnTriangle.setText('Треугольник')
        self.btnToolTriangle.setToolTip('Инструмент: Треугольник')
        self.btnArc.setText('Дуга')
        self.btnToolArc.setToolTip('Инструмент: Дуга выбранной толщины')
        self.btnHeart.setText('Сердце')
        self.btnToolHeart.setToolTip('Инструмент: Сердце с заливкой')
        self.btnWidtn.setText('Толщина')
        self.btnToolWidtn.setToolTip('Изменить толщину кисти и линий')
        self.btnColor1.setIconText(' Цвет 1 (' + self.color.name() + ')')
        self.btnColor2.setIconText(' Цвет 2 (' + self.color2.name() + ')')
        self.btnToolPen.setText(self.btnPen.text())
        self.btnToolBrush.setText(self.btnBrush.text())
        self.btnToolLine.setText(self.btnLine.text())
        self.btnToolEllipse.setText(self.btnEllipse.text())
        self.btnToolRectangle.setText(self.btnRectangle.text())
        self.btnToolTriangle.setText(self.btnTriangle.text())
        self.btnToolArc.setText(self.btnArc.text())
        self.btnToolHeart.setText(self.btnHeart.text())
        self.btnToolWidtn.setText(self.btnWidtn.text())
        self.btnPolygons.setText('Многоугольники')
        self.btnSystems.setText('L-система')
        self.btnCancel.setText('Отменить')
        self.btnReturn.setText('Вернуть')
        self.btnLanguage.setText('Сменить язык')
        self.btnChangeFont.setText('Поменять шрифт тулбара')
        self.btnReturnToolBar.setText('Вернуть панель инструментов')
        self.btnChange_canvas_size.setText('Изменить размер листа')
        self.btnNew.setText('Создать')
        self.btnOpen.setText('Открыть')
        self.btnSave.setText('Сохранить')
        self.btnExport.setText('Экспорт')
        self.btnExit.setText('Выход')
        self.btnHelp.setText('О приложении')
        self.tsave = 'Сохранить изображение'
        self.bigtsave = 'Рисунки PyPaint (*.pi.txt);;Текстовые файлы (*.txt);;Все файлы (*)'
        self.tsizes = 'Размер холста', 'Ширина', 'Высота'
        self.text_error = 'Содержимое файла задано неверно'
        self.want_save_text = 'Хотите сохранить файл перед закрытием?'
        self.text_open = 'Открыть рисунок'
        self.choose_size_brush_text = 'Ширина кисти', 'Выберите ширину кисти'
        self.choose_language_text = 'Выбрать язык', 'Выберите язык из списка'

    elif language == ENGLISH:
        self.tcolor = ' Color'
        self.file.setTitle('File')
        self.edit.setTitle('Edit')
        self.tools.setTitle('Tools')
        self.jokes.setTitle('Jokes')
        self.help.setTitle('Help')
        self.btnPen.setText('Pencil')
        self.btnToolPen.setToolTip('Tool: Custom line with size 1')
        self.btnBrush.setText('Brush')
        self.btnToolBrush.setToolTip('Tool: Custom line')
        self.btnLine.setText('Line')
        self.btnToolLine.setToolTip('Tool: Straight line')
        self.btnEllipse.setText('Ellipse')
        self.btnToolEllipse.setToolTip('Tool: Ellipse (circle)')
        self.btnRectangle.setText('Rectangle')
        self.btnToolRectangle.setToolTip('Tool: Rectangle (square)')
        self.btnTriangle.setText('Triangle')
        self.btnToolTriangle.setToolTip('Tool: Triangle')
        self.btnArc.setText('Arc')
        self.btnToolArc.setToolTip('Tool: Arc with selected size')
        self.btnHeart.setText('Heart')
        self.btnToolHeart.setToolTip('Tool: heart with fill')
        self.btnWidtn.setText('Size')
        self.btnToolWidtn.setToolTip('Change the size of brush and lines')
        self.btnColor1.setIconText(' Color 1 (' + self.color.name() + ')')
        self.btnColor2.setIconText(' Color 2 (' + self.color2.name() + ')')
        self.btnToolPen.setText(self.btnPen.text())
        self.btnToolBrush.setText(self.btnBrush.text())
        self.btnToolLine.setText(self.btnLine.text())
        self.btnToolEllipse.setText(self.btnEllipse.text())
        self.btnToolRectangle.setText(self.btnRectangle.text())
        self.btnToolTriangle.setText(self.btnTriangle.text())
        self.btnToolArc.setText(self.btnArc.text())
        self.btnToolHeart.setText(self.btnHeart.text())
        self.btnToolWidtn.setText(self.btnWidtn.text())
        self.btnPolygons.setText('Polygons')
        self.btnSystems.setText('L-system')
        self.btnCancel.setText('Undo')
        self.btnReturn.setText('Redo')
        self.btnLanguage.setText('Change language')
        self.btnChangeFont.setText("Change toolbar's font")
        self.btnReturnToolBar.setText('Return toolbar')
        self.btnChange_canvas_size.setText('Change canvas size')
        self.btnNew.setText('New')
        self.btnOpen.setText('Open')
        self.btnSave.setText('Save')
        self.btnExport.setText('Export')
        self.btnExit.setText('Exit')
        self.btnHelp.setText('About the program')
        self.tsave = 'Save image'
        self.bigtsave = 'PyPaint Drawings (*.pi.txt);; Text ' \
                        'files (*.txt);; All files (*)'
        self.tsizes = 'Canvas Size', 'Width', 'Height'
        self.text_error = 'The contents of the file are not set correctly'
        self.want_save_text = 'Do you want to save the file before closing?'
        self.text_open = 'Open a drawing'
        self.choose_size_brush_text = 'Brush width', 'Select the brush width'
        self.choose_language_text = 'Select a language', 'Select a language from the list'

    elif language == ITALIAN:
        self.tcolor = ' Colore'
        self.file.setTitle('File')
        self.edit.setTitle('Raddrizzatura')
        self.tools.setTitle('Strumenti')
        self.jokes.setTitle('Scherzi')
        self.help.setTitle('Informazione')
        self.btnPen.setText('Matita')
        self.btnToolPen.setToolTip('Strumento: linea arbitraria '
                                   'con uno spessore di 1 pixel')
        self.btnBrush.setText('Pennello')
        self.btnToolBrush.setToolTip('Strumento: linea arbitraria')
        self.btnLine.setText('Retta')
        self.btnToolLine.setToolTip('Strumento: Linea Retta')
        self.btnEllipse.setText('Ovale')
        self.btnToolEllipse.setToolTip('Strumento: ovale (cerchio)')
        self.btnRectangle.setText('Rettangolo')
        self.btnToolRectangle.setToolTip('Strumento: Rettangolo (quadrato)')
        self.btnTriangle.setText('Triangolo')
        self.btnToolTriangle.setToolTip('Strumento: Triangolo')
        self.btnArc.setText('Arco')
        self.btnToolArc.setToolTip('Strumento: Arco di spessore selezionato')
        self.btnHeart.setText('Cuore')
        self.btnToolHeart.setToolTip('Strumento: cuore con riempimento')
        self.btnWidtn.setText('Spessore')
        self.btnToolWidtn.setToolTip('Modificare lo spessore del pennello e delle linee')
        self.btnColor1.setIconText(' Colore uno (' + self.color.name() + ')')
        self.btnColor2.setIconText(' Colore due (' + self.color2.name() + ')')
        self.btnToolPen.setText(self.btnPen.text())
        self.btnToolBrush.setText(self.btnBrush.text())
        self.btnToolLine.setText(self.btnLine.text())
        self.btnToolEllipse.setText(self.btnEllipse.text())
        self.btnToolRectangle.setText(self.btnRectangle.text())
        self.btnToolTriangle.setText(self.btnTriangle.text())
        self.btnToolArc.setText(self.btnArc.text())
        self.btnToolHeart.setText(self.btnHeart.text())
        self.btnToolWidtn.setText(self.btnWidtn.text())
        self.btnPolygons.setText('Poligoni')
        self.btnSystems.setText('L-sistema')
        self.btnCancel.setText('Annullare')
        self.btnReturn.setText('Restituire')
        self.btnLanguage.setText('Cambia lingua')
        self.btnChangeFont.setText('Cambia il carattere della barra degli strumenti')
        self.btnReturnToolBar.setText('Ripristina barra degli strumenti')
        self.btnChange_canvas_size.setText('Ridimensionare il foglio')
        self.btnNew.setText('Creare')
        self.btnOpen.setText('Aprire')
        self.btnSave.setText('Mantenere')
        self.btnExport.setText('Esportazione')
        self.btnExit.setText('Uscita')
        self.btnHelp.setText("Circa l'applicazione")
        self.tsave = 'Salva immagine'
        self.bigtsave = 'Disegni PyPaint (*.pi.txt);;File ' \
                        'di testo (*.txt);; Tutti i file (*)'
        self.tsizes = 'Dimensione Tela', 'Larghezza', 'Altezza'
        self.text_error = 'Il contenuto del file non è specificato correttamente'
        self.want_save_text = 'Vuoi salvare il file prima di chiuderlo?'
        self.text_open = 'Aprire il disegno'
        self.choose_size_brush_text = 'Larghezza pennello', 'Seleziona larghezza pennello'
        self.choose_language_text = 'Seleziona lingua', "Selezionare una lingua dall'elenco"

    elif language == CHINISE:
        self.tcolor = ' 颜色'
        self.file.setTitle('文件')
        self.edit.setTitle('更正')
        self.tools.setTitle('工具')
        self.jokes.setTitle('有趣的事情')
        self.help.setTitle('参考')
        self.btnPen.setText('铅笔')
        self.btnToolPen.setToolTip('工具：厚度为1像素的自定义线')
        self.btnBrush.setText('刷')
        self.btnToolBrush.setToolTip('工具：自定义线')
        self.btnLine.setText('直')
        self.btnToolLine.setToolTip('工具：直线')
        self.btnEllipse.setText('椭圆形')
        self.btnToolEllipse.setToolTip('工具：椭圆形（圆形)')
        self.btnRectangle.setText('矩形')
        self.btnToolRectangle.setToolTip('工具：矩形（正方形)')
        self.btnTriangle.setText('三角形')
        self.btnToolTriangle.setToolTip('工具：三角形')
        self.btnArc.setText('拱形')
        self.btnToolArc.setToolTip('工具：选定厚度的弧')
        self.btnHeart.setText('心')
        self.btnToolHeart.setToolTip('工具：心与填充')
        self.btnWidtn.setText('厚度')
        self.btnToolWidtn.setToolTip('改变画笔和线条的厚度')
        self.btnColor1.setIconText(' 颜色一 (' + self.color.name() + ')')
        self.btnColor2.setIconText(' 颜色二 (' + self.color2.name() + ')')
        self.btnToolPen.setText(self.btnPen.text())
        self.btnToolBrush.setText(self.btnBrush.text())
        self.btnToolLine.setText(self.btnLine.text())
        self.btnToolEllipse.setText(self.btnEllipse.text())
        self.btnToolRectangle.setText(self.btnRectangle.text())
        self.btnToolTriangle.setText(self.btnTriangle.text())
        self.btnToolArc.setText(self.btnArc.text())
        self.btnToolHeart.setText(self.btnHeart.text())
        self.btnToolWidtn.setText(self.btnWidtn.text())
        self.btnPolygons.setText('多边形')
        self.btnSystems.setText('L-系统')
        self.btnCancel.setText('禄谩卤拢潞')
        self.btnReturn.setText('返回')
        self.btnLanguage.setText('更改语言')
        self.btnChangeFont.setText('更改工具栏的字体')
        self.btnReturnToolBar.setText('返回工具栏')
        self.btnChange_canvas_size.setText('更改工作表大小')
        self.btnNew.setText('创建')
        self.btnOpen.setText('打开')
        self.btnSave.setText('保存')
        self.btnExport.setText('导出')
        self.btnExit.setText('退出')
        self.btnHelp.setText('关于应用程序')
        self.tsave = "保存图像"
        self.bigtsave = 'PyPaint 图纸（*.pi.txt);;文本文件(*.txt);;所有文件(*)'
        self.tsizes = '画布大小', '宽度', '高度'
        self.text_error = '文件的内容设置不正确'
        self.want_save_text = '你想在关闭文件之前保存文件吗？'
        self.text_open = '打开绘图'
        self.choose_size_brush_text = "画笔宽度", "选择画笔宽度"
        self.choose_language_text = '选择语言', '从列表中选择一种语言'

    else:
        self.tcolor = ' Колір'
        self.file.setTitle('Файл')
        self.edit.setTitle('Правка')
        self.tools.setTitle('Інструмент')
        self.jokes.setTitle('Прикіл')
        self.help.setTitle('Довідка')
        self.btnPen.setText('Олівець')
        self.btnToolPen.setToolTip('Інструмент: довільна лінія з товщиною 1 піксель')
        self.btnBrush.setText('Кисть')
        self.btnToolBrush.setToolTip('Інструмент: довільна лінія')
        self.btnLine.setText('Пряма')
        self.btnToolLine.setToolTip('Інструмент: Пряма лінія')
        self.btnEllipse.setText('Овал')
        self.btnToolEllipse.setToolTip('Інструмент: Овал (коло)')
        self.btnRectangle.setText('Прямокутник')
        self.btnToolRectangle.setToolTip('Інструмент: прямокутник (квадрат)')
        self.btnTriangle.setText('Трикутник')
        self.btnToolTriangle.setToolTip('Інструмент: Трикутник')
        self.btnArc.setText('Дуга')
        self.btnToolArc.setToolTip('Інструмент: дуга обраної товщини')
        self.btnHeart.setText('Серце')
        self.btnToolHeart.setToolTip('Інструмент: серце з заливкою')
        self.btnWidtn.setText('Товщина')
        self.btnToolWidtn.setToolTip('Змінити товщину кисті і ліній')
        self.btnColor1.setIconText(' Колір 1 (' + self.color.name() + ')')
        self.btnColor2.setIconText(' Колір 2 (' + self.color2.name() + ')')
        self.btnToolPen.setText(self.btnPen.text())
        self.btnToolBrush.setText(self.btnBrush.text())
        self.btnToolLine.setText(self.btnLine.text())
        self.btnToolEllipse.setText(self.btnEllipse.text())
        self.btnToolRectangle.setText(self.btnRectangle.text())
        self.btnToolTriangle.setText(self.btnTriangle.text())
        self.btnToolArc.setText(self.btnArc.text())
        self.btnToolHeart.setText(self.btnHeart.text())
        self.btnToolWidtn.setText(self.btnWidtn.text())
        self.btnPolygons.setText('Багатокутник')
        self.btnSystems.setText('L-система')
        self.btnCancel.setText('Відмінивши')
        self.btnReturn.setText('Повернувши')
        self.btnLanguage.setText('Змінити мову')
        self.btnChangeFont.setText('Змінити шрифт панелі інструментів')
        self.btnReturnToolBar.setText('Повернути панель інструментів')
        self.btnChange_canvas_size.setText('Змінити розмір аркуша')
        self.btnNew.setText('Утворити')
        self.btnOpen.setText('Відкривши')
        self.btnSave.setText('Зберігши')
        self.btnExport.setText('Експорт')
        self.btnExit.setText('Вихід')
        self.btnHelp.setText('Про програму')
        self.tsave = 'Зберегти зображення'
        self.bigtsave = 'Малюнки PyPaint(*.pi.txt) ;;Текстові файли(*.txt);;Всі файли(*)'
        self.tsizes = 'Розмір полотна', 'Ширина', 'Висота'
        self.text_error = 'Вміст файлу задано невірно'
        self.want_save_text = 'Хочете зберегти файл перед закриттям?'
        self.text_open = 'Відкрити малюнок'
        self.choose_size_brush_text = 'Ширина кисті', 'Виберіть ширину кисті'
        self.choose_language_text = 'Вибрати мову', 'Виберіть мову зі списку'


def polygons_set_language(self, language):
    if language == RUSSIAN:
        self.btn_text = 'Перенести на главный холст'
        self.cbtn_text = 'Сменить\n цвет'
        self.tcolor = 'Цвет'
        self.text_size = 'Толщина линий:'
        self.text_number = 'Количество углов:'
        self.text_koef = 'Коэффицент'
        self.text_kol = 'Количество'
        self.big_text = 'Будьте аккуратны, расстояние ' \
                        'отсчитывается\nс левого верхнего '
        self.big_text += 'угла главного холста,\nдо левого верхнего угла окна систем.'
        self.coords, self.left, self.right = 'Координаты', 'Слева: ', 'Справа:'
    elif language == ENGLISH:
        self.btn_text = 'Move to the main canvas'
        self.cbtn_text = 'Change\n color'
        self.tcolor = 'Color'
        self.text_size = 'Line width:'
        self.text_number = 'Number of corners:'
        self.text_koef = 'Coefficient'
        self.text_kol = 'Number'
        self.big_text = 'Be careful, the distance is counted\nfrom the top left '
        self.big_text += 'corner of the main canvas,\n to the ' \
                         'upper-left corner of the systems window.'
        self.coords, self.left, self.right = 'Coordinates', ' Left: ', ' Right: '
    elif language == UCRAINE:
        self.btn_text = 'Перенести на головний полотно'
        self.cbtn_text = 'Змінити \n колір'
        self.tcolor = 'Колір'
        self.text_size = 'Товщина ліній:'
        self.text_number = 'Кількість кутів:'
        self.text_koef = 'Коефіцієнт'
        self.text_kol = 'Кількість'
        self.big_text = 'Будьте обережні, відстань відраховується\nс лівого верхнього'
        self.big_text += 'кута головного полотна,\nдо ' \
                         'лівого верхнього кута вікна систем.'
        self.coords, self.left, self.right = 'Координати', 'Зліва: ', 'Справа:'
    elif language == ITALIAN:
        self.btn_text = 'Sposta sulla tela principale'
        self.cbtn_text = 'Cambia \n Colore'
        self.tcolor = 'Colore'
        self.text_size = 'Spessore delle linee:'
        self.text_number = 'Numero di angoli:'
        self.text_koef = 'Coefficiente'
        self.text_kol = 'Numero'
        self.big_text = "Tenga cuidado, la distancia se cuenta desde la esquina\n"
        self.big_text += " superior izquierda del lienzo principal, hasta la\n"
        self.big_text += " esquina superior izquierda de la ventana de sistemas."
        self.coords, self.left, self.right = 'Coordinate', ' Sinistra: ', 'Destra: '
    else:
        self.btn_text = '移动到主画布'
        self.cbtn_text = '更改\n颜色'
        self.tcolor = '颜色'
        self.text_size = '线宽:'
        self.text_number = '角数:'
        self.text_koef = '系数'
        self.text_kol = '数量'
        self.big_text = '要小心，距离计算从左上角'
        self.big_text += '主画布的角落，直到系统窗口的左上角。'
        self.coords, self.left, self.right = '坐标', '左: ', '右: '


def systems_set_language(self, language):
    if language == RUSSIAN:
        self.error_message = 'Содержимое файла задано неверно'
        self.big_text = 'Будьте аккуратны, расстояние отсчитывается\nс левого верхнего '
        self.big_text += 'угла главного холста,\nдо левого верхнего угла окна систем.'
        self.coords, self.left, self.right = 'Координаты', 'Слева: ', 'Справа:'
        self.tcolor = 'Цвет: '
        self.text = 'Файл с L-системой (*.ls);;Текстовый файл (*.txt);;Все файлы (*)'
        self.text_1 = 'Выбрать файл со строками: название системы, угол, аксиома и теоремы'
        self.tip1 = 'Аккуратнее со слайдером'
        self.btn1 = 'Переместить на\nглавный холст'
        self.btn2 = 'Сменить\n цвет'
        self.lab1_text = 'Толщина линий:'
        self.lab2_text = 'Длина линий:'
        self.tip2 = 'Я же говорил.'
    elif language == ENGLISH:
        self.error_message = 'The contents of the file is incorrectly'
        self.big_text = 'Be careful, the distance is counted\nfrom the top left '
        self.big_text += 'corner of the main canvas,\n to ' \
                         'the upper-left corner of the systems window.'
        self.coords, self.left, self.right = 'Coordinates', ' Left: ', ' Right: '
        self.tcolor = 'Color: '
        self.text = 'L-system file (*.ls);;Text file (*.txt);;All files (*)'
        self.text_1 = 'Select a file with the following lines: ' \
                 'system name, angle, axiom, and theorems'
        self.tip1 = 'Be careful with the slider'
        self.btn1 = 'Move to\nmain canvas'
        self.btn2 = 'To change\ncolor'
        self.lab1_text = 'Line width:'
        self.lab2_text = 'Line length:'
        self.tip2 = 'I told you.'
    elif language == ITALIAN:
        self.error_message = 'Il contenuto del file non è specificato correttamente'
        self.big_text = "Tenga cuidado, la distancia se cuenta desde la esquina\n"
        self.big_text += " superior izquierda del lienzo principal, hasta la\n"
        self.big_text += " esquina superior izquierda de la ventana de sistemas."
        self.coords, self.left, self.right = 'Coordinate', ' Sinistra: ', 'Destra: '
        self.tcolor = 'Colore: '
        self.text = 'File con L-sistema (*.ls);;file di testo (*.txt);; tutti i file (*)'
        self.text_1 = 'Seleziona file con stringhe: nome ' \
                 'del sistema, angolo, assioma e teoremi'
        self.tip1 = 'Fai attenzione con il cursore'
        self.btn1 = 'Sposta su\ntela principale'
        self.btn2 = 'Cambia\nColore'
        self.lab1_text = 'Spessore delle linee:'
        self.lab2_text = 'Lunghezza delle linee:'
        self.tip2 = "Te l'avevo detto."
    elif language == UCRAINE:
        self.error_message = 'Вміст файлу задано невірно'
        self.big_text = 'Будьте обережні, відстань відраховується\nс лівого верхнього'
        self.big_text += 'кута головного полотна,\nдо ' \
                         'лівого верхнього кута вікна систем.'
        self.coords, self.left, self.right = 'Координати', 'Зліва: ', 'Справа:'
        self.tcolor = 'Колір: '
        self.text = 'Файл з L-системою (*.ls);;Текстовий файл ( * .txt);; Всі файли (*)'
        self.text_1 = 'Вибрати файл з рядками: назва системи, кут, аксіома і теореми'
        self.tip1 = 'Акуратніше зі слайдером'
        self.btn1 = 'Перемістити на \n головний полотно'
        self.btn2 = 'Змінити \n колір'
        self.lab1_text = 'Товщина ліній:'
        self.lab2_text = 'Довжина ліній:'
        self.tip2 = 'Я ж говорив'
    else:
        self.error_message = '文件的内容设置不正确'
        self.big_text = '要小心，距离计算从左上角'
        self.big_text += '主画布的角落，直到系统窗口的左上角。'
        self.coords, self.left, self.right = '坐标', '左: ', '右: '
        self.tcolor = '颜色: '
        self.text = 'L-系统文件 (*.ls);;文本文件 (*.txt);;所有文件 (*)'
        self.text_1 = '选择具有以下行的文件：系统名称、角度、公理和定理'
        self.tip1 = '小心滑块'
        self.btn1 = '移动到主画布'
        self.btn2 = '要更改颜色'
        self.lab1_text = '线宽:'
        self.lab2_text = '线长:'
        self.tip2 = '我告诉过你'
