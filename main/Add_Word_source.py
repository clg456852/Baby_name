#! usr/bin/env python
# coding:utf-8

import create_name
import convertZh

def add_word_source(file_path, result_path):
    name_source_list = []
    name_sources = []

    with open(file_path, 'r') as name_file:
        for name in name_file:
            if name.startswith("来源: "):
                name_sources.append(name)
    count = 0
    with open(file_path, 'r') as name_file:
        for name in name_file:
            if len(name.strip()) < 1:
                continue
            if not name.startswith("来源: "):
                content = name.strip() + ' ' + name_sources[count]
                name_source_list.append(content)
            else:
                count += 1
    with open(result_path, 'w') as result_file:
        for name in name_source_list:
            result_file.write(name)

def add_word_source_for_file(file_path):
    target_path = create_name.find_target_names(file_path)
    file_path = create_name.attach_pre_name_to('postive_', target_path)
    result_path = create_name.attach_pre_name_to('withSrc_postive_', target_path)
    add_word_source(file_path, result_path)


if __name__ == '__main__':
    add_word_source_for_file(convertZh.chu_ci)
    add_word_source_for_file(convertZh.shi_jing)
    add_word_source_for_file(convertZh.tang_300_peom)
    add_word_source_for_file(convertZh.song_300_verse)
