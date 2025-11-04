import random
from collections import Counter
from src.constants import (
    BOARD_SIZE, ROWS, COLS, CENTER, RACK_SIZE, LETTER_SCORES,
    TRIPLE_WORD, DOUBLE_WORD, TRIPLE_LETTER, DOUBLE_LETTER
)
import src.move_evaluator as evaluator

class TileGuesserGame:
    def __init__(self, player1, player2, dictionary, tile_bag_template, letter_scores, rack_size, silent=False):
        self.silent = silent
        self.log(f"Initializing Game (RACK_SIZE = {rack_size})")
        self.board = {r + c: 0 for r in ROWS for c in COLS}
        self.bag = tile_bag_template.copy()
        random.shuffle(self.bag)
        
        self.valid_dictionary = dictionary
        self.letter_scores = letter_scores
        self.rack_size = rack_size
        
        self.players = {
            player1.name: player1,
            player2.name: player2
        }
        self.racks = {
            player1.name: [],
            player2.name: []
        }
        self.scores = {
            player1.name: 0,
            player2.name: 0
        }
        
        self.current_player_name = player1.name
        self.game_over = False
        self.pass_count = 0
        
        self.letter_index = {}
        for word in self.valid_dictionary:
            for l in set(word):
                self.letter_index.setdefault(l, set()).add(word)
        self.log("Game initialized. Dictionary loaded.")
        self.log(f"Bag has {len(self.bag)} tiles.")
        self.log(f"Center tile is: {CENTER}")

    def log(self, message):
        if not self.silent:
            print(message)

    def draw_tiles(self, player_name, num=1):
        rack = self.racks[player_name]
        if len(rack) >= self.rack_size:
            self.log(f"{player_name} tries to draw (pass), but rack is already full!")
            return 0
        draw_count = 0
        for _ in range(num):
            if not self.bag:
                self.log(f"{player_name} tries to draw, but bag is empty.")
                break
            if len(rack) >= self.rack_size:
                self.log(f"{player_name} rack became full while drawing.")
                break
            tile = self.bag.pop()
            rack.append(tile)
            draw_count += 1
        self.log(f"{player_name} drew {draw_count} tiles (as a PASS). New rack: {self.racks[player_name]}")
        return draw_count

    def draw_to_fill(self, player_name):
        rack = self.racks[player_name]
        num_to_draw = self.rack_size - len(rack)
        if num_to_draw <= 0:
            return 0
        draw_count = 0
        for _ in range(num_to_draw):
            if not self.bag:
                self.log(f"{player_name} tries to refill, but bag is empty.")
                break
            tile = self.bag.pop()
            rack.append(tile)
            draw_count += 1
        if draw_count > 0:
            self.log(f"{player_name} drew {draw_count} tiles to refill. New rack: {self.racks[player_name]}")
        return draw_count

    def exchange_tiles(self, player_name, tiles_to_exchange):
        rack = self.racks[player_name]
        num_to_exchange = len(tiles_to_exchange)
        if num_to_exchange == 0:
            self.log(f"{player_name} wanted to exchange, but had no tiles to swap.")
            return 0
        if num_to_exchange > len(self.bag):
            self.log(f"{player_name} cannot exchange {num_to_exchange} tiles, bag only has {len(self.bag)}.")
            return 0
        self.log(f"{player_name} will EXCHANGE {num_to_exchange} tiles: {tiles_to_exchange}")
        temp_rack = rack.copy()
        for tile in tiles_to_exchange:
            if tile in temp_rack:
                temp_rack.remove(tile)
            elif '_' in temp_rack:
                temp_rack.remove('_')
            else:
                self.log(f"ERROR: Tried to exchange '{tile}' but not in rack {rack}")
        self.racks[player_name] = temp_rack
        for tile in tiles_to_exchange:
            self.bag.append(tile)
            new_tile = self.bag.pop(0)
            self.racks[player_name].append(new_tile)
        random.shuffle(self.bag)
        self.log(f"{player_name} drew {num_to_exchange} new tiles. New rack: {self.racks[player_name]}")
        return num_to_exchange

    def print_board(self):
        if self.silent:
            return
        print("\n    " + " ".join(COLS))
        for r in ROWS:
            row_str = r + "   "
            for c in COLS:
                val = self.board[r + c]
                coord = r + c
                if val == 0:
                    if coord in TRIPLE_WORD: row_str += "T "
                    elif coord in DOUBLE_WORD: row_str += "D "
                    elif coord in TRIPLE_LETTER: row_str += "t "
                    elif coord in DOUBLE_LETTER: row_str += "d "
                    else: row_str += ". "
                else:
                    row_str += val.upper() + " "
            print(row_str)
        print("-" * (BOARD_SIZE * 2 + 5))

    def switch_player(self):
        players = list(self.players.keys())
        current_index = players.index(self.current_player_name)
        self.current_player_name = players[1 - current_index]

    def take_turn(self):
        player_name = self.current_player_name
        player_obj = self.players[player_name]
        rack = self.racks[player_name]
        
        self.log(f"\n--- {player_name}'s Turn ---")
        self.log(f"Rack: {rack} (Size: {len(rack)})")
        self.log(f"Bag: {len(self.bag)} tiles left")
        self.log(f"Current Score: {self.scores[player_name]}")

        playable_goals, future_goals = evaluator.analyze_all_moves(
            self.board,
            self.bag,
            rack,
            self.letter_index,
            self.valid_dictionary,
            self.letter_scores,
            self.rack_size
        )

        chosen_goal = player_obj.choose_move(playable_goals, future_goals, len(self.bag), self.log)

        if chosen_goal:
            if chosen_goal['prob'] == 1.0:
                self.log(f"{player_name} will PLAY the word '{chosen_goal['word']}'")
                
                for tile, coord in chosen_goal['all_move_tiles']:
                    if tile in rack: rack.remove(tile)
                    elif '_' in rack: rack.remove('_')
                    else: 
                        self.log(f"!! {player_name} RACK ERROR: Tried to play '{tile}' but not in {rack} !!")
                        self.game_over = True; return
                    self.board[coord] = tile
                
                self.pass_count = 0
                score_for_turn = chosen_goal['score']
                completed_words_str = {w for w, s, o in chosen_goal['all_formed_words']}

                if score_for_turn > 0:
                    self.log(f"{player_name} completed: {completed_words_str}. +{score_for_turn} points!")
                    self.scores[player_name] += score_for_turn

                self.draw_to_fill(player_name)
            
            else:
                tiles_to_keep_counter = Counter(chosen_goal['tiles_to_keep'])
                rack_counter = Counter(rack)
                tiles_to_exchange = []
                for tile, count in rack_counter.items():
                    if tiles_to_keep_counter[tile] > 0:
                        num_to_exchange = count - tiles_to_keep_counter[tile]
                        if num_to_exchange > 0: tiles_to_exchange.extend([tile] * num_to_exchange)
                    else:
                        tiles_to_exchange.extend([tile] * count)
                
                if not tiles_to_exchange or len(tiles_to_exchange) > len(self.bag):
                    self.log(f"{player_name}: Gamble failed (no tiles to exchange or bag empty). Passing.")
                    self.pass_count += 1
                    self.draw_tiles(player_name, num=1)
                else:
                    self.exchange_tiles(player_name, tiles_to_exchange)
                    self.pass_count += 1
        
        else:
            self.log(f"{player_name}: No playable words or good gambles found.")
            if len(rack) == self.rack_size:
                self.log(f"{player_name}: Rack is full and cannot play. GAME OVER.")
                self.game_over = True
            else:
                self.log(f"{player_name} will PASS (draw 1 tile).")
                self.pass_count += 1
                self.draw_tiles(player_name, num=1)

        if self.pass_count >= 6: 
            self.game_over = True
            self.log("Game over: 6 consecutive passes.")
        
        if not self.bag and (len(self.racks[player_name]) == 0):
            self.game_over = True
            self.log(f"Game over: Bag is empty and {player_name} emptied their rack.")

    def run_game(self):
        self.log("\n=== GAME START ===")
        self.log(f"Filling racks to {self.rack_size} tiles...")
        for player_name in self.players.keys():
            self.draw_to_fill(player_name)

        self.current_player_name = list(self.players.keys())[0]
        self.log(f"\n--- {self.current_player_name} Turn 0 (Special) ---")
        
        first_move_found = False
        rack = self.racks[self.current_player_name]
        for char1 in rack:
            for char2 in rack:
                if char1 == char2: continue
                word = char1 + char2
                if word in self.valid_dictionary:
                    self.log(f"{self.current_player_name} *must* play on center ({CENTER}). Playing '{word}'.")
                    self.board[CENTER] = char1
                    self.board[ROWS[BOARD_SIZE // 2] + COLS[BOARD_SIZE // 2 + 1]] = char2
                    rack.remove(char1)
                    rack.remove(char2)
                    score, mult = evaluator.score_word(word, CENTER, 'H', {CENTER, ROWS[BOARD_SIZE // 2] + COLS[BOARD_SIZE // 2 + 1]}, self.letter_scores)
                    self.scores[self.current_player_name] += score * mult
                    first_move_found = True
                    break
            if first_move_found: break
        
        if not first_move_found and rack:
            first_tile = self.racks[self.current_player_name].pop() 
            self.log(f"{self.current_player_name} *must* play its tile ('{first_tile}') on center ({CENTER}).")
            self.board[CENTER] = first_tile
            score, mult = evaluator.score_word(first_tile, CENTER, 'H', {CENTER}, self.letter_scores)
            self.scores[self.current_player_name] += score * mult

        self.draw_to_fill(self.current_player_name)
        self.print_board()
        self.switch_player()
        
        turn_count = 1
        while not self.game_over and turn_count < 100:
            self.log(f"\n==================== TURN {turn_count} ====================")
            self.take_turn()
            
            if not self.game_over:
                self.print_board()
                self.log(f"Bag: {len(self.bag)} tiles left. Passes: {self.pass_count}/6")
                self.log(f"Scores: {self.scores}")
                self.log(f"Current Racks: {self.racks}")
                self.switch_player()
                turn_count += 1
        
        self.log("\n==================== GAME OVER ====================")
        self.print_board()
        
        p1_name = list(self.players.keys())[0]
        p2_name = list(self.players.keys())[1]
        
        p1_unplayed_score = sum(self.letter_scores[tile] for tile in self.racks[p1_name])
        p2_unplayed_score = sum(self.letter_scores[tile] for tile in self.racks[p2_name])

        if len(self.racks[p1_name]) == 0:
             self.log(f"{p1_name} emptied their rack! Adding {p2_unplayed_score} points.")
             self.scores[p1_name] += p2_unplayed_score
        elif len(self.racks[p2_name]) == 0:
             self.log(f"{p2_name} emptied their rack! Adding {p1_unplayed_score} points.")
             self.scores[p2_name] += p1_unplayed_score
        
        self.log(f"{p1_name} loses {p1_unplayed_score} points for unplayed tiles: {self.racks[p1_name]}")
        self.scores[p1_name] -= p1_unplayed_score
        self.log(f"{p2_name} loses {p2_unplayed_score} points for unplayed tiles: {self.racks[p2_name]}")
        self.scores[p2_name] -= p2_unplayed_score

        self.log(f"\nFinal Scores:")
        self.log(f"  {p1_name}: {self.scores[p1_name]}")
        self.log(f"  {p2_name}: {self.scores[p2_name]}")
        
        winner_name = "TIE"
        if self.scores[p1_name] > self.scores[p2_name]:
            winner_name = p1_name
        elif self.scores[p2_name] > self.scores[p1_name]:
            winner_name = p2_name

        if winner_name == "TIE":
             self.log("\nIt's a TIE!")
        else:
            self.log(f"\nWinner: {winner_name}!")
            
        return winner_name
