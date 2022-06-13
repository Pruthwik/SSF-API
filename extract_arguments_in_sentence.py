"""Find arguments from dependency relations in sentences."""
import ssfAPI as ssf
from sys import argv
from re import search


def read_ssf_files_from_folder(folder_path):
    """Read files from a folder."""
    file_list = ssf.folderWalk(folder_path)
    file_list = sorted(file_list)
    for fl in file_list:
        print('File :', fl[fl.rfind('/') + 1:])
        doc = ssf.Document(fl)
        for tree in doc.nodeList:
            sent_verb_args = dict()
            pof_verb_chunks = set()
            print('Sentence ID =', tree.sentenceID)
            print('Sentence SSF Text =', tree.text)
            print('Sentence Raw Text =', tree.generateSentence())
            for chunkNode in tree.nodeList:
                print('Chunk Type =', chunkNode.type, 'Chunk ID =', chunkNode.name, 'Parent =', chunkNode.parent)
                if chunkNode.type == 'VGF':
                    auxilaries = list()
                    root, vibh = '', ''
                    for node in chunkNode.nodeList:
                        if node.type == 'VM':
                            morph_features = node.getAttribute('af')
                            root, vibh = morph_features.split(',')[0], morph_features.split(',')[6]
                            sent_verb_args[chunkNode.name] = (root, vibh, chunkNode.parentRelation, chunkNode.parent)
                        elif node.type == 'VAUX':
                            auxilary_root = node.getAttribute('af').split(',')[0]
                            auxilaries.append(auxilary_root)
                    if auxilaries and root:
                        sent_verb_args[chunkNode.name] = (root, vibh + '+' + '+'.join(auxilaries), chunkNode.parentRelation, chunkNode.parent)
                        root, vibh = '', ''
                elif chunkNode.type == 'NP':
                    post_positions = list()
                    root, vibh = '', ''
                    if chunkNode.parentRelation == 'pof' and search('^VGF', chunkNode.parent):
                        pof_verb_chunks.add(chunkNode.parent)
                    else:
                        for node in chunkNode.nodeList:
                            if node.type == 'NN':
                                morph_features = node.getAttribute('af')
                                root, vibh = morph_features.split(',')[0], morph_features.split(',')[6]
                                sent_verb_args[chunkNode.name] = (root, vibh, chunkNode.parentRelation, chunkNode.parent)
                            elif node.type == 'PSP':
                                post_positions.append(node.lex)
                        if post_positions and root:
                            sent_verb_args[chunkNode.name] = (root, vibh + '+' + '+'.join(post_positions), chunkNode.parentRelation, chunkNode.parent)
                            root, vibh = '', ''
                elif chunkNode.parentRelation == 'pof' and search('^VGF', chunkNode.parent):
                    pof_verb_chunks.add(chunkNode.parent)
            print(sent_verb_args)
            print(pof_verb_chunks)
            verb_args_dict = find_verb_arguments_and_add_to_dict(sent_verb_args, pof_verb_chunks)
            print(verb_args_dict)


def find_verb_arguments_and_add_to_dict(sent_verb_args, pof_verb_chunks):
    """Find arguments verb wise in a sentence."""
    verb_args_dict = dict()
    for key in sent_verb_args:
        if search('^NP', key):
            key_info = sent_verb_args[key]
            if search('^VGF', key_info[3]):
                verb_info = (sent_verb_args[key_info[3]][0], sent_verb_args[key_info[3]][1])
                if key_info[3] not in pof_verb_chunks and search('k*', key_info[2]):
                    verb_args_dict.setdefault(verb_info, list()).append((key_info[1], key_info[2]))
    return verb_args_dict


def main():
    """Pass arguments and call functions here."""
    input_folder_path = argv[1]
    read_ssf_files_from_folder(input_folder_path)


if __name__ == '__main__':
    main()
