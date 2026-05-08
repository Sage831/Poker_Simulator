import random                                                                   #simulate shuffling deck and hands
import time                                                                     #enforce 10 second limit
import math                                                                     #for Upper Confidence Bound 1 (UCB1)
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

    valid_ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']         #creates a list of valid card ranks
    valid_suits = ['\u2660','\u2663','\u2665','\u2666']                          #creates a list of valid card suits

    if rank not in valid_ranks:                                                 #checks if the rank is invalid
        return None                                                             #returns None for invalid input

    if suit not in valid_suits:                                                 #checks if the suit is invalid
        return None                                                             #returns None for invalid input

    return rank + suit                                                          #returns the normalized card using the same format as the rest of the program


def get_card_from_user(prompt):

    card = None                                                                 #creates a variable to store the validated card

    while card is None:                                                         #loops until the user enters a valid card
        card_input = input(prompt)                                               #gets the raw card input from the user
        card = normalize_card_input(card_input)                                  #normalizes and validates the card input

        if card is None:                                                        #checks if the user entered an invalid card
            print("Invalid card. Use format like AS, 10H, 7D, or QC.")           #prints an explanation of the expected card format

    return card                                                                 #returns the valid normalized card


def get_unique_card_from_user(prompt, used_cards):

    card = get_card_from_user(prompt)                                           #gets a valid card from the user

    while card in used_cards:                                                   #checks if the card was already entered
        print("That card has already been used. Enter a different card.")        #prints a duplicate-card warning
        card = get_card_from_user(prompt)                                       #asks the user for another valid card

    used_cards.append(card)                                                     #adds the card to the used-cards list
    return card                                                                 #returns the unique card


def deal_my_cards():

    deck_of_cards = full_deck()                                                 #creates a deck of cards using full_deck()
    my_cards = [deck_of_cards.pop(), deck_of_cards.pop()]                       #pops two cards from deck for my hand
    return my_cards                                                             #returns my cards


def deal_community_cards(my_cards):

    deck_of_cards = full_deck()                                                 #creates a deck of cards using full_deck()
    
    for card in my_cards:                                                       #iterates through my cards
        deck_of_cards.remove(card)                                              #removes cards in my hand from the deck of cards

    community_cards = [deck_of_cards.pop(), deck_of_cards.pop(),deck_of_cards.pop()]                #pops three cards from deck for community cards
    return community_cards                                                                          #returns the community cards


