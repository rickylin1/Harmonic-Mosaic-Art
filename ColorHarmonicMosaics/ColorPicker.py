import tkinter as tk
from tkinter import Canvas

class ColorPickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RGB Color Picker")

        # RGB values
        self.red = 0
        self.green = 0
        self.blue = 0

        # Hexadecimal color label
        self.hex_label = tk.Label(self.root, text="Hexadecimal Color:", font=("Arial", 12))
        self.hex_label.pack(pady=10)

        # Canvas to display color
        self.color_canvas = Canvas(self.root, width=200, height=200, bg="#000000")
        self.color_canvas.pack()

        # Slider for Red color
        self.red_slider = tk.Scale(self.root, from_=0, to=255, orient=tk.HORIZONTAL, label="Red", command=self.update_color)
        self.red_slider.pack(pady=5)

        # Slider for Green color
        self.green_slider = tk.Scale(self.root, from_=0, to=255, orient=tk.HORIZONTAL, label="Green", command=self.update_color)
        self.green_slider.pack(pady=5)

        # Slider for Blue color
        self.blue_slider = tk.Scale(self.root, from_=0, to=255, orient=tk.HORIZONTAL, label="Blue", command=self.update_color)
        self.blue_slider.pack(pady=5)

    def update_color(self, event=None):
        # Update RGB values
        self.red = self.red_slider.get()
        self.green = self.green_slider.get()
        self.blue = self.blue_slider.get()

        # Convert RGB to hexadecimal
        hex_color = f"#{self.rgb_to_hex(self.red)}{self.rgb_to_hex(self.green)}{self.rgb_to_hex(self.blue)}"

        # Update color canvas background
        self.color_canvas.configure(bg=hex_color)

        # Update hexadecimal color label
        self.hex_label.config(text=f"Hexadecimal Color: {hex_color}")

    def rgb_to_hex(self, rgb):
        # Convert an integer RGB value to hexadecimal
        return "{:02X}".format(rgb)

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorPickerApp(root)
    root.mainloop()
