import argparse
import sys
import tkinter as tk
from vfs import VFS
from shell import Shell
from gui import ConsoleGUI


def main():
    parser = argparse.ArgumentParser(description="UNIX-like OS Shell Emulator (Variant 2)")
    parser.add_argument("--vfs", type=str, help="Путь к JSON файлу VFS", default=None)
    parser.add_argument("--script", type=str, help="Путь к стартовому скрипту", default=None)

    args = parser.parse_args()

    vfs = VFS()
    if args.vfs:
        try:
            vfs.load_from_json(args.vfs)
        except Exception as e:
            print(f"Критическая ошибка загрузки VFS: {e}")
            sys.exit(1)
    else:
        vfs.mkdir("/home")
        vfs.mkdir("/home/user")

    root = tk.Tk()
    shell = Shell(vfs_instance=vfs, output_callback=print)
    app = ConsoleGUI(root, shell)

    if args.script:
        app.print_to_console(f"Автозапуск: {args.script}\n", "yellow")
        shell.run_script(args.script)
        app.update_prompt()

    root.mainloop()


if __name__ == "__main__":
    main()