import tkinter as tk
from tkinter import messagebox


class MarioBikeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mario Bike 64")
        self.root.geometry("400x350")
        self.selected_mode = None

        self.label = tk.Label(
            root, text="Select Input Mode", font=("Helvetica", 16, "bold"), pady=20
        )
        self.label.pack()

        self.create_button("Power Meter Mode", "POWER")
        self.create_button("Speed Sensor Mode", "SPEED")
        self.create_button("Heart Rate Mode", "HR")

        self.status = tk.Label(root, text="Waiting for selection...", fg="gray")
        self.status.pack(side="bottom", pady=10)

    def create_button(self, text, mode_value):
        btn = tk.Button(
            self.root,
            text=text,
            command=lambda: self.set_mode(mode_value),
            width=25,
            height=2,
            font=("Helvetica", 11),
        )
        btn.pack(pady=10)

    def set_mode(self, mode):
        self.selected_mode = mode
        print(f"Selected Mode: {self.selected_mode}")
        self.root.destroy()  # Close GUI to start the logic script


def get_user_mode():
    root = tk.Tk()
    app = MarioBikeGUI(root)
    root.mainloop()
    return app.selected_mode


class BluetoothSelectionGUI:
    def __init__(self, root, devices):
        self.root = root
        self.root.title("Mario Bike 64")
        self.root.geometry("400x350")
        self.target_address = None

        self.label = tk.Label(
            root,
            text="Select Bluetooth Device",
            font=("Helvetica", 16, "bold"),
            pady=20,
        )
        self.label.pack()

        for d in devices:
            if d.name:
                self.create_button(f"{d.name}", d.address)

        self.status = tk.Label(root, text="Waiting for selection...", fg="gray")
        self.status.pack(side="bottom", pady=10)

    def create_button(self, text, address):
        btn = tk.Button(
            self.root,
            text=text,
            command=lambda: self.select_device(address, text),
            width=25,
            height=2,
            font=("Helvetica", 11),
        )
        btn.pack(pady=10)

    def select_device(self, address, name):
        self.target_address = address
        print(f"Selected Device: {name} - {self.target_address}")
        self.root.destroy()  # Close GUI to start the logic script


if __name__ == "__main__":
    mode = get_user_mode()

    if mode == "POWER":
        print("Initializing Assioma logic...")
    elif mode == "SPEED":
        print("Initializing Speed Sensor logic...")
    elif mode == "HR":
        print("Initializing Heart Rate logic...")
    else:
        print("No mode selected. Exiting.")
