import random
import pickle


class BlackJackAgentTerrible:

    def __init__(self):
        self.Q = {((0, 2, 0), "hit"): 0, ((0, 2, 0), "hold"): 0,
                  ((0, 3, 0), "hit"): 0, ((0, 3, 0), "hold"): 0, }  # etc
        self.N_sa = {}
        self.s = {'player_total': 0, 'has_ace': False,
                  'dealer_card': 0, 'state_of_game': 'continue',
                  'reward': 0}
        self.a = None

    def show_percept(self):
        print(self.s)

    def decide_action(self, percept):
        player_total, has_ace, dealer_card, state_of_game, reward = percept

        self.s = {'player_total': player_total, 'has_ace': has_ace,
                  'dealer_card': dealer_card, 'state_of_game': state_of_game,
                  'reward': reward}
        if self.s['player_total'] <= 18:
            self.a = "hit"
        elif self.s['state_of_game'] not in ['win', 'lose']:
            self.a = "hold"
        else:
            self.a = None
        return self.a

    def resetState(self):
        self.s = None


class BlackJackAgentLearned:

    def __init__(self):
        self.Q = {}
        self.N_sa = {}

        for p in range(32):
            for ace in [True, False]:
                for d in range(32):
                    for action in ["hit", "hold"]:
                        tupQ = (p, ace, d, action)
                        self.Q[tupQ] = 0.0
                        self.N_sa[tupQ] = 0
        self.s = None
        self.a = None
        self.prob = .8
        self.gamma = 1

    def show_percept(self):
        print(self.s)

    def decide_action(self, percept):
        player_total, has_ace, dealer_card, state_of_game, reward = percept

        tupPrimeHit = (player_total, has_ace, dealer_card, "hit")
        tupPrimeHold = (player_total, has_ace, dealer_card, "hold")

        if self.s is not None:
            tupQ = (self.s['player_total'], self.s['has_ace'], self.s['dealer_card'], self.a)

            self.N_sa[tupQ] += 1

            alpha = (1000 / (1000 + self.N_sa[tupQ]))
            maxStuff = max(self.Q[tupPrimeHit], self.Q[tupPrimeHold])
            selfTupNum = self.Q[tupQ]
            calc = (alpha *
                             (reward + (self.gamma * maxStuff) - selfTupNum))

            self.Q[tupQ] += calc

        self.s = {'player_total': player_total, 'has_ace': has_ace,
                  'dealer_card': dealer_card}

        action_val = max(self.Q[tupPrimeHold], self.Q[tupPrimeHold])

        if self.Q[tupPrimeHit] == action_val:
            # this means that we chose the action to hit
            rand = random.randrange(1, 11)
            if rand < 9:
                self.a = "hit"
            else:
                self.a = "hold"
        else:
            # this means that we chose the action to hold
            rand = random.randrange(1, 11)
            if rand < 9:
                self.a = "hold"
            else:
                self.a = "hit"

        return self.a

    def saveQ(self, name):
        newName = name + 'Q.pkl'
        with open(newName, 'wb') as f:
            pickle.dump(self.Q, f)
        f.close()

        newName = name + 'NSA.pkl'
        with open(newName, 'wb') as f2:
            pickle.dump(self.N_sa, f2)
        f2.close()


    def loadQ(self, name):
        with open('pickleQ.pkl', 'rb') as f:
            self.Q = pickle.load(f)
        f.close()

        with open('pickleNSA.pkl', 'rb') as f2:
            self.N_sa = pickle.load(f2)
        f2.close()

    def resetState(self):
        self.s = None

# a' = argmax of a' (Q(s', a')) with probability p, do other action with probability 1-p
