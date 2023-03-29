import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
from tkinter import messagebox as mb
import cv2
import pafy

# Подключить каскад для поиска черты
def connectCascade(cascadeName):
    mouth_cascade = cv2.CascadeClassifier(cascadeName)

    # Если каскад не был найден
    if mouth_cascade.empty():
        raise IOError('Unable to load the cascade classifier xml file')
    return mouth_cascade

# Распознать черту
def findFeature(feature_cascade, frame):
    # Перевод изображения в ч/б формат
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Распознание черты
    feature_rects = feature_cascade.detectMultiScale(gray, 1.7, 11)

    # Отрисовать рамку
    drawFrame(frame, feature_rects)

    # Показать кадр
    cv2.imshow('Feature Detector', frame)

# Отрисовать рамку
def drawFrame(frame, feature_rects):
    # Для каждой черты
    for (x, y, w, h) in feature_rects:
        # Задать рамку
        y = int(y - 0.15 * h)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Закрыть окно при нажатии Esc
def closeWindow():
        c = cv2.waitKey(1)
        if c == 27:
            return True


# Распознание черты на фото
def findFeatureOnPhoto(filename, xml_name):
    try:
        # Подключить каскад для поиска черты
        feature_cascade = connectCascade(f"XMLs//{xml_name}.xml")

        img = cv2.imread(filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Распознание черты
        feature_rects = feature_cascade.detectMultiScale(gray, 1.7, 11)

        # Отрисовать рамку
        drawFrame(img, feature_rects)

        while True:
            # Показать изображение
            cv2.imshow('Feature Detector', img)

            # Закрытие окна при нажатии Esc
            if (closeWindow()): break


        cv2.destroyAllWindows()
        window.focus()
    except cv2.error:
        errorMsg = mb.showerror(
            title="Сообщение об ошибке",
            message="Некорректное название файла. Возможно, не на латинице.")

# Распознание черты на видео
def findFeatureOnVideoFile(filename, xml_name):
    # Подключить каскад для поиска черты
    feature_cascade = connectCascade(f"XMLs//{xml_name}.xml")

    cap = cv2.VideoCapture(filename)
    # Пока видео открыто
    while cap.isOpened():
        ret, frame = cap.read()
        findFeature(feature_cascade, frame)

        # Закрытие окна при нажатии Esc
        if(closeWindow()): break

    cap.release()
    cv2.destroyAllWindows()

# Распознание черты на видео с вебкамеры
def findFeatureOnVebcam(xml_name):
    # Подключить каскад для поиска черты
    feature_cascade = connectCascade(f"XMLs//{xml_name}.xml")

    # Подключение камеры
    cap = cv2.VideoCapture(0)

    # Цикл для постоянного считывания с камеры
    while True:
        ret, frame = cap.read()
        findFeature(feature_cascade, frame)

        # Закрытие окна при нажатии Esc
        if(closeWindow()): break

    cap.release()
    cv2.destroyAllWindows()
    window.focus()

# Распознание черты на видео по ссылке
def findFeatureOnVideoLink(url, xml_name):
    try:
        urlPafy = pafy.new(url)
        videoplay = urlPafy.getbest()

        if(urlPafy == 0):
            print("Ошибка")

        # Подключить каскад для поиска черты
        feature_cascade = connectCascade(f"XMLs//{xml_name}.xml")

        cap = cv2.VideoCapture(videoplay.url)
        # Пока видео открыто
        while cap.isOpened():
            ret, frame = cap.read()
            findFeature(feature_cascade, frame)

            # Закрытие окна при нажатии Esc
            if(closeWindow()): break

        cap.release()
        cv2.destroyAllWindows()
    except ValueError:
        errorMsg = mb.showerror(
            title="Сообщение об ошибке",
            message="Некорректное URL видео")
        videoLink.delete(0, 'end')


# Получить режим обработки
def getRes():
    if(cb.get() == "Фото"):
        filetypes = (("Изображение", "*.jpg *.gif *.png"), ("Любой", "*"))
        filename = fd.askopenfilename(title="Открыть файл", initialdir="/",
                                      filetypes=filetypes)
        findFeatureOnPhoto(filename, fc.get())
    elif(cb.get() == "Видеофайл"):
        filetypes = (("Видеофайл", "*.avi *.mp4"), ("Любой", "*"))
        filename = fd.askopenfilename(title="Открыть файл", initialdir="/",
                                      filetypes=filetypes)
        findFeatureOnVideoFile(filename, fc.get())
    elif(cb.get() == "Видео с вебкамеры"):
        findFeatureOnVebcam(fc.get())
    elif (cb.get() == "Видео по ссылке"):
        link = videoLink.get()
        findFeatureOnVideoLink(link, fc.get())

def checkValue(event):
    if (cb.get() == "Фото"):
        linkLabel.pack_forget()
        videoLink.pack_forget()
    elif (cb.get() == "Видеофайл"):
        linkLabel.pack_forget()
        videoLink.pack_forget()
    elif (cb.get() == "Видео с вебкамеры"):
        linkLabel.pack_forget()
        videoLink.pack_forget()
    elif (cb.get() == "Видео по ссылке"):
        linkLabel.pack(anchor=tk.N, side='top', pady=10)
        videoLink.pack(anchor=tk.N, side='top', pady=10)


# Создание окна
window = tk.Tk()
window.title('Feature Detector')              # Задать заголовок окна
window.geometry('640x480')                  # Задать размер окна
window.wm_resizable(False, False)           # Задать запрет на изменение размера окна
window.iconbitmap("feature.ico")          # Задать иконку окна
window.configure(background='#a8e05e')      # Задать фон окна

# LABEL
label = ttk.Label(window, text="Выберите формат входных данных:", background='#a8e05e', font="Arial",
                  width=30)
label.pack(anchor=tk.N, side='top', pady=10)

# LABEL ССЫЛКИ
linkLabel = ttk.Label(window, text="Вставьте ссылку:", background='#a8e05e', font="Arial",
                  width=27)

# ПОЛЕ ССЫЛКИ
myFont = ("Courier", 13)
videoLink = tk.Entry(width=27, font=myFont)

# COMBOBOX
cb = ttk.Combobox(window, values=["Фото", "Видеофайл", "Видео с вебкамеры", "Видео по ссылке"],
                  state="readonly", font=myFont, width=25)
cb.current(2)
cb.pack(anchor=tk.N, side='top', pady=10)
cb.bind("<<ComboboxSelected>>", checkValue)

# FEATURE CHOSE
fc = ttk.Combobox(window, values=['clock', 'eye', 'eye_tree_eyeglasses', 'frontalface', 'frontalface_alt', 'frontalface_alt_tree', 'frontalface_alt2', 'frontalface_default', 'fullbody', 'lefteye_2splits', 'lowerbody', 'mcs_eyepair_big', 'mcs_eyepair_small', 'mcs_leftear', 'mcs_lefteye', 'mcs_mouth', 'mcs_nose', 'msc_rightear', 'mcs_righteye', 'mcs_upperbody', 'pedestrians', 'profileface', 'righteye_2splits', 'upperbody'],
                  state="readonly", font=myFont, width=25)
fc.current(1)
fc.pack(anchor=tk.N, side='top', pady=10)
fc.bind("<<ComboboxSelected>>", checkValue)

# BUTTON
btn = ttk.Button(window, text="Выбрать", command=getRes, width=44)
btn.pack(anchor=tk.N, side='top', pady=10)

window.mainloop()