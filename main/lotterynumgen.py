
import csv
import random
from collections import Counter

# Load previous winning numbers from mega millions
def load_past_draws(filename):
    white_balls = []
    mega_balls = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            white_balls.extend([int(row[f'WhiteBall{i}']) for i in range(1, 6)])
            mega_balls.append(int(row['MegaBall']))
    return white_balls, mega_balls

# Generate numbers based on frequency on mega millions
def generate_likely_numbers(white_balls, mega_balls):
    # Get top 15 frequent white balls and top 5 Mega Balls
    top_white = [num for num, _ in Counter(white_balls).most_common(15)]
    top_mega = [num for num, _ in Counter(mega_balls).most_common(5)]

    # Randomly pick 5 unique white balls and 1 Mega Ball from the frequent ones
    chosen_white = sorted(random.sample(top_white, 5))
    chosen_mega = random.choice(top_mega)

    return chosen_white, chosen_mega

def main():
    filename = 'mega_millions.csv'  # Path to your file
    white_balls, mega_balls = load_past_draws(filename)
    
    attempts = 0
    while attempts < 5:
        white, mega = generate_likely_numbers(white_balls, mega_balls)
        print(f"Your Mega Millions pick: {white} + Mega Ball: {mega}")
        attempts += 1

if __name__ == '__main__':
    main()