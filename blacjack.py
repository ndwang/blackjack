class card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    def __repr__(self):
        return f"{self.rank} of {self.suit}"
    
    def __add__(self,other):
        value = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}
        if isinstance(other, self.__class__):
            return value[self.rank] + value[other.rank]
        elif isinstance(other, int):
            return other + value[self.rank]
        else:
            raise NotImplementedError
        
    def __radd__(self,other):
        value = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}
        if isinstance(other, int):
            return other + value[self.rank]
        else:
            raise NotImplementedError

class hand:
    def __init__(self, cards):
        self.cards = cards
        self.sum = sum(cards)
        self.soft = any(card.rank=='Ace' for card in cards)
        
    def __str__(self):
        return ", ".join([str(card) for card in self.cards])
    
    def add(self, card):
        self.cards.append(card)
        self.soft = card.rank=='Ace'
        self.sum = self.sum + card
        return self.busted()
        
    def busted(self):
        if self.soft and self.sum>21:
            self.sum -= 10
            self.soft = False
        return self.sum>21

class shoe:
    from random import shuffle
    def __init__(self, ndeck=4, penetration=0.5):
        self.ndeck = ndeck
        self.penetration = penetration
        self.reshuffle(ndeck)
    
    def deal(self, n=1):
        if n>1:
            return [self.deck.pop() for i in range(n)]
        return self.deck.pop()
    
    def isEmpty(self):
        return (len(self.deck) < self.ndeck*52*(1-self.penetration))
    
    def reshuffle(self, ndeck):
        self.deck = []
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        for i in range(ndeck):
            for suit in suits:
                for rank in ranks:
                    self.deck.append(card(suit, rank))
        self.shuffle(self.deck)

class game:
    def __init__(self, bank):
        self.bank = bank
        self.shoe = shoe()
        self.last_bet = 0
        while self.bank > 0:
            print(f'Current money: {self.bank}')
            self.turn(int(input('Place your bet: ')))
            print('')
            
        print('Get outta here!')
        input()
        
    def turn(self, bet=0):
        if bet==0:
            bet = self.last_bet
        self.last_bet = bet
        self.bank -= bet
        
        self.dealer_hand = hand(self.shoe.deal(2))
        self.player_hand = hand(self.shoe.deal(2))
        
        while True:
            print(f"Player hand: {self.player_hand} ({self.player_hand.sum})")
            print(f"Dealer hand: {self.dealer_hand.cards[0]}, <face down>")
            
            action = input('Action? ')
            if action=='hit':
                if self.player_hand.add(self.shoe.deal()): break
            elif action=='stand':
                break
            elif action=='double':
                self.bank -= bet
                bet *= 2
                self.last_bet = bet
                self.player_hand.add(self.shoe.deal())
                break
                
        print(f"Player hand: {self.player_hand} ({self.player_hand.sum})")
        print(f"Dealer hand: {self.dealer_hand} ({self.dealer_hand.sum})")
        
        if self.player_hand.busted():
            print('Player busted!')
            print(f'You lost ${bet}!')
            return
        
        if self.dealer_strategy():
            print('Dealer busted!')
            print(f'You won ${bet}!')
            self.bank += 2*bet
            return
        
        if self.dealer_hand.sum > self.player_hand.sum:
            print(f'You lost ${bet}!')
        elif self.dealer_hand.sum == self.player_hand.sum:
            print('Push!')
        else:
            print(f'You won ${bet}!')
            self.bank += 2*bet
            
    def dealer_strategy(self):
        # stand on soft 17
        if self.dealer_hand.sum >= 17: return False
        while (self.dealer_hand.sum < 17):
            self.dealer_hand.add(self.shoe.deal())
        print(f"Dealer hand: {self.dealer_hand} ({self.dealer_hand.sum})")
        return self.dealer_hand.busted()
    

def main():
    g = game(int(input('Deposit money here: ')))

if __name__ == "__main__":
    main()