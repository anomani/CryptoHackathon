import csv
import random
from datetime import datetime, timedelta

tokens = [
    ['dogwifhat', '$WIF', 'Solana'],
    ['Shark Cat', 'SC', 'Solana'],
    ['Costco Hot Dog', 'COST', 'Solana'],
    ['Runestone', 'Runes', 'Solana'],
]

def generate_token_transactions():
    with open('token_transactions.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        # Header
        writer.writerow(["Token", "Date", "Chain", "Price (USD)", "Amount", "BUY/SELL"])

        # Write the data
        now = datetime.now()
        secondDelta = 0
        while secondDelta < 10000:
            now = now + timedelta(seconds=1)
            secondDelta += 1

            for token in tokens:
                # compute randomized datapoint
                # naive randomization for simplicity
                price = random.random() * 0.5
                amount = random.random() * 10000
                buySell = random.choice(['BUY', 'SELL'])

                writer.writerow([token[0], now, token[2], price, amount, buySell])


def generate_social_media_data():
    with open('token_transactions.csv', 'r', newline='') as readfile:
        reader = csv.reader(readfile)
        next(reader)
        reader = list(reader)
        with open('social_media_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)

            # Header
            writer.writerow(["Token", "Date", "Chain", "Price (USD)", "User", "Message", "Sentiment Score"])

            # Write the data
            now = datetime.now()
            secondDelta = 0
            readerIndex = 0
            while secondDelta < 10000:
                now = now + timedelta(seconds=1)
                secondDelta += 1

                for token in tokens:
                    # compute randomized datapoint
                    # naive randomization for simplicity
                    price = reader[readerIndex][3]
                    readerIndex += 1

                    user = "@user" + str(random.randint(1, 100))
                    bullOrBear = random.choice([0, 1])
                    message = ["I'm bearish on " + token[0] + "!", "I'm bullish on " + token[0] + "!"][bullOrBear]
                    sentiment = (random.random() + bullOrBear) * 0.5

                    writer.writerow([token[0], now, token[2], price, user, message, sentiment])


if __name__ == '__main__':
    generate_token_transactions()            
    generate_social_media_data()