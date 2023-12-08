from HR_logic import *


def main():
    application = QApplication([])
    window = MainLogic()
    window.show()
    application.exec()


if __name__ == '__main__':
    main()
