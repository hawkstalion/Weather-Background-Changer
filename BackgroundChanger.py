import urllib
import os
import subprocess
import sys
import re

weather = []
typesOfWeather = ["clear","rain","cloudy","sunny","shower"]

backgrounds = os.getenv("HOME") + '/.background/' #location of images to use for backgrounds
images = "http://dl.dropbox.com/u/17715314/" #location of images online, public dropbox folder for now

cel = degree_symbol = unichr(176).encode("latin-1") + "C"
far = degree_symbol = unichr(176).encode("latin-1") + "F"#only way to get the degree symbol to print

def download(location,url): #function to download webpage
	webFile = urllib.urlopen(url)
	localFile = open(location, 'w')
	localFile.write(webFile.read())
	webFile.close()
	localFile.close()
	
def checkImages(): #checks if the backgrounds location has all the images
	for types in typesOfWeather:
		if not os.path.exists(backgrounds + types + '.jpg'):
			download(backgrounds + types + '.jpg',images + types + '.jpg')#if not download them

def getLocationData():#downloads the webpage and parses the weather station out
	download('locationData','http://www.ip2location.com')
	
	for line in open("locationData"):
		if "for=\"chkWeather\"" in line: 
			weather.append(line) 

	location = weather[1].split('>') 
	location = location[2].split('<')

	result = location[0].split('(')
	result1 = result[1].split(')')

	final = result[0] + result1[0]
	final = final.split(' ') #parses the location out of the HTML
	
	os.remove('locationData')
	return final

def getWeatherData(location): #gets the weather.com page and returns it
	page = urllib.urlopen("http://www.weather.com/weather/today/" + location[0] +"+" + location[1])
	return page.read()	
	
def getWeather(page):#parses the weather status fr
	weather = []
	weather=re.compile('<span class="wx-value" itemprop="weather-phrase">(.*?)</span>').search(page)
	currentWeather =  weather.group(1)
	return currentWeather.lower() #gets the current weather from the page
	
def getTemp(page):	
	temp = []
	temp=re.compile('<span class="wx-value" itemprop="temperature-fahrenheit">(.*?)</span>').search(page)
	return temp.group(1) #gets the current temp from the page
	
def getScreenSize():	
	output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]
	output = output.rstrip('\n') ##previous commands returns a trailing \n so rstrip removes it
	return output
		
def convertToCel(currentTemp):
	currentTemp = ((int(currentTemp) - 32) * 5/9)
	currentTemp = str(currentTemp)
	return currentTemp

def setBackground(currentTemp,currentWeather,output):	
	outputs = output.split('x')
	outputs[0] = str(int(outputs[0]) - 200)
	
	for i in range(0,len(typesOfWeather)): #checks what kind of weather it is
		if typesOfWeather[i] in currentWeather: #picks what background to use and add weather status and tempature text to it
			if(len(sys.argv) > 1):
				if(sys.argv[1] == 'c'):
					os.system('convert ' + backgrounds + typesOfWeather[i] + '.jpg -resize ' + output + '! -font Bookman-DemiItalic -pointsize 48 -stroke White -draw \"text ' + outputs[0] + ',70 \'' +currentWeather + '\'\" ' + backgrounds + 'now.jpg')
					os.system('convert ' + backgrounds + 'now.jpg -resize ' + output + '! -font Bookman-DemiItalic -pointsize 48 -stroke White -draw \"text ' + outputs[0] + ',120 \'' +currentTemp + cel + '\'\" ' + backgrounds + 'now.jpg')
					break
			else:#convert is a linux tool to add text to images and resize them to match the screen size
				os.system('convert ' + backgrounds + typesOfWeather[i] + '.jpg -resize ' + output + '! -font Bookman-DemiItalic -pointsize 48 -stroke White -draw \"text ' + outputs[0] + ',70 \'' +currentWeather + '\'\" ' + backgrounds + 'now.jpg')	
				os.system('convert ' + backgrounds + 'now.jpg -resize ' + output + '! -font Bookman-DemiItalic -pointsize 48 -stroke White -draw \"text ' + outputs[0] + ',120 \'' +currentTemp + far + '\'\" ' + backgrounds + 'now.jpg')
				break
				
	os.system('gsettings set org.gnome.desktop.background picture-uri "file:///' + backgrounds + 'now.jpg"') #sets background only works in gnome		

def main():

	if not os.path.exists(backgrounds): #check if directory for backgrounds exist
		os.makedirs(backgrounds)#if it doesnt create it
	
	checkImages()	
	location = getLocationData()
	page = getWeatherData(location)
	currentWeather = getWeather(page)
	currentTemp = getTemp(page)
	if(len(sys.argv) > 1):
		if(sys.argv[1] == "c"):
			currentTemp = convertToCel(currentTemp)
	output = getScreenSize()
	setBackground(currentTemp,currentWeather,output)
	
if __name__ == "__main__":
    main()
