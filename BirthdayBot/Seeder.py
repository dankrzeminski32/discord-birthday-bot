from BirthdayBot.Models import Base, BirthdayMessages
from BirthdayBot.Models import Base, BirthdayImages
from BirthdayBot.Utils import session_scope, logger


class Seeder(object):
    def __init__(self, bdayQuotes_path: str):
        self.bdayQuotesPath = bdayQuotes_path
        self.bdayQuotesFile = open(self.bdayQuotesPath, "r")

    def seedDBIfEmpty(self) -> None:
        try:
            with session_scope() as s:
                if not s.query(BirthdayMessages).all():
                    logger.info("Birthday Quotes table was empty. Now seeding...")
                    self.quoteSeed()
                else:
                    logger.info("Birthday Quotes table is filled")
        except Exception as e:
            logger.error("Database Seeding Issue, %s" % e)

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
