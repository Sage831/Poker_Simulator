import random                                                                   #simulate shuffling deck and hands
import time                                                                     #enforce time limit
import itertools                                                                #create card combinations


def full_deck():

    cards = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']              #creates a list for cards in a deck
    suits = ['\u2660','\u2663','\u2665','\u2666']                               #creates a list for suits in a deck [Spades, Clubs, Hearts, Diamonds]
    deck_of_cards = []                                                          #empty list to store suited cards

    for card in cards:                                                          #iterates through cards list
        for suit in suits:                                                      #iterates through suits list
            deck_of_cards.append(card + suit)                                   #appends suited cards to deck of cards list

    random.shuffle(deck_of_cards)                                               #shuffles deck of cards
    return deck_of_cards                                                        #returns shuffled deck of cards


def normalize_card_input(card_input):

    card_input = card_input.strip()                                             #removes leading and trailing whitespace from the user input
    card_input = card_input.upper()                                             #converts the rank part of the card to uppercase

    suit_replacements = {                                                       #creates a dictionary that maps easy suit letters to suit symbols
        "S": "\u2660",                                                          #maps S to spades
        "C": "\u2663",                                                          #maps C to clubs
        "H": "\u2665",                                                          #maps H to hearts
        "D": "\u2666"                                                           #maps D to diamonds
    }

    if len(card_input) < 2:                                                     #checks if the input is too short to be a valid card
        return None                                                             #returns None for invalid input

    rank = card_input[:-1]                                                      #stores every character except the last one as the card rank
    suit = card_input[-1]                                                       #stores the last character as the card suit

    if suit in suit_replacements:                                               #checks if the suit was entered as a letter
        suit = suit_replacements[suit]                                          #replaces the suit letter with the matching suit symbol

    valid_ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']        #creates a list of valid card ranks
    valid_suits = ['\u2660','\u2663','\u2665','\u2666']                         #creates a list of valid card suits

    if rank not in valid_ranks:                                                 #checks if the rank is invalid
        return None                                                             #returns None for invalid input

    if suit not in valid_suits:                                                 #checks if the suit is invalid
        return None                                                             #returns None for invalid input

    return rank + suit                                                          #returns the normalized card using the same format as the rest of the program


def get_card_from_user(prompt):

    card = None                                                                 #creates a variable to store the validated card

    while card is None:                                                         #loops until the user enters a valid card
        card_input = input(prompt)                                              #gets the raw card input from the user
        card = normalize_card_input(card_input)                                 #normalizes and validates the card input

        if card is None:                                                        #checks if the user entered an invalid card
            print("Invalid card. Use format like AS, 10H, 7D, or QC.")          #prints an explanation of the expected card format

    return card                                                                 #returns the valid normalized card


def get_unique_card_from_user(prompt, used_cards):

    card = get_card_from_user(prompt)                                           #gets a valid card from the user

    while card in used_cards:                                                   #checks if the card was already entered
        print("That card has already been used. Enter a different card.")       #prints a duplicate-card warning
        card = get_card_from_user(prompt)                                       #asks the user for another valid card

    used_cards.append(card)                                                     #adds the card to the used-cards list
    return card                                                                 #returns the unique card


def get_player_count_from_user():

    player_count = None                                                         #creates a variable to store the validated player count

    while player_count is None:                                                 #loops until the user enters a valid player count

        player_count_raw = input("Enter total number of players including you: ")   #gets the raw player count input from the user
        player_count_raw = player_count_raw.strip()                                 #removes leading and trailing whitespace from the input

        try:                                                                    #attempts to convert the input into an integer
            player_count = int(player_count_raw)                                #converts the raw input into an integer

        except ValueError:                                                      #runs if the input cannot be converted into an integer
            print("Invalid number. Enter a whole number from 2 to 10.")         #prints an invalid-number warning
            player_count = None                                                 #resets player_count so the loop continues
            continue                                                            #returns to the top of the loop

        if player_count < 2 or player_count > 10:                               #checks if the player count is outside normal poker table limits
            print("Invalid player count. Enter a number from 2 to 10.")         #prints an invalid-player-count warning
            player_count = None                                                 #resets player_count so the loop continues

    return player_count                                                         #returns the valid total player count


