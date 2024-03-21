
import threading
import queue
import time

# Kuyruk oluşturalım
q = queue.Queue(1)

def printer():
    while True:
        arg = q.get(block=True)  # Kuyruktan bir öğe al
        print(arg)
        q.task_done()  # İşlem tamamlandı olarak işaretle

def func1():
    while True:
        q.put(1)  # Kuyruğa veri ekle

def func2():
    while True:
        q.put(2)  # Kuyruğa veri ekle

        
# İş parçacıklarını oluşturup başlatalım
th_printer = threading.Thread(target=printer)
th_printer.daemon = True  # Arka planda çalışan bir iş parçacığı olarak ayarlayalım
th_printer.start()

th1 = threading.Thread(target=func1)
th1.start()

th2 = threading.Thread(target=func2)
th2.start()