import cv2
import numpy as np
import pyautogui
import time
import datetime

screen_width, screen_height = pyautogui.size()
bottom_right_region = (screen_width // 2, screen_height // 2, screen_width, screen_height)

plus_image_paths = [
    "ImageReferens/plus_icon.png",
    "ImageReferens/plus_icon_google.png"
]
input_image_paths = [
    "ImageReferens/input_message.png",
    "ImageReferens/input_message_google.png"
]

# Загрузка изображений
plus_images = [cv2.imread(path, cv2.IMREAD_GRAYSCALE) for path in plus_image_paths if cv2.imread(path, cv2.IMREAD_GRAYSCALE) is not None]
input_images = [cv2.imread(path, cv2.IMREAD_GRAYSCALE) for path in input_image_paths if cv2.imread(path, cv2.IMREAD_GRAYSCALE) is not None]

if not plus_images or not input_images:
    print("Error: One or more template images could not be loaded. Exiting.")
else:
    found_plus = False
    while not found_plus:
        screenshot = pyautogui.screenshot()
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        img_quarter = img[bottom_right_region[1]:bottom_right_region[3], bottom_right_region[0]:bottom_right_region[2]]
        gray_img = cv2.cvtColor(img_quarter, cv2.COLOR_BGR2GRAY)

        for plus_image in plus_images:
            if gray_img.shape[0] >= plus_image.shape[0] and gray_img.shape[1] >= plus_image.shape[1]:
                res = cv2.matchTemplate(gray_img, plus_image, cv2.TM_CCOEFF_NORMED)
                threshold = 0.8
                loc = np.where(res >= threshold)

                if loc[0].size > 0:
                    print("Символ '+' найден через изображение!")
                    found_plus = True

                    for input_image in input_images:
                        res = cv2.matchTemplate(gray_img, input_image, cv2.TM_CCOEFF_NORMED)
                        threshold = 0.6
                        loc = np.where(res >= threshold)

                        if loc[0].size > 0:
                            top_left = (loc[1][0] + bottom_right_region[0], loc[0][0] + bottom_right_region[1])
                            bottom_right = (top_left[0] + input_image.shape[1], top_left[1] + input_image.shape[0])
                            center_x = top_left[0] + (bottom_right[0] - top_left[0]) // 2
                            center_y = top_left[1] + (bottom_right[1] - top_left[1]) // 2

                            pyautogui.click(center_x, center_y)
                            time.sleep(0.5)
                            pyautogui.write("+")
                            pyautogui.press("enter")
                            print("Сообщение отправлено: +")
                            break
                        else:
                            print("Область ввода не найдена с использованием текущего шаблона.")
                if found_plus:
                    break

        cv2.imshow("Extracted Quarter", img_quarter)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.5)

    if found_plus:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        cv2.imwrite(filename, img)
        print(f"Сохранен финальный скриншот с меткой: {filename}")

    cv2.destroyAllWindows()
    print("Программа завершена.")
