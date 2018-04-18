#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 18:26:46 2018

@author: pseudosecret
"""

import nltk
import re
import math
import FoxDot
import time
import random

class ParserMusician():
    def __init__(self):
        self.key = ([0, "minor"], [-5, "minor"], [5, "minor"], [-2, "major"], 
                    [3, "major"], [-4, "major"], [1, "minor"])
        FoxDot.Root.default.set(self.key[0][0])
        FoxDot.Scale.default.set(self.key[0][1])
        self.previous_time = time.clock()
        self.duration_to_bass_rhythm_dictionary = {
                       3: [0.25, 0.25, FoxDot.rest(0.5), 0.25, FoxDot.rest(0.25), 0.5, 0.25, 0.75],
                       4: [0.25, 0.25, FoxDot.rest(0.5), 0.25, FoxDot.rest(0.25), 0.25, 0.25, 0.5, 0.25],
                       6: [0.25, 0.25, FoxDot.rest(0.5), 0.25, FoxDot.rest(0.25), 0.25, 0.5, 0.75],
                       8: [1, 1, 0.25, 0.25, FoxDot.rest(0.25), 0.25, 0.25, 0.25]}
        self.letter_to_rhythm_dictionary = {"B": "$", "C": "E", "D": "%", "F": "F",
                                  "G": "A", "J": "L", "K": "#", "P": "P",
                                  "Q": "r", "S": "=", "T": "n", "V": "V",
                                  "X": "H", "Z": "W", "H": ".",
                                  "b": "D", "c": "k", "d": "i", "f": "l",
                                  "g": "M", "j": "j", "k": ":", "p": "p", 
                                  "q": "T", "s": "~", "t": "-", "v": "R", 
                                  "x": "h", "z": "g", "h": ".",
                                  ".": "X", "\"": "[xx]", "'": "v", ",": "v",
                                  ";": "[vx]", ":": "[xX]",
                                  "č": "S", "Þ": "@", "ṣ": "/", "ɸ": "\\\\",
                                  "ç": "I", "ð": "e", "ʃ": "o", " ": ""}
                                 # miscellaneous
        self.pos_to_chord_dictionary = {"``": 0, "''": 0, "$": 0, "(": 0, ")": 0,
                                 ",": 0, "--": 0, ".": 0, ":": 0, "CD": 1,
                                 "SYM": 2, "LS": 2,
                                 # nouns
                                 "NN": 3, "NNP": 4, "NNPS": 5, "NNS": 6,
                                 # genitive marker and pronouns
                                 "POS": 7, "PRP": 8, "PRP$": 9, "WP": 10,
                                 "WP$": 11,
                                 # adjectives, determiners
                                 "JJ": 12, "JJR": 13, "JJS": 14, "WDT": 15, "DT": 16,
                                 "PDT": 17,
                                 # adverbs
                                 "RB": 18, "RBR": 19, "RBS": 20, "WRB": 21,
                                 # verbs
                                 "VB": 22, "VBD": 23, "VBG": 24, "VBN": 25,
                                 "VBP": 26, "VBZ": 27,
                                 # fillers
                                 "TO": 28, "RP": 29, "EX": 30,
                                 # conjunction, modal auxiliary, prep
                                 "CC": 31, "IN": 32, "MD": 33,
                                 # foreign words and interjections
                                 "FW": 34, "UH": 35}
        self.pos_to_chord_bass_dictionary = {"``": 0, "''": 0, "$": 0, "(": 0, ")": 0,
                                 ",": 0, "--": 0, ".": 0, ":": 0, "CD": 0,
                                 "SYM": 0, "LS": 0,
                                 # nouns
                                 "NN": -4, "NNP": 4, "NNPS": 5, "NNS": 5,
                                 # genitive marker and pronouns
                                 "POS": -4, "PRP": 4, "PRP$": -4, "WP": 4,
                                 "WP$": -4,
                                 # adjectives, determiners
                                 "JJ": 0, "JJR": 1, "JJS": -1, "WDT": 2, "DT": 3,
                                 "PDT": 3,
                                 # adverbs
                                 "RB": -2, "RBR": -2, "RBS": 0, "WRB": -5,
                                 # verbs
                                 "VB": -3, "VBD": 3, "VBG": -3, "VBN": -3,
                                 "VBP": -3, "VBZ": 3,
                                 # fillers
                                 "TO": 4, "RP": -2, "EX": -2,
                                 # conjunction, modal auxiliary, prep
                                 "CC": -2, "IN": -2, "MD": -4,
                                 # foreign words and interjections
                                 "FW": 0.5, "UH": -0.5}
        self.chord_bass_to_bass_line_dictionary = {
                                 0: [0, 0, 1, -1, 0, -4],
                                 1: [1, 1, 1, 1, 0, 1, 4],
                                 2: [2, 2, 2, 2, 1, 9, 8],
                                 3: [3, 3, 4, 2, 3, 0, 1],
                                 4: [4, 4, 2, 2, 4, 0, 1],
                                 5: [5, 5, 3, 4, 5, 1],
                                -1: [-1, -1, -3, -2, -1, 1],
                                -2: [-2, -1, -4, 0, -1, 1],
                                -3: [-3, -3, -3, -1],
                                -4: [-4, -4, -4, 1, 2],
                               0.5: [0.5, 1.5, 2.5, 1.5, -0.5],
                              -0.5: [-0.5, 1.5, 2.5, 1.5, 0.5]}
        self.chord_to_voicing_dictionary = {
                                 # symbols
                                 0: (1, 2, 5),
                                 1: (1, 2, 5, 6),
                                 2: (-3, 0, 2, 4, 6),
                                 # nouns
                                 3: (4, 5, 6, 8),
                                 4: (4, 5, 6, 9),
                                 5: (0, 4, 5, 9),
                                 6: (0, 2, 4, 5),
                                 # genitive marker and pronouns
                                 7: (-1, 0, 1, 5),
                                 8: (-1, 0, 1, 5, 6),
                                 9: (-1, 1, 5, 6, 8),
                                10: (-1, 0, 2, 4),
                                11: (-1, 0, 2, 4, 5),
                                # adjectives, determiners
                                12: (0, 2, 4, 6, 8, 10),
                                13: (1, 3, 5, 7, 9, 11),
                                14: (-1, 1, 3, 5, 7, 9),
                                15: (2, 4, 6, 8, 10, 12),
                                16: (3, 5, 7, 9, 11, 13),
                                17: (3, 5, 7, 8, 9),
                                # adverbs
                                18: (-5, -3, 0, 1, 2, 3, 4),
                                19: (-5, -3, 0, 1),
                                20: (-5, -3, 0, 2, 5),
                                21: (-5, -3, 0, 2, 5, 6, 11),
                                # verbs
                                22: (-7, 0, 1, 2, 6),
                                23: (-7, 0, 1, 2, 6, 8),
                                24: (-7, 0, 1, 2, 6, 9),
                                25: (-7, -1, 1, 2, 6, 7),
                                26: (-7, -3, 1, 4, 6, 7),
                                27: (-7, -3, 0, 2, 4, 6, 10),
                                # fillers
                                28: (3, 4, 5),
                                29: (3, 4, 5, 9),
                                30: (3, 4, 5, 10),
                                # conjunctions, modal auxiliary, and prepositions 
                                31: (5, 6, 7),
                                32: (5, 6, 7.5, 9),
                                33: (5, 6, 7, 10),
                                # foreign words and interjections
                                34: (0.5, 2.5, 3.5, 5.5, 9.5),
                                35: (-0.5, 2.5, -3.5, 5.5, 12.5)}
    
    def __parse_pos_create_chords_and_bass(self, text):
        text = nltk.word_tokenize(text)
        average = math.floor(sum(map(len, text)) / len(text))
        meter = 4
        if int(average) % 2 == 1:
            meter = 3
        tags = nltk.pos_tag(text)
        chords = []
        for pos in tags:
            chords.append(self.chord_to_voicing_dictionary[self.pos_to_chord_dictionary[pos[1]]])
        durations = []
        for p in tags:
            if p[1]=="VB" or p[1]=="VBD" or p[1]=="VBG" or p[1]=="VBN" or p[1]=="VBP" or p[1]=="VBZ":
                durations.append(meter * 2)
            else:
                durations.append(meter)
        bass = []
        for pos in tags:
            bass.append(self.chord_bass_to_bass_line_dictionary[self.pos_to_chord_bass_dictionary[pos[1]]])
        p = tags[0][1]
        b_dur = meter
        if p=="VB" or p=="VBD" or p=="VBG" or p=="VBN" or p=="VBP" or p=="VBZ":
            b_dur *= 2
        chords_bass_and_durations = {}
        chords_bass_and_durations["chords"] = chords
        chords_bass_and_durations["chord_durations"] = durations
        chords_bass_and_durations["bass_line"] = bass
        chords_bass_and_durations["bass_durations"] = self.duration_to_bass_rhythm_dictionary[b_dur]        
        return chords_bass_and_durations
    
    def __parse_consonants_create_rhythms(self, text):
        # replace target digraphs with "unused" characters"
        text.replace("CH", "č")
        text.replace("Ch", "č")
        text.replace("ch", "ç")
        text.replace("cH", "ç")
        text.replace("Th", "Þ")
        text.replace("TH", "Þ")
        text.replace("th", "ð")
        text.replace("tH", "ð")
        text.replace("Sh", "ṣ")
        text.replace("SH", "ṣ")
        text.replace("sh", "ʃ")
        text.replace("sH", "ʃ")
        text.replace("Ph", "ɸ")
        text.replace("PH", "ɸ")
        text.replace("ph", "f")
        text.replace("pH", "f")
        # split the words by " "        
        text = text.split(" ")
        # Get rid of the non-letters in each of the array members
        for i in range(0, len(text)):
            text[i] = re.sub("[^BCDFGJKPQSTVXZHbcdfgjkpqstvxzh\.\"\'\,\;\:\č\ç\Þ\ð\ṣ\ʃ\ɸ]", "", text[i])
        # Any members that are "" convert to " "
        for i in range(0, len(text)):
            if text[i] == "":
                text[i] = " "
        perc_version = ""
        for phrase in text:
            perc_version += "["
            for i in range(0, len(phrase)):
                perc_version += self.letter_to_rhythm_dictionary[phrase[i]]
            perc_version += "]"
        perc_version = perc_version.replace("[]", ".")
        return perc_version
        
    def parse_string(self, text):
        """takes a string of text, returns a dictionary of pos, consonants, vowels"""
        dictionary = {}
        dictionary["pos"] = self.__parse_pos_create_chords_and_bass(text)
        dictionary["consonants"] = self.__parse_consonants_create_rhythms(text)
        print("Starting sentence: " + text)
        print(dictionary["consonants"])
        print(dictionary["pos"])
        print("\n")
        self.__play_music(dictionary)
    
    def __play_music(self, dictionary):
        if time.clock() - self.previous_time > 15:
            self.__set_root_and_scale()                  
        FoxDot.r0 >> FoxDot.play("X...o...X..Xo...", sample=1, amp=1.2)
        FoxDot.r1 >> FoxDot.play(dictionary["consonants"], amp=0.8)
        notes = []
        for c in dictionary["pos"]["chords"]:
            notes.append(c)
        durations = []
        for d in dictionary["pos"]["chord_durations"]:
            durations.append(d)
        FoxDot.c1 >> FoxDot.scatter(notes, dur=durations)
        FoxDot.b1 >> FoxDot.dirt(dictionary["pos"]["bass_line"], dur=dictionary["pos"]["bass_durations"])
        
    def __set_root_and_scale(self):
        selection = random.choice(self.key)
        FoxDot.Root.default.set(selection[0])        
        FoxDot.Scale.default.set(selection[1])        