def deal_my_cards():

    deck_of_cards = full_deck()                                                 #creates a deck of cards using full_deck()
    my_cards = [deck_of_cards.pop(), deck_of_cards.pop()]                       #pops two cards from deck for my hand
    return my_cards                                                             #returns my cards


def deal_community_cards(my_cards):

    deck_of_cards = full_deck()                                                 #creates a deck of cards using full_deck()
    
    for card in my_cards:                                                       #iterates through my cards
        deck_of_cards.remove(card)                                              #removes cards in my hand from the deck of cards

    community_cards = [deck_of_cards.pop(), deck_of_cards.pop(), deck_of_cards.pop()]   #pops three cards from deck for community cards
    return community_cards                                                              #returns the community cards


def deal_opponents_cards(my_cards, community_cards):
    
    deck_of_cards = full_deck()                                                 #creates a deck of cards using full_deck()
    
    for card in my_cards:                                                       #iterates through my cards
        deck_of_cards.remove(card)                                              #removes cards in my hand from the deck of cards

    for card in community_cards:                                                #iterates through community cards
        deck_of_cards.remove(card)                                              #removes community cards from the deck of cards

    opponents_cards = [deck_of_cards.pop(), deck_of_cards.pop()]                #pops two cards from deck for opponent's hand
    return opponents_cards                                                      #returns opponent's cards


