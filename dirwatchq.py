# import time module, Observer, FileSystemEventHandler
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
from queue import Queue
import json




class OnMyWatch:
	

	def __init__(self):
		self.observer = Observer()
		# Set the directory on watch
		self.watchDirectory = "" #填入需要觀察的資料夾
		#輸入linebot1 token
		self.channel_access_token1 = '' #輸入line-bot1的 Acess Tolen
		#輸入linebot2 token
		self.channel_access_token2 = ''
		#輸入linebot3 token
		self.channel_access_token3 = ''
		#輸入linebot4 token
		self.channel_access_token4 = ''
		#輸入linebot5 token
		self.channel_access_token5 = ''
		#輸入linebot6 token
		self.channel_access_token6 = ''
		#輸入linebot7 token
		self.channel_access_token7 = ''
		#輸入linebot8 token
		self.channel_access_token8 = ''
		#輸入linebot9 token
		self.channel_access_token9 = ''
		
		self.url = 'https://api.line.me/v2/bot/message/quota/consumption'
		self.channel_token_list = [self.channel_access_token1, self.channel_access_token2, self.channel_access_token3, self.channel_access_token4, self.channel_access_token5
					   		,self.channel_access_token6, self.channel_access_token7, self.channel_access_token8, self.channel_access_token9]
		self.headers_list = []
		for index in range(len(self.channel_token_list)):
			self.headers_list.append({'Authorization': f'Bearer {self.channel_token_list[index]}'})
		
	def check_remain_quota(self,):
		i = 0
		for header in self.headers_list:
			i += 1
			response = requests.get(self.url, headers=header)
			if response.status_code == 200:
				linebot1_res = response.json() # Output remaining free messages
				remaining_quota = linebot1_res.get('remaining', 'No remaining quota information available')
				total_usage = linebot1_res.get('totalUsage', 'No usage data available')
				print(f'Remaining Quota: {remaining_quota}')
				print(f'Total Usage: {total_usage}')
				if total_usage == 190: # 可以自行更改成需要的值, 當使用量達到此上限, 自動切換下一個line bot
					if i == len(self.headers_list): # 如果達到 channel_token_list 切換上限, 程式會自動停掉
						print(f"all line-bots have no remain quota")
						i = 0
						return {"line-bot": i, "payload": total_usage}
					else:
						print(f"line-bot: {i} no remain quota")
						continue
				
				else:
					print(f"line-bot: {i} has remain quota, use it")
					return {"line-bot": i, "payload": total_usage}
			
			else:
				print(f"Error: {response.status_code}, {response.text}")
				i = 0
				return {"line-bot":i, "payload": response.status_code}




	def run(self):
		
		event_handler = Handler()
		self.observer.schedule(event_handler, self.watchDirectory, recursive = True)
		self.observer.start()
		# linebot = 0
		
		try:
			while True:
				while not event_handler.event_q.empty():
					data, ts = event_handler.event_q.get()
					payload = self.check_remain_quota()
					if payload["line-bot"] == 0:
						print(payload["payload"])
						break
					try:
						data = data.split("\\")[-1] #將路徑資訊砍掉, 保留檔案名稱
						data = {'message': data, "linebot": payload["line-bot"], "quotas": payload["payload"]}
						print(data)
						headers = {'Content-Type': 'application/json; charset=UTF-8'}  # Correct header for JSON data}
						response = requests.post('http://127.0.0.1:5000/api/stocklinebot', data=json.dumps(data, ensure_ascii=False).encode('utf8'), headers=headers)
						print(response)
						
						if response == "OK":
							print("line-bot app recive data")
						
						else:
							print("line-bot get something wrong")

					except requests.exceptions.RequestException as e:	
						print(f"Request error: {e}")
				time.sleep(1)
		except KeyboardInterrupt:
			self.observer.stop()  # Handle manual termination by keyboard
			print("Observer Stopped")


class Handler(FileSystemEventHandler):
    def __init__(self):
        self.event_q = Queue()

    # @staticmethod
    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Event is created, you can process it now
            print("Watchdog received created event - % s." % event.src_path)
            data = event.src_path
            self.event_q.put((data, time.time()))

if __name__ == '__main__':

	watch = OnMyWatch()
	watch.run()
	