def deal_opponents_cards(my_cards, community_cards):
    
    deck_of_cards = full_deck()                                                 #creates a deck of cards using full_deck()
    
    for card in my_cards:                                                       #iterates through my cards
        deck_of_cards.remove(card)                                              #removes cards in my hand from the deck of cards

    for card in community_cards:                                                #iterates through community cards
        deck_of_cards.remove(card)                                              #removes community cards from the deck of cards

    opponents_cards = [deck_of_cards.pop(), deck_of_cards.pop()]                #pops two cards from deck for my hand
    return opponents_cards                                                      #returns oppenent's cards


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

    rank_counts = {}                                                            #empty dictionary to store pairs
    for rank in card_number_list:                                               #iterates through list of cards in hand
        if rank in rank_counts:                                                 #if card already in rank_count, increment by 1
            rank_counts[rank] += 1
        else:                                                                   #if not in rank_count, create key and assign value of 1
            rank_counts[rank] = 1    

    unique_ranks = []                                                           #empty list to store unique ranks
    for rank in rank_counts:                                                    #iterates through rank count dictionary
        unique_ranks.append(rank)                                               #appends rank to unique ranks list                                                 

    def sort_key(rank):                                                         #helper function that sorts keys
        return (rank_counts[rank], card_rank[rank])                             #returns tuple(frequency, card rank)
    
    unique_ranks.sort(key=sort_key, reverse=True)                               #sorts unique_rank base on frequency, then card rank; reverse to sort highest to lowest

    flush = True                                                                #sets flush to True
    first_suit = suit_list[0]                                                   #sets first suit to suit of first card
    for suit in suit_list:                                                      #iterates through suit_list   
        if suit != first_suit:                                                  #if suit doesn't match first suit, set flush to False
            flush = False
            break                                                               #break out of loop

    card_numbers = []                                                           #create empty list to store card numbers                                                
    for rank in card_number_list:                                               #iterates throught card_rank_list list 
        card_numbers.append(card_rank[rank])                                    #appends card rank to card_numbers list

    unique_values = []                                                          #create empty list to store unique card numbers
    for values in card_numbers:                                                 #iterates through card_numbers list
        if values not in unique_values:                                         #if card number not in list, appends card to unique_values list
            unique_values.append(values)
    unique_values.sort()                                                        #sorts unique_values

    straight = False                                                            #sets straight to False
    high_card = None                                                            #create variable to store high card and set to None
    if len(unique_values) == 5:                                                 #determines if 5 unique cards are in hand
        if unique_values[-1] - unique_values[0] == 4:                           
            straight = True                                                     #sets straight to True
            high_card = unique_values[-1]                                       #stores last (highest) value to high card
        elif unique_values == [1, 2, 3, 4, 13]:                                 #special straight with a low Ace
            straight = True                                                     #sets straight to True
            high_card = card_rank['5']                                          #sets high card to 5, not Ace

    if flush and straight:
        if high_card == 13:                                                     #royal flush if high card is Ace
            return (9, None)                                                    #returns hand value as 9
        else:
            return (8, high_card)                                               #returns hand value as 8

    for rank in unique_ranks:                                                   #iterates over unique_ranks list
        if rank_counts[rank] == 4:                                              #checks if 4-way pair in hand
            for different_card in unique_ranks:                                 #iterates over cards to find the non-paired card
                if different_card != rank:
                    kicker = card_rank[different_card]                          #sets different card to the kicker
                    break                                                       #break out of loop
            return (7, card_rank[rank], kicker)                                 #returns hand value as 7, the strength of 4-of-a-kind, and the kicker

    three_of_a_kind = None                                                      #set three_of_a_kind to None
    two_pair = None                                                             #set two_pair to None
    for rank in unique_ranks:                                                   #iterates through unique_ranks
        if rank_counts[rank] == 3:                                              #if rank_count is 3, stores 3-of-a-kind
            three_of_a_kind = rank
        elif rank_counts[rank] == 2:                                            #if rank_count is 2, stores 2-pair
            two_pair = rank
    if three_of_a_kind != None and two_pair != None:                            #checks if 3-of-a-kind and 2-pair exist in hand                                        
        return (6, card_rank[three_of_a_kind], card_rank[two_pair])             #returns hand value as 6 and the strength of the 3-of-a-kind and 2-pair

    if flush:                                                                   #determines if hand is a flush
        flush_values = []                                                       #empty list to store flush values
        for rank in card_number_list:                                           #iterates through card numbers
            flush_values.append(card_rank[rank])                                #appends card numbers to flush_values list
        flush_values.sort(reverse=True)                                         #sorts flush_values and reverses to have highest number first
        return tuple([5] + flush_values)                                        #returns hand value as 5, followed by flush_values

    if straight:                                                                #determines if hand is a straight
        return (4, high_card)                                                   #returns hand value as 4 and highest card of straight
   
    if three_of_a_kind:                                                         #determines if hand is a 3-of-a-kind
        kickers = []                                                            #empty list to store kickers
        for rank in unique_ranks:                                               #iterates through unique_ranks list
            if rank != three_of_a_kind:                                         #if card not part of 3-of-a-kind, append it to kickers list
                kickers.append(card_rank[rank])
        kickers.sort(reverse=True)                                              #sorts kickers list and reverse to have highest kicker first
        return (3, card_rank[three_of_a_kind], kickers[0], kickers[1])          #returns hand value as 3, the 3-of-a-kind, and the two kickers

    pairs = []                                                                  #list to store pairs
    for rank in unique_ranks:                                                   #iterates through unique_ranks
        if rank_counts[rank] == 2:                                              #if rank count is two, its a pair
            pairs.append(rank)                                                  #appends pair to pairs list
    
    if len(pairs) == 2:                                                         #determines if 2 pairs in hand
        if card_rank[pairs[0]] < card_rank[pairs[1]]:                           #sorts pairs to have highest pair first
            pairs[0], pairs[1] = pairs[1], pairs[0]
        for rank in unique_ranks:                                               #iterates through unique_ranks
            if rank not in pairs:                                               #finds card not in pair
                kicker = card_rank[rank]                                        #sets that card as the kicker
                break                                                           #breaks from loop
        return (2, card_rank[pairs[0]], card_rank[pairs[1]], kicker)            #returns hand value as 2, the two pairs, and the kicker

    if len(pairs) == 1:                                                         #determines if 1 pair in hand
        pair_cards = pairs[0]                                                   #stores pair
        kickers = []                                                            #list to store kickers
        for rank in unique_ranks:                                               #iterates through unique_ranks
            if rank != pair_cards:                                              #finds cards not in pair
                kickers.append(card_rank[rank])                                 #appends card to kickers list
        kickers.sort(reverse=True)                                              #sorts kickers list and reverse to have highest kicker first
        return (1, card_rank[pair_cards], kickers[0], kickers[1], kickers[2])   #returns hand value as 1, the pair, and the remaining kickers

    high_cards = []                                                                                 #list to determine high card
    for rank in unique_ranks:                                                                       #iterates through unique_ranks
        high_cards.append(card_rank[rank])                                                          #appends card to high_card list
    high_cards.sort(reverse=True)                                                                   #sorts high_cards list and reverse to have highest kicker first
    return (0, high_cards[0], high_cards[1], high_cards[2], high_cards[3], high_cards[4])           #returns hand value as 0 and the list of high cards
    

