from datetime import datetime

def logfile(message, file='out.log'):
	with open(file, 'a', encoding='utf-8') as f:
		f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
