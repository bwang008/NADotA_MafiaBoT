########NADOTA MAFIA BOT. Ver 0.1a#############

from selenium import webdriver
import re
import time
import configparser
import os
import math
import sys

##debug
#import pdb	

###Log###
#To-do
#Add in timer feature, modify config file to have the bot automatically post at EOD with final vote count and who died. If tied, bot rolls a random number to determine the loser.
#Add URL section to the config file so other users can easily specify their own game thread instead of going into the code.

###Define Functions###
###LOGIN INFORMATION GOES HERE
def LoginBot():
	print("Logging le bot into the system...")
	driver.get("https://forum.mafiascum.net/ucp.php?mode=login")
	time.sleep(1)
	####username####
	driver.find_element_by_xpath("""//*[@id="username"]""").send_keys("ironstove")
	driver.find_element_by_xpath("""//*[@id="autologin"]""").click()
	####password####
	driver.find_element_by_xpath("""//*[@id="password"]""").send_keys('peachfish')
	driver.find_element_by_xpath("""//*[@id="login"]/div[1]/div/div/fieldset/dl[4]/dd/input[3]""").click()
	time.sleep(1)
	#driver.find_element_by_xpath("""//*[@id="login"]/div[1]/div/div/fieldset/dl[4]/dd/input[3]""").click()
	#wait for login page to finish load before navigating away
	time.sleep(5)
	
def PostVotes():
	print("PostVotes: Posting the votes onto the forum...")
	time.sleep(5)
	driver.find_element_by_xpath("""//*[@id="cke_contents_vB_Editor_QR_editor"]/textarea""").send_keys("Beep Boop, I'm a bot. Vote count was requested.\n")
	driver.find_element_by_xpath("""//*[@id="cke_contents_vB_Editor_QR_editor"]/textarea""").send_keys("\n[b][SIZE=4]Lynch Votes:[/SIZE][/b]\n")
	for user in lynchref:
		if "PLAYERLIST" not in user and user != "":
			driver.find_element_by_xpath("""//*[@id="cke_contents_vB_Editor_QR_editor"]/textarea""").send_keys("[b]",user,"[/b]", " - ")#, ['{}, '.format(elem) for elem in lynchref[user]], "\n")
			for voter in lynchref[user]:
				driver.find_element_by_xpath("""//*[@id="cke_contents_vB_Editor_QR_editor"]/textarea""").send_keys(voter,", ")
			driver.find_element_by_xpath("""//*[@id="cke_contents_vB_Editor_QR_editor"]/textarea""").send_keys("\b\b\n")
	driver.find_element_by_xpath("""//*[@id="cke_contents_vB_Editor_QR_editor"]/textarea""").send_keys("\n[b][SIZE=4]Not Voting:[/SIZE][/b]\n")
	for player in lynchref:
		if player not in lynches and "PLAYERLIST" not in player and player != "":
			driver.find_element_by_xpath("""//*[@id="cke_contents_vB_Editor_QR_editor"]/textarea""").send_keys(player,"\n")

	hammer = CalcHammer()
	totp = len(lynchref)
	driver.find_element_by_xpath("""//*[@id="cke_contents_vB_Editor_QR_editor"]/textarea""").send_keys("\n[b][SIZE=4]", totp," Players Remaining\n\n", hammer, " to hammer[/SIZE][/b]\n")
	driver.find_element_by_xpath("""//*[@id="qr_submit"]""").click()
	
def EndDay(lynched):
	print("EndDay: Ending the day, majority is reached. Posting final vote then exiting loop.\n")
	time.sleep(5)
	driver.find_element_by_xpath("""//*[@id="cke_contents_vB_Editor_QR_editor"]/textarea""").send_keys("Beep Boop, I'm a bot. Majority has been reached. Please stop posting.\n")
	driver.find_element_by_xpath("""//*[@id="cke_contents_vB_Editor_QR_editor"]/textarea""").send_keys("\n[b][size=4]",lynched," has been lynched![/size][/b]\n")
	driver.find_element_by_xpath("""//*[@id="cke_contents_vB_Editor_QR_editor"]/textarea""").send_keys("\n[b][SIZE=4]Lynch Votes:[/SIZE][/b]\n")
	for user in lynchref:
		if "PLAYERLIST" not in user and user != "":
			driver.find_element_by_xpath("""//*[@id="cke_contents_vB_Editor_QR_editor"]/textarea""").send_keys("[b]",user,"[/b]", " - ")#, ['{}, '.format(elem) for elem in lynchref[user]], "\n")
			for voter in lynchref[user]:
				driver.find_element_by_xpath("""//*[@id="cke_contents_vB_Editor_QR_editor"]/textarea""").send_keys(voter,", ")
			driver.find_element_by_xpath("""//*[@id="cke_contents_vB_Editor_QR_editor"]/textarea""").send_keys("\b\b\n")
	driver.find_element_by_xpath("""//*[@id="cke_contents_vB_Editor_QR_editor"]/textarea""").send_keys("\n[b][SIZE=4]Not Voting:[/SIZE][/b]\n")
	for player in lynchref:
		if player not in lynches and "PLAYERLIST" not in player and player != "":
			driver.find_element_by_xpath("""//*[@id="cke_contents_vB_Editor_QR_editor"]/textarea""").send_keys(player,"\n")
			
	driver.find_element_by_xpath("""//*[@id="qr_submit"]""").click()
	
	lynches.clear()
	InitVotes()

	return True
	
