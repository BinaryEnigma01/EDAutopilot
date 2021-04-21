# direct inputs
# source to this solution and code:
# http://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
# http://www.gamespp.com/directx/directInputKeyboardScanCodes.html

import keyboard

EDKeyCodes = {
    'Key_0': 0x0B,  # KEY_0
    'Key_1': 0x02,  # KEY_1
    'Key_2': 0x03,  # KEY_2
    'Key_3': 0x04,  # KEY_3
    'Key_4': 0x05,  # KEY_4
    'Key_5': 0x06,  # KEY_5
    'Key_6': 0x07,  # KEY_6
    'Key_7': 0x08,  # KEY_7
    'Key_8': 0x09,  # KEY_8
    'Key_9': 0x0A,  # KEY_9
    'Key_A': 0x1E,  # KEY_A
    'Key_B': 0x30,  # KEY_B
    'Key_C': 0x2E,  # KEY_C
    'Key_D': 0x20,  # KEY_D
    'Key_E': 0x12,  # KEY_E
    'Key_F': 0x21,  # KEY_F
    'Key_G': 0x22,  # KEY_G
    'Key_H': 0x23,  # KEY_H
    'Key_I': 0x17,  # KEY_I
    'Key_J': 0x24,  # KEY_J
    'Key_K': 0x25,  # KEY_K
    'Key_L': 0x26,  # KEY_L
    'Key_M': 0x32,  # KEY_M
    'Key_N': 0x31,  # KEY_N
    'Key_O': 0x18,  # KEY_O
    'Key_P': 0x19,  # KEY_P
    'Key_Q': 0x10,  # KEY_Q
    'Key_R': 0x13,  # KEY_R
    'Key_S': 0x1F,  # KEY_S
    'Key_T': 0x14,  # KEY_T
    'Key_U': 0x16,  # KEY_U
    'Key_V': 0x2F,  # KEY_V
    'Key_W': 0x11,  # KEY_W
    'Key_X': 0x2D,  # KEY_X
    'Key_Y': 0x15,  # KEY_Y
    'Key_Z': 0x2C,  # KEY_Z
    'Key_Numpad_0': 0x52,  # KEY_NUMPAD_0
    'Key_Numpad_1': 0x4F,  # KEY_NUMPAD_1
    'Key_Numpad_2': 0x50,  # KEY_NUMPAD_2
    'Key_Numpad_3': 0x51,  # KEY_NUMPAD_3
    'Key_Numpad_4': 0x4B,  # KEY_NUMPAD_4
    'Key_Numpad_5': 0x4C,  # KEY_NUMPAD_5
    'Key_Numpad_6': 0x4D,  # KEY_NUMPAD_6
    'Key_Numpad_7': 0x47,  # KEY_NUMPAD_7
    'Key_Numpad_8': 0x48,  # KEY_NUMPAD_8
    'Key_Numpad_9': 0x49,  # KEY_NUMPAD_9
    'Key_Numpad_Add': 0x4E,  # KEY_NUMPAD_PLUS
    'Key_Numpad_Decimal': 0x53,  # KEY_NUMPAD_DECIMAL
    'Key_Numpad_Divide': 0xB5 + 1024,  # KEY_NUMPAD_DIVIDE
    'Key_Numpad_Enter': 0x9C + 1024,  # KEY_NUMPAD_ENTER
    'Key_Numpad_Multiply': 0x37,  # KEY_NUMPAD_MULTIPLY
    'Key_Numpad_Subtract': 0x4A,  # KEY_NUMPAD_SUBTRACT
    'Key_LeftAlt': 0x38,  # KEY_LEFT_ALT
    'Key_LeftControl': 0x1D,  # KEY_LEFT_CTRL
    'Key_LeftShift': 0x2A,  # KEY_LEFT_SHIFT
    'Key_RightAlt': 0xB8 + 1024,  # KEY_RIGHT_ALT
    'Key_RightControl': 0x9D + 1024,  # KEY_RIGHT_CTRL
    'Key_RightShift': 0x36,  # KEY_RIGHT_SHIFT
    'Key_º': 0x28,  # Key with º and ª on PT keyboard
    'Key_Apostrophe': 0x28,  # KEY_APOSTROPHE
    'Key_Hash': 0x2B,  # /shrug
    'Key_BackSlash': 0x2B,  # KEY_BACKSLASH
    'Key_Comma': 0x33,  # KEY_COMMA
    'Key_Enter': 0x1C,  # KEY_ENTER
    'Key_«': 0x0D,  # Key with « and » on PT keyboard
    'Key_Equals': 0x0D,  # KEY_EQUALS
    'Key_Grave': 0x29,  # KEY_BACKTICK
    'Key_Plus': 0x1A,  # Key with + and * on PT keyboard
    'Key_LeftBracket': 0x1A,  # KEY_LEFT_BRACKET
    'Key_Minus': 0x0C,  # KEY_DASH
    'Key_Period': 0x34,  # KEY_PERIOD
    'Key_RightBracket': 0x1B,  # KEY_RIGHT_BRACKET
    'Key_ç': 0x27,  # Key with ç on PT keyboard
    'Key_SemiColon': 0x27,  # KEY_SEMICOLON
    'Key_Slash': 0x35,  # KEY_SLASH
    'Key_Space': 0x39,  # KEY_SPACE
    'Key_Tab': 0x0F,  # KEY_TAB
    'Key_F1': 0x3B,  # KEY_F1
    'Key_F2': 0x3C,  # KEY_F2
    'Key_F3': 0x3D,  # KEY_F3
    'Key_F4': 0x3E,  # KEY_F4
    'Key_F5': 0x3F,  # KEY_F5
    'Key_F6': 0x40,  # KEY_F6
    'Key_F7': 0x41,  # KEY_F7
    'Key_F8': 0x42,  # KEY_F8
    'Key_F9': 0x43,  # KEY_F9
    'Key_F10': 0x44,  # KEY_F10
    'Key_F11': 0x57,  # KEY_F11
    'Key_F12': 0x58,  # KEY_F12
    'Key_Backspace': 0x0E,  # KEY_BACKSPACE
    'Key_Delete': 0xD3 + 1024,  # KEY_DELETE
    'Key_DownArrow': 0xD0 + 1024,  # KEY_DOWN
    'Key_End': 0xCF + 1024,  # KEY_END
    'Key_Home': 0xC7 + 1024,  # KEY_HOME
    'Key_Insert': 0xD2 + 1024,  # KEY_INSERT
    'Key_LeftArrow': 0xCB + 1024,  # KEY_LEFT
    'Key_PageDown': 0xC9 + 1024,  # KEY_PAGE_UP
    'Key_PageUp': 0xD1 + 1024,  # KEY_PAGE_DOWN
    'Key_RightArrow': 0xCD + 1024,  # KEY_RIGHT
    'Key_UpArrow': 0xC8 + 1024  # KEY_UP
}


# Key_Plus
# Actual Functions


def PressKey(hexKeyCode):
    keyboard.press(keyboard.parse_hotkey(hexKeyCode))


def ReleaseKey(hexKeyCode):
    keyboard.release(keyboard.parse_hotkey(hexKeyCode))
