import time
from random import randint
import threading
from queue import Queue
from itertools import cycle
from threading import Thread

q=Queue()

class Table:

    def __init__(self,number,guest=None):
        self.number=number
        self.guest=guest





class Guest(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name=name

    def run(self):
        time.sleep(randint(3,10))

class Cafe(threading.Thread):
    def __init__(self,*tables,queue=q):
        threading.Thread.__init__(self)
        self.tables=tables
        self.queue=queue

    def guest_arrival(self, *guests):
        list_guests=list(guests)
        lenth_guest=len(list_guests)
        table_flag = 0
        for i in range(lenth_guest):
            guest=list_guests.pop()

            for table in self.tables:

                if table.guest==None:
                    table.guest=guest
                    print(f'{guest.name} сел(-а) за стол номер {table.number} : Поток {threading.current_thread()}')
                    table_flag+=1
                    table.guest.start()
                    break
                elif table_flag>=len(self.tables):
                    self.queue.put(guest)
                    print(f'Гость {guest.name} в очереди : Поток {threading.current_thread()}')
                    break

                elif table.guest!=None:
                    continue




    def discuss_guests(self):
        for table in cycle(self.tables): #бесконечный перебор столов
            proof_table = 0 #счетчик на выход из бесконечного цикла
            if not self.queue.empty():      #проверка на пустую очередь
                                            #Если очередь есть
                if table.guest == None:         # проверка что стол пустой
                    table.guest = self.queue.get()  #Если пустой, помещаем гостя из очереди

                    table.guest.start()
                    print(f"{table.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}: Поток {threading.current_thread()}")


                else:
                    if not table.guest.is_alive(): #Если запущено обслуживание
                        print(f"{table.guest.name} за столом {table.number} покушал(-а) и ушёл(ушла) : Поток {threading.current_thread()}")
                        print(f"Стол номер {table.number} свободен : Поток {threading.current_thread()}" )
                        table.guest=None


            else: #Если очереди нет
                if isinstance(table.guest,Thread):
                    if not table.guest.is_alive():  # Если запущено обслуживание
                        print(f"{table.guest.name} за столом {table.number} покушал(-а) и ушёл(ушла) : Поток {threading.current_thread()}")
                        print(f"Стол номер {table.number} свободен")
                        table.guest = None

                for tab_pr in self.tables:  #Проверяем все ли столы свободны
                    if tab_pr.guest==None:
                        proof_table+=1
                if proof_table>=len(self.tables): #Если все столы свободны, закрываем бесконечный цикл
                    break







# Создание столов
tables = [Table(number) for number in range(1,8)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra','Petr','Athanasii', 'Gerasim','Pascal','Levin'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
#thread1=threading.Thread(target=cafe.guest_arrival,args=guests)
cafe.guest_arrival(*guests)

# Обслуживание гостей
thread2=threading.Thread(target=cafe.discuss_guests())
thread2.start()
#cafe.discuss_guests()
#for i in range(6):
#    print(q.get())
#print(list(x.guest==None for x  in cafe.tables))
#print(cafe.tables)
#for ges in cafe.tables:
#    print(ges.guest)


