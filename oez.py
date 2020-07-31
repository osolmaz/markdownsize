import argparse
import re
import os
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="Path to the input Markdown file")
parser.add_argument("output", type=str, help="Path to the output file")

TWEET_SEP = "[...]"
PARAGRAPH_SEP = "{...}"
CHAR_LIMIT = 140


if __name__ == "__main__":
    args = parser.parse_args()

    if args.input == args.output:
        raise Exception("Input and output cannot be the same")

    content = open(args.input, "r").read()

    header_list = re.findall(r"^(---\s.*?\s---)", content, flags=re.DOTALL)
    header = None

    if header_list:
        header = header_list[0]
        content = content[len(header):].strip()

    tokens = re.split("(\[\.\.\.\]|\{\.\.\.\})", content)
    tokens = [t.strip() for t in tokens]

    for n, token in enumerate(tokens):
        if (
            token is not TWEET_SEP
            and token is not PARAGRAPH_SEP
            and len(token) > CHAR_LIMIT
        ):
            tokens[n] = token[:CHAR_LIMIT] + "~~" + token[CHAR_LIMIT:] + "~~"

    tokens = [" " if t == TWEET_SEP else t for t in tokens]
    tokens = ["\n\n" if t == PARAGRAPH_SEP else t for t in tokens]

    content = "".join(tokens)

    if header:
        content = header + "\n\n" + content

    if args.output[-3:] == ".md":
        open(args.output, "w").write(content)
    else:
        tmp_path = "tmp_" + args.output + ".md"

        ofile = open(tmp_path, "w")
        ofile.write(content)
        ofile.close()

        subprocess.call(["pandoc", tmp_path, "-o", args.output])

        os.remove(tmp_path)
