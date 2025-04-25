import csv
import random
from collections import Counter

class LotteryData:
    def __init__(self, filename):
        self.filename = filename
        self.white_balls = []
        self.mega_balls = []
        self.power_balls = [] # TODO: Implement Power Ball functionality
        self.super_balls = [] # TODO: Implement SuperLotto functionality

    def load_past_draws(self):
        with open(self.filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.white_balls.extend([int(row[f'WhiteBall{i}']) for i in range(1, 6)])
                self.mega_balls.append(int(row['MegaBall']))

class LotteryGenerator:
    def __init__(self, white_balls, mega_balls):
        self.white_balls = white_balls
        self.mega_balls = mega_balls

    def generate_likely_megamillions_numbers(self):
        # Get top 15 frequent white balls and top 5 Mega Balls
        top_white = [num for num, _ in Counter(self.white_balls).most_common(15)]
        top_mega = [num for num, _ in Counter(self.mega_balls).most_common(5)]

        # Randomly pick 5 unique white balls and 1 Mega Ball from the frequent ones
        chosen_white = sorted(random.sample(top_white, 5))
        chosen_mega = random.choice(top_mega)

        return chosen_white, chosen_mega

class LotteryApp:
    def __init__(self, filename):
        self.data = LotteryData(filename)

    def run(self):
        self.data.load_past_draws()
        generator = LotteryGenerator(self.data.white_balls, self.data.mega_balls)

        attempts = 0
        while attempts < 5:
            white, mega = generator.generate_likely_megamillions_numbers()
            print(f"Your Mega Millions pick: {white} + Mega Ball: {mega}")
            attempts += 1

if __name__ == '__main__':
    app = LotteryApp('mega_millions.csv')
    app.run()