def rank_hand(five_card_hand):

    card_rank = {'2':1,'3':2,'4':3,'5':4,'6':5,'7':6,'8':7,'9':8,'10':9,        #hashmap to assign values to cards
                 'J':10,'Q':11,'K':12,'A':13}
    
    card_number_list = []                                                       #empty list to store card numbers
    suit_list = []                                                              #empty list to store card suits

    for card in five_card_hand:                                                 #iterates through five card hand
        rank = card[:-1]                                                        #stores the card rank
        card_number_list.append(rank)                                           #appends card rank to card rank list
        suit = card[-1]                                                         #stores the card suit
        suit_list.append(suit)                                                  #appends card suit to suit list

    rank_counts = {}                                                            #empty dictionary to store rank frequencies

    for rank in card_number_list:                                               #iterates through list of cards in hand
        if rank in rank_counts:                                                 #checks if rank already exists in rank_counts
            rank_counts[rank] += 1                                              #increments the rank count by one
        else:                                                                   #handles ranks not already in rank_counts
            rank_counts[rank] = 1                                               #creates the rank key and assigns it a count of one

    unique_ranks = []                                                           #empty list to store unique ranks

    for rank in rank_counts:                                                    #iterates through rank count dictionary
        unique_ranks.append(rank)                                               #appends rank to unique ranks list                                                 

    def sort_key(rank):                                                         #helper function that sorts keys
        return (rank_counts[rank], card_rank[rank])                             #returns tuple(frequency, card rank)
    
    unique_ranks.sort(key=sort_key, reverse=True)                               #sorts unique_ranks by frequency, then card rank from highest to lowest

    flush = True                                                                #sets flush to True
    first_suit = suit_list[0]                                                   #sets first suit to suit of first card

    for suit in suit_list:                                                      #iterates through suit_list   
        if suit != first_suit:                                                  #checks if suit does not match first suit
            flush = False                                                       #sets flush to False
            break                                                               #breaks out of loop

    card_numbers = []                                                           #creates empty list to store card numbers                                                

    for rank in card_number_list:                                               #iterates through card_number_list
        card_numbers.append(card_rank[rank])                                    #appends card rank value to card_numbers list

    unique_values = []                                                          #creates empty list to store unique card numbers

    for values in card_numbers:                                                 #iterates through card_numbers list
        if values not in unique_values:                                         #checks if card number is not already in unique_values
            unique_values.append(values)                                        #appends card number to unique_values list

    unique_values.sort()                                                        #sorts unique_values from low to high

    straight = False                                                            #sets straight to False
    high_card = None                                                            #creates variable to store high card and sets it to None

    if len(unique_values) == 5:                                                 #determines if five unique cards are in hand
        if unique_values[-1] - unique_values[0] == 4:                           #checks if highest and lowest values are four apart
            straight = True                                                     #sets straight to True
            high_card = unique_values[-1]                                       #stores highest value as the straight high card
        elif unique_values == [1, 2, 3, 4, 13]:                                 #checks for special straight with a low Ace
            straight = True                                                     #sets straight to True
            high_card = card_rank['5']                                          #sets high card to 5, not Ace

    if flush and straight:                                                      #checks if the hand is both a flush and a straight
        if high_card == 13:                                                     #checks if the straight flush has an Ace high card
            return (9, None)                                                    #returns hand value as 9 for royal flush
        else:                                                                   #handles non-royal straight flushes
            return (8, high_card)                                               #returns hand value as 8 and the straight high card

    for rank in unique_ranks:                                                   #iterates over unique_ranks list
        if rank_counts[rank] == 4:                                              #checks if rank appears four times
            for different_card in unique_ranks:                                 #iterates over ranks to find the non-paired card
                if different_card != rank:                                      #checks if current rank is not the four-of-a-kind rank
                    kicker = card_rank[different_card]                          #sets different card to the kicker
                    break                                                       #breaks out of loop

            return (7, card_rank[rank], kicker)                                 #returns hand value as 7, four-of-a-kind strength, and kicker

    three_of_a_kind = None                                                      #sets three_of_a_kind to None
    two_pair = None                                                             #sets two_pair to None

    for rank in unique_ranks:                                                   #iterates through unique_ranks
        if rank_counts[rank] == 3:                                              #checks if rank appears three times
            three_of_a_kind = rank                                              #stores the three-of-a-kind rank
        elif rank_counts[rank] == 2:                                            #checks if rank appears two times
            two_pair = rank                                                     #stores the pair rank

    if three_of_a_kind != None and two_pair != None:                            #checks if three-of-a-kind and pair both exist
        return (6, card_rank[three_of_a_kind], card_rank[two_pair])             #returns hand value as 6 and the full-house ranks

    if flush:                                                                   #determines if hand is a flush
        flush_values = []                                                       #empty list to store flush values

        for rank in card_number_list:                                           #iterates through card ranks
            flush_values.append(card_rank[rank])                                #appends card rank values to flush_values list

        flush_values.sort(reverse=True)                                         #sorts flush_values from highest to lowest
        return tuple([5] + flush_values)                                        #returns hand value as 5, followed by flush_values

    if straight:                                                                #determines if hand is a straight
        return (4, high_card)                                                   #returns hand value as 4 and highest card of straight
   
    if three_of_a_kind:                                                         #determines if hand is a three-of-a-kind
        kickers = []                                                            #empty list to store kickers

        for rank in unique_ranks:                                               #iterates through unique_ranks list
            if rank != three_of_a_kind:                                         #checks if card is not part of the three-of-a-kind
                kickers.append(card_rank[rank])                                 #appends card value to kickers list

        kickers.sort(reverse=True)                                              #sorts kickers list from highest to lowest
        return (3, card_rank[three_of_a_kind], kickers[0], kickers[1])          #returns hand value as 3, the three-of-a-kind, and two kickers

    pairs = []                                                                  #creates list to store pairs

    for rank in unique_ranks:                                                   #iterates through unique_ranks
        if rank_counts[rank] == 2:                                              #checks if rank count is two
            pairs.append(rank)                                                  #appends pair rank to pairs list
    
    if len(pairs) == 2:                                                         #determines if two pairs are in hand
        if card_rank[pairs[0]] < card_rank[pairs[1]]:                           #checks if the second pair is stronger than the first pair
            pairs[0], pairs[1] = pairs[1], pairs[0]                             #swaps pairs so the higher pair comes first

        for rank in unique_ranks:                                               #iterates through unique_ranks
            if rank not in pairs:                                               #finds the card not part of either pair
                kicker = card_rank[rank]                                        #sets that card as the kicker
                break                                                           #breaks from loop

        return (2, card_rank[pairs[0]], card_rank[pairs[1]], kicker)            #returns hand value as 2, the two pairs, and the kicker

    if len(pairs) == 1:                                                         #determines if one pair is in hand
        pair_cards = pairs[0]                                                   #stores pair rank
        kickers = []                                                            #creates list to store kickers

        for rank in unique_ranks:                                               #iterates through unique_ranks
            if rank != pair_cards:                                              #checks if rank is not the pair rank
                kickers.append(card_rank[rank])                                 #appends card value to kickers list

        kickers.sort(reverse=True)                                              #sorts kickers list from highest to lowest
        return (1, card_rank[pair_cards], kickers[0], kickers[1], kickers[2])   #returns hand value as 1, the pair, and the remaining kickers

    high_cards = []                                                             #creates list to determine high card

    for rank in unique_ranks:                                                   #iterates through unique_ranks
        high_cards.append(card_rank[rank])                                      #appends card value to high_cards list

    high_cards.sort(reverse=True)                                                           #sorts high_cards list from highest to lowest
    return (0, high_cards[0], high_cards[1], high_cards[2], high_cards[3], high_cards[4])   #returns hand value as 0 and the list of high cards
    