def evaluate_best_hand(seven_cards):

    current_best_combo_value = (-1, None)                                       #sets best combo to value of -1
    for combo in itertools.combinations(seven_cards, 5):                        #iterates over potential combos of the 7 available cards using itertools import
        rank = rank_hand(list(combo))                                           #ranks each combo using rank_hand() function
        if rank > current_best_combo_value:                                     #if better combo occurs, replace current combo with better combo                                                   
            current_best_combo_value = rank
    return current_best_combo_value                                             #returns best combo


def UCB1(wins, rounds, total_simulations, c):
    
    if rounds == 0:                                                             #determines if any rounds have been played
        return float('inf')                                                     #forces exploration

    exploitation = wins / rounds                                                #calculates exploitation
    exploration = math.sqrt(math.log(total_simulations) / rounds)               #calculates exploration using math import
    return exploitation + c * exploration                                       #returns UCB1 equation                                     


def monte_carlo_search_tree(my_cards, community_cards, c=math.sqrt(2), time_limit=10.0):

    deck_of_cards = full_deck()                                                 #creates full deck of cards
    for card in my_cards + community_cards:                                     #iterates through my cards and community cards
        deck_of_cards.remove(card)                                              #removes those cards from the deck

    possible_opponent_hands = list(itertools.combinations(deck_of_cards, 2))    #uses itertools to iterate through all possible hands in opponent's hand

    stats = {}                                                                  #dictionary to track stats
    for hand in possible_opponent_hands:                                        #iterates through possible opponent hands
        stats[hand] = [0.0, 0]                                                  #tracks wins and visits

    total_rollouts = 0                                                          #sets number of rollouts to 0
    start = time.time()                                                         #sets timer

    while time.time() - start < time_limit:                                     #while time limit hasn't been reached
        opponents_best_hand = None                                              #sets best_hand to None
        best_score = -float('inf')                                              #sets best_score to negative infinity
        for hand, (wins, visits) in stats.items():                              #iterates through all possible opponent hands to find highest UCB1 score
            current_score = UCB1(wins, visits, total_rollouts, c)               #calculates scores with UCB1() function
            if current_score > best_score:                                      #if current score better, set best score to current score
                best_score, opponents_best_hand = current_score, hand           #tuple unpacking

        deck_copy = deck_of_cards.copy()                                        #make copy of deck of cards
        
        for card in opponents_best_hand:                                        #iterates through opponent's hand      
            deck_copy.remove(card)                                              #removes opponent's cards from deck copy

        random.shuffle(deck_copy)                                               #shuffles the remaining unknown cards before dealing future community cards

        community_cards_copy = community_cards.copy()                           #makes copy of community cards
        for table_cards in range(5 - len(community_cards_copy)):                #determines remaining community cards to deal
            community_cards_copy.append(deck_copy.pop())                        #pops card from deck copy and appends to community cards copy

        my_hand = evaluate_best_hand(my_cards + community_cards_copy)                                       #determines value of my hand
        opponents_hand = evaluate_best_hand(list(opponents_best_hand) + community_cards_copy)               #determines value of opponent's hand
        if my_hand > opponents_hand:                                                                        #if my hand is better, result = 1.0
            result = 1.0
        elif my_hand == opponents_hand:                                                                     #if the hands tie, result = 0.5
            result = 0.5
        else:                                                                                               #if opponent's hand is better, result = 0.0
            result = 0.0

        stats[opponents_best_hand][1] += 1                                      #increments visit count for hand
        stats[opponents_best_hand][0] += result                                 #add result to win calculation
        total_rollouts += 1                                                     #increment rollout

    total_wins = 0.0                                                            #sets total_wins to 0
    for wins, visits in stats.values():                                         #iterates over stats dictionary
        total_wins += wins                                                      #adds wins to total_wins

    total_visits = 0                                                            #sets total_visits to 0
    for wins, visits in stats.values():                                         #iterates over stats dictionary
        total_visits += visits                                                  #adds visits to total_visits

    win_probability = total_wins / total_visits                                 #calculates win probability
    if win_probability >= 0.5:                                                  #if win_probability greater than 0.5, play out the hand
        decision = "stay"  
    else:                                                                       #if win_probability less than than 0.5, fold
        decision = "fold"
    return decision, win_probability, total_rollouts


