from math import comb
from collections import Counter
from src.constants import (
    BOARD_SIZE, ROWS, COLS, CENTER, RACK_SIZE,
    TRIPLE_WORD, DOUBLE_WORD, TRIPLE_LETTER, DOUBLE_LETTER
)

def get_valid_placements(board):
    valid_placements = set()
    filled_tiles = {t for t, val in board.items() if val != 0}
    if not filled_tiles:
        return {CENTER}
    for tile_coord in filled_tiles:
        r_idx = ROWS.index(tile_coord[0])
        c_idx = COLS.index(tile_coord[1])
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r_idx + dr, c_idx + dc
            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                neighbor_coord = ROWS[nr] + COLS[nc]
                if board[neighbor_coord] == 0:
                    valid_placements.add(neighbor_coord)
    return valid_placements

def find_all_candidates(board, letter_index):
    candidates_dict = {}
    filled_tiles = {t for t, val in board.items() if val != 0}
    if not filled_tiles:    
        return {}
    for tile in filled_tiles:
        r = ROWS.index(tile[0])
        c = COLS.index(tile[1])
        letter_here = board[tile]
        if letter_here not in letter_index: continue
        candidate_words = letter_index[letter_here]
        for word in candidate_words:
            positions = [i for i, l in enumerate(word) if l == letter_here]
            for pos in positions:
                start_c = c - pos
                end_c = start_c + len(word) - 1
                if 0 <= start_c and end_c < BOARD_SIZE:
                    fits = True
                    letters_to_add = 0
                    for j_check in range(len(word)):
                        t = ROWS[r] + COLS[start_c + j_check]
                        if board[t] != 0 and board[t] != word[j_check]:
                            fits = False; break
                        if board[t] == 0: letters_to_add += 1
                    if fits and letters_to_add > 0:
                        candidates_dict.setdefault(tile, {}).setdefault(word, set()).add((ROWS[r] + COLS[start_c], 'H'))
                start_r = r - pos
                end_r = start_r + len(word) - 1
                if 0 <= start_r and end_r < BOARD_SIZE:
                    fits = True
                    letters_to_add = 0
                    for i_check in range(len(word)):
                        t = ROWS[start_r + i_check] + COLS[c]
                        if board[t] != 0 and board[t] != word[i_check]:
                            fits = False; break
                        if board[t] == 0: letters_to_add += 1
                    if fits and letters_to_add > 0:
                        candidates_dict.setdefault(tile, {}).setdefault(word, set()).add((ROWS[start_r] + COLS[c], 'V'))
    return candidates_dict

def get_words_formed(board, start_tile, orientation, word, all_move_tiles, valid_dictionary):
    r_idx = ROWS.index(start_tile[0])
    c_idx = COLS.index(start_tile[1])
    temp_board = board.copy()
    
    placed_tiles_set = {coord for (char, coord) in all_move_tiles}

    for i, char in enumerate(word):
        tile = ROWS[r_idx] + COLS[c_idx+i] if orientation == 'H' else ROWS[r_idx+i] + COLS[c_idx]
        temp_board[tile] = char

    formed_words = [(word, start_tile, orientation)]

    for (char, tile_coord) in all_move_tiles:
        tile_r_idx = ROWS.index(tile_coord[0])
        tile_c_idx = COLS.index(tile_coord[1])
        
        if orientation == 'H':
            r_start_idx = tile_r_idx
            while r_start_idx > 0 and temp_board[ROWS[r_start_idx-1] + COLS[tile_c_idx]] != 0:
                r_start_idx -= 1
            r_end_idx = tile_r_idx
            while r_end_idx < BOARD_SIZE-1 and temp_board[ROWS[r_end_idx+1] + COLS[tile_c_idx]] != 0:
                r_end_idx += 1
            if r_end_idx - r_start_idx >= 1:
                cross_word = ""
                for r in range(r_start_idx, r_end_idx + 1):
                    cross_word += temp_board[ROWS[r] + COLS[tile_c_idx]]
                cross_start_tile = ROWS[r_start_idx] + COLS[tile_c_idx]
                formed_words.append((cross_word, cross_start_tile, 'V'))
        else:
            c_start_idx = tile_c_idx
            while c_start_idx > 0 and temp_board[ROWS[tile_r_idx] + COLS[c_start_idx-1]] != 0:
                c_start_idx -= 1
            c_end_idx = tile_c_idx
            while c_end_idx < BOARD_SIZE-1 and temp_board[ROWS[tile_r_idx] + COLS[c_end_idx+1]] != 0:
                c_end_idx += 1
            if c_end_idx - c_start_idx >= 1:
                cross_word = ""
                for c in range(c_start_idx, c_end_idx + 1):
                    cross_word += temp_board[ROWS[tile_r_idx] + COLS[c]]
                cross_start_tile = ROWS[tile_r_idx] + COLS[c_start_idx]
                formed_words.append((cross_word, cross_start_tile, 'H'))

    for w, _start, _orient in formed_words:
        if w not in valid_dictionary:
            return None
    
    return formed_words

