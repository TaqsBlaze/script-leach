import requests
import os
import time
import re
import warnings

warnings.simplefilter("ignore")

class Leach:
	
	def __init__(self,data):
		self.data = data
		self.temp_file = "temp.txt"
		self.split_file = "split.txt"
		self.link_file = "links.txt"
		self.regex = re.compile(r"(?<=src=)[^=].*$")
		self.wmode = "w"
		self.rmode = "r"
		self.amode = "a"
		self.downloader = requests
		
	def attach(self) -> bool:
		
		try:
			with open(self.temp_file,self.wmode) as temp:
				temp.write(self.data)
				return True
		except:
			return False

	def sip(self, target) -> set:
		
		with open(self.temp_file, self.rmode) as tempfile:
			
			data = tempfile.readlines()
		
		try:	
			for chunk in data:
					
				with open(self.link_file, self.amode) as linkfile:
							

						if chunk.startswith("<script") and target.split("//")[1] in chunk:
							
							link = re.findall(self.regex,str(chunk))
							
							try:
								link = link[0].split(" ")[0]
								print(" * Link 🔗:",link)
								linkfile.write(link+"\n")
							except:
								continue
								
			print(" * Done...")				
			return [True, self.link_file]
		except Exception as error:
					print(error)
					return [False, None]
					

	def suck_script(self,file):
				
				with open(file, self.rmode) as linkfile:
					
					link_file = linkfile.readlines()
				
				for link in link_file:
					
					try:
						file_name = link.split("/")[-1].strip("\s\n\r").replace("'","")
						data = self.downloader.get(link.strip("\n\s\r").replace("'",""))
						
						if data.status_code == 200:
							
							with open(f"{file_name}", self.wmode) as file:
								
								file.write(str(data.text))
								
					except Exception as error:
						print(error)
						return False
						
				return True
				
				
					
					

v =f'''
{'+'*48}
	Script-Leach
	by: TaqsBlaze
	
leach all urls leading to scripts from any website
{'+'*48}
'''
print(v)

url = str(input(" * Url:"))

print("* Connecting...💫")

data =requests.get(url,
	headers={"User-Agent":"Android"}
)

#print(data.text)
if data.status_code == 200:
	leach = Leach(data.text)
	
	if leach.attach():
		sip = leach.sip(url)
		if sip[0]:
			print(" * Got all links...😎")
			print(" * Would you like to download found js scripts")
			download = str(input(" * y/n:"))
			
			if download.lower() == "y":
				get_files = leach.suck_script(sip[1])
				if get_files:
					print(" * Script files downloaded..📑")
				else:
					print(" * Failed to download scripts..🚫")
			elif download.lower() == "n":
				print(" * We are done...")
				exit()
			else:
				print(" * Out of bound⚠️")
				exit()
		else:
			print(" * Failed to attach...😢")
		
	else:
		print(" * Failed to attach...😢")
		
else:
	exit()

