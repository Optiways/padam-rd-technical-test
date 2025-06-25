SHELL := /bin/zsh

simple:
	time python main.py -i ./instances/simple_eul.txt -s blossom
	time python main.py -i ./instances/simple_semi.txt -s blossom
	time python main.py -i ./instances/simple_non.txt -s blossom
	time python main.py -i ./instances/simple_dis.txt -s blossom

simple-blossom:
	time python main.py -i ./instances/simple_eul.txt -s blossom
	time python main.py -i ./instances/simple_semi.txt -s blossom
	time python main.py -i ./instances/simple_non.txt -s blossom
	time python main.py -i ./instances/simple_dis.txt -s blossom

choose:
	time python main.py -i ./instances/hard_to_choose.txt

islands:
	time python main.py -i ./instances/islands.txt

paris:
	time python main.py -i ./instances/paris_map.txt

blossom:
	time python main.py -i ./instances/paris_map.txt -s blossom

freeze:
	pip freeze > requirements.txt

.PHONY: choose islands paris freeze simple simple-blossom
