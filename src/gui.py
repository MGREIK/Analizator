from tkinter import Tk, font, filedialog, messagebox
from tkinter.ttk import Label, Button, Frame, Style
from PIL import ImageTk, Image
from .core import find_pixel_ranges, boloto_percentage
import os


class App:
    def __init__(self, master: Tk) -> None:
        self.master = master

        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family="Inter", size=12, weight=font.NORMAL)
        style = Style()
        style.configure("TButton", font=("Inter", 12))
        style.configure("MainFrame.TFrame", background="white")
        style.configure("ButtonFrame.TFrame", background="#ececec")
        style.configure("ImageFrame.TFrame", background="#131313")

        self.image = None
        self.image_path = ""

        self.create_containers()

    def create_containers(self) -> None:
        main_container = Frame(self.master, padding=[0])
        main_container.configure(style="MainFrame.TFrame")
        buttons_container = Frame(main_container, padding=[12], border=0)
        buttons_container.configure(style="ButtonFrame.TFrame")
        image_container = Frame(main_container, padding=[24], border=0)
        image_container.configure(style="ImageFrame.TFrame")

        main_container.pack(anchor="nw", side="top",
                            expand=True, fill="both")
        buttons_container.pack(
            anchor="nw", expand=True, side="top", fill="x")
        image_container.pack(
            anchor="nw", expand=True, fill="both", side="top"
        )

        self.add_buttons(buttons_container)
        self.add_image(image_container)

    def add_buttons(self, container: Frame) -> None:
        file_choose_button = Button(
            container, text="Выбрать файл", command=self.choose_file)
        calculate_boloto = Button(
            container, text="Посчитать заболоченость", command=self.calculate_boloto)

        file_choose_button.pack(side="left", padx=(0, 24))
        calculate_boloto.pack(side="left")

        label = Label(container, text="Заболоченность: 0.0%")
        label.pack(side="left", padx=24)
        self.label = label

    def change_image(self) -> None:
        if self.image_path == "" or not self.image_path.endswith((".jpg", ".png")):
            return None
        lake_image = self.open_image()
        [image_width, image_height] = lake_image.size
        # 976 663
        [max_image_height, max_image_widht] = (976, 663)
        new_height = image_height
        new_width = image_width
        if image_height > max_image_height:
            new_height = max_image_height
            new_width = int((image_width / image_height) * new_height)
        if image_width > max_image_widht:
            new_width = max_image_widht
            new_height = int((image_height / image_width) * new_width)
        lake_image = lake_image.resize((new_width, new_height), Image.LANCZOS)
        test = ImageTk.PhotoImage(lake_image)
        self.image_label.configure(image=test)
        self.image_label.image = test

    def add_image(self, container: Frame) -> None:
        image_label = Label(container)
        image_label.pack(expand=False, side="top")
        self.image_label = image_label
        self.change_image()

    def open_image(self) -> None:
        self.image = Image.open(self.image_path)
        return self.image

    def choose_file(self) -> None:
        initial_dir = "./images"
        file_path = filedialog.askopenfilename(initialdir=initial_dir)
        if not file_path:
            return None
        _, ext = os.path.splitext(file_path)
        if ext.lower() not in [".png"]:
            messagebox.showerror("Ошибка",
                                 "Выбранный файл не поддерживается. Поддерживаемый формат: PNG.")
            return None
        self.image_path = file_path
        self.change_image()
        self.label.configure(text=f"Заболоченность: -")

    def calculate_boloto(self) -> None:
        ranges = find_pixel_ranges(self.image_path)
        print(len(ranges))
        percent = boloto_percentage(ranges)
        print(percent)
        self.label.configure(text=f"Заболоченность: {percent:.2%}")

    def add_color_ranges(self, parent, input_colors, reversed=False) -> None:
        if reversed:
            input_colors.reverse()
        for [i, [range, color]] in enumerate(input_colors):
            start = f"{range[0]:.3f}"
            end = f"{range[1]:.3f}"
            range_label = Label(
                parent, text=f"{start}...{end}")
            color_label = Label(
                parent, text="              ")
            color_label.configure(
                background=f"#{color[2]:02x}{color[1]:02x}{color[0]:02x}")
            range_label.grid(row=i, column=0)
            color_label.grid(row=i, column=1, padx=8)
