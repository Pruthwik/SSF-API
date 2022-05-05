# how to run the code
# python3 extract_data_from_ssf_in_conll_format.py --input InputFilePath --output OutputFilePath --level 0/1/2/3
# level argument: 0 for token, 1 for token+pos, 2 for token+pos+morph, 3 for token+pos+chunk
# no need to create an output file, only give a name
# author : Pruthwik Mishra, LTRC, IIIT-H
import ssfAPI as ssf
import os
import argparse
import re


def readFileAndExtractSentencesInConLL(inputFilePath, outputFilePath, level=0):
    """Read file and extract sentence and info in CoNLL."""
    allSentences = list()
    d = ssf.Document(inputFilePath)
    sentencesList = list()
    print(inputFilePath)
    for tree in d.nodeList:
        print(tree.sentenceID)
        if level == 0:
            sentencesList.append('\n'.join([token for token in tree.generateSentence(
            ).split() if not re.search('^NUL', token)]) + '\n')
        elif level == 1:
            tokensWithPOS = [node.lex + '\t' + node.type.replace(
                '__', '_') for chunkNode in tree.nodeList for node in chunkNode.nodeList if not re.search('^NUL', node.lex)]
            sentencesList.append('\n'.join(tokensWithPOS) + '\n')
        elif level == 2:
            tokensWithPOSMorph = [node.lex + '\t' + node.type.replace('__', '_') + '\t' + node.getAttribute(
                'af') for chunkNode in tree.nodeList for node in chunkNode.nodeList if not re.search('^NUL', node.lex)]
            sentencesList.append('\n'.join(tokensWithPOSMorph) + '\n')
        else:
            tokenPOSAndChunk = list()
            for chunkNode in tree.nodeList:
                for indexNode, node in enumerate(chunkNode.nodeList):
                    if indexNode == 0:
                        if not re.search('^NUL', node.lex):
                            tokenPOSAndChunk.append(
                                node.lex + '\t' + node.type.replace('__', '_') + '\tB-' + chunkNode.type)
                    else:
                        if not re.search('^NUL', node.lex):
                            tokenPOSAndChunk.append(
                                node.lex + '\t' + node.type.replace('__', '_') + '\tI-' + chunkNode.type)
            sentencesList.append('\n'.join(tokenPOSAndChunk) + '\n')
    writeListToFile(sentencesList, outputFilePath)


def writeListToFile(dataList, outFilePath):
    """Write a list to a file."""
    with open(outFilePath, 'w', encoding='utf-8') as fileWrite:
        fileWrite.write('\n'.join(dataList) + '\n')
        fileWrite.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest='inp',
                        help="Add the input file path")
    parser.add_argument('--output', dest='out',
                        help="Add the output file path")
    parser.add_argument('--level', dest='level',
                        help="Add the level 0: token, 1: token + pos, 2: token + pos + morph, 3 for token + pos + chunk", type=int, default=0)
    args = parser.parse_args()
    readFileAndExtractSentencesInConLL(args.inp, args.out, args.level)
