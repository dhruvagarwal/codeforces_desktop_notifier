from bs4 import BeautifulSoup as BS
import requests,json,os
import pynotify as pn
import datetime,time

def init_temp(usernames):
	global userlog
	try:
		userlog = json.loads(open('temp_targets.txt').read())
	except:
		for username in usernames:
			userlog[username] = 0
		with open('temp_targets.txt','w+') as f:
			f.write(json.dumps(userlog))

def rem_temp():
	os.system('rm temp_targets.txt')

def update_logs():
	with open('temp_targets.txt','w+') as f:
		f.write(json.dumps(userlog))	

def local_to_cftz(local_dt):
	cf_dt = local_dt - datetime.timedelta(hours = 2,minutes = 30)
	return cf_dt

def popup(title, message):
	pn.init('CF Notifier')
	pop	= pn.Notification(title,message)
	pop.show()
	return

def inlimits(timestamp):
	timestamp = datetime.datetime.strptime(timestamp,"%Y-%m-%d %H:%M:%S")
	# print contest_time <= timestamp
	return local_to_cftz(contest_config['start-time']) <= timestamp

def text(td):
	return td.text.strip()

def strip_row(tr):
	# this is CodeForces specific
	data_dict = {}
	tds = tr.findAll('td')
	data_dict['subid'] = text(tds[0])
	data_dict['timestamp'] = text(tds[1])
	data_dict['username'] = text(tds[2])
	data_dict['prob_link'] = tds[3].a['href']
	data_dict['prob_name'] = text(tds[3])
	data_dict['verdict'] = text(tds[5])
	# print json.dumps(data_dict,indent = 4)
	return data_dict

def scrape(url, username):
	r = requests.get(url + username)
	html = r.content
	soup = BS(html)
	table = soup.findAll('table',{'class':'status-frame-datatable'})[0]
	trs = table.findAll('tr')
	c = 2 # counter for row num
	data = strip_row(trs[1])
	while data['subid'] != userlog[username] and inlimits(data['timestamp']):
		if c == 2:
			userlog[username] = data['subid']

		if data['verdict'] == "Accepted":
			popup(data['username'],'AC on '+data['prob_name']+' \nat '+data['timestamp'])
			# break
		data = strip_row(trs[c])
		c += 1
	update_logs()

def configure_contest():
	contest_config = {}
	details = raw_input("Enter Contest Details:\n<start-time( HH:MM )> <duration-in-hours( eg. 2.5 )>\n").split(' ')
	contest_config['start-time'] = datetime.datetime.now()
	hours = int(details[0].split(':')[0])
	minutes = int(details[0].split(':')[1])
	contest_config['start-time'] = contest_config['start-time'].replace(hour = hours,minute = minutes,second = 0,microsecond = 0)
	# print contest_config['start-time']
	contest_config['duration'] = float(details[1])
	return contest_config

if __name__ == "__main__":
	_basic_url = 'http://codeforces.com/submissions/'
	userlog = {}
	contest_config = configure_contest()
	usernames = open('targets.txt').read().split()
	init_temp(usernames)
	if contest_config['start-time'] > datetime.datetime.now():
		print 'Please Wait until the contest starts !\nScript will start automatically on event start\nDon\'t Terminate this process'
		time.sleep((contest_config['start-time'] - datetime.datetime.now()).total_seconds())
	while contest_config['start-time']+datetime.timedelta(hours = int(contest_config['duration']),minutes = 60*(contest_config['duration'] - int(contest_config['duration']))) > datetime.datetime.now() :
		for username in usernames:
			# TODO: make all threads
			scrape(_basic_url, username)
		time.sleep(180) # for 3 minutes
	print 'It\'s Over Now !'
	rem_temp()

# take a list of usernames
# store a list of problems for both the divs -- on the starting 
# for each username -- scrape the submissions and record until not scanned
# check for problems submitted for the existing contests
# if there's an update -- display a notification
# *****imp : check for timezone and adjust accordingly