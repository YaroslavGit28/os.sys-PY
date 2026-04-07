Использованные источники
При разработке и документировании проекта «Консольный файловый менеджер на os и os.system» использовались следующие источники. 
Официальная документация Python

Модули os и os.path: Использовались для понимания базовых функций, таких как os.getcwd(), os.listdir(), os.mkdir(), os.rmdir(), os.remove(), и особенно os.system(). Несмотря на то, что в итоговом коде был выбран pathlib, понимание os было критически важно.

Ссылка: https://docs.python.org/3/library/os.html

Модуль pathlib: Стал основой для работы с путями. Изучался раздел «Basic use», особенно методы Path.cwd(), Path.iterdir(), Path.exists(), Path.is_dir(), Path.rmdir() и оператор /.

Ссылка: https://docs.python.org/3/library/pathlib.html

Модуль sys: Нужен был только для одного — доступа к sys.platform, чтобы определять операционную систему. Информация бралась из раздела «System-specific parameters and functions».

Ссылка: https://docs.python.org/3/library/sys.html

Статьи и туториалы (Stack Overflow, Habr, Real Python)

Определение ОС в Python: Главный вопрос, который я искал: «как правильно и надёжно определить Windows, Linux и macOS». На Stack Overflow нашёл несколько вариантов, и sys.platform оказался самым простым и распространённым. Там же увидел, что для macOS значение 'darwin' — это legacy, но до сих пор работает.

Пример обсуждения: https://stackoverflow.com/questions/1854/how-to-identify-on-which-os-python-is-running

Команды для открытия файлового менеджера из терминала: Узнал, что на Linux нет единой команды. xdg-open — это стандарт де-факто для открытия файлов и папок программой по умолчанию. Про open . на macOS тоже узнал из статей.

Ссылка: https://ru.wikipedia.org/wiki/Xdg-open

Почему rmdir не удаляет непустые папки: Это было неожиданностью, когда программа начала выдавать ошибку. Пришлось читать про разницу между os.rmdir() и shutil.rmtree(). Понял, что rmdir — это более безопасный инструмент, и для учебного примера это даже плюс.

Ссылка: https://realpython.com/python-pathlib/ (отличный гайд по pathlib)


