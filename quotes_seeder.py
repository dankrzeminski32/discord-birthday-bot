from BirthdayBot.models import Base, BirthdayMessages
from settings import session_scope

file1 = open('BirthdayMessages.txt', 'r')
Lines = file1.readlines()


try:
    with session_scope() as s:
        for line in Lines:
            message = BirthdayMessages(bdayMessage = line)
            s.add(message)
        print("success")
except Exception as e:
    print(e)


