from . import AbstractPlayer
import vlc

class VLCPlayer(AbstractPlayer):
    def __init__(self):
        self.player = vlc.MediaPlayer()
        self.program = None

    def open(self, program):
        self.player.set_mrl(program.media.path)

    def play(self):
        self.player.play()

    def stop(self):
        self.player.stop()

    def wait(self):
        while self.player.is_playing():
            pass


