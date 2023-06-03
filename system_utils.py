import ctypes
import msvcrt
import os


def clear_terminal() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def press_any_key_to_continue() -> None:
    print("Press any key to continue...")
    msvcrt.getch()


def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
