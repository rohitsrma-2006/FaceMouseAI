import pyautogui


class MouseController:
    def __init__(self):
        self.screen_w, self.screen_h = pyautogui.size()

        pyautogui.PAUSE = 0
        pyautogui.FAILSAFE = True

    def move_relative(self, dx, dy):
        try:
            x, y = pyautogui.position()

            new_x = max(5, min(self.screen_w - 5, x + dx))
            new_y = max(5, min(self.screen_h - 5, y + dy))

            pyautogui.moveTo(new_x, new_y, duration=0)

        except pyautogui.FailSafeException:
            pass