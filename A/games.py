import discord
from discord.ext import commands
import random

class BlackjackGame:
    def __init__(self, ctx):
        self.ctx = ctx
        self.deck = []
        self.player_cards = []
        self.computer_cards = []

    async def deal_card(self):
        """Deal a random card from the deck."""
        cards = [
            ('\U0001F0A1', 'Ace'),    # Ace
            ('\U0001F0A2', '2'),      # 2
            ('\U0001F0A3', '3'),      # 3
            ('\U0001F0A4', '4'),      # 4
            ('\U0001F0A5', '5'),      # 5
            ('\U0001F0A6', '6'),      # 6
            ('\U0001F0A7', '7'),      # 7
            ('\U0001F0A8', '8'),      # 8
            ('\U0001F0A9', '9'),      # 9
            ('\U0001F0AA', '10'),     # 10
            ('\U0001F0AB', 'Jack'),   # Jack
            ('\U0001F0AD', 'Queen'),  # Queen
            ('\U0001F0AE', 'King'),   # King
        ]
        return random.choice(cards)

    async def start_game(self):
        self.player_cards = [await self.deal_card(), await self.deal_card()]
        self.computer_cards = [await self.deal_card(), await self.deal_card()]

        player_hand = ', '.join([f"{symbol} ({value})" for symbol, value in self.player_cards])
        computer_hand = ', '.join([f"{symbol} ({value})" for symbol, value in self.computer_cards[:-1]])
        await self.ctx.send(f"Your cards: {player_hand}, current score: {self.calculate_score(self.player_cards)}")
        await self.ctx.send(f"Computer's first card: {computer_hand} and one hidden card")

    async def play(self):
        await self.start_game()

        while True:
            user_score = self.calculate_score(self.player_cards)
            computer_score = self.calculate_score(self.computer_cards)

            if user_score == 0 or computer_score == 0 or user_score > 21:
                break

            hit_or_stand = await self.ctx.send("Type 'hit' to get another card, or 'stand' to pass: ")
            try:
                msg = await self.ctx.bot.wait_for(
                    "message",
                    check=lambda m: m.author == self.ctx.author and m.channel == self.ctx.channel,
                    timeout=30.0
                )
            except asyncio.TimeoutError:
                await self.ctx.send("Timeout. The game has ended.")
                return

            if msg.content.lower() == 'hit':
                self.player_cards.append(await self.deal_card())
                player_hand = ', '.join([f"{symbol} ({value})" for symbol, value in self.player_cards])
                await self.ctx.send(f"You draw a card. Your cards: {player_hand}, current score: {self.calculate_score(self.player_cards)}")
            elif msg.content.lower() == 'stand':
                break

        await self.finish_game()

    async def finish_game(self):
        computer_score = self.calculate_score(self.computer_cards)

        while computer_score < 17:
            self.computer_cards.append(await self.deal_card())
            computer_score = self.calculate_score(self.computer_cards)

        player_hand = ', '.join([f"{symbol} ({value})" for symbol, value in self.player_cards])
        computer_hand = ', '.join([f"{symbol} ({value})" for symbol, value in self.computer_cards])
        await self.ctx.send(f"Your final hand: {player_hand}, final score: {self.calculate_score(self.player_cards)}")
        await self.ctx.send(f"Computer's final hand: {computer_hand}, final score: {computer_score}")

        await self.ctx.send(self.compare_scores())

    def compare_scores(self):
        user_score = self.calculate_score(self.player_cards)
        computer_score = self.calculate_score(self.computer_cards)

        if user_score > 21 and computer_score > 21:
            return "You went over. You lose!"
        if user_score > 21:
            return "You went over. You lose!"
        if computer_score > 21:
            return "Computer went over. You win!"
        if user_score > computer_score:
            return "You win!"
        else:
            return "You lose!"

    def calculate_score(self, cards):
        card_values = {
            '\U0001F0A1': 1,   # Ace
            '\U0001F0A2': 2,   # 2
            '\U0001F0A3': 3,   # 3
            '\U0001F0A4': 4,   # 4
            '\U0001F0A5': 5,   # 5
            '\U0001F0A6': 6,   # 6
            '\U0001F0A7': 7,   # 7
            '\U0001F0A8': 8,   # 8
            '\U0001F0A9': 9,   # 9
            '\U0001F0AA': 10,  # 10
            '\U0001F0AB': 10,  # Jack
            '\U0001F0AD': 10,  # Queen
            '\U0001F0AE': 10   # King
        }
        score = sum(card_values.get(card[0], 0) for card in cards)
        if '\U0001F0A1' in cards and score + 10 <= 21:
            score += 10
        return score