def print_current_odds(my_cards, community_cards, time_limit=3.0):

    decision, win_probability, total_rollouts = monte_carlo_search_tree(         #runs the simulation using the known cards
        my_cards=my_cards,                                                       #passes my current hand
        community_cards=community_cards,                                         #passes the currently known community cards
        time_limit=time_limit                                                    #passes the amount of time allowed for simulation
    )

    win_percentage = win_probability * 100                                       #converts the win probability into a percentage

    if len(community_cards) == 3:                                                #checks if only the flop has been entered
        street = "Flop"                                                          #stores the current poker street as flop
    elif len(community_cards) == 4:                                              #checks if the turn has been entered
        street = "Turn"                                                          #stores the current poker street as turn
    elif len(community_cards) == 5:                                              #checks if the river has been entered
        street = "River"                                                         #stores the current poker street as river
    else:                                                                        #handles any unexpected number of community cards
        street = "Current Hand"                                                  #stores a generic street name

    print()                                                                      #prints a blank line for readability
    print("=" * 50)                                                              #prints the top border of the results section
    print(f"{street.upper()} ODDS UPDATE")                                       #prints the current street title
    print("=" * 50)                                                              #prints the bottom border of the title section

    print(f"My Hand:           {my_cards[0]}  {my_cards[1]}")                    #prints my two hole cards
    print(f"Community Cards:   {'  '.join(community_cards)}")                    #prints the known community cards
    print("-" * 50)                                                              #prints a separator line

    print(f"Win Probability:   {win_percentage:.2f}%")                           #prints the estimated win probability as a percentage
    print(f"Decimal Odds:      {win_probability:.4f}")                           #prints the estimated win probability as a decimal
    print(f"Simulations Run:   {total_rollouts}")                                #prints the number of completed simulations
    print(f"Suggested Move:    {decision.upper()}")                              #prints the suggested decision in uppercase

    print("=" * 50)                                                              #prints the closing border of the results section
    print()                                                                      #prints a blank line for readability


def run_interactive_game():

    used_cards = []                                                              #creates a list to track cards that have already been entered
    my_cards = []                                                                #creates a list to store my two hole cards
    community_cards = []                                                         #creates a list to store the community cards

    print("Enter cards using format like AS, 10H, 7D, or QC.")                   #prints card input instructions
    print("S = spades, C = clubs, H = hearts, D = diamonds")                     #prints suit input instructions
    print()                                                                      #prints a blank line for readability

    my_cards.append(get_unique_card_from_user("Enter your first card: ", used_cards))      #gets my first hole card
    my_cards.append(get_unique_card_from_user("Enter your second card: ", used_cards))     #gets my second hole card

    community_cards.append(get_unique_card_from_user("Enter flop card 1: ", used_cards))   #gets the first flop card
    community_cards.append(get_unique_card_from_user("Enter flop card 2: ", used_cards))   #gets the second flop card
    community_cards.append(get_unique_card_from_user("Enter flop card 3: ", used_cards))   #gets the third flop card

    print_current_odds(my_cards, community_cards, time_limit=3.0)                #prints updated odds after the flop

    turn_card = get_unique_card_from_user("Enter turn card: ", used_cards)       #gets the turn card
    community_cards.append(turn_card)                                            #adds the turn card to the community cards

    print_current_odds(my_cards, community_cards, time_limit=3.0)                #prints updated odds after the turn

    river_card = get_unique_card_from_user("Enter river card: ", used_cards)     #gets the river card
    community_cards.append(river_card)                                           #adds the river card to the community cards

    print_current_odds(my_cards, community_cards, time_limit=3.0)                #prints updated odds after the river
    

if __name__ == "__main__":
    run_interactive_game()

