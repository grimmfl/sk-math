from pynput import keyboard
from string import digits, ascii_letters, punctuation
import os

KEYCODES = [keyboard.KeyCode(char=c) for c in digits + ascii_letters + punctuation]


class Editor:
    def __init__(self):
        self.text = ""
        self.line = 1
        self.cursor_position = (0, 0)
        self.print()
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

    def on_press(self, key: keyboard.KeyCode):
        if key in KEYCODES:
            self.text += key.char
            self.cursor_position += (0, 1)
        if key == keyboard.Key.enter:
            self.text += "\n"
        self.print()

    def print(self):
        os.system("cls")
        lines = self.text.split("\n")
        for i in range(len(lines)):
            print(f"{i + 1}   ", end="")
            line = lines[i]
            for j in range(len(line)):
                if self.cursor_position == (i, j):
                    print("|", end="")
                print(line[i], end="")
