'''
Цель: Применить очереди в работе с потоками, используя класс Queue.

Задача "Потоки гостей в кафе":
Необходимо имитировать ситуацию с посещением гостями кафе.
Создайте 3 класса: Table, Guest и Cafe.
Класс Table:
Объекты этого класса должны создаваться следующим способом - Table(1)
Обладать атрибутами number - номер стола и guest - гость, который сидит за этим столом (по умолчанию None)
Класс Guest:
Должен наследоваться от класса Thread (быть потоком).
Объекты этого класса должны создаваться следующим способом - Guest('Vasya').
Обладать атрибутом name - имя гостя.
Обладать методом run, где происходит ожидание случайным образом от 3 до 10 секунд.
Класс Cafe:
Объекты этого класса должны создаваться следующим способом - Cafe(Table(1), Table(2),....)
Обладать атрибутами queue - очередь (объект класса Queue) и tables - столы в этом кафе (любая коллекция).
Обладать методами guest_arrival (прибытие гостей) и discuss_guests (обслужить гостей).
Метод guest_arrival(self, *guests):
Должен принимать неограниченное кол-во гостей (объектов класса Guest).
Далее, если есть свободный стол, то садить гостя за стол (назначать столу guest), запускать поток гостя и выводить на экран строку "<имя гостя> сел(-а) за стол номер <номер стола>".
Если же свободных столов для посадки не осталось, то помещать гостя в очередь queue и выводить сообщение "<имя гостя> в очереди".
Метод discuss_guests(self):
Этот метод имитирует процесс обслуживания гостей.
Обслуживание должно происходить пока очередь не пустая (метод empty) или хотя бы один стол занят.
Если за столом есть гость(поток) и гость(поток) закончил приём пищи(поток завершил работу - метод is_alive), то вывести строки "<имя гостя за текущим столом> покушал(-а) и ушёл(ушла)" и "Стол номер <номер стола> свободен". Так же текущий стол освобождается (table.guest = None).
Если очередь ещё не пуста (метод empty) и стол один из столов освободился (None), то текущему столу присваивается гость взятый из очереди (queue.get()). Далее выводится строка "<имя гостя из очереди> вышел(-ла) из очереди и сел(-а) за стол номер <номер стола>"
Далее запустить поток этого гостя (start)
Таким образом мы получаем 3 класса на основе которых имитируется работа кафе:
Table - стол, хранит информацию о находящемся за ним гостем (Guest).
Guest - гость, поток, при запуске которого происходит задержка от 3 до 10 секунд.
Cafe - кафе, в котором есть определённое кол-во столов и происходит имитация прибытия гостей (guest_arrival) и их обслуживания (discuss_guests).

Пример результата выполнения программы:
Выполняемый код:
class Table:
...
class Guest:
...
class Cafe:
...
# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()

Вывод на консоль (последовательность может меняться из-за случайного время пребывания гостя):
Maria сел(-а) за стол номер 1
Oleg сел(-а) за стол номер 2
Vakhtang сел(-а) за стол номер 3
Sergey сел(-а) за стол номер 4
Darya сел(-а) за стол номер 5
Arman в очереди
Vitoria в очереди
Nikita в очереди
Galina в очереди
Pavel в очереди
Ilya в очереди
Alexandra в очереди
Oleg покушал(-а) и ушёл(ушла)
Стол номер 2 свободен
Arman вышел(-ла) из очереди и сел(-а) за стол номер 2
.....
Alexandra покушал(-а) и ушёл(ушла)
Стол номер 4 свободен
Pavel покушал(-а) и ушёл(ушла)
Стол номер 3 свободен
Примечания:
Для проверки значения на None используйте оператор is (table.guest is None).
Для добавления в очередь используйте метод put, для взятия - get.
Для проверки пустоты очереди используйте метод empty.
Для проверки выполнения потока в текущий момент используйте метод is_alive.
Файл module_10_4.py загрузите на ваш GitHub репозиторий. В решении пришлите ссылку на него.
'''

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


