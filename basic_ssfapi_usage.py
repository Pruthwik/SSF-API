"""Find arguments from dependency relations in sentences."""
import ssfAPI as ssf
from sys import argv
from re import search


def read_ssf_file(file_path):
    """Read a ssf file."""
    doc = ssf.Document(file_path)
    for tree in doc.nodeList:
        # tree is actually sentence.
        sentence_id = tree.sentenceID
        print('Sentence ID =', sentence_id)
        # Parse chunks in a sentence.
        for chunkNode in tree.nodeList:
            chunk_type = chunkNode.type
            chunk_id = chunkNode.name
            print('Chunk Type =', chunk_type)
            print('Chunk ID =', chunk_id)
            # parse tokens
            for node in chunkNode.nodeList:
                pos_tag = node.type
                token = node.lex
                morph_features = node.getAttribute('af')
                print('token =', token)
                print('pos tag =', pos_tag)
                print('morph features =', morph_features)


def main():
    """Pass arguments and call functions here."""
    input_file_path = argv[1]
    read_ssf_file(input_file_path)


if __name__ == '__main__':
    main()
