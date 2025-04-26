import tkinter as tk
from tkinter import messagebox
from lotterynumgen import LotteryApp, LotteryGenerator

class LotteryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lottery Number Generator")
        self.root.geometry("1280x720")

        # Title Label
        self.title_label = tk.Label(root, text="Lottery Number Generator", font=("Arial", 16))
        self.title_label.pack(pady=10)

        # Lottery Selection Label
        self.selection_label = tk.Label(root, text="Select a Lottery:", font=("Arial", 12))
        self.selection_label.pack(pady=5)

        # Lottery Buttons
        self.mega_button = tk.Button(root, text="Mega Millions", command=self.generate_mega)
        self.mega_button.pack(pady=5)

        self.power_button = tk.Button(root, text="Powerball", command=self.generate_power)
        self.power_button.pack(pady=5)

        self.super_button = tk.Button(root, text="SuperLotto", command=self.generate_super)
        self.super_button.pack(pady=5)

        self.all_button = tk.Button(root, text="Generate All", command=self.generate_all)
        self.all_button.pack(pady=5)

        # Output Text Box
        self.output_text = tk.Text(root, height=50, width=100, state="disabled")
        self.output_text.pack(pady=10)

    def display_output(self, message):
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, message)
        self.output_text.config(state="disabled")

    def generate_mega(self):
        app = LotteryApp('mega_millions.csv', 'Mega Millions')
        self.run_lottery(app)

    def generate_power(self):
        app = LotteryApp('powerball.csv', 'Powerball')
        self.run_lottery(app)

    def generate_super(self):
        app = LotteryApp('superlotto.csv', 'SuperLotto')
        self.run_lottery(app)

    def generate_all(self):
        output = ""
        for filename, lottery_type in [('mega_millions.csv', 'Mega Millions'),
                                       ('powerball.csv', 'Powerball'),
                                       ('superlotto.csv', 'SuperLotto')]:
            app = LotteryApp(filename, lottery_type)
            output += f"\n{lottery_type}:\n"
            output += self.run_lottery(app, return_output=True)
        self.display_output(output)

    def run_lottery(self, app, return_output=False):
        try:
            app.data.load_past_draws()
            generator = LotteryGenerator(app.data.white_balls, app.data.mega_balls if app.lottery_type == 'Mega Millions' else
                                         app.data.power_balls if app.lottery_type == 'Powerball' else app.data.super_balls)
            output = ""
            for _ in range(5):
                white, special = generator.generate_numbers()
                output += f"Your {app.lottery_type} pick: {white} + Special Ball: {special}\n"
            if return_output:
                return output
            else:
                self.display_output(output)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    gui = LotteryGUI(root)
    root.mainloop()