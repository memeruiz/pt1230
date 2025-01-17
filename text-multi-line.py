#!/usr/bin/env python3
from optparse import OptionParser
import math, os, sys
from subprocess import check_output
from functools import reduce

class Label(object):
    def __init__(self, text_lines_list, font="Times New Roman", fontsize=100, complete_line_width=64):
        self.text_lines_list=text_lines_list
        self.font=font
        self.complete_line_width=complete_line_width
        self.set_fontsize(fontsize)

    def set_fontsize(self, fontsize):
        self.fontsize=fontsize
        self.each_line_width=int(self.fontsize*0.01*(self.complete_line_width/len(self.text_lines_list)))
        #print("each line width: ", self.each_line_width)
        self.rest_width=self.complete_line_width-self.each_line_width*len(self.text_lines_list)
        #print("Rest width: ", self.rest_width)


    def get_max_length(self):
        self._text_lines_byte_list=[]
        max_length=0
        for line in self.text_lines_list:
            #print("line: ", line)
            bytes_result=check_output(["textlabel","--font", "\""+str(self.font)+"\"", "--width", str(self.each_line_width), line])
            self._text_lines_byte_list.append(bytes_result.split(b"\n")[:-1])
            #print("bytes list:\n", self._text_lines_byte_list[-1])
            #print("line lenght: ", len(self._text_lines_byte_list[-1]))
            if len(self._text_lines_byte_list[-1]) > max_length:
                max_length=len(self._text_lines_byte_list[-1])
        #print("Max length: ", max_length)
        return(max_length)

    def fill_lines(self, max_length):
        #print("Filling lines!!! \n \n")
        for i,line in enumerate(self._text_lines_byte_list):
            #print("line: "+str(i)+"  "+str(line))
            #print("Filling "+str((max_length-len(line))//2)+" zeros")
            diff=(max_length-len(line))//2
            more=(max_length-len(line))%2
            for j in range(diff):
                self._text_lines_byte_list[i].insert(0, b'0'*len(line[0]))
            for j in range(diff+more):
                self._text_lines_byte_list[i].append(b'0'*len(line[0]))

    def add_extra_cols(self):
        self._final_render_bytes=[]
        extra_margin=self.rest_width//2
        rest_extra_margin=self.rest_width%2
        for i, line in enumerate(self._pre_final_render_bytes):
            self._final_render_bytes.append(b'0'*extra_margin+line+b'0'*(extra_margin+rest_extra_margin))




    def get_render(self):
        max_length=self.get_max_length()
        self.fill_lines(max_length)
        for line in self._text_lines_byte_list:
            #print("length of line is: ", len(line))
            #print(line)
            pass
        self._text_lines_byte_list.reverse()
        self._pre_final_render_bytes=([reduce(lambda x,y:x+y, i) for i in zip(*self._text_lines_byte_list)])
        self.add_extra_cols()
        final_render=[]
        for line in self._final_render_bytes:
            final_render.append(line.decode("utf-8"))
        return(final_render)



if __name__=="__main__":
    parser = OptionParser()
    parser.add_option("-f", "--font", action="store", type="string",
                      dest="font", default="Times New Roman", help="font used by textlabel")
    parser.add_option("-s", "--font-size", type="int", dest="fontsize",
                      default=100, help="font size percentage")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")

    (options, args) = parser.parse_args()
    text=args[0]
    if text=="-":
        text=sys.stdin.read()
    text_list=text.split("\n")

    #print("text:\n", text)
    #print("text list:\n", text_list)
    #print("Font :", options.font)
    #print("Font size percentage: ", options.fontsize)

    label=Label(text_list, font=options.font, fontsize=options.fontsize)
    for line in label.get_render():
        print(line)
    #print(len(line))

