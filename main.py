import socket
import sys
import threading
import time


def check(target, port):
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			sock.settimeout(3)

			if sock.connect_ex((target, port)) == 0:
				print("Port found on {}:{}".format(target, port))
	except socket.error:
		pass


def main():
	if len(sys.argv) < 4:
		sys.exit("Usage: {} <Target> <Port Range (E.g: 0-65535)> <Threads> <Delay (E.g: 0.2)>".format(sys.argv[0]))

	target = sys.argv[1]
	ranges = list(map(int, sys.argv[2].split("-")))
	threads = int(sys.argv[3])
	timeout = float(sys.argv[4])

	main_thread = threading.current_thread()

	for port in range(ranges[0], ranges[1]+1):
		threading.Thread(target=check, args=(target, port)).start()
		
		if threads == threading.active_count()-1:
			for thread in threading.enumerate():
				if thread == main_thread:
					continue

				thread.join()

		time.sleep(timeout)


if __name__ == "__main__":
	main()
