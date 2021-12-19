import os
import time
from string import digits, ascii_letters, punctuation
from typing import Tuple

from sshkeyboard import listen_keyboard, stop_listening

keys = digits + ascii_letters + punctuation


class Editor:
    def __init__(self):
        self.text = ""
        self.line = 1
        self.cursor_position = (0, 0)
        self._print()
        listen_keyboard(on_press=self._on_press, on_release=None, delay_second_char=0.05, lower=False)

    def _get_line_length(self, line: int) -> int:
        lines = self.text.split("\n")
        return len(lines[line])

    def _get_end(self) -> Tuple[int, int]:
        lines = self.text.split("\n")
        return len(lines) - 1, self._get_line_length(len(lines) - 1) - 1

    def _move_cursor(self, direction: str):
        if direction == "left" and self.cursor_position != (0, 0):
            if self.cursor_position[1] == 0:
                newline = self.cursor_position[0] - 1
                self.cursor_position = (newline, self._get_line_length(newline))
            else:
                self.cursor_position = (self.cursor_position[0], self.cursor_position[1] - 1)
        end = self._get_end()
        end = (end[0], end[1] + 1)
        if direction == "right" and self.cursor_position != end:
            if self.cursor_position[1] == self._get_line_length(self.cursor_position[0]):
                self.cursor_position = (self.cursor_position[0] + 1, 0)
            else:
                self.cursor_position = (self.cursor_position[0], self.cursor_position[1] + 1)
        if direction == "up" and self.cursor_position[0] > 0:
            newline = self.cursor_position[0] - 1
            newline_length = self._get_line_length(newline)
            if newline_length < self.cursor_position[1]:
                self.cursor_position = (self.cursor_position[0] - 1, newline_length)
            else:
                self.cursor_position = (self.cursor_position[0] - 1, self.cursor_position[1])
        if direction == "down" and self.cursor_position[0] < self._get_end()[0]:
            newline = self.cursor_position[0] + 1
            newline_length = self._get_line_length(newline)
            if newline_length < self.cursor_position[1]:
                self.cursor_position = (self.cursor_position[0] + 1, newline_length)
            else:
                self.cursor_position = (self.cursor_position[0] + 1, self.cursor_position[1])

    def _insert(self, key: str):
        index = 0
        for i in range(0, self.cursor_position[0]):
            index += self._get_line_length(i) + 1  # + 1 because of \n
        index += self.cursor_position[1]
        self.text = self.text[:index] + key + self.text[index:]

    def _remove(self):
        index = 0
        for i in range(0, self.cursor_position[0]):
            index += self._get_line_length(i) + 1  # + 1 because of \n
        index += self.cursor_position[1]
        self.text = self.text[:index - 1] + self.text[index:]

    def _on_press(self, key):
        switch = {
            "space": " "
        }
        if key == "enter":
            self._insert("\n")
            self._move_cursor("right")
        elif key == "backspace":
            self._remove()
            self._move_cursor("left")
        elif key == "left" or key == "right" or key == "up" or key == "down":
            self._move_cursor(key)
        elif key == "f10":
            stop_listening()
            time.sleep(0.1)
        elif key == "tab":
            for i in range(0, 3):
                self._insert(" ")
                self._move_cursor("right")
        elif key in keys or key in switch.keys():
            self._insert(switch[key] if key in switch.keys() else key)
            self._move_cursor("right")
        self._print()

    def _print(self):
        os.system("cls")
        print("F10      Compile code written in editor")
        print("")
        lines = self.text.split("\n")
        for i in range(len(lines)):
            print(f"{i + 1}   ", end="")
            line = lines[i]
            for j in range(len(line)):
                if self.cursor_position == (i, j):
                    print("|", end="")
                print(line[j], end="")
            if self.cursor_position == (i, len(line)):
                print("|", end="")
            print("")


if __name__ == "__main__":
    e = Editor()