def evaluate_best_hand(seven_cards):

    current_best_combo_value = (-1, None)                                       #sets best combo to value of -1

    for combo in itertools.combinations(seven_cards, 5):                        #iterates over potential 5-card combos from the available cards
        rank = rank_hand(list(combo))                                           #ranks each combo using rank_hand() function

        if rank > current_best_combo_value:                                     #checks if the current combo is better than the current best combo
            current_best_combo_value = rank                                     #replaces current best combo with better combo

    return current_best_combo_value                                             #returns best combo value


def monte_carlo_search_tree(my_cards, community_cards, player_count, time_limit=10.0):

    number_of_opponents = player_count - 1                                      #calculates how many opponents are at the table

    deck_of_cards = full_deck()                                                 #creates full deck of cards

    for card in my_cards + community_cards:                                     #iterates through my cards and community cards
        deck_of_cards.remove(card)                                              #removes known cards from the deck

    total_rollouts = 0                                                          #sets number of rollouts to zero
    total_wins = 0.0                                                            #sets total wins to zero
    start = time.time()                                                         #sets timer

    while time.time() - start < time_limit:                                     #runs simulations until the time limit is reached

        deck_copy = deck_of_cards.copy()                                        #makes a copy of the remaining unknown deck
        random.shuffle(deck_copy)                                               #shuffles the copied deck for this rollout

        opponents_cards = []                                                    #creates a list to store each opponent's two-card hand

        for opponent in range(number_of_opponents):                             #loops once for each opponent at the table
            opponent_hand = [deck_copy.pop(), deck_copy.pop()]                  #deals two cards to the current opponent
            opponents_cards.append(opponent_hand)                               #adds the opponent hand to the opponents list

        community_cards_copy = community_cards.copy()                           #makes a copy of the currently known community cards

        for table_cards in range(5 - len(community_cards_copy)):                #determines how many unknown community cards still need to be dealt
            community_cards_copy.append(deck_copy.pop())                        #deals one unknown community card from the copied deck

        my_hand = evaluate_best_hand(my_cards + community_cards_copy)           #determines the value of my best possible hand

        opponents_best_hands = []                                               #creates a list to store each opponent's best hand

        for opponent_hand in opponents_cards:                                               #loops through each opponent hand
            opponent_best_hand = evaluate_best_hand(opponent_hand + community_cards_copy)   #determines the opponent's best possible hand
            opponents_best_hands.append(opponent_best_hand)                                 #adds the opponent's best hand to the list

        best_opponent_hand = max(opponents_best_hands)                          #finds the strongest opponent hand at the table

        if my_hand > best_opponent_hand:                                        #checks if my hand beats every opponent hand
            result = 1.0                                                        #counts the rollout as a full win
        elif my_hand == best_opponent_hand:                                     #checks if my hand ties the strongest opponent hand
            result = 0.5                                                        #counts the rollout as a half win
        else:                                                                   #handles the case where at least one opponent beats my hand
            result = 0.0                                                        #counts the rollout as a loss

        total_wins += result                                                    #adds the rollout result to total wins
        total_rollouts += 1                                                     #increments the rollout count

    win_probability = total_wins / total_rollouts                               #calculates estimated win probability across all rollouts

    if win_probability >= 0.5:                                                  #checks if estimated win probability is at least 50 percent
        decision = "stay"                                                       #recommends staying in the hand
    else:                                                                       #handles estimated win probability below 50 percent
        decision = "fold"                                                       #recommends folding the hand

    return decision, win_probability, total_rollouts                            #returns the decision, probability, and rollout count


