import cv2

# Открытие видеофайла
cap = cv2.VideoCapture('test2.mp4')

# Проверка успешного открытия видеофайла
if not cap.isOpened():
    print("Ошибка открытия видеофайла")
    exit()

# Получение первого кадра
ret, frame = cap.read()

# Проверка успешного получения кадра
if not ret:
    print("Не удалось получить первый кадр")
    exit()

# Сохранение первого кадра в файл
cv2.imwrite('cadr.png', frame)

# Освобождение ресурсов
cap.release()
