import random
import copy
DEFAULT_CHIPS = 20

class Card:
	value_to_name = {1:"Ace", 2:"Two", 3:"Three", 4:"Four", 5:"Five", 6:"Six", 7:"Seven",8:"Eight", 9:"Nine", 10:"Ten", 11:"Jack", 12:"Queen", 13:"King"}
	suit_id_to_name = {1:"Clubs", 2:"Diamonds", 3:"Hearts", 4:"Spades"}

	def __init__(self, value, suit_id):
		self.value = value
		self.suit_id = suit_id

	def __repr__(self):
		return "%s of %s" % (self.value_to_name[self.value], self.suit_id_to_name[self.suit_id])

	def get_score(self):
		if self.value <= 10:
			if self.value == 1:
				return [1, 11]
			else:
				return [self.value]
		else:
			painted = self.value - 10
			return [painted]

class Hand:
	def __init__(self, cards):
		self.cards = cards

	def get_score(self):
		sum_score = [0]
		for card in self.cards:
                        sum_list = []
                        score_list = card.get_score()
                        for s1 in score_list:
                                for s2 in sum_score:
                                        sum_list.append(s1 + s2)
                        sum_score = sum_list
		return sum_score

	def can_split(self):
		if len(self.cards) == 2 and self.cards[0].value == self.cards[1].value:
			return True
		else:
			return False

	def is_busted(self):
		scores = self.get_score()
		for s in scores:
                        if s <= 21:
                                return False
                return True

	def __repr__(self):
		return str(self.cards)

class Deck:
	unshuffled_deck = [Card(value, suit_id) for value in range(1, 14) for suit_id in range(1, 5)]
	
	def __init__(self, num_decks=1):
		self.deck = self.unshuffled_deck * num_decks
		random.shuffle(self.deck)

	def deal_card(self):
		return self.deck.pop()

	def deal_hand(self):
		return Hand([self.deal_card()])

class Player:
	def __init__(self, name="Player 1", chips=DEFAULT_CHIPS):
		self.name = name
		self.chips = chips
		self.current_bet = 0
		self.hands = []
		self.is_splitted = False
		self.is_standing_l = [False]

	def new_hand(self, hand):
		self.hands.append(hand)

	def add_card_to_hand(self, card, hand_id=0):
		self.hands[hand_id].cards.append(card)

	def hit(self, card, hand_id=0):
		self.hands[hand_id].cards.append(card)

	def is_busted(self, hand_id=0):
                if self.hands == []:
                        return False
		return self.hands[hand_id].is_busted()
        
        def is_busted_or_standing(self):
                for hand_id in xrange(0, len(self.hands)):
                        if not self.is_busted(hand_id) and not self.is_standing_l[hand_id]:
                                return False
                return True
        
        def is_standing(self):
                if self.hands == []:
                        return False
                for hand_id in xrange(0, len(self.hands)):
                        if not self.is_standing_l[hand_id]:
                                return False
                return True

	def can_split(self):
		if self.is_splitted:
			return False
		else:
			return self.hands[0].can_split()

	def split(self, deck): #requires deck to deal cards after split. Because has to hit after split.
		if self.can_split():
			second_card = copy.deepcopy(self.hands[0].cards[1])
			del self.hands[0].cards[1]
			self.new_hand(hand([second_card]))
			self.is_splitted = True
			self.is_standing_l.append(False)
#			HAS TO HIT AFTER SPLIT
                        self.hit(deck.deal_card(), 0)
                        self.hit(deck.deal_card(), 1)
		else:
			 print 'ERROR: call split without can_split'

	def get_score(self, hand_id=0):
                if self.hands == []:
                        return [0]
		return self.hands[hand_id].get_score()
        
        def get_busted(self):
                self.chips -= self.current_bet
                self.current_bet = 0
                
        def make_win(self):
                self.chips += self.current_bet*2 # winning rate: 2 times of the bet.
                self.current_bet = 0
        
        def clear_for_next_hands(self):
                self.current_bet = 0
		self.hands = []
		self.is_splitted = False
		self.is_standing_l = [False]

	def __repr__(self):
		player_str = self.name
		if self.is_busted():
			player_str += " BUSTED"
                elif self.is_standing():
			player_str += " STANDING"
		return "Player: {}\nChips left: {}\nCurrent Bet: {}\nCards: {}\nScore: {}\n".format(player_str, self.chips, self.current_bet, self.hands, self.get_score())

