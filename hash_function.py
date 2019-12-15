""" Хеш строковых значений с помощью алгоритмов: SHA256, X11, SCrypt """

import time 
import os 
import psutil 
from hashlib import sha256 
#import scrypt
from x11_hash import getPoWHash

#  Строки отвечают за время и использованную память.
start_time = time.time() 
pid = os.getpid() 
py = psutil.Process(pid) 
cpuUse = py.cpu_percent() 
memoryUse = py.memory_info()[0]/2.**30 


def hash_func(string_value, algorithm): 
	if algorithm.lower() == 'sha256':
		#  SHA256 хеш.
		hash_object = sha256(bytes(str(string_value), 'utf-8')).hexdigest()
		print('\nSHA256 хеш: ' + hash_object)
	elif algorithm.lower() == 'scrypt':
		#  SCrypt хеш.
		hash_object = scrypt.hash(password=string_value, salt=b'pass')
		print('\nSCrypt хеш: ' + str(hash_object)) 
	elif algorithm.lower() == 'x11':
		#  X11 хеш.
		hash_object = getPoWHash(bytes(string_value, 'utf-8'))
		print('\nX11 PoW: ' + str(hash_object))
	else:
		print('\nФункция не поддерживает данный алгоритм или он написан с ошибкой.')


# hash_func(input('строка: '), input('алгоритм хеширования: '))

print('.'*60, '\nПамяти использовано:', memoryUse)
print('Загрузка ЦП в момент выполнения программы: ', psutil.cpu_percent(), '%')
print('Время выполнения: %s секунд.' % (time.time() - start_time))
