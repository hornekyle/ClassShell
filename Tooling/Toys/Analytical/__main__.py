from gui.window import MainWindow

from cme.part1 import Function1D
from cme.part2 import Function2D
from cme.part3 import FunctionVector
from cme.part4 import Transistors
import hierarchy


def main():
	problems = [
		Function1D(),
		Function2D(),
		FunctionVector(),
		Transistors(),
		]
	window = MainWindow(problems)
	# hierarchy.graphviz(window,'tree.dot')
	window()


if __name__=='__main__': main()
