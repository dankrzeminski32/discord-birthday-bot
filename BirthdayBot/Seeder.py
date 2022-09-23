from BirthdayBot.models import Base, BirthdayMessages
from BirthdayBot.models import Base, BirthdayImages
from db_settings import session_scope


class Seeder:
    def __init__(self, bdayImages_path, bdayQuotes_path):
        self.bdayImagePath = bdayImages_path
        self.bdayQuotesPath = bdayQuotes_path
        self.bdayImagesFile = open(self.bdayImagePath, "r")
        self.bdayQuotesFile = open(self.bdayQuotesPath, "r")

    def imageSeed(self):
        file1 = self.bdayImagesFile
        Lines = file1.readlines()

        try:
            with session_scope() as s:
                for line in Lines:
                    imageUrl = BirthdayImages(bdayImage=line)
                    s.add(imageUrl)
            print("success")
        except Exception as e:
            print(e)

    def quoteSeed(self):
        file2 = self.bdayQuotesFile
        Lines = file2.readlines()

        try:
            with session_scope() as s:
                for line in Lines:
                    author = line.rsplit(";", 1)
                    author = author[1].rstrip()
                    author_Column = author
                    bdayMessage_column = line.rsplit(";", 1)[0]
                    bdayMessage_column = bdayMessage_column.encode("cp1252").decode(
                        "utf-8"
                    )
                    message2 = BirthdayMessages(
                        bdayMessage=bdayMessage_column, author=author_Column
                    )
                    s.add(message2)
                print("success")
        except Exception as e:
            print(e)
