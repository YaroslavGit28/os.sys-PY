import os
import sys
import time
from pathlib import Path

# Текущая директория (синхронизируем и с os.getcwd/os.chdir)
CURRENT_DIR = Path(os.getcwd())


def pause() -> None:
    input("Нажмите Enter, чтобы продолжить...")


def _safe_name_only(name: str) -> bool:
    """Учебная проверка: ожидаем имя, а не путь."""
    if not name:
        return False
    if any(sep in name for sep in ("/", "\\")):
        return False
    if name.startswith(".."):
        return False
    return True


def _sync_cwd_from_os() -> None:
    """Синхронизирует CURRENT_DIR из os.getcwd()."""
    global CURRENT_DIR
    CURRENT_DIR = Path(os.getcwd())


def _sync_os_from_current_dir() -> None:
    """Синхронизирует os.getcwd() через os.chdir(CURRENT_DIR)."""
    os.chdir(CURRENT_DIR)


def clear_screen() -> None:
    """Очищает экран через os.system (учебное использование)."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def print_header() -> None:
    """Печатает шапку с текущей директорией."""
    print("=" * 50)
    print("УЧЕБНЫЙ ФАЙЛОВЫЙ МЕНЕДЖЕР (много функций os)")
    print("=" * 50)
    print(f"Текущая директория (CURRENT_DIR): {CURRENT_DIR}")
    print(f"Текущая директория (os.getcwd):  {os.getcwd()}")
    print("-" * 50)


def list_dir() -> None:
    """Показывает содержимое через os.listdir (учебно)."""
    print("\nСодержимое директории (os.listdir):")
    try:
        for name in os.listdir(CURRENT_DIR):
            full = os.path.join(CURRENT_DIR, name)
            mark = "[DIR]" if os.path.isdir(full) else "     "
            print(f"{mark} {name}")
    except OSError as e:
        print(f"Ошибка чтения директории: {e}")
    print()

def list_dir_scandir() -> None:
    """Показывает содержимое через os.scandir (быстро и структурно)."""
    print("\nСодержимое директории (os.scandir):")
    try:
        with os.scandir(CURRENT_DIR) as it:
            for entry in it:
                mark = "[DIR]" if entry.is_dir(follow_symlinks=False) else "     "
                print(f"{mark} {entry.name}")
    except OSError as e:
        print(f"Ошибка scandir: {e}")
    print()


def show_file_info() -> None:
    """Показывает информацию о файле/папке через os.path и os.stat."""
    name = input("Введите имя файла/папки: ").strip()
    if not _safe_name_only(name):
        print("Введите только имя (без пути и ..).\n")
        return

    target = os.path.join(CURRENT_DIR, name)
    if not os.path.exists(target):
        print("Такого файла/папки нет.\n")
        return

    print("\nИнформация (os.path / os.stat):")
    print(f"- Путь:           {target}")
    print(f"- Абсолютный:     {os.path.abspath(target)}")
    print(f"- Это файл:       {os.path.isfile(target)}")
    print(f"- Это папка:      {os.path.isdir(target)}")
    print(f"- Размер (байт):  {os.path.getsize(target) if os.path.isfile(target) else '—'}")
    print(f"- Время измен.:   {time.ctime(os.path.getmtime(target))}")
    print(f"- Время доступа:  {time.ctime(os.path.getatime(target))}")

    st = os.stat(target)
    print("\nos.stat:")
    print(f"- st_size:        {st.st_size}")
    print(f"- st_mode:        {st.st_mode}")
    print(f"- st_mtime:       {time.ctime(st.st_mtime)}")
    print(f"- st_atime:       {time.ctime(st.st_atime)}")
    print()


def make_empty_file() -> None:
    """Создаёт пустой файл через os.open/os.close (низкоуровнево) или os.utime."""
    name = input("Введите имя файла для создания (например, note.txt): ").strip()
    if not _safe_name_only(name):
        print("Введите только имя файла (без пути и ..).\n")
        return

    target = os.path.join(CURRENT_DIR, name)
    try:
        fd = os.open(target, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.close(fd)
        print(f"Файл создан: {name}\n")
    except FileExistsError:
        print("Файл уже существует.\n")
    except OSError as e:
        print(f"Ошибка создания файла: {e}\n")


def touch_file() -> None:
    """Обновляет время файла через os.utime (аналог touch)."""
    name = input("Введите имя файла для touch: ").strip()
    if not _safe_name_only(name):
        print("Введите только имя файла (без пути и ..).\n")
        return

    target = os.path.join(CURRENT_DIR, name)
    if not os.path.exists(target):
        print("Файла нет. Сначала создайте его.\n")
        return

    try:
        os.utime(target, None)
        print("Время файла обновлено (os.utime).\n")
    except OSError as e:
        print(f"Ошибка os.utime: {e}\n")


def change_dir() -> None:
    """Меняет директорию и через CURRENT_DIR, и через os.chdir."""
    global CURRENT_DIR

    new_dir = input("Введите папку (.. чтобы выйти назад): ").strip()
    if not new_dir:
        print("Путь не введён.\n")
        return

    if new_dir == "..":
        CURRENT_DIR = CURRENT_DIR.parent.resolve()
        try:
            _sync_os_from_current_dir()
        except OSError as e:
            print(f"Не удалось os.chdir: {e}\n")
            _sync_cwd_from_os()
            return
        print(f"Текущая директория: {CURRENT_DIR}\n")
        return
    if new_dir == ".":
        print("Остаёмся в текущей директории.\n")
        return

    new_path = Path(new_dir)
    if not new_path.is_absolute():
        new_path = CURRENT_DIR / new_dir

    if new_path.is_dir():
        CURRENT_DIR = new_path.resolve()
        try:
            _sync_os_from_current_dir()
        except OSError as e:
            print(f"Не удалось os.chdir: {e}\n")
            _sync_cwd_from_os()
            return
        print(f"Текущая директория: {CURRENT_DIR}\n")
    else:
        print("Директория не найдена.\n")


def make_dir() -> None:
    """Создаёт папку через os.mkdir."""
    name = input("Введите имя папки для создания: ").strip()
    if not _safe_name_only(name):
        print("Введите только имя папки (без пути и ..).\n")
        return

    target = os.path.join(CURRENT_DIR, name)
    try:
        os.mkdir(target)
        print(f"Папка создана: {name}\n")
    except FileExistsError:
        print("Такая папка уже существует.\n")
    except OSError as e:
        print(f"Ошибка при создании папки: {e}\n")

def make_dirs() -> None:
    """Создаёт вложенные папки через os.makedirs."""
    path_str = input("Введите относительный путь папок (например, a\\b\\c): ").strip()
    if not path_str:
        print("Путь не может быть пустым.\n")
        return
    if path_str.startswith(".."):
        print("Не используйте .. в учебном режиме.\n")
        return
    target = os.path.join(CURRENT_DIR, path_str)
    try:
        os.makedirs(target, exist_ok=False)
        print("Вложенные папки созданы (os.makedirs).\n")
    except FileExistsError:
        print("Такая папка/структура уже существует.\n")
    except OSError as e:
        print(f"Ошибка os.makedirs: {e}\n")


def remove_item() -> None:
    """Удаляет файл или пустую папку внутри CURRENT_DIR."""
    name = input("Введите имя файла/папки для удаления: ").strip()
    if not _safe_name_only(name):
        print("Введите только имя (без пути и ..).\n")
        return

    target = os.path.join(CURRENT_DIR, name)
    if not os.path.exists(target):
        print("Такого файла/папки нет.\n")
        return

    try:
        if os.path.isdir(target):
            os.rmdir(target)
            print(f"Папка удалена: {name}\n")
        else:
            os.remove(target)
            print(f"Файл удалён: {name}\n")
    except OSError as e:
        print(f"Не удалось удалить: {e}\n")

def rename_item() -> None:
    """Переименовывает файл/папку через os.rename."""
    old = input("Старое имя: ").strip()
    new = input("Новое имя: ").strip()
    if not _safe_name_only(old) or not _safe_name_only(new):
        print("Используйте только имена без пути и ..\n")
        return
    src = os.path.join(CURRENT_DIR, old)
    dst = os.path.join(CURRENT_DIR, new)
    if not os.path.exists(src):
        print("Исходного файла/папки нет.\n")
        return
    try:
        os.rename(src, dst)
        print("Переименование выполнено (os.rename).\n")
    except OSError as e:
        print(f"Ошибка os.rename: {e}\n")


def replace_item() -> None:
    """
    Замена через os.replace: если dst существует, будет заменён.
    Удобно показать отличие от rename (в учебном смысле поведения).
    """
    src_name = input("Имя источника: ").strip()
    dst_name = input("Имя назначения (будет заменено, если есть): ").strip()
    if not _safe_name_only(src_name) or not _safe_name_only(dst_name):
        print("Используйте только имена без пути и ..\n")
        return
    src = os.path.join(CURRENT_DIR, src_name)
    dst = os.path.join(CURRENT_DIR, dst_name)
    if not os.path.exists(src):
        print("Источника нет.\n")
        return
    try:
        os.replace(src, dst)
        print("Замена выполнена (os.replace).\n")
    except OSError as e:
        print(f"Ошибка os.replace: {e}\n")


def show_env_demo() -> None:
    """Показывает работу с окружением: os.environ, os.getenv."""
    print("\nОкружение (os.environ / os.getenv):")
    print(f"- USERNAME: {os.getenv('USERNAME')}")
    print(f"- USERPROFILE: {os.getenv('USERPROFILE')}")
    print(f"- PATH (первые 200 символов): {str(os.getenv('PATH'))[:200]}...")
    print("\nДобавим переменную окружения внутри процесса:")
    os.environ["FILE_MANAGER_DEMO"] = "1"
    print(f"- FILE_MANAGER_DEMO через getenv: {os.getenv('FILE_MANAGER_DEMO')}")
    print()


def show_system_info() -> None:
    """Показывает системные сведения через os.*."""
    print("\nСистемная информация (os.*):")
    print(f"- os.name:        {os.name}")
    print(f"- sys.platform:   {sys.platform}")
    print(f"- os.getpid():    {os.getpid()}")
    print(f"- os.cpu_count(): {os.cpu_count()}")
    try:
        print(f"- os.getlogin():  {os.getlogin()}")
    except OSError:
        print("- os.getlogin():  недоступно в этой среде")
    print()


def check_access() -> None:
    """Проверка доступа через os.access."""
    name = input("Введите имя файла/папки для проверки доступа: ").strip()
    if not _safe_name_only(name):
        print("Введите только имя (без пути и ..).\n")
        return
    target = os.path.join(CURRENT_DIR, name)
    if not os.path.exists(target):
        print("Такого файла/папки нет.\n")
        return
    print("\nДоступ (os.access):")
    print(f"- READ:    {os.access(target, os.R_OK)}")
    print(f"- WRITE:   {os.access(target, os.W_OK)}")
    print(f"- EXECUTE: {os.access(target, os.X_OK)}")
    print()


def open_explorer() -> None:
    """
    Открывает текущую директорию в файловом менеджере через os.system.

    Windows: explorer
    macOS: open
    Linux: xdg-open
    """
    if os.name == "nt":
        cmd = f'explorer "{CURRENT_DIR}"'
    elif sys.platform == "darwin":
        cmd = f'open "{CURRENT_DIR}"'
    else:
        cmd = f'xdg-open "{CURRENT_DIR}"'

    print(f"Выполняю: {cmd}")
    os.system(cmd)
    print()


def open_shell_here() -> None:
    """
    Открывает новый терминал в CURRENT_DIR через os.system.

    На Windows: новый PowerShell с нужной папкой.
    На других ОС: просто печатает подсказку.
    """
    if os.name != "nt":
        print("Эта функция для Windows (PowerShell). Используйте Windows-терминал вручную.\n")
        return

    # start "" нужен, чтобы заголовок окна не съедал первый аргумент
    path = str(CURRENT_DIR)
    cmd = f'start "" powershell -NoExit -Command "Set-Location -LiteralPath \'{path}\'"'

    print(f"Выполняю: {cmd}")
    os.system(cmd)
    print()


def show_menu() -> None:
    """Печатает меню команд."""
    print("Выберите действие:")
    print("1. Список (os.listdir)")
    print("2. Список (os.scandir)")
    print("3. Сменить директорию (os.chdir + os.getcwd)")
    print("4. Создать папку (os.mkdir)")
    print("5. Создать вложенные папки (os.makedirs)")
    print("6. Создать пустой файл (os.open/os.close)")
    print("7. Удалить файл/пустую папку (os.remove/os.rmdir)")
    print("8. Переименовать (os.rename)")
    print("9. Заменить/перезаписать (os.replace)")
    print("10. Информация о файле (os.path + os.stat)")
    print("11. Touch файла (os.utime)")
    print("12. Проверка доступа (os.access)")
    print("13. Показать env (os.environ/os.getenv)")
    print("14. Системная инфо (os.getpid/os.cpu_count/...)")
    print("15. Открыть директорию в проводнике (os.system)")
    print("16. Открыть PowerShell тут (os.system)")
    print("0. Выход")
    print()


def main() -> None:
    _sync_os_from_current_dir()
    while True:
        clear_screen()
        print_header()
        show_menu()

        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            list_dir()
            pause()
        elif choice == "2":
            list_dir_scandir()
            pause()
        elif choice == "3":
            change_dir()
            pause()
        elif choice == "4":
            make_dir()
            pause()
        elif choice == "5":
            make_dirs()
            pause()
        elif choice == "6":
            make_empty_file()
            pause()
        elif choice == "7":
            list_dir_scandir()
            remove_item()
            pause()
        elif choice == "8":
            rename_item()
            pause()
        elif choice == "9":
            replace_item()
            pause()
        elif choice == "10":
            list_dir_scandir()
            show_file_info()
            pause()
        elif choice == "11":
            touch_file()
            pause()
        elif choice == "12":
            check_access()
            pause()
        elif choice == "13":
            show_env_demo()
            pause()
        elif choice == "14":
            show_system_info()
            pause()
        elif choice == "15":
            open_explorer()
            pause()
        elif choice == "16":
            open_shell_here()
            pause()
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте ещё раз.\n")
            pause()


if __name__ == "__main__":
    # Для Windows-консолей помогает отображение UTF-8 (учебная мелочь)
    if os.name == "nt":
        os.system("chcp 65001 > nul")
    main()