def ShowVotes():
	print("\nIndividual Lynch Votes:\n")
	for user in lynchref:
		if "PLAYERLIST" not in user and user != "":
			print (user, "-", lynchref[user])
		
#	print("\nLynch Table:\n")
#	for lynch in lynches:
#			print(lynch, "voting", lynches[lynch])
	
	print("\nNot Voting\n")
	for player in lynchref:
		if player not in lynches and "PLAYERLIST" not in player and player != "":
			print(player)
	print("-----")
	
def AddLynch(lynch, username):
	print ("Examining lynch vote...", username + " voting " + lynch)
	for target in lynchref:
		if lynch.upper() in target:
			print("Matching lynch ", lynch, " to ", target)
			lynch = target
			
	if username in lynchref and lynch in lynchref:
		print ("Username is in lynch references and valid player")
		
		if username in lynches:
            #keep track of who is voting who. If username is voting for a player, remove username from that player and move to new target.
			prevlynch = lynches[username]
			print ("prevlynch is:",prevlynch, lynchref[prevlynch])
			#remove player from voting
			lynchref[prevlynch].remove(username)
			##print ("finished if statement")
		#add in new reference
		lynches[username]=lynch
		WriteCfg('Votes',username,lynch)
		#add player in
		lynchref[lynch].append(username)
		##print ("Finished adding lynch")
	elif username not in lynchref:
		print ("Invalid User, not part of the game")
	elif lynch not in lynchref:
		print ("Invalid lynch, player is not in the pool")

def Unlynch(username):
	if username in lynches:
		print("Removing lynch vote for: ", username)
		prevlynch = lynches[username]
		lynchref[prevlynch].remove(username)
		del lynches[username]
	
def CheckCommand(post_txt, username):
	post_text = post_txt.get_attribute('innerHTML').replace(" ","").replace(u"\u200b","").upper()
	#print(post_txt.get_attribute('innerHTML').upper().replace(" ",""))
	#print(post_text)
	#pdb.set_trace()
	if "<B>LYNCH" in post_text:
		#print ("Detected vote")
		bolds=post_txt.find_elements_by_tag_name("b")
		for bold in bolds:
			#print (bold.text)
			if "LYNCH" in bold.text.upper():
				#print ("Qualifies as lynch:", username, " posted ", bold.text.upper())
				lynchrep=re.compile(re.escape('lynch '), re.IGNORECASE)
				lynch=lynchrep.sub("", bold.text).upper()
				#print ("lynch is",lynch)
				AddLynch(lynch, username)
				#Add the lynch to local records as well.
				##print ("Out of add lynch command")
	if "<B>UNLYNCH" in post_text:
		Unlynch(username)
	if "<B>NIGHTBEGINS" in post_text and username == op_name.upper():
		print ("Night Begins.")
		#ShowVotes()
		#InitVotes()
	if "<B>DAYBEGINS" in post_text and username == op_name.upper():
		print ("Day Begins, resetting votes...")
		lynches.clear()
		InitVotes()
		ShowVotes()
		#PostVotes()
	if "<B>VOTECOUNT" in post_text:
		global voteflag
		print ("Vote count requested:\n")
		ShowVotes()
		#PostVotes()
		voteflag=1
		
	if ("WASKILLED</B>" in post_text or "<B>KILL" in post_text) and username == op_name.upper():
		killrep=re.compile(re.escape(' was killed'), re.IGNORECASE)
		kill2rep=re.compile(re.escape('kill '), re.IGNORECASE)
		bolds=post_txt.find_elements_by_tag_name("b")
		print("Received kill command...")
		for bold in bolds:
			if "WAS KILLED" in bold.text.upper():
				username=killrep.sub("",bold.text).upper()
				if username in lynchref:
					print ("Removing player from game:", username)
					lynches.pop(username,None)
					lynchref.pop(username,None)
					deadref[username]=1
					WriteCfg('Players',username, 'Dead')
				else:
					print ("Invalid Kill Command:", bold.text)
			if "KILL " in bold.text.upper():
				username=kill2rep.sub("",bold.text).upper()
				if username in lynchref:
					print ("Removing player from game:", username)
					lynches.pop(username,None)
					lynchref.pop(username,None)
					deadref[username]=1
					WriteCfg('Players',username, 'Dead')
				else:
					print ("Invalid Kill Command:", bold.text)
		hammer = CalcHammer()
	if "<B>ADD" in post_text and username == op_name.upper():
		print("Adding player to the game...")
		addrep=re.compile(re.escape('add '), re.IGNORECASE)
		bolds=post_txt.find_elements_by_tag_name("b")
		for bold in bolds:
			if "ADD " in bold.text.upper():
				username=addrep.sub("",bold.text).upper()
				if username not in lynchref:
					print ("Adding player:", username, " to the game")
					lynchref[username]=[]
					WriteCfg('Players',username,'Alive')
				else:
					print("username already exists in the player list:", username)
				

