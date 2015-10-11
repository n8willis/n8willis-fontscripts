#!/usr/bin/env python
#
#   Copyright (C) 2015, Nathan Willis
#   nwillis /atsign/ glyphography /dotcom/
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see "http://www.gnu.org/licenses/".
#
#   This is a FontForge script that recursively rebuilds the compound glyphs
#   in a font. I.e., all glyphs that are a letter with one diacritic are
#   rebuilt first, followed by all glyphs that use two diacritics, then
#   three, etc.  
#
#   This produces better results than simply selecting all composites and
#   running "build composite" on them, since that method stumbles on glyphs
#   that include references to references.
#
#   The script stops at three diacritics (and/or four total references),
#   since that seems to be sufficient for Latin, Greek, and Cyrillic.
#   If you want to use it with another writing system, you might need
#   to adjust for that limitation.
#
#   Also note that the script only processes the glyphs that are already
#   present; it does not generate any new compound glyphs.



import fontforge
import sys

def refresh_compound_glyphs(dummy, f):

    three_d = []
    two_d = []
    one_d = []

    for g in f.glyphs():
        length = len(g.references)

        if length < 1:
            pass
        elif length == 1:
            print "\n", g
            print "Adding to one-diacritic counter."
            one_d.append(g.encoding)
        elif length == 2:
            print "\n", g
            print g.references

            print f[g.references[0][0]]
            print f[g.references[1][0]]

            if len(f[g.references[0][0]].references) <= 1 and len(f[g.references[1][0]].references) <= 1:
                print "Adding to one-diacritic counter."
                one_d.append(g.encoding)
            else:
                print "Reference is compound; adding to two-diacritic counter."
                two_d.append(g.encoding)
        elif length == 3:
            print "\n", g
            print "Adding to two-diacritic counter."
            two_d.append(g.encoding)
        elif length == 4:
            print "\n", g
            print "Adding to three-diacritic counter."
            three_d.append(g.encoding)
        else:
            pass


    print "\nProcessing single diacritics..."
    for n in xrange(0, len(one_d)):
        f[one_d[n]].build()
        print "Building: %s" % f[one_d[n]]

    print "\nProcessing double diacritics..."
    for n in xrange(0, len(two_d)):
        f[two_d[n]].build()
        print "Building: %s" % f[two_d[n]]

    print "\nProcessing triple diacritics..." 
    for n in xrange(0, len(three_d)):
        f[three_d[n]].build()
        print "Building: %s" % f[three_d[n]]




if fontforge.hasUserInterface():
    print "Loaded progressive refresh script."
    fontforge.registerMenuItem(refresh_compound_glyphs, None, None , "Font", None, "Refresh All Compound Glyphs")

else:
    if len(argv) == 2:
        inputfile = argv[1]
        outputfile = inputfile
    elif len(argv) == 3:
        script, inputfile, outputfile = argv
    else:
        print "Usage: progressive_accents.py inputfile [outputfile]"
        exit(1)

    font = fontforge.open(inputfile)
    # print "Opening %s..." % fontfile

    refresh_compound_glyphs(None, font)

    font.save(outputfile)

    font.close()
    exit(0)

