import os
import subprocess
import sys

os.system('wget -O location.html www.ip2location.com') #download webpage with location details

weather = []
typesOfWeather = ["clear","rain","cloudy","sunny","showers"] #list of possible weather types
backgrounds = os.getenv("HOME") + '/background/' #location of images to use for backgrounds
images = "http://dl.dropbox.com/u/17715314/" #location of images online, public dropbox folder for now
cel = degree_symbol = unichr(176).encode("latin-1") + "C"
far = degree_symbol = unichr(176).encode("latin-1") + "F"

if not os.path.exists(backgrounds): #check if directory for backgrounds exist
    os.makedirs(backgrounds)		#if it doesnt create it
    
for types in typesOfWeather: #checks if the backgrounds location has all the images
	if not os.path.exists(backgrounds + types + '.jpg'):
		os.system('wget -O ' + backgrounds + types + '.jpg ' + images + types + '.jpg') #if not download them

for line in open("location.html"):
 if "for=\"chkWeather\"" in line: #looks for weather station section 
   weather.append(line) #and grabs the line its on

location = weather[1].split('>') 
location = location[2].split('<')

result = location[0].split('(')
result1 = result[1].split(')')
final = result[0] + result1[0]
final = final.split(' ') #parses the location out of the HTML
 
os.system('wget -O weather.html http://www.weather.com/weather/today/' + final[0] + '+' +final[1]) #download the weather page for the correct location

weather = []
for line in open("weather.html"):
	if "itemprop=\"weather-phrase\"" in line:#looks for weather status now section
		weather.append(line) #and grabs the line its on

temp = []		
for line in open("weather.html"):
	if "itemprop=\"temperature-fahrenheit\">" in line: #looks for the current temp
		temp.append(line) #and grabs the line its on		

output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]
output = output.split('\n') #adds a trailing newline for some reason
		
currentWeather = weather[0].split('>')
currentWeather = currentWeather[1].split('<') #parses the weather status out e.g cloudy etc.
currentWeather = currentWeather[0].lower() #converts it to lowercase easier to compare

currentTemp = temp[0].split('>') #parses out the temp from the HTML
currentTemp = currentTemp[1].split('<') #currentTemp[0] holds the tempature in Fahrenheit

if(len(sys.argv) > 1):
	if(sys.argv[1] == "c"):
		currentTemp[0] = ((int(currentTemp[0])  -  32) * 5/9)
		currentTemp[0] = str(currentTemp[0])
		print "Cel"

for i in range(0,len(typesOfWeather)): #checks what kind of weather it is
	if typesOfWeather[i] in currentWeather: #picks what background to use and add weather status and tempature text to it
		if(len(sys.argv) > 1):
			if(sys.argv[1] == 'c'):
				os.system('convert ' + backgrounds + typesOfWeather[i] + '.jpg -resize ' + output[0] + '! -font Bookman-DemiItalic -pointsize 48 -stroke White -draw \"text 25,70 \'' +currentWeather + ' ' + currentTemp[0] + cel + '\'\" ' + backgrounds + 'now.jpg')
				print "CEL"
			else:
				os.system('convert ' + backgrounds + typesOfWeather[i] + '.jpg -resize ' + output[0] + '! -font Bookman-DemiItalic -pointsize 48 -stroke White -draw \"text 25,70 \'' +currentWeather + ' ' + currentTemp[0] + far + '\'\" ' + backgrounds + 'now.jpg')	
				print "FAR"
		os.system('gsettings set org.gnome.desktop.background picture-uri "file:///' + backgrounds + 'now.jpg"') #sets background only works in gnome