def ScrapPosts( driver ):

	driver.execute_script('''
	var element = document.getElementsByClassName("message"), index;
    for (index = element.length - 1; index >= 0; index--) {
        element[index].parentNode.removeChild(element[index]);
    }
	''')
	posts=driver.find_elements_by_css_selector(".postbitlegacy.postbitim.postcontainer.old")
	print("Total number of posts on this page:", len(posts))
	for post in posts:
		username=post.find_element_by_tag_name("Strong").text.upper()
		postnumber=post.find_element_by_class_name("postcounter").text.replace("#","")
		#index the last post
		#check if current post is greater than last analyzed post, if not then skip.
		try:
			lastpost=config.get('Thread','LastPost')
		except:
			lastpost=0
		if int(postnumber) > int(lastpost):
			print("Examining post #",postnumber)
			WriteCfg('Thread','LastPost',postnumber)
			post_txt=post.find_element_by_class_name("content")
			CheckCommand(post_txt,username)
		#time.sleep(2)
		
def InitVotes():
	print("=======Initializing Votes========")
	for lynch in lynchref:
		lynchref[lynch]=[]
	config.remove_section('Votes')
	config.add_section('Votes')

def WriteCfg(section, option, value):
        config.set(section, option, value)

def UnwriteCfg(section, option):
        config.remove_option(section, option)
		
def CheckHammer(hammer):
	print("Checking if majority (",hammer,") is reached...")
	for lynch in lynchref:
		if len(lynchref[lynch]) == hammer:
			lynched = lynch
			DayOver = EndDay(lynched)
			return True
	print("No majority, the game goes on...")
	
def CalcHammer():
	totplayers = len(lynchref)
	if totplayers%2 == 0:
		#testing to see if this saves
		hammer = totplayers/2 + 1
	else:
		hammer = math.ceil(totplayers/2)
	return hammer
				
###Init stuff###
shell="true"
chrome_driver = r"chromedriver.exe"
driver = webdriver.Chrome(chrome_driver)
#pause here and enter any web address into browser
driver.get("http://nadota.com/")
LoginBot()

#################################################################
####################GAME URL GOES HERE ##########################
#################################################################
#driver.get("http://nadota.com/forumdisplay.php?60-SpAm")
#driver.get("http://nadota.com/showthread.php?42181-ONGOING-Ironstove-s-Black-Box-Mafia")
driver.get("https://forum.mafiascum.net/")
#################################################################
####################GAME URL GOES HERE ##########################
#################################################################

titles=driver.find_elements_by_class_name("threadtitle")
for title in titles:
	print(title.text)
	if "[ONGOING" in title.text:
		title.click()
		break

###dict refs and vars###
plist={}
lynches={}
lynchref={}
postref={}
deadref={}
voteflag=0
totplayers=0
hammer=100
DayOver = False

###set up the configuration file###
cfgfile=open(os.path.abspath(os.path.join('config.txt')),'r+')
config=configparser.ConfigParser()
config.read(os.path.abspath(os.path.join('config.txt')))
checkgame=len(config.sections())
print("Check game is ",checkgame)

