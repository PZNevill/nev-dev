#!/usr/bin/env python
"""
script to dynamically convert json files to a flattened format

usage: python flatten_json.py -f data.json -c client1 -s , -e utf-8-sig -d 20210326 -x dat -g HealthPlans
usage w/ defaults: python flatten_json.py -f data.json -c client1
"""
__author__ = "Philip Nevill"

import argparse
import datetime
import json
import logging

logging.basicConfig(
	format='%(asctime)s %(levelname)-8s %(message)s',
	level=logging.INFO,
	datefmt='%Y-%m-%d %H:%M:%S'
)

# parse parameters
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str, help="name/path of the data to be converted", required=True)
parser.add_argument("-fn", "--file_name", type=str, help="name of file to be generated", default=None)
parser.add_argument("-c", "--client", type=str, help="client for which the json was provided", required=True)
parser.add_argument("-s", "--separator", type=str, help="flat file separator", default="|")
parser.add_argument("-e", "--encoding", type=str, help="specify file encoding if different than utf-8", default="utf-8")
parser.add_argument("-d", "--date", type=str, help="should represent the tday used in metl process", default=datetime.datetime.now().strftime("%Y%m%d"))
parser.add_argument("-x", "--extension", type=str, help="extension of the outputted file", default="txt", choices=["dat","txt","csv"])
parser.add_argument("-g", "--groupby", type=str, help="inflate flat file by a specific branch", default=None)
args = parser.parse_args()


def flatten_json(raw_data):
	"""wrapper function for flatten()"""
	out = {}

	def flatten(x, name=""):
		"""function to convert json to a flat format"""

		if type(x) is dict:
			for a in x:
				flatten(x[a], name + a + "_")

		elif type(x) is list:
			j = 1
			for a in x:
				flatten(a, name + str(j) + "_")
				j += 1

		else:
			out[name[:-1]] = x

	flatten(raw_data)
	return out


def main(file, filename, client, date, ext, enc, sep, groupby):
	"""main processing routine"""

	def format_row(data, row, index, sep):
		if str(data).find(sep) != -1:
			return sep + add_quote(str(data)) if row is not None else add_quote(str(data))
		else:
			return sep + str(data) if row is not None else str(data)

	def lower_then_sort(elem):
		"""nested function to lower an element for sort"""
		return elem.lower()

	def add_quote(x):
		"""nested function to add quotes when sep is found in string"""
		return '"%s"' % x

	def get_row(data, header, sep, groupby=None, groupby_header=None):
		"""nested function to retrieve row from flattened data"""
		if groupby is not None:
			rows = set([])
			counter = set([])
			groupby_keys = {}
			# determine max number of networks
			for groupby_header_index in groupby_header:
				# grab groupby data from row
				if groupby_header_index in data:
					# necessary variables from parsed data
					parsed_key = groupby_header_index.split("_")[-1:][0]
					parsed_counter = int(groupby_header_index.split("_")[1])
					# initialize a list if key has not been called yet
					if parsed_key not in groupby_keys.keys():
						groupby_keys[parsed_key] = {}
					# add data and increase counter
					groupby_keys[parsed_key][parsed_counter] = data[groupby_header_index]
					counter.add(parsed_counter)

			for counter_index in counter:
				row = None
				for header_key in header:
					original_key = "%s_%s_%s" % (groupby, counter_index, header_key)
					if original_key in data:
						r = format_row(data[original_key], row, header_key, sep)
						if row is not None:
							row += r
						else:
							row = "" + r
					elif header_key in data:
						r = format_row(data[header_key], row, header_key, sep)
						if row is not None:
							row += r
						else:
							row = "" + r
					else:
						r = format_row("", row, header_key, sep)
						if row is not None:
							row += r
						else:
							row = "" + r

				rows.add(row + "\n")
			return "".join(rows)
		else:
			row = None
			for header_index in header:
				if header_index in data:
					r = format_row(data[header_index], row, header_index, sep)
					if row is not None:
						row += r
					else:
						row = "" + r
				else:
					r = format_row("", row, header_index, sep)
					if row is not None:
						row += r
					else:
						row = "" + r

			return row + "\n"

	# parse json
	try:
		with open(file, encoding=enc) as serialized_data:
			data = json.load(serialized_data)  # deserialized data
			parent_branch = list(data.keys())[0]  # retreive top branch that defines file type
	except Exception as e:
		raise e

	# define header
	try:
		header = set([])
		groupby_header = None
		# run through data to create comprehensive header
		for row in data[parent_branch]:
			flat_row = flatten_json(row)
			for key in flat_row.keys():
				header.add(key)

		# routine to redefine header if a groupby has been defined
		if groupby is not None:
			groupby_header = set([])

			# determine columns to be grouped
			for header_index in header:
				if groupby in header_index:
					groupby_header.add(header_index)
			# remove repeated columns and add in new singluar columns for determined groupby
			for groupby_header_index in groupby_header:
				header.remove(groupby_header_index)
				header.add(groupby_header_index.split("_")[-1:][0])

			groupby_header = sorted(groupby_header, key=lower_then_sort)

		header = sorted(header, key=lower_then_sort)
	except Exception as e:
		raise e

	# csv creation routine
	file = filename if filename is not None else "%s_%s_%s.%s" % (client, parent_branch.lower(), date, ext)
	with open(file, "w") as flat_file:
		counter = 0
		for row in data[parent_branch]:
			output_row = ""
			try:
				if counter == 0:
					output_row += sep.join(header) + "\n"  # first record is always the header
				flat_row = flatten_json(row)  # flatten passed row from parsed json
				output_row += get_row(flat_row, header, sep, groupby, groupby_header)  # format row
				flat_file.write(output_row)  # output row to file
				counter += 1
			except Exception as e:
				print("Row %s encountered an error: " % counter)
				print(row)
				raise e


if __name__ == "__main__":
	main(args.file, args.file_name, args.client, args.date, args.extension, args.encoding, args.separator, args.groupby)
