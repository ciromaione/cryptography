import argparse
import shift_cipher


def encrypt(text, key):
    text = text.lower()

    index, mod, out = 0, len(key), ''
    for c in text:
        if c.isalpha():
            out += chr((ord(c) - 97 + ord(key[index]) - 97) % 25 + 97)
            index = (index + 1) % mod
        else:
            out += c

    return out


def decrypt(text, key):
    text = text.lower()

    index, mod, out = 0, len(key), ''
    for c in text:
        if c.isalpha():
            out += chr((ord(c) - ord(key[index])) % 25 + 97)
            index = (index + 1) % mod
        else:
            out += c

    return out


def crack(text, limit):
    """Vigenere crack function for english texts"""

    text = text.lower()

    def calc_freq(t):
        q = [0 for x in range(26)]
        length = 0
        for c in t:
            if c.isalpha():
                index = ord(c) - 97
                q[index] += 1
                length += 1
        return list(map(lambda x: x / length, q))

    array_text = [c for c in text if c.isalpha()]

    # predict the period
    period, var = 0, 100.0
    for w in range(1, limit+1):
        t = ''.join(array_text[0::w])
        q = calc_freq(t)
        score = 0
        for i in range(26):
            score += q[i] * q[i]
        actual_var = abs(score - 0.065)
        if actual_var < var:
            var = actual_var
            period = w

    # predict the key
    key = ''
    for i in range(period):
        t = ''.join(array_text[i::period])
        key += chr(shift_cipher.crack(t) + 97)

    return key


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', choices=['encrypt', 'decrypt', 'crack'])
    parser.add_argument('-f', '--file', help='input text file')
    parser.add_argument('-o', '--out', help='output text file')
    parser.add_argument('-k', '--key', help='encrypt/decrypt key')
    parser.add_argument('--limit', help='limit for key length', type=int)
    return parser


if __name__ == '__main__':
    args = make_parser().parse_args()

    if args.operation == 'encrypt':
        if args.file is None:
            print("You must specify a file")
            exit(1)
        if args.key is None:
            print("You must specify a key")
            exit(1)
        with open(args.file, 'r') as f:
            out = encrypt(f.read(), args.key)
            if args.out is None:
                print(out)
            else:
                with open(args.out, 'w+') as o:
                    o.write(out)
    elif args.operation == 'decrypt':
        if args.file is None:
            print("You must specify a file")
            exit(1)
        if args.key is None:
            print("You must specify a key")
            exit(1)
        with open(args.file, 'r') as f:
            out = decrypt(f.read(), args.key)
            if args.out is None:
                print(out)
            else:
                with open(args.out, 'w+') as o:
                    o.write(out)
    elif args.operation == 'crack':
        if args.file is None:
            print("You must specify a file")
            exit(1)
        if args.limit is None:
            args.limit = 10
        elif args.limit <= 0:
            print("Key limit must be positive")
            exit(1)
        with open(args.file, 'r') as f:
            key = crack(f.read(), args.limit)
            print("The predicted key is:", key)