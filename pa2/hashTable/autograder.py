#!/usr/bin/python3

# Author: @nate-blum

import os
import datetime
from random import random, sample
import subprocess

albums = [
	"Portishead", "Chromatica", "Back to Black", "Mezzanine", "OIL OF EVERY PEARL'S UN-INSIDES", "MAGDALENE", "Heaven or Las Vegas", "Homogenic", "Vespertine", "Icedancer", "Dummy", "Charli", "how i'm feeling now", "EXETER", "SAWAYAMA", "1000 gecs",
	"10,000 gecs", "Nevermind", "In Utero", "Bleach", "KiCk i", "KiCk ii", "KiCk iii", "KiCk iiii", "KiCk iiiii", "Wlfgrl", "Future Nostalgia", "Stratosphere", "Random Access Memories", "Debut", "Post", "Vulnicura", "Utopia", "Fossora", "Voulez-Vous",
	"The OOZ", "6 Feet Beneath The Moon", "Grace"
] # 38

cmds = [
	"SHOW_STOCK",
	"RESTOCK",
	"SALE"
]

def generate_test(filenum, command_count, table_start_size, album_count, path="./"):
	commands = []
	with open(f"{path}tests/test{filenum}.txt", "w") as infile:
		infile.write(f"{table_start_size}\n")

		albums_used = []		
		sub_albums = sample(albums, album_count)
		for i in range(command_count):
			rand = random()
			cmd = "RESTOCK" if i == 0 else cmds[2 if 0.55 < rand and rand <= 1\
									    else (1 if 0.1 < rand and rand <= 0.55 else 0)]
			count = 0 if cmd == "SHOW_STOCK" else round(random() * 50)
			album = sub_albums[round(random() * album_count - 1)]
			if i < (3 * (command_count / 4))\
				and (cmd == "SALE" or cmd == "SHOW_STOCK")\
				and album not in albums_used\
				and len(albums_used) > 0:
				while album not in albums_used:
					album = sub_albums[round(random() * album_count - 1)]
			
			if cmd == "RESTOCK" and album not in albums_used:
				albums_used.append(album)

			infile.write(f"{cmd} {count} {album}\n")
			commands.append((cmd, count, album))

	with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:
		stock = dict()
		table_fullness = 0
		table_size = table_start_size
		for cmd in commands:
			if cmd[0] == "SHOW_STOCK":
				if cmd[2] in stock:
					outfile.write(f"Current stock of {cmd[2]}: {stock[cmd[2]]}\n")
				else:
					outfile.write(f"No stock of {cmd[2]}\n")
			elif cmd[0] == "SALE":
				if cmd[2] not in stock:
					outfile.write(f"No stock of {cmd[2]}\n")
				elif stock[cmd[2]] - cmd[1] < 0:
					outfile.write(f"Not enough stock of {cmd[2]}\n")
				else:
					stock[cmd[2]] -= cmd[1]
			else:
				if cmd[2] in stock:
					stock[cmd[2]] += cmd[1]
				else:
					stock[cmd[2]] = cmd[1]
					table_fullness += 1
					if table_fullness >= (table_size / 2):
						outfile.write(f"Resizing the table from {table_size} to {table_size * 2}\n")
						table_size *= 2
		
		outfile.write("-------- FINAL COUNTS --------\n")
		for album, ct in stock.items():
			outfile.write(f"{album}: {ct}\n")
		outfile.write("------------------------------\n")
		

def generate_test_suite():
	os.makedirs("tests", exist_ok=True)
	os.makedirs("answers", exist_ok=True)

	for i in range(4, 8):
		generate_test(i, command_count=2**(i+1), table_start_size=2**(i-2), album_count=10+(5*(i-4)))

def test_hashTable(filenum, path = "./", verbose = False):
	try:
		with open(f"{path}answers/answer{filenum}.txt", "r") as outfile:
			answerList = []
			for line in filter(lambda l: l, outfile.read().split('\n')):
				if line:
					answerList.append(line)
			if answerList[-1] != "\n":
				answerList.append("\n")
	except EnvironmentError: # parent of IOError, OSError
		print (f"answers/answer{filenum}.txt missing")

	try:
		result = subprocess.run(
			["./hashTable", f"tests/test{filenum}.txt"],
			cwd=path,
			check=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.STDOUT,
			encoding="ASCII",
			timeout=datetime.timedelta(seconds=2).total_seconds(),
		)

		resultList = []
		for line in filter(lambda l: l, result.stdout.split("\n")):
			resultList.append(line)
		if resultList[-1] != "\n":
			resultList.append("\n")

		if verbose:
			print (' '.join(result.args))

		ans_cts_begin = answerList.index("-------- FINAL COUNTS --------")
		ans_cts_end = answerList.index("------------------------------")
		ans_final_counts = sorted(answerList[ans_cts_begin + 1:ans_cts_end])

		res_cts_begin = resultList.index("-------- FINAL COUNTS --------")
		res_cts_end = resultList.index("------------------------------")
		res_final_counts = sorted(resultList[res_cts_begin + 1:res_cts_end])

		assert all(
			[
				line1.lower().strip(" .") == line2.lower().strip(" .")
				for line1, line2 in zip(
					resultList[:res_cts_begin] + res_final_counts, 
					answerList[:ans_cts_begin] + ans_final_counts
					)
			]
		), f"The lines in your result don't match those in answers/answer{filenum}.txt."
		return True
	except subprocess.CalledProcessError as e:
		print (e.output)
		print ("Calling ./hashTable returned an error.")
	except ValueError as e:
		print (' '.join(result.args))
		print (result.stdout)
		print ("Please check your output formatting.")
	except AssertionError as e:
		print (result.stdout)
		print (e.args[0])

	return False

def grade_hashTable(path="./", verbose=False ):
	score = 0

	try:
		subprocess.run( ["make", "clean"], cwd=path, check=True, )
		subprocess.run( ["make", "-B"], cwd=path, check=True, )
	except subprocess.CalledProcessError as e:
		print ("Couldn't compile hashTable.c.")
		return score
	
	for i in range(0, 8):
		if test_hashTable(i, path, verbose):
			score += 3 if i < 7 else 4
		else:
			break

	print(f"Score on hashTable: {score} out of 25.")
	return score

if __name__ == '__main__':
	generate_test_suite()
	grade_hashTable(verbose=True)
	exit()