def print_current_odds(my_cards, community_cards, player_count, time_limit=3.0):

    decision, win_probability, total_rollouts = monte_carlo_search_tree(        #runs the simulation using the known cards and player count
        my_cards=my_cards,                                                      #passes my current hand
        community_cards=community_cards,                                        #passes the currently known community cards
        player_count=player_count,                                              #passes the total number of players at the table
        time_limit=time_limit                                                   #passes the amount of time allowed for simulation
    )

    win_percentage = win_probability * 100                                      #converts the win probability into a percentage
    number_of_opponents = player_count - 1                                      #calculates how many opponents are at the table

    if len(community_cards) == 3:                                               #checks if only the flop has been entered
        street = "Flop"                                                         #stores the current poker street as flop
    elif len(community_cards) == 4:                                             #checks if the turn has been entered
        street = "Turn"                                                         #stores the current poker street as turn
    elif len(community_cards) == 5:                                             #checks if the river has been entered
        street = "River"                                                        #stores the current poker street as river
    else:                                                                       #handles any unexpected number of community cards
        street = "Current Hand"                                                 #stores a generic street name

    print()                                                                     #prints a blank line for readability
    print("=" * 56)                                                             #prints the top border of the results section
    print(f"{street.upper()} ODDS UPDATE")                                      #prints the current street title
    print("=" * 56)                                                             #prints the bottom border of the title section

    print(f"Players at Table:      {player_count}")                             #prints the total number of players at the table
    print(f"Opponents Remaining:   {number_of_opponents}")                      #prints the number of opponents being simulated against
    print(f"My Hand:               {my_cards[0]}  {my_cards[1]}")               #prints my two hole cards
    print(f"Community Cards:       {'  '.join(community_cards)}")               #prints the known community cards
    print("-" * 56)                                                             #prints a separator line

    print(f"Win Probability:       {win_percentage:.2f}%")                      #prints the estimated win probability as a percentage
    print(f"Decimal Probability:   {win_probability:.4f}")                      #prints the estimated win probability as a decimal
    print(f"Simulations Run:       {total_rollouts}")                           #prints the number of completed simulations
    print(f"Suggested Move:        {decision.upper()}")                         #prints the suggested decision in uppercase

    print("=" * 56)                                                             #prints the closing border of the results section
    print()                                                                     #prints a blank line for readability


def run_interactive_game():

    used_cards = []                                                             #creates a list to track cards that have already been entered
    my_cards = []                                                               #creates a list to store my two hole cards
    community_cards = []                                                        #creates a list to store the community cards

    print("Enter cards using format like AS, 10H, 7D, or QC.")                  #prints card input instructions
    print("S = spades, C = clubs, H = hearts, D = diamonds")                    #prints suit input instructions
    print()                                                                     #prints a blank line for readability

    player_count = get_player_count_from_user()                                 #gets the total number of players at the table including me

    print()                                                                     #prints a blank line for readability

    my_cards.append(get_unique_card_from_user("Enter your first card: ", used_cards))       #gets my first hole card
    my_cards.append(get_unique_card_from_user("Enter your second card: ", used_cards))      #gets my second hole card

    community_cards.append(get_unique_card_from_user("Enter flop card 1: ", used_cards))    #gets the first flop card
    community_cards.append(get_unique_card_from_user("Enter flop card 2: ", used_cards))    #gets the second flop card
    community_cards.append(get_unique_card_from_user("Enter flop card 3: ", used_cards))    #gets the third flop card

    print_current_odds(my_cards, community_cards, player_count, time_limit=3.0)             #prints updated odds after the flop

    turn_card = get_unique_card_from_user("Enter turn card: ", used_cards)                  #gets the turn card
    community_cards.append(turn_card)                                                       #adds the turn card to the community cards

    print_current_odds(my_cards, community_cards, player_count, time_limit=3.0)             #prints updated odds after the turn
    river_card = get_unique_card_from_user("Enter river card: ", used_cards)                #gets the river card
    community_cards.append(river_card)                                                      #adds the river card to the community cards

    print_current_odds(my_cards, community_cards, player_count, time_limit=3.0)             #prints updated odds after the river
 

if __name__ == "__main__":                                                      #checks if this script is being run directly
    run_interactive_game()                                                      #runs the interactive poker odds tool

