import fontforge
import sys

font = fontforge.open(sys.argv[1])
missing = set()

for lookup in font.gsub_lookups + font.gpos_lookups:
    kind = font.getLookupInfo(lookup)[0]
    for subtable in font.getLookupSubtables(lookup):
        if "context" in kind:
            # no API to get the context
            pass
        elif "gsub" in kind:
            for glyph in font.glyphs():
                for possub in glyph.getPosSub(subtable):
                    missing.update([n for n in possub[2:] if n not in font])
if missing:
    print "Font is missing: %s" % " ".join([n for n in missing])
    sys.exit(1)