class Table:
	def __init__(self):
		self.players = []
	def add_player(self, player):
		self.players.append(player)
        def are_all_players_busted_or_standing(self):
                for p in xrange(1, len(table.players)):
                        if not table.players[p].is_busted_or_standing():
                                return False
                return True
        def is_any_player_standing(self):
                for p in xrange(1, len(table.players)):
                        if table.players[p].is_standing():
                                return True
                return False
        
        def does_player_win_against_bank(self, player, hand_id, bank_player_id=0):
                player_scores = player.get_score(hand_id)
                bank_scores = self.players[bank_player_id].get_score(0)
                best_ps = 0
                best_bs = 0
                # find best score of player
                for ps in player_scores:
                        if ps <= 21:
                                if ps > best_ps:
                                        best_ps = ps
                # find best score of bank
                for bs in bank_scores:
                        if bs <= 21:
                                if bs > best_bs:
                                        best_bs = bs
                if best_ps > best_bs:
                        return True
                else:
                        return False
        
        def clear_for_next_hands(self):
                for player in self.players:
                        player.clear_for_next_hands()
        
        def remove_players_without_chips(self):
                self.players = [player for player in self.players if player.chips > 0]
        
        def __repr__(self):
                output = "Current Status of All Players\n------\n"
                for player in self.players:
                        output += "{}\n".format(player)
                return output

