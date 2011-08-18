from __future__ import division
import pygtk; pygtk.require('2.0')
import gtk
import glob
import os
import annotate
import sys
import datetime

if len(sys.argv) > 1:
    files = sys.argv[1:]
else:
    files = glob.glob("*.jpg")
    
for f in files:
    sys.stderr.write("%s\n" % f)

func = annotate.process
class Image_Example(object):

    def pressButton(self, widget, data=None):
        self.set_next()

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()
        
    def set_image(self, fname):
        pb = gtk.gdk.pixbuf_new_from_file(fname)
        width = pb.get_width()
        height = pb.get_height()
        ratio = width / height
        self.image.set_from_pixbuf(pb.scale_simple(int(400*ratio),400,gtk.gdk.INTERP_BILINEAR))
        
    def set_next(self):
        self.index += 1
        if self.index >= len(self.flist):
            self.index = 0
        fname = self.flist[self.index]
        self.set_image(fname)
        
    def process(self):
        quit = False
        for index, fname in enumerate(self.flist):
            if "_4nn." in fname:
                continue
            self.set_image(fname)
            name = ''
            while True:
                name = self.dialog()
                day_of_year = int(datetime.datetime.now().strftime("%j"))
                rename = '%#03d_%#02d_%s_4nn.jpg' % (day_of_year, index, name)
                if name == 'exit':
                    quit = True
                    break
                elif name.strip() == '':
                    continue
                else:
                    break
            if quit:
                break
                
            func(fname, os.path.join(os.path.split(fname)[0], rename))
            #sys.stderr.write("%s\n" % rename)
           

    def __init__(self, flist):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)
        self.window.move(300,20)

        self.button = gtk.Button()
        self.button.connect("clicked", self.pressButton, None)
        #self.button.connect_object("clicked", gtk.Widget.destroy, self.window)

        self.image = gtk.Image()
        self.image.show()

        self.button.add(self.image)
        self.window.add(self.button)
        self.button.show()
        self.window.show()
        self.flist = flist
        self.index = -1
        self.process()
        #self.set_next()

    def main(self):
        gtk.main()
        
    def responseToDialog(self, entry, dialog, response):
        dialog.response(response)

    def dialog(self):
        # With some help from http://ardoris.wordpress.com/2008/07/05/pygtk-text-entry-dialog/
        #base this on a message dialog
        dialog = gtk.MessageDialog(
            None,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_QUESTION,
            gtk.BUTTONS_OK,
            None)
        dialog.move(300,500)
        dialog.set_markup('Please enter the filename, xx_filename.jpg')
        #create the text input field
        entry = gtk.Entry()
        entry.connect("activate", lambda x,y,z: y.response(z), dialog, gtk.RESPONSE_OK)
        hbox = gtk.HBox()
        #hbox.pack_start(gtk.Label("Name:"), False, 5, 5)
        hbox.pack_end(entry)
        #add it and show it
        dialog.vbox.pack_end(hbox, True, True, 0)
        dialog.show_all()
        dialog.run()
        text = entry.get_text()
        dialog.destroy()
        return text



if __name__ == '__main__':
    im = Image_Example(files)
    im.main()

