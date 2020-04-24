from instabot import InstaBot
from time import sleep
import datetime
import random

class Sorteio:
    """
    This class gets 2 random usernames on a instagram account followers list and
    comment these accounts on the link passed as argument.

    """
    def __init__(self, link):
        """
        :param link: link to the sorteio
        :type link: string

        """
        # Get instagram account
        self.account = InstaBot()
        # Saving the sorteio link
        self.link = link
        # Used usernames:
        self.used = []
        # Comments per hour
        self.comments_per_hour = 60
        # Seconds per comment
        self.seconds_per_comment = int(60 * 60 / self.comments_per_hour)
    def run(self, quantity):
        """
        Run the script that comments iterations times.
        :param iterations: number of iterations that the script should run.
        :type iterations: int

        """
        # Acess the sorteio page
        self.account.driver.get(self.link)
        sleep(2)
        # Counts the quantity of comments
        count = 0
        # Counts the time
        get_time = 0
        import time
        before = time.time()
        while True:
            after = time.time()
            get_time += after - before
            before = after
            if get_time >= self.seconds_per_comment:
                # Get usernames to be used
                usernames = self._get_random_usernames(quantity)
                while True:
                    try:
                        # Get text area
                        self.account.driver.find_element_by_xpath("//textarea[@placeholder=\"Adicione um comentário...\"]")\
                            .click()
                        # Put keys
                        self.account.driver.find_element_by_xpath("//textarea[@placeholder=\"Adicione um comentário...\"]")\
                            .send_keys(usernames)
                        # Send it out
                        self.account.driver.find_element_by_xpath("//button[contains(text(), 'Publicar')]")\
                            .click()
                        sleep(2)
                        try:
                            print('Checking error...')
                            self.account.driver.find_element_by_xpath("//p[contains(text(), 'Não foi possível publicar o comentário.')]")
                            print('Found error.')
                            self.account.driver.refresh()
                            sleep(5)
                        except:
                            pass
                        break
                    except:
                        self.account.driver.refresh()
                        sleep(5)

                # Refresh
                get_time = 0
                count += 1
                print(count)
                

    def _get_random_usernames(self, quantity):
        """
        Gets two random usernames from the followers list.
        @return usernames: the usernames generated
        @type usernames: string

        """
        # Create random usernames
        usernames = ""
        # Checks if we used all the possible combinations divided by the quantity
        if len(self.used) == len(self.account.followers) / quantity:
            self.used = []

        for i in range(quantity):
            # Generate a new random user
            generate = self.account.followers[random.randint(0,len(self.account.followers)-1)]
            # Avoids using a repeated user
            while generate in self.used:
                generate = self.account.followers[random.randint(0,len(self.account.followers)-1)]
            # Add the username
            usernames += f'@{generate} '
            # Saves the username used
            self.used.append(generate)

        return usernames

sorteio = Sorteio('https://www.instagram.com/p/B_OJb8Uh5Wf/')
sorteio.run(2)