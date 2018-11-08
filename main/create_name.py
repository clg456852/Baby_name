#!usr/bin/env python
# coding:utf-8

import convertZh
import os
import re
import random
import jieba
from snownlp import SnowNLP

# def create_names():

excluds = {'兮', '忧', '恶', '愁', '陷', '乱', '穷', '邪', '哀', '萎', '靡', '险', '黑', '下', '戚', '惨', '瘦', '雕', '鬼', '龟'}

def find_corpus(text_file):
    dir_name, base_name = os.path.split(text_file)
    corpus = dir_name + '/corpus_' + base_name
    return corpus

def find_target_names(text_file):
    dir_name, base_name = os.path.split(text_file)
    names_file = dir_name + '/names_from_' + base_name
    return names_file

def clauses_from_sentence(sentence):
    clauses = re.split(u"，|。|！|？|；", sentence)
    # clauses = sentence.split(u"，。！？；")
    cn_clauses = []
    i = 0
    while i < len(clauses):
        clause = clauses[i]
        cn = re.sub(u"[^\u4e00-\u9fa5]", u"", clause)
        if len(cn) > 0:
            cn_clauses.append(cn)
        i += 1
    return cn_clauses


def add_new_name(n, names):
    if n not in names:
        names.append(n)


def create_names_based_on(text_line):
    clauses = clauses_from_sentence(text_line)
    names = []
    # 子句内
    for clause in clauses:
        if len(clause) > 3:
            add_new_name(clause[0] + clause[1], names)
            add_new_name(clause[len(clause)-2] + clause[len(clause)-1], names)
            add_new_name(clause[-1] + clause[-3], names)

            seg_list = jieba.cut(clause, cut_all=True)
            for seg in seg_list:
                if len(seg) == 2:
                    add_new_name(seg,seg)
                if len(seg) == 4:
                    add_new_name(seg[0] + seg[1], names)
                    add_new_name(seg[-2] + seg[-1], names)
    # 子句间
    if len(clauses) > 1:
        for i in range(len(clauses)):
            if (i + 1) < len(clauses):
                clause_pre = clauses[i]
                clause_post = clauses[i+1]
                add_new_name(clause_pre[-1] + clause_post[-1], names)
                add_new_name(clause_pre[0] + clause_post[0], names)
                idx0 = random.randint(0, len(clause_pre)-1)
                idx1 = random.randint(0, len(clause_post)-1)
                add_new_name(clause_pre[idx0] + clause_post[idx1], names)
            if (i + 2) < len(clauses):
                clause_pre = clauses[i]
                clause_post = clauses[i + 2]
                add_new_name(clause_pre[-1] + clause_post[-1], names)
                add_new_name(clause_pre[0] + clause_post[0], names)
                idx0 = random.randint(0, len(clause_pre)-1)
                idx1 = random.randint(0, len(clause_post)-1)
                add_new_name(clause_pre[idx0] + clause_post[idx1], names)

    names.append(u"\n来源: " + text_line)
    return names

def attach_pre_name_to(prefix,file_path):
    dir_name, base_name = os.path.split(file_path)
    result_file = dir_name + '/' + prefix + base_name
    return result_file


def create_name_from(corpus):
    selected_corpus = corpus
    corpus_path = find_corpus(selected_corpus)
    target_path = find_target_names(selected_corpus)
    postive_target_path = attach_pre_name_to('postive_', target_path)
    name_source = None
    useful_source = False
    if os.path.isfile(postive_target_path):
        os.remove(postive_target_path)
    with open(corpus_path, 'r') as corpus:
        with open(target_path, 'w') as target:
            target.write('\n')
        result_names = []
        for line in corpus:
            names = create_names_based_on(line.decode('utf-8'))
            for n in names:
                add_new_name(n, result_names)
                print("add name to result_names" + ' ' + n)
        with open(target_path, 'w') as target_names:
            for n in result_names:
                target_names.write(n.encode('utf-8') + "\n")
        with open(postive_target_path, 'w') as postive_targets:
            for n in result_names:
                has_added = False
                source = None
                if n.encode('utf-8').startswith('\n来源:') or len(n.encode('utf-8').strip()) < 1:
                    if n.encode('utf-8').startswith('\n来源:'):
                        source = n.encode('utf-8')
                        # name_source = source
                        if useful_source and source:
                            postive_targets.write(source + '\n')
                            useful_source = False
                    continue
                need_exclude = False
                if len(n.encode('utf-8')) <= 6:
                    for e in excluds:
                        if e in n.encode('utf-8'):
                            need_exclude = True
                            break
                if need_exclude:
                    continue
                if u'全独' == n:
                    print("全独^^^&&&&&")
                s = SnowNLP(n)
                if s.sentiments > 0.8:
                    if s.pinyin:
                        for py in s.pinyin:
                            if py.encode('utf-8').endswith("o") or py.encode('utf-8').startswith("g"):
                                # Pin Yin
                                has_added = True
                                if py.encode('utf-8').endswith("uo"):
                                    postive_targets.write(n.encode('utf-8') + "\n")
                                    print(n.encode('utf-8') + '******\n')
                                else:
                                    postive_targets.write(n.encode('utf-8') + "\n")
                        if s.tags and not has_added:
                            for tag in s.tags:
                                # 获取词性
                                if not has_added and ((tag[0] == n[0] and tag[1] == u'v') or tag[1] == u'a'):
                                    has_added = True
                                    postive_targets.write(n.encode('utf-8') + "\n")
                                    print(n.encode('utf-8') + '\n')
                                if len(s.tags) > 2:
                                    assert 0
                if has_added:
                    useful_source = True

    print("created name from %s" % selected_corpus)

if __name__ == '__main__':

    # n = u'\n来源: 寿考且宁，以保我后生。\n'
    # print(n[0] + n[3:-1])
    # s = n.encode('utf-8')
    # if n.encode('utf-8').startswith('\n来源: '):
    #     print("1")
    # if len(n.encode('utf-8').strip()) < 1:
    #     print('2')
    # 诗经
    # create_name_from(convertZh.shi_jing)
    # # # 楚辞
    # create_name_from(convertZh.chu_ci)
    # # # 300 tang
    # create_name_from(convertZh.tang_300_peom)
    # # 300 chu
    # create_name_from(convertZh.song_300_verse)
    # quan tang song verse
    create_name_from(convertZh.all_tang_song_verse)
