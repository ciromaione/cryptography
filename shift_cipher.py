import argparse


def encrypt(text, key):
    text = text.lower()
    out = ''
    for char in text:
        if char.isalpha():
            out += chr((ord(char) - 97 + key) % 25 + 97)
        else:
            out += char
    return out


def decrypt(text, key):
    text = text.lower()
    out = ''
    for char in text:
        if char.isalpha():
            out += chr((ord(char) - 97 - key) % 25 + 97)
        else:
            out += char
    return out


def crack(text):
    """Shift Cipher crack function for english texts"""

    text = text.lower()

    # letter frequency array for english
    p = [0.082, 0.015, 0.028, 0.043, 0.127, 0.022, 0.02, 0.061, 0.07, 0.002, 0.008, 0.04, 0.024, 0.067, 0.015, 0.019,
         0.001, 0.06, 0.063, 0.091, 0.028, 0.01, 0.024, 0.002, 0.02, 0.001]

    # letter frequency array for the ciphertext
    q = [0 for x in range(26)]
    length = 0

    for c in text:
        if c.isalpha():
            index = ord(c) - 97
            q[index] += 1
            length += 1

    q = list(map(lambda x: x / length, q))

    key, var = 0, 100.0
    for j in range(26):
        score = 0
        for i in range(26):
            score += p[i] * q[((i + j) % 25)]
        actual_var = abs(score - 0.060)
        if actual_var < var:
            var = actual_var
            key = j

    return key


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', choices=['encrypt', 'decrypt', 'crack'])
    parser.add_argument('-f', '--file', help='input text file')
    parser.add_argument('-o', '--out', help='output text file')
    parser.add_argument('-k', '--key', help='encrypt/decrypt key', type=int)
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
        with open(args.file, 'r') as f:
            key = crack(f.read())
            print("The predicted key is:", key)
