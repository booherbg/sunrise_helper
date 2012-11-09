# -*- coding: iso-8859-1 -*-
#^-- for the copyright symbol (c)
'''
Try not to run this directly...

run view.py instead

Blaine Booher
Ault Park Sunrise
http://aultparksunrise.com
http://github.com/booherbg/sunrise_helper

'''
from __future__ import division #for float division, not integer division
import os
import glob
import sys
import datetime

#import pdb;pdb.set_trace()
if len(sys.argv) > 1:
    files = sys.argv[1:]
else:
    files = glob.glob("*.jpg")
a_label='  © aultparksunrise.com %s' % (datetime.datetime.now().year)
#a_label=''
resize = 1280 #width to resize to
fontsize_wide = 29 #font size for widescreen pictures
fontsize_normal = 20 #font size for normal 4:3 pictures 

class UnknownAspectRatio(Exception): pass

def htmlOutput(filename, dimensions):
    '''Creates the necessary xhtml output for wordpress based on the filenames
        and today's date
        
        filenames is a list of filename, dimension pairs like this:
        [('00_sunrise_4nn.jpg', (1024,768)),
         ('01_overlook_4nn.jpg', (1024,768))]
         
        <p style="text-align: center;">
        <a href="http://aultparksunrise.files.wordpress.com/2011/05/37_aphids_on_stem_4nn.jpg">
        <img class="aligncenter size-large wp-image-1026" title="37_aphids_on_stem_4nn" src="http://aultparksunrise.files.wordpress.com/2011/05/37_aphids_on_stem_4nn.jpg?w=1024" alt="" width="1024" height="768" />
        </a>Aphids on a tree</p>
    <p style="text-align: left;">Lorem Ipsum</p>
    '''
    
    html = '''<p style="text-align: center;"><a href="http://aultparksunrise.files.wordpress.com/%d/%#02d/%s" alt="click for higher quality!"><img class="aligncenter size-large" title="%s" src="http://aultparksunrise.files.wordpress.com/%d/%#02d/%s?w=%d" width="%d" height="%d"/></a>Caption</p>\n\n'''
    date = datetime.datetime.now()
    year = date.year
    month = date.month
    width, height = dimensions
    sys.stdout.write(html % (year, month, filename, filename, year, month, filename, width, width, height))
    
    
def process(f, output):
    label = a_label
    html_queue = []
    #sys.stderr.write('process\n')
    if "_4nn." in f:
        return False
    skip_annotate = False
    
    # What could go wrong?
    width, height = map(float, os.popen("identify '%s'" % f).read().split()[2].split("x"))
    aspect = (width / height)
    #sys.stderr.write("%s\n" % aspect)
    #import pdb;pdb.set_trace()
    gravity = "SouthEast"
    print aspect
    if abs(aspect - 1.78) <= 0.1:
        # Widescreen Mode
        if width <= 2600:
            # unsure of where this resolution came from. imgur??
            fontsize = fontsize_wide - 6
        else:
            fontsize = fontsize_wide
    elif abs(aspect - 1.33333) <= 0.1:
        # Normal Mode
        fontsize = fontsize_normal
    elif abs(aspect - 0.66) <= 0.05:
        # Widescreen Mode sideways
        if width <= 1500:
            fontsize = fontsize_wide - 8
        else:
            fontsize = fontsize_wide + 15
    elif abs(aspect - 0.75) <= 0.1:
        # Normal Mode sideways
        fontsize = fontsize_normal - 2
    elif abs(aspect - 0.56) <= 0.1:
        # Widescreen Mode sideways
        if width <= 1500:
            fontsize = fontsize_wide - 8
        else:
            fontsize = fontsize_wide
    elif abs(aspect - 1.65818) <= 0.1:
        # Special Sunrise/Bike Eden Park Gradient
        fontsize = fontsize_wide - 6
    elif abs(aspect - 1.16117) <= 0.1:
        # Web high dev image
        # special case for shorpy.com - no (c) ault park
        fontsize = fontsize_normal - 2
        
    elif abs(aspect - 1.50000) <= 0.1:
        # Tara's photos, also from Canon SLR
        fontsize = fontsize_normal + 20
    else:
        # Unknown Aspect Ratio
        sys.stderr.write("#"*80)
        sys.stderr.write("\n");
        sys.stderr.write("error, %s unknown aspect ratio %d/%d=%.5f\n" % (f, width, height, width/height))
        sys.stderr.write("**** skipping ****\n")
        return False
        
    if width == 1280:
        # probably taken with cell phone
        fontsize = 12
    #convert Cincinnati-Tiara.jpg -fill white -undercolor '#00000080' -gravity \
    # SouthWest -font helvetica-bold -pointsize 36 \
    # -annotate +0+5 '  http://aultparksunrise.com © Blaine Booher 2011' \
    # -resize 1280x Cincinnati-Tiara_4nn.jpg
    cmd = '''convert %s -auto-orient -fill white -undercolor '#00000080' -gravity %s \
    -font helvetica-bold -pointsize %d -annotate +0+5 '%s'  -resize %d %s
    ''' % (f, gravity, fontsize, label, resize, output)
    #cmd = '''convert %s label:'%s' -fill white -background black -gravity %s -font helvetica-bold \
    #-pointsize %d -append -resize %d %s''' % (f, label, gravity, fontsize, resize, output)
    #sys.stderr.write("%s\n" % cmd)
    os.popen(cmd)
    
    # For xhtml output - these dimensions may be buggy, so keep an eye on them
    x, y = map(float, os.popen("identify '%s'" % output).read().split()[2].split("x"))
    # 1024 is default width of web page
    if (x > y):
        # horizontal - 1024xH
        width = 1024
        height = width*(y/x)
    else:
        # vertical - Wx1024
        height = 1024
        width = height*(x/y)
    html_filename = os.path.basename(output)
    htmlOutput(html_filename.lower(), (width, height))
    
if __name__ == "__main__":
    for f in files:
        process(f, '%s_4nn.jpg' % os.path.splitext(f)[0])