def score_word(word, start_coord, orientation, newly_placed_coords_set, letter_scores):
    word_score = 0
    word_multiplier = 1
    r_start_idx = ROWS.index(start_coord[0])
    c_start_idx = COLS.index(start_coord[1])
    
    for i, char in enumerate(word):
        if orientation == 'H':
            r_idx, c_idx = r_start_idx, c_start_idx + i
        else:
            r_idx, c_idx = r_start_idx + i, c_start_idx
        tile_coord = ROWS[r_idx] + COLS[c_idx]
        
        letter_score = letter_scores.get(char, 0)

        if tile_coord in newly_placed_coords_set:
            if tile_coord in TRIPLE_LETTER:
                letter_score *= 3
            elif tile_coord in DOUBLE_LETTER:
                letter_score *= 2
            
            if tile_coord in TRIPLE_WORD:
                word_multiplier *= 3
            elif tile_coord in DOUBLE_WORD:
                word_multiplier *= 2
        
        word_score += letter_score
        
    return word_score, word_multiplier

def analyze_all_moves(board, bag, rack, letter_index, valid_dictionary, letter_scores, rack_size):
    rack_counter = Counter(rack)
    all_tiles_count = Counter(bag)
    total_remaining_tiles = len(bag)
    playable_goals = [] 
    future_goals = []   
    valid_placement_tiles = get_valid_placements(board)
    if not valid_placement_tiles:
        return [], []

    all_candidates = find_all_candidates(board, letter_index)

    for anchor in all_candidates:
        for word, positions in all_candidates[anchor].items():
            for start_tile, orientation in positions:
                r_idx_start = ROWS.index(start_tile[0])
                c_idx_start = COLS.index(start_tile[1])
                all_missing_letters = Counter()
                first_missing_tile_info = None 
                all_move_tiles = []
                
                for i, char in enumerate(word):
                    tile_coord = ROWS[r_idx_start] + COLS[c_idx_start + i] if orientation == 'H' else ROWS[r_idx_start + i] + COLS[c_idx_start]
                    if board[tile_coord] == 0:
                        all_missing_letters[char] += 1
                        all_move_tiles.append((char, tile_coord))
                        if first_missing_tile_info is None and tile_coord in valid_placement_tiles:
                            first_missing_tile_info = (char, tile_coord)
                
                if not all_missing_letters or first_missing_tile_info is None:
                    continue 

                formed_words_info = get_words_formed(board, start_tile, orientation, word, all_move_tiles, valid_dictionary)
                if formed_words_info is None:
                    continue 

                temp_rack = rack_counter.copy()
                letters_needed_from_bag = Counter()
                tiles_to_keep = []
                for char, count in all_missing_letters.items():
                    if temp_rack[char] >= count:
                        temp_rack[char] -= count
                        tiles_to_keep.extend([char] * count)
                    else:
                        needed_after_rack = count - temp_rack[char]
                        tiles_to_keep.extend([char] * temp_rack[char])
                        temp_rack[char] = 0
                        if temp_rack['_'] >= needed_after_rack:
                            temp_rack['_'] -= needed_after_rack
                            tiles_to_keep.extend(['_'] * needed_after_rack)
                        else:
                            blanks_needed_from_bag = needed_after_rack - temp_rack['_']
                            tiles_to_keep.extend(['_'] * temp_rack['_'])
                            temp_rack['_'] = 0
                            letters_needed_from_bag[char] = blanks_needed_from_bag

                newly_placed_coords_set = {coord for char, coord in all_move_tiles}
                total_move_score = 0
                
                for w, start, orient in formed_words_info:
                    word_score, word_multiplier = score_word(w, start, orient, newly_placed_coords_set, letter_scores)
                    total_move_score += word_score * word_multiplier
                
                if len(all_move_tiles) == rack_size:
                    total_move_score += 50
                
                score = total_move_score

                prob = 0.0
                if not letters_needed_from_bag:
                    prob = 1.0
                else:
                    total_needed = sum(letters_needed_from_bag.values())
                    num_we_can_draw = rack_size - (len(rack) - sum(all_missing_letters.values()))
                    if total_needed > num_we_can_draw or total_needed > (total_remaining_tiles + rack_counter['_']) or any(letters_needed_from_bag[l] > all_tiles_count[l] for l in letters_needed_from_bag):
                        prob = 0.0
                    else:
                        try:
                            denom = comb(total_remaining_tiles, total_needed)
                            prob_raw = 1
                            for char, count in letters_needed_from_bag.items():
                                prob_raw *= comb(all_tiles_count[char], count)
                            prob = (prob_raw / denom) if denom > 0 else 0.0
                        except ValueError:
                            prob = 0.0

                if prob == 0.0 and not prob == 1.0:
                    continue 

                prob_adj = prob ** (1 / ((len(word))**0.5)) 
                expected_score = score * prob_adj
                
                goal_data = {
                    'word': word,
                    'placement': (start_tile, orientation),
                    'score': score,
                    'prob': prob,
                    'expected_score': expected_score,
                    'letters_needed_from_bag': dict(letters_needed_from_bag),
                    'all_move_tiles': all_move_tiles,
                    'tiles_to_keep': tiles_to_keep,
                    'all_formed_words': formed_words_info
                }
                
                if prob == 1.0:
                    playable_goals.append(goal_data)
                else:
                    future_goals.append(goal_data)

    return playable_goals, future_goals
