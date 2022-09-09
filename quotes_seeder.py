from BirthdayBot.models import Base, BirthdayMessages
from settings import session_scope

file1 = open('BirthdayMessages.txt', 'r')
Lines = file1.readlines()


try:
    with session_scope() as s:
        for line in Lines:
            author = line.rsplit(";", 1)
            author = author[1].rstrip()
            author_Column = author
            bdayMessage_column = line.rsplit(';', 1)[0]
            message2 = BirthdayMessages(bdayMessage = bdayMessage_column, author = author_Column)
            s.add(message2)
        print("success")
except Exception as e:
    print(e)


