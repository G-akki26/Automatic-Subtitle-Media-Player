import sys
import gi
import autosub_app as app
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
gi.require_version('GdkX11', '3.0')
from gi.repository import GdkX11

import vlc

MRL = ""

class ApplicationWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Python-Vlc Media Player")
        self.player_paused=False
        self.is_player_active = False
        self.connect("destroy",Gtk.main_quit)
           
    def show(self):
        self.show_all()

    def _realized(self, widget, data=None):
        self.vlcInstance = vlc.Instance("--no-xlib")
        self.player = self.vlcInstance.media_player_new()
        win_id = widget.get_window().get_xid()
        self.player.set_xwindow(win_id)
        self.player.set_mrl(MRL)
        self.player.play()
        self.playback_button.set_image(self.pause_image)
        self.is_player_active = True    
        
    def setup_objects_and_events(self):
        self.playback_button = Gtk.Button()
        self.stop_button = Gtk.Button()
        self.subhi_button = Gtk.Button.new_with_label("Hindi")
        self.suben_button = Gtk.Button.new_with_label("English")

        self.play_image = Gtk.Image.new_from_icon_name(
                "gtk-media-play",
                Gtk.IconSize.MENU
            )
        self.pause_image = Gtk.Image.new_from_icon_name(
                "gtk-media-pause",
                Gtk.IconSize.MENU
            )
        self.stop_image = Gtk.Image.new_from_icon_name(
                "gtk-media-stop",
                Gtk.IconSize.MENU
            )
        # self.suben_image = Gtk.Image.new_from_icon_name(
        #         "gtk-media-subtitle1",
        #         Gtk.IconSize.MENU
        #     )
        # self.subhi_image = Gtk.Image.new_from_icon_name(
        #         "gtk-media-menu",
        #         Gtk.IconSize.MENU
        #     )
        
        self.playback_button.set_image(self.play_image)
        self.stop_button.set_image(self.stop_image)
        # self.subhi_button.set_image(self.subhi_image)
        # self.suben_button.set_image(self.suben_image)

        self.playback_button.connect("clicked", self.toggle_player_playback)
        self.stop_button.connect("clicked", self.stop_player)
        self.subhi_button.connect("clicked", self.subhi_gen)
        self.suben_button.connect("clicked", self.suben_gen)

        self.draw_area = Gtk.DrawingArea()
        self.draw_area.set_size_request(300,300)
        
        self.draw_area.connect("realize",self._realized)

        self.progressbar = Gtk.ProgressBar()
        self.timeout_id = GLib.timeout_add(50, self.on_timeout, None)
        
        self.hbox = Gtk.Box(spacing=6)
        self.hbox.pack_start(self.playback_button, True, True, 0)
        self.hbox.pack_start(self.stop_button, True, True, 0)
        self.hbox.pack_start(self.subhi_button, True, True, 0)
        self.hbox.pack_start(self.suben_button, True, True, 0)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.vbox)
        self.vbox.pack_start(self.draw_area, True, True, 0)
        self.vbox.pack_start(self.hbox, False, False, 0)
        self.vbox.pack_start(self.progressbar, True, True, 0)

    def on_timeout(self, user_data):
        """
        Update value on the progress bar
        """
             
        new_value =  self.player.get_position()
        
        if new_value > 1:
            new_value = 0

        self.progressbar.set_fraction(new_value)

        # As this is a timeout function, return True so that it
        # continues to get called
        return True    

    def stop_player(self, widget, data=None):
        self.player.stop()
        self.is_player_active = False
        self.playback_button.set_image(self.play_image)
        
    def toggle_player_playback(self, widget, data=None):

        """
        Handler for Player's Playback Button (Play/Pause).
        """

        if self.is_player_active == False and self.player_paused == False:
            self.player.play()
            self.playback_button.set_image(self.pause_image)
            self.is_player_active = True

        elif self.is_player_active == True and self.player_paused == True:
            self.player.play()
            self.playback_button.set_image(self.pause_image)
            self.player_paused = False

        elif self.is_player_active == True and self.player_paused == False:
            self.player.pause()
            self.playback_button.set_image(self.play_image)
            self.player_paused = True
        else:
            pass    

    def subhi_gen(self, widget, data=None):
        self.player.stop()
        self.is_player_active = False
        self.playback_button.set_image(self.play_image)

        app.main("hi","hi",MRL)
        subtitle_path = MRL[:len(MRL)-3]
        subtitle_path = subtitle_path + 'srt'

    def suben_gen(self, widget, data=None):
        self.player.stop()
        self.is_player_active = False
        self.playback_button.set_image(self.play_image)
        
        app.main("en","en",MRL)
        subtitle_path = MRL[:len(MRL)-3]
        subtitle_path = subtitle_path + 'srt'        

    

if __name__ == '__main__':
    if not sys.argv[1:]:
       print "Exiting \nMust provide the MRL."
       sys.exit(1)
    if len(sys.argv[1:]) == 1:
        MRL = sys.argv[1]
        window = ApplicationWindow()
        window.setup_objects_and_events()
        window.show()
        Gtk.main()
        window.player.stop()
        window.vlcInstance.release()