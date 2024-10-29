import cv2
import numpy as np
import pyautogui
import time
import datetime

screen_width, screen_height = pyautogui.size()
bottom_right_region = (screen_width // 2, screen_height // 2, screen_width, screen_height)

found_plus = False
plus_image_path = "ImageReferens\\plus_icon.png"

plus_image = cv2.imread(plus_image_path, cv2.IMREAD_GRAYSCALE)

while not found_plus:
    screenshot = pyautogui.screenshot()
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    if img.size == 0:
        print("Screenshot is empty!")
        time.sleep(1)
        continue

    img_quarter = img[bottom_right_region[1]:bottom_right_region[3], bottom_right_region[0]:bottom_right_region[2]]
    gray_img = cv2.cvtColor(img_quarter, cv2.COLOR_BGR2GRAY)
    _, thresh_img = cv2.threshold(gray_img, 150, 255, cv2.THRESH_BINARY)
    cv2.imshow("Extracted Quarter", img_quarter)

    # Remove the Tesseract text detection part
    # text = pytesseract.image_to_string(thresh_img)

    # Search for the '+' icon in the captured quarter
    res = cv2.matchTemplate(gray_img, plus_image, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)

    if loc[0].size > 0:
        print("Символ '+' найден через изображение!")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        cv2.imwrite(filename, img)
        print(f"Сохранен скриншот: {filename}")
        found_plus = True

    if found_plus:
        input_image_path = "ImageReferens/input_message.png"
        input_coords = pyautogui.locateOnScreen(input_image_path, confidence=0.8)

        if input_coords is not None:
            center_x = input_coords.left + input_coords.width // 2
            center_y = input_coords.top + input_coords.height // 2
            pyautogui.click(center_x, center_y)
            time.sleep(0.5)
            pyautogui.write("+")
            pyautogui.press("enter")
            print("Сообщение отправлено: +")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.5)

cv2.destroyAllWindows()
print("Программа завершена.")
