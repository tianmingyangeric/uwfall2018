def alter(file,old_str,new_str):
	file_data = ""
	with open(file, "r", encoding="utf-8") as f:
		for line in f:
			print (line,'x')
			if old_str in line:
				line = line.replace(old_str,new_str)
			file_data += line
	with open(file,"w",encoding="utf-8") as f:
		f.write(file_data)



alter("config.py", "business_id = '-yZXurhfOYlNKmH0ZyNGIQ'", "python")