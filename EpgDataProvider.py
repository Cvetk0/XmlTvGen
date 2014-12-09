# coding=utf-8
"""
Data file loader, CSV file parser and provider of multi-language EPG data dictionaries
"""
import json
import io
import random


class EpgDataProvider(object):
    def __init__(self, datafile):
        self.suplang = {'en', 'fa'}
        self.supgenre = {'news', 'sport', 'cartoon', 'movie', 'documentary'}
        self.data = {}
        for lang in self.suplang:
            self.data[lang] = {}
            for genre in self.supgenre:
                self.data[lang][genre] = []
        self.read_data(datafile)

    def __str__(self):
        return json.dumps(self.data, indent=4, encoding='utf-8')

    def read_data(self, datafile):
        with io.open(datafile, mode='r') as data:
            for line in data.readlines():
                line = line.split(';')
                # Currently line has to have 14 fields!
                if len(line) != 14:
                    raise ValueError('Error parsing the line, invalid number of fields')
                lang, genre = line[:2]
                if lang in self.suplang and genre in self.supgenre:
                    self.data[lang][genre].append(line[2:])
                else:
                    print 'Skipping line, unknown language ' + lang + ' or genre ' + genre

    def get_random_show(self, lang_list, genre):
        max_len = 0
        for lang in lang_list:
            if lang not in self.suplang:
                raise ValueError('Language %r not supported' % (lang))
            if len(self.data[lang][genre]) > max_len:
                max_len = len(self.data[lang][genre])
        if genre not in self.supgenre:
            raise ValueError('Genre %r not supported' % (genre))
        idx = random.randrange(max_len)
        duration = int(self.data[lang_list[0]][genre][idx][-1])
        data = {}
        for lang in lang_list:
            data[lang] = self.data[lang][genre][idx][:-1]
        return (duration, data)

#provider = EpgDataProvider(datafile)
#print provider
#print provider.get_random_show(['en'], 'movie')