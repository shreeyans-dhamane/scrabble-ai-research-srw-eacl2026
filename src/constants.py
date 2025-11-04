BOARD_SIZE = 15
ROWS = 'abcdefghijklmno'
COLS = 'abcdefghijklmno'
CENTER = ROWS[BOARD_SIZE // 2] + COLS[BOARD_SIZE // 2]
RACK_SIZE = 7

LETTER_SCORES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5,
    'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1,
    'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '_': 0
}

TILE_BAG_TEMPLATE = list(
    'a' * 9 + 'b' * 2 + 'c' * 2 + 'd' * 4 + 'e' * 12 + 'f' * 2 + 'g' * 3 + 'h' * 2 +
    'i' * 9 + 'j' * 1 + 'k' * 1 + 'l' * 4 + 'm' * 2 + 'n' * 6 + 'o' * 8 + 'p' * 2 +
    'q' * 1 + 'r' * 6 + 's' * 4 + 't' * 6 + 'u' * 4 + 'v' * 2 + 'w' * 2 + 'x' * 1 +
    'y' * 2 + 'z' * 1 + '_' * 2
)

TRIPLE_WORD = {'aa', 'ah', 'ao', 'ha', 'ho', 'oa', 'oh', 'oo'}
DOUBLE_WORD = {
    'bb', 'nb', 'cc', 'mc', 'dd', 'ld', 'ee', 'ke',
    'kk', 'ek', 'll', 'dl', 'mm', 'cm', 'nn', 'bn',
    CENTER
}
TRIPLE_LETTER = {
    'bf', 'bj', 'fb', 'ff', 'fj', 'fn',
    'jb', 'jf', 'jj', 'jn', 'nf', 'nj'
}
DOUBLE_LETTER = {
    'ad', 'al', 'cg', 'ci', 'da', 'dh', 'do', 'gc', 'gg', 'gi', 'gm',
    'hd', 'hl', 'ic', 'ig', 'ii', 'im', 'la', 'lh', 'lo',
    'mg', 'mi', 'od', 'ol'
}
