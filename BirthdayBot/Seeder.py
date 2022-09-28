from BirthdayBot.Models import Base, BirthdayMessages
from BirthdayBot.Models import Base, BirthdayImages
from BirthdayBot.Utils import session_scope, logger


class Seeder(object):
    def __init__(self, bdayImages_path: str, bdayQuotes_path: str):
        self.bdayImagePath = bdayImages_path
        self.bdayQuotesPath = bdayQuotes_path
        self.bdayImagesFile = open(self.bdayImagePath, "r")
        self.bdayQuotesFile = open(self.bdayQuotesPath, "r")

    def seedDBIfEmpty(self) -> None:
        try:
            with session_scope() as s:
                if not s.query(BirthdayImages).all():
                    logger.info("Birthday Images table was empty. Now seeding...")
                    self.imageSeed()
                else:
                    logger.info("Birthday Images table is filled")

                if not s.query(BirthdayMessages).all():
                    logger.info("Birthday Quotes table was empty. Now seeding...")
                    self.quoteSeed()
                else:
                    logger.info("Birthday Quotes table is filled")
        except Exception as e:
            logger.error("Database Seeding Issue, %s" % e)

    def imageSeed(self) -> None:
        file1 = self.bdayImagesFile
        Lines = file1.readlines()

        try:
            with session_scope() as s:
                total_images_added = 0
                for line in Lines:
                    imageUrl = BirthdayImages(bdayImage=line)
                    s.add(imageUrl)
                    total_images_added += 1
                logger.info(
                    "Images seeder has ran successfully. %s Images added"
                    % total_images_added
                )
        except Exception as e:
            logger.error("Image Logger has failed, %s" % e)

    def quoteSeed(self) -> None:
        file2 = self.bdayQuotesFile
        Lines = file2.readlines()

        try:
            with session_scope() as s:
                total_added_quotes = 0
                for line in Lines:
                    try:
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
                        total_added_quotes += 1
                    except:
                        author = line.rsplit(";", 1)
                        author = author[1].rstrip()
                        author_Column = author
                        bdayMessage_column = line.rsplit(";", 1)[0]
                        message2 = BirthdayMessages(
                            bdayMessage=bdayMessage_column, author=author_Column
                        )
                        s.add(message2)
                        total_added_quotes += 1
                logger.info(
                    "Quotes seeder has ran successfully. %s Quotes added"
                    % total_added_quotes
                )
        except Exception as e:
            logger.error("Quotes Logger has failed, %s" % e)
