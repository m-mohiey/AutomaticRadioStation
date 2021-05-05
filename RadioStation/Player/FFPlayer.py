from . import AbstractPlayer
import subprocess

class FFPlayer(AbstractPlayer):
    def __init__(self):
        self.command = 'ffplay -hide_banner -autoexit -nodisp -i "{}"'
        self.player = None
        self.path = None

    def open(self, program):
        self.path = program.media.path

    def play(self):
        self.player = subprocess.Popen(self.command.format(self.path), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def stop(self):
        if self.player:
            self.player.terminate()

    def wait(self):
        self.player.wait()