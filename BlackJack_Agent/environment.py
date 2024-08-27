from deck import Deck
from card import Card


class BlackjackEnvironment:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = []
        self.dealer_hand = []
        self.last_agent_action = None
        self.reset()

    def reset(self):
        self.deck = Deck()
        self.deck.populate()
        self.deck.shuffle()
        self.player_hand = [self.deck.draw(), self.deck.draw()]
        self.dealer_hand = [self.deck.draw()]
        self.last_agent_action = 'None'

    # to get a state
    # Sum total of agent hand (with aces as ones), is there an ace in the hand, dealer card, win/lose/continue
    # this gets sent to the agent
    def get_percept(self):
        # if the player has an ace in their hand
        has_ace = True if sum(1 for card in self.player_hand if card.rank == "Ace") >= 1 else False

        # is the game still going?

        if get_hand_value(self.player_hand) == 21:
            game_status = "win"
        elif get_hand_value(self.dealer_hand) > 21:
            game_status = "win"
        elif get_hand_value(self.player_hand) > 21:
            game_status = "lose"
        elif self.last_agent_action == 'hold':
            if (get_hand_value(self.player_hand) > get_hand_value(self.dealer_hand)
                    or get_hand_value(self.dealer_hand) > 21):
                game_status = "win"
            elif get_hand_value(self.player_hand) == get_hand_value(self.dealer_hand) and get_hand_value(
                    self.dealer_hand) != 21:
                game_status = "tie"
            else:
                game_status = "lose"
        else:
            game_status = "continue"

        # get rewards based on condition of game
        if game_status == "win":
            rewards = 1
        elif game_status == "continue" or game_status == "tie":
            rewards = 0
        else:
            rewards = -1

        return (get_hand_value(self.player_hand), has_ace,
                get_hand_value(self.dealer_hand), game_status,
                rewards)

    def run_game(self, agent):
        self.reset()
        agent.resetState()

        self.last_agent_action = 'init'
        while self.last_agent_action is not None:
            self.last_agent_action = agent.decide_action(self.get_percept())
            if self.last_agent_action == 'hit':
                self.player_hand.append(self.deck.draw())
                player_total = get_hand_value(self.player_hand)
                if player_total > 21:
                    agent.decide_action(self.get_percept())
                    return -1  # Player busted
            elif self.last_agent_action == "hold" or self.last_agent_action is None:
                while get_hand_value(self.dealer_hand) < 17:
                    self.dealer_hand.append(self.deck.draw())
                dealer_total = get_hand_value(self.dealer_hand)
                player_total = get_hand_value(self.player_hand)
                if dealer_total > 21 or dealer_total < player_total:
                    agent.decide_action(self.get_percept())
                    return 1  # Player wins
                elif dealer_total > player_total:
                    agent.decide_action(self.get_percept())
                    return -1  # Dealer wins
                else:
                    agent.decide_action(self.get_percept())
                    return 0  # Tie

    def run_game_strategic(self, agent, player_tot_init, dealer_tot_init):
        self.deck = Deck()
        self.player_hand = []
        self.dealer_hand = []
        self.last_agent_action = None

        if player_tot_init >= 11:
            self.player_hand.append(Card('Hearts', '10'))
            self.player_hand.append(Card('Hearts', str(player_tot_init - 10)))
        else:
            self.player_hand.append(Card('Hearts', str(player_tot_init)))

        self.dealer_hand.append(Card('Hearts', str(dealer_tot_init)))

        agent.resetState()

        self.last_agent_action = 'init'
        while self.last_agent_action is not None:
            self.last_agent_action = agent.decide_action(self.get_percept())
            if self.last_agent_action == 'hit':
                self.player_hand.append(self.deck.draw())
                player_total = get_hand_value(self.player_hand)
                if player_total > 21:
                    agent.decide_action(self.get_percept())
                    return -1  # Player busted
            elif self.last_agent_action == "hold" or self.last_agent_action is None:
                while get_hand_value(self.dealer_hand) < 17:
                    self.dealer_hand.append(self.deck.draw())
                dealer_total = get_hand_value(self.dealer_hand)
                player_total = get_hand_value(self.player_hand)
                if dealer_total > 21 or dealer_total < player_total:
                    agent.decide_action(self.get_percept())
                    return 1  # Player wins
                elif dealer_total > player_total:
                    agent.decide_action(self.get_percept())
                    return -1  # Dealer wins
                else:
                    agent.decide_action(self.get_percept())
                    return 0  # Tie


def get_hand_value(hand):
    num_aces = sum(1 for card in hand if card.rank == "Ace")
    s = 11 * num_aces

    for card in hand:
        if card.rank in ['Jack', 'Queen', 'King']:
            s += 10
        elif card.rank == "Ace":
            s += 0
        else:
            s += int(card.rank)

    while s > 21 and num_aces > 0:
        s -= 10
        num_aces -= 1

    return s