if __name__ == "__main__":
	print "Welcome to 21!"
	while True:
		try:
			number_of_players = int(raw_input("How many players would you like? Please enter a number.\n"))
			if number_of_players < 1:
				raise ValueError
			break
		except ValueError:
			print("Ops! That can't be the number of players. Try again...")
	
	print "\n"
	table = Table()
	for p in xrange(0, number_of_players+1):
		if p == 0:
			p_name = "Bank"
		else:
			p_name = "Player " + str(p)
		table.add_player(Player(p_name))
		print "{} is created.".format(p_name)
	
	print "Each player has {} chips.".format(DEFAULT_CHIPS)

        while len(table.players) > 1:
                number_of_decks = (len(table.players) -2) / 3 + 1
                print "The game will be played with {} deck(s).\n".format(number_of_decks)

                deck = Deck(number_of_decks)
                print "Deck is shuffled.\n"

                #Deal first cards
                for player in table.players:
                        player.new_hand(deck.deal_hand())
                print "The first cards are dealt.\n"
                print "Taking turns to put in bets.\n"
                

                #Ask and receive first bets
                for p in xrange(1, len(table.players)): # Bank does not bet
                        print "{}'s turn. Here is your hand:".format(table.players[p].name)
                        print (table.players[p].hands[0])
                        print "and current possible scores for it: {}".format(table.players[p].get_score(0))
                        print "\n"
                        while True:
                                try:
                                        bet = int(raw_input("{}, you have {} chips left. How many chips do you bet? Please enter a number between 1 and {}.\n".format(table.players[p].name, table.players[p].chips, table.players[p].chips)))
                                        if bet < 1 or bet > table.players[p].chips:
                                                raise ValueError
                                        break
                                except ValueError:
                                        print("\nOps! That can't be bet. Try again...")
                        table.players[p].chips -= bet
                        table.players[p].current_bet = bet
                        print "\n"
                
                #Deal second cards
                for player in table.players:
                        player.add_card_to_hand(deck.deal_card())
                        
                print "The second cards are dealt.\n"
                
                print "Taking turns to play.\n"

                #Ask and receive action until all players are busted or standing.
                while not table.are_all_players_busted_or_standing():
                        p = 1 # Bank does not play yet.
                        while p < len(table.players):
                                if table.players[p].is_busted():
                                        print "{} is busted. So skipping.\n".format(table.players[p].name)
                                        p += 1
                                        continue
                                
                                if table.players[p].is_standing():
                                        print "{} is standing. So skipping.\n".format(table.players[p].name)
                                        p += 1
                                        continue
                                
                                print "{}'s turn. Here is your hand:".format(table.players[p].name)
                                print (table.players[p].hands[0])
                                print "and current possible scores for it: {}".format(table.players[p].get_score(0))
                                if table.players[p].is_splitted:
                                        # then print the second hand as well
                                        print "This is your splitted hand:"
                                        print (table.players[p].hands[1])
                                        print "and current possible scores for it: {}".format(table.players[p].get_score(1))
                                print "\n"
                                        
                                while True:
                                        if table.players[p].can_split():
                                                input_text = "{}, please choose one of the following actions. A split is also possible.\n(h)it\t(s)tand\ts(p)lit\n".format(table.players[p].name)
                                        elif table.players[p].is_splitted:
                                                # then this player plays two times, one hand each.
                                                input_text = "{}, please choose one of the following actions for each of your hands. One letter for your first hand and one letter for your splitted hand. Two letters without space. A split is not possible.\n(h)it\t(s)tand\n".format(table.players[p].name)
                                        else: 
                                                # this player cannot split and did not split.
                                                input_text = "{}, please choose one of the following actions. A split is not possible.\n(h)it\t(s)tand\n".format(table.players[p].name)
                                        try:
                                                action = raw_input(input_text)
                                                if table.players[p].is_splitted:
                                                        if not len(action) == 2:
                                                                raise ValueError
                                                elif not len(action) == 1:
                                                        raise ValueError
                                                for a in xrange(0, len(action)): #loop through each action a in action
                                                        if not action[a] == "h" and not action[a] == "s" and (table.players[p].can_split() and not action[a] == "p"):
                                                                raise ValueError
                                                break
                                        except ValueError:
                                                print("\nOps! That is not a valid action. Try again...")
                                
                                there_is_split = False #if there is split then the current player will play again
                                for a in xrange(0, len(action)): #loop through each action a in action
                                        if action[a] == "h":
                                                table.players[p].hit(deck.deal_card(), a)
                                                print "{} hits.".format(table.players[p].name)
                                                print "{}'s new hand:".format(table.players[p].name)
                                                print (table.players[p].hands[0])
                                                print "and current possible scores for it: {}".format(table.players[p].get_score(0))
                                                if table.players[p].is_splitted:
                                                        # then print the second hand as well
                                                        print "This is her splitted hand:"
                                                        print (table.players[p].hands[1])
                                                        print "and current possible scores for it: {}".format(table.players[p].get_score(1))
                                                print "\n"
                                                if table.players[p].is_busted():
                                                        print "{} is BUSTED! He is out until the end of this round of hands.".format(table.players[p].name)
                                        elif action[a] == "s":
                                                table.players[p].is_standing_l[a] = True
                                                print "{} stands.".format(table.players[p].name)
                                        else: # if action[a] == "p" and table.players[p].can_split()
                                                table.players[p].split(deck)
                                                print "{} splits. Then automatically hits for each hand. Now {} plays again!".format(table.players[p].name, table.players[p].name)
                                                there_is_split = True
                                
                                print "\n"
                                if not there_is_split:
                                        p += 1 #next player

                # print player status
                print table
                
                # to follow ui easily
                enter = raw_input("Players are done with turns. Bank is going to play. Press Enter to continue.\n")
                
                #Make the bank play, only if there are players who are not busted.
                bank_status = 1 # 1: No other player standing, Bank wins. 2: Bank stands. 3: Bank is busted. Standing players win.
                if table.is_any_player_standing():
                        # Bank's turn
                        while min(table.players[0].get_score(0)) <= 16:
                                print "{}'s turn. Here is {}'s hand:".format(table.players[0].name, table.players[0].name)
                                print (table.players[0].hands[0])
                                print "and current possible scores for it: {}\n".format(table.players[0].get_score(0))
                        
                                # Bank hits.
                                table.players[0].hit(deck.deal_card())
                                print "{} hits.\n".format(table.players[0].name)
                        
                        print "{}'s turn. Here is Bank's hand:".format(table.players[0].name)
                        print (table.players[0].hands[0])
                        print "and current possible scores for it: {}\n".format(table.players[0].get_score(0))
                        
                        if table.players[0].is_busted():
                                bank_status = 3
                                print "{} is BUSTED! She lost!".format(table.players[0].name)
                        
                        else:
                                table.players[0].is_standing_l[0] = True
                                bank_status = 2
                                print "{} stands. Checking scores...".format(table.players[0].name)
                else:
                        # No need for the bank to play. She wins.
                        bank_status = 1
                        print "There is no need for {} to play. No player left standing. So, {} wins!".format(table.players[0].name, table.players[0].name)
                
                # to follow ui easily
                enter = raw_input("Bank is done with her turns. Press Enter to continue.\n")
                
                #Decide on who wins and give players chips accordingly.
                if bank_status == 1:
                        for p in xrange(1, len(table.players)):
                                table.players[p].get_busted()
                elif bank_status == 2:
                        for p in xrange(1, len(table.players)):
                                if table.players[p].is_standing():
                                        for hand_id in xrange(0, len(table.players[p].hands)):
                                                if table.does_player_win_against_bank(table.players[p], hand_id):
                                                        table.players[p].make_win()
                                                        print "{} wins against the {}!".format(table.players[p].name, table.players[0].name)
                                                else:
                                                        table.players[p].get_busted()
                                                        print "{} loses against the {}!".format(table.players[p].name, table.players[0].name)
                
                elif bank_status == 3:
                        for p in xrange(1, len(table.players)):
                                if table.players[p].is_standing():
                                        table.players[p].make_win()
                                        print "Since the {} is busted, {} wins!".format(table.players[0].name, table.players[p].name)
                
                print "\nChips updated.\n"
                
                for p in xrange(1, len(table.players)):
                        if table.players[p].chips <= 0:
                                print "{} has no chips left. She is out of game.\n".format(table.players[p].name)
                
                table.remove_players_without_chips()
                table.clear_for_next_hands()
                
                print table
        
        print "All players have lost their chips completely. The {} wins forever!".format(table.players[0].name)
	