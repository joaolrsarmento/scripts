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

    def run(self, iterations):
        """
        Run the script that comments iterations times.
        :param iterations: number of iterations that the script should run.
        :type iterations: int

        """
        # Acess the sorteio page
        self.account.driver.get(self.link)
        sleep(2)
        for i in range(iterations):
            print('Iteration', iterations)
            # Get usernames to be used
            usernames = self._get_random_usernames(2)
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
            generate = self.account.followers[random.randint(0,len(self.account.followers))]
            # Avoids using a repeated user
            while generate in self.used:
                generate = self.account.followers[random.randint(0,len(self.account.followers))]
            # Add the username
            usernames += f'@{generate} '
            # Saves the username used
            self.used.append(generate)

        return usernames

sorteio = Sorteio('https://www.instagram.com/p/B_OJb8Uh5Wf/')
sorteio.run(2)