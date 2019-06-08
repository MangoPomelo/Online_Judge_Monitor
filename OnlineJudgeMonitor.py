from bs4 import BeautifulSoup
from urllib.request import urlopen
from tqdm import tqdm
from prettytable import PrettyTable

class Monitor:
	def __init__(self, usernamelist):
		self.usernamelist = usernamelist
		self.rootURL = 'http://10.162.32.3/'
		self.userInfo = dict()
		self.ProcessOnUsers()
	
	def ProcessOnEachUser(self, usernameTuple):
		realname, username = usernameTuple
		html = BeautifulSoup(urlopen(self.rootURL + 'userinfo.php?user=' + username).read().decode('utf-8'), 'lxml')
		solvedSet = [item.get_text().strip() for item in html.select('#main > center > font')[-2].select('a')]
		unsolvedSet = [item.get_text().strip() for item in html.select('#main > center > font')[-1].select('a')]
		self.userInfo[username] = User(realname, username, solvedSet, unsolvedSet)

	def ProcessOnUsers(self):
		print("加载中...")
		for usernameTuple in tqdm(self.usernamelist):
			self.ProcessOnEachUser(usernameTuple)
		print("加载完成")

	def LookUp(self, usernamelist = [], lookupList = {}, mode = 'default', filepath = './LookUpResult.csv'):
		if len(usernamelist) == 0:
			usernamelist = self.usernamelist
		if 'csv' in mode:
			head = "姓名,用户名,完成数"
			for result in lookupList:
				head += "," + str(result)
			head += '\n'
			rows = ""
			for _, username in usernamelist:
				if self.userInfo[username]:
					user = self.userInfo[username]
					rows += user.realname + ',' + user.username + ',' + str(user.totalDone)
					for item in lookupList:
						rows += ',' + ('√' if user.CheckDone(item) else '×')
				rows += '\n'
			with open(filepath, 'w', encoding = "utf-8") as file:
				file.write(head + rows)
			return ("成功输出csv文件于 " + filepath)
		elif 'default' in mode:
			head = ["姓名", "用户名", "完成数"]; head.extend(lookupList); table = PrettyTable(head)
			for username in usernamelist:
				if self.userInfo[username]:
					user = self.userInfo[username]
					row = [user.realname, user.username, str(user.totalDone)]; row.extend(['√' if user.CheckDone(item) else '×' for item in lookupList]); table.add_row(row) 
			return table
	
	def PrintIntoFile(self, filepath = "./usersInfo.txt"):
		with open(filepath, 'w', encoding='utf-8') as file:
			content = ""
			for _, user in self.userInfo.items():
				content += str(user) + '\n'
			file.write(content)
		print("成功输出详情文件于 " + filepath)
		

class User:
	def __init__(self, realname, username, solvedSet, unsolvedSet):
		self.realname = realname
		self.username = username
		self.solvedSet = solvedSet
		self.unsolvedSet = unsolvedSet

	def CheckDone(self, solved):
		return (str(solved) in self.solvedSet)
	
	@property
	def totalDone(self):
		return len(self.solvedSet)

	def __str__(self):
		return "NAME: " + self.realname + "\tUSER: " + self.username + "\tSOLVED: " + str(self.solvedSet) + "\tUNSOLVED: " + str(self.unsolvedSet)

def main():
	monitor = Monitor([("张炫",'nico'),("孟钦宇",'meng5080'),('王润霖', 'wangrunlin'), ('赵如浩', '201713137027'), ('陈都', '201713137030'),
                ('谢瑞辉', '1517'), ('张啸宇', '201713137042'), ('刘诗琪', '171313'), ('熊皓哲', 'xhz1128'), ('李晟', '2418511539'), ('毛竹', 'mz'),
                ('陆晨阳', '1096441708'), ('李峰', 'lf15727151440'), ('许文亮', '58327549'), ('唐思缘', '20010722'), ('孙奕涵', 'sunyihansz'),
                ('郑天伦', 'simplify'), ('王哲', '201713137103'), ('刘俊', 'JUN'), ('蔡祎恺', '201713137111'), ('王志', '201713137118'),
                ('周宇轩', '131415'), ('齐轶', '2393838377'), ('李创', '1952511149'), ('邓澳坤', 'crazyjoker'), ('余卓晖', '2'), ('刘俊伟','1938804043'),
                 ('贺涛', 'hetao'), ('付博伦', 'Fblun'), ('张少哲', '945717428')])
	print(monitor.LookUp(lookupList = {1094, 1200, 1432, 1447, 1462}, mode = 'csv'))
	print(monitor.LookUp(usernamelist = ['nico', 'meng5080', '1517'], lookupList = {1094, 1200, 1432, 1447, 1462}))

if __name__ == '__main__':
	main()