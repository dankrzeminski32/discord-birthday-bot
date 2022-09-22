from BirthdayBot.models import Base, BirthdayImages
from db_settings import session_scope

file1 = open("BirthdayImages.txt", "r")
Lines = file1.readlines()


try:
    with session_scope() as s:
        for line in Lines:
            imageUrl = BirthdayImages(bdayImage=line)
            s.add(imageUrl)
        print("success")
except Exception as e:
    print(e)
