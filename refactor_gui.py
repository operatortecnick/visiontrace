import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path


def refactor_python_files_to_task(directory: str) -> None:
    base_dir = Path(directory)
    py_files = list(base_dir.rglob("*.py"))

    for py_file in py_files:
        if py_file.name.endswith(".task.py"):
            continue
        try:
            content = py_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"\u26a0 Pulando arquivo com erro de codifica\u00e7\u00e3o: {py_file}")
            continue

        if "__name__" in content:
            lines = content.splitlines()
            new_lines = []
            inside_main = False
            for line in lines:
                if "__name__" in line:
                    inside_main = True
                    new_lines.append("import asyncio\n\n\nasync def main():")
                elif inside_main:
                    if line.strip() and not line.strip().startswith("#"):
                        new_lines.append("    " + line)
                else:
                    new_lines.append(line)
            new_lines.append("\n\nif __name__ == '__main__':\n    asyncio.run(main())")
            content = "\n".join(new_lines)

        new_file = py_file.with_name(py_file.stem + ".task.py")
        new_file.write_text(content, encoding="utf-8")
        print(f"[\u2713] {py_file.name} \u2192 {new_file.name}")


def run_refactor() -> None:
    directory = filedialog.askdirectory()
    if not directory:
        return
    refactor_python_files_to_task(directory)
    messagebox.showinfo("Conclu\u00eddo", "Refatora\u00e7\u00e3o finalizada!")


def main() -> None:
    root = tk.Tk()
    root.title("Refatorador de Python")
    root.geometry("400x200")
    root.resizable(False, False)

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(expand=True, fill="both")

    label = tk.Label(
        frame, text="Selecione a pasta base para refatora\u00e7\u00e3o", font=("Arial", 12)
    )
    label.pack(pady=(0, 10))

    button = tk.Button(
        frame,
        text="Escolher Pasta",
        command=run_refactor,
        width=20,
        height=2,
        bg="#4CAF50",
        fg="white",
    )
    button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
