#!usr/bin/env python
# coding:utf-8

import zhconv
import codecs
import os
import re
import jieba


all_tang_song_verse = "../corpus/corpus-master/hans_全宋词_全唐五代词.txt"
tang_300_peom = "../corpus/corpus-master/hans_唐诗三百首.txt"
song_300_verse = "../corpus/corpus-master/hans_宋词三百首.txt"
shi_jing = "../corpus/corpus-master/hans_诗经.txt"
chu_ci = "../corpus/corpus-master/hans_楚辞.txt"
lun_yu = "../corpus/corpus-master/hans_论语.txt"
# 设置分句的标志符号；可以根据实际需要进行修改
cutlist = "。！？；".decode('utf-8')

def convert_file_to_hans(target_file):
    with codecs.open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()
        dir_name, base_name = os.path.split(target_file)
        hans_base_name = "hans_" + zhconv.convert(base_name.decode('utf-8'), 'zh-hans').encode('utf-8')
        hans = zhconv.convert(content, 'zh-hans')
        with codecs.open(dir_name + "/" + hans_base_name, 'w', encoding='utf-8') as res:
            res.write(hans)


def convert_hant2hans():
    input_dir = raw_input("directory to convert: ")
    for f in os.listdir(input_dir):
        if f.endswith('.txt') and not f.startswith("hans"):
            convert_file_to_hans(input_dir + "/" + f)
    print("convert finished")


# 检查某字符是否分句标志符号的函数；如果是，返回True，否则返回False
def FindToken(cutlist, char):
    if char in cutlist:
        return True
    else:
        return False


# 进行分句的核心函数
def Cut(cutlist, lines):  # 参数1：引用分句标志符；参数2：被分句的文本，为一行中文字符
    l = []  # 句子列表，用于存储单个分句成功后的整句内容，为函数的返回值
    line = []  # 临时列表，用于存储捕获到分句标志符之前的每个字符，一旦发现分句符号后，就会将其内容全部赋给l，然后就会被清空

    for i in lines:  # 对函数参数2中的每一字符逐个进行检查 （本函数中，如果将if和else对换一下位置，会更好懂）
        if FindToken(cutlist, i):  # 如果当前字符是分句符号
            line.append(i)  # 将此字符放入临时列表中
            l.append(''.join(line))  # 并把当前临时列表的内容加入到句子列表中
            line = []  # 将符号列表清空，以便下次分句使用
        else:  # 如果当前字符不是分句符号，则将该字符直接放入临时列表中
            line.append(i)
    return l


def create_corpus(resource, peom_prefix="", impurities=[]):
    sentences_list = []
    with open(resource, 'r') as text_file:
        for text_line in text_file:
            sentences = Cut(list(cutlist), list(text_line.decode('utf-8')))
            for sentence in sentences:
                if sentence.strip() != "":
                    sentence = sentence.strip()
                    if len(peom_prefix.strip()) > 0:
                        sentence = sentence.replace(peom_prefix, u"\n")
                    for s in impurities:
                        sentence = re.sub(s, "", sentence)
                    sentences_list.append(sentence)
        print("Cut sentence finished")
    dir_name, base_name = os.path.split(resource)
    corpus = dir_name + '/corpus_' + base_name
    with open(corpus, 'w') as corpus:
        for sentence in sentences_list:
            s = sentence.encode('utf-8')
            corpus.write("%s\n" % s)
        print("corpus created")


# 全宋词_全唐五代词
def create_corpus_of_all_tang_song_verse():
    create_corpus(all_tang_song_verse, u"词文：", [u'【.*】?。?'])


# 300唐诗
def create_corpus_of_300_tang_peom():
    create_corpus(tang_300_peom, u'诗文:', [u"\(.*\)"])


# 300宋词
def create_corpus_of_300_song_verse():
    create_corpus(song_300_verse, u"词文:")


# 楚辞
def create_corpus_of_chu_ci():
    create_corpus(chu_ci)


# 诗经
def create_corpus_of_shi_jing():
    create_corpus(shi_jing)


# 论语
def create_corpus_of_lun_yu():
    create_corpus(lun_yu)

if __name__ == '__main__':

    # convert_hant2hans()

    # create_corpus_of_300_tang_peom()

    # create_corpus_of_300_song_verse()

    # create_corpus_of_chu_ci()

    # create_corpus_of_shi_jing()

    create_corpus_of_lun_yu()

