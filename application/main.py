import sys
import os

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../')

import Classes.game as Game

def main():

	game = Game.Game()

	game.play()


main()