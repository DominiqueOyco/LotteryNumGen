import csv
import random
from collections import Counter

class LotteryData:
    def __init__(self, filename):
        self.filename = filename
        self.white_balls = []
        self.mega_balls = []
        self.power_balls = []
        self.super_balls = []

    def load_past_draws(self):
        try:
            with open(self.filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                if not reader.fieldnames:
                    raise ValueError("The file is empty or has no headers.")
                
                for row in reader:
                    try:
                        if self.filename == 'mega_millions.csv':
                            self.white_balls.extend([int(row[f'WhiteBall{i}']) for i in range(1, 6)])
                            self.mega_balls.append(int(row['MegaBall']))
                        elif self.filename == 'powerball.csv':
                            self.white_balls.extend([int(row[f'WhiteBall{i}']) for i in range(1, 6)])
                            self.power_balls.append(int(row['PowerBall']))
                        elif self.filename == 'superlotto.csv':
                            self.white_balls.extend([int(row[f'WhiteBall{i}']) for i in range(1, 6)])
                            self.super_balls.append(int(row['SuperBall']))
                        else:
                            raise ValueError("Unsupported file format.")
                    except (ValueError, KeyError) as e:
                        print(f"Skipping invalid row: {row}. Error: {e}")
                
                if not self.white_balls:
                    raise ValueError("The file does not contain valid lottery data.")
        except FileNotFoundError:
            print(f"Error: The file {self.filename} was not found.")
            exit(1)
        except ValueError as e:
            print(f"Error: {e}")
            exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            exit(1)

class LotteryGenerator:
    def __init__(self, white_balls, special_balls):
        self.white_balls = white_balls
        self.special_balls = special_balls

    def generate_numbers(self):
        top_white = [num for num, _ in Counter(self.white_balls).most_common(15)]
        top_special = [num for num, _ in Counter(self.special_balls).most_common(5)]

        chosen_white = sorted(random.sample(top_white, 5))
        chosen_special = random.choice(top_special)

        return chosen_white, chosen_special

class LotteryApp:
    def __init__(self, filename, lottery_type):
        self.data = LotteryData(filename)
        self.lottery_type = lottery_type

    def run(self):
        self.data.load_past_draws()
        if self.lottery_type == 'Mega Millions':
            generator = LotteryGenerator(self.data.white_balls, self.data.mega_balls)
        elif self.lottery_type == 'Powerball':
            generator = LotteryGenerator(self.data.white_balls, self.data.power_balls)
        elif self.lottery_type == 'SuperLotto':
            generator = LotteryGenerator(self.data.white_balls, self.data.super_balls)
        else:
            print("Invalid lottery type.")
            return

        for _ in range(5):
            white, special = generator.generate_numbers()
            print(f"Your {self.lottery_type} pick: {white} + Special Ball: {special}")

if __name__ == '__main__':
    print("Welcome to the Lottery Number Generator!")
    lotteryInput = input("1. Mega Millions\n2. Powerball\n3. SuperLotto\n4. All\n")

    if lotteryInput == '1':
        app = LotteryApp('mega_millions.csv', 'Mega Millions')
        app.run()
    elif lotteryInput == '2':
        app = LotteryApp('powerball.csv', 'Powerball')
        app.run()
    elif lotteryInput == '3':
        app = LotteryApp('superlotto.csv', 'SuperLotto')
        app.run()
    elif lotteryInput == '4':
        print("Generating numbers for all lotteries:")
        for filename, lottery_type in [('mega_millions.csv', 'Mega Millions'),
                                       ('powerball.csv', 'Powerball'),
                                       ('superlotto.csv', 'SuperLotto')]:
            print(f"\n{lottery_type}:")
            app = LotteryApp(filename, lottery_type)
            app.run()
    else:
        print("Invalid input. Please enter 1, 2, 3, or 4.")