###Create bot log
###botlog=open(os.path.abspath(os.path.join('config.txt')),'w+')
###orig_stdout = sys.stdout
###sys.stdout = botlog

###Entered thread: Main Execution###

#check if this is a new game or if previous game exists
if checkgame == 0:
	#new game started
	print("Starting a new game")
	config.add_section('Players')
	config.add_section('Votes')
	config.add_section('Thread')
	config.add_section('Host')
	op=driver.find_element_by_class_name("userinfo")
	op_name=op.find_element_by_tag_name("Strong").text.upper()
	config.set('Host','Host', op_name)
	op_rpost=driver.find_element_by_class_name("content")
	
	playerlist=op_rpost.find_element_by_tag_name("b")
	players=playerlist.get_attribute('innerHTML').replace("\n","").split("<br>")
	for player in players:
		plist[player.upper()]=1
		##print ("checking deadref", player)
		if player not in deadref and "PLAYERLIST" not in player and player != "":
			##print("Congrats, not dead")
			lynchref[player.upper()]=[]
			WriteCfg('Players',player,'Alive')
		else:
			print("The dead (", player ,") doesn't speak...")
			
	lynches.clear()
	InitVotes()
elif checkgame > 0:
	#previous game exists
	print("Loading previous game")
	lastpage=config.get('Thread','LastPage')
	driver.get(lastpage)
	lastpost=config.get('Thread','LastPost')
	op_name=config.get('Host','Host')
	cfgplayers=config.options('Players')
	for player in cfgplayers:
		status = config.get('Players',player)
		if status == "Alive":
			lynchref[player.upper()]=[]
		elif status == "Dead":
			deadref[player.upper()] = []
	cfgvotes=config.options('Votes')
	for voter in cfgvotes:
		username = voter.upper()
		lynch = config.get('Votes',voter)
		AddLynch(lynch, username)

hammer = CalcHammer()
		

#initial data pull
ScrapPosts( driver )
nextlink=1

#Basically infinite loop. 2160 iterations = 36 hours. Bot seems to crash after about 2-3 hours, so will try to do a 100 hour test at some point.
count = 0

while count < 5000:
	print("Loop iteration:", count)
	while nextlink != 0:		
		try:
			nextlink=driver.find_elements_by_class_name("prev_next")
			if "NEXT PAGE" in nextlink[0].get_attribute('innerHTML').upper():
				ScrapPosts ( driver )
				nextlink[0].click()
				time.sleep(3)
				print("===Moving to next page===")
			elif "NEXT PAGE" in nextlink[1].get_attribute('innerHTML').upper():
				ScrapPosts ( driver )
				nextlink[1].click()
				time.sleep(3)
				print("===Moving to next page===")
			else:
				print("===On last page already===")
				nextlink=0
				#store last thread page
				ScrapPosts ( driver )
				lastpage=driver.current_url
				WriteCfg('Thread','LastPage',lastpage)
		except Exception as e:
			print(e)
			print("===Completed web scraping===")
			nextlink=0
			lastpage=driver.current_url
			WriteCfg('Thread','LastPage',lastpage)
	lastpost = config.get('Thread','LastPost')
	print("Sleeping bot, last post recorded is ", lastpost)
	#write to config file
	###write the file###
	cfgfile.truncate(0)
	config.write(cfgfile)
	#cfgfile.truncate() #for some reason this truncate isn't working... File is appending when using fsync and flush. 
	#cfgfile.flush()
	#os.fsync(cfgfile.fileno())
	cfgfile.close()
	cfgfile = open(os.path.abspath(os.path.join('config.txt')),'r+')

	hammer = CalcHammer()
	DayOver = CheckHammer(hammer)

	if DayOver == True:
		#Day has ended, kill the bot. Re-run when the day has restarted.
		sys.exit(0)

	if voteflag == 1:
		print("Vote Count requested, calling post votes")
		PostVotes()
		voteflag = 0
	else:
		print("No votes requested. Voteflag is:", voteflag)
	print("Pause for 45s")
	time.sleep(45)
	try:
		driver.get(lastpage)
		print("     Successfully refreshed page this iteration")
	except Exception as e:
		print(e)
		print("#####Failed to refresh page, will try again next iteration.")
	print("Pause for 15s")
	time.sleep(15)
	nextlink = 1
	count = count + 1

###botlog.close()
###sys.stdout = orig_stdout
