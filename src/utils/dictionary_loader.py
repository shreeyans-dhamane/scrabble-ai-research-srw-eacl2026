import os

def load_dictionary(filepath):
    if not os.path.exists(filepath):
        print(f"Warning: '{filepath}' not found. Creating a small dummy file.")
        dummy_content = (
            "aa\naah\naal\nab\naba\nsea\nser\nseller\ninsert\nlearn\nreal\nraise\ntie\n"
            "a\nin\non\nelle\ninsertion\nsa\nler\nrn\nsate\nsateya\nsatesr\nsat\nsal\nsez\n"
            "myoid\ndownier\npr\nun\noften\njizzes\nz\njazzes\njehu\npozzies\n"
            "hieracosphinxes\njehus\nzaxes\nexchequering\nee\nxi\nzesty\nret\nny\n"
            "bedwarfed\nquarterbacking\ngauje\n"
            "peavy\nar\nee\ngutcher\nzayins\nzex\nfrieze\ntelexed\nmozz\ncoquito\ncoquitos\n"
            "towze\nwe\noi\nquep\nut\njack\nfjeld\nextra\nglowed\noo\nda\njacky\nmalmier\n"
            "favour\ndingily\nhaika\ncoverup\nre\nur\nfjelds\noutby\nat\nfap\nbowing\nna\n"
        )
        with open(filepath, 'w') as f:
            f.write(dummy_content)

    valid_dict = set()
    with open(filepath, 'r') as f:
        for line in f:
            word = line.strip().lower()
            valid_dict.add(word)
    return valid_dict
