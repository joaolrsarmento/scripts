from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import json


class InstaBot:
    def __init__(self, username, pw):
        """
        This class contains some methods to do auto tasks using an instagram account.
        
        :param username: contains the account username
        :type username: string
        :param pw: contains the account password
        :type pw: string

        """
        # Get ChromeDriver
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        # Save username
        self.username = username
        # Access the instagram on web
        self.driver.get("https://instagram.com")
        # Wait for the page to load
        sleep(2)
        # Input username
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        # Input password
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pw)
        # Login
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        # Wait for the page to load
        sleep(4)
        # Tests if the notification option has appeared
        try: 
            self.driver.find_element_by_xpath("//button[contains(text(), 'Agora não')]")\
                .click()
            sleep(2)
        except:
            pass

    def _get_info(self):
        """
        This method saves the info on the class.
        Infos saved:
            - followers: usernames that are followers
            - following: usernames that the account are following
            - not_following_back: usernames that is on following but not on followers

        """
        # Go the the user profile
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username))\
            .click()
        sleep(2)
        # Go to the following page
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
            .click()
        self.following = self._get_names()
        # Go to the followers page
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()
        self.followers = self._get_names()
        # Creates the intersection
        self.not_following_back = [user for user in following if user not in followers]
        

    def _get_names(self):
        """
        Given a page containing a list of users, it is possible to get the list of the usernames
        This scrolls the page.

        @return names: usernames on the list
        @type names: array of strings

        """
        sleep(2)
        sleep(2)
        # Get scroll box
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button")\
            .click()                      
        return names

    def unfollow_unfollowers(self):
        """
        Acess the not following back users and stop following them/

        """
        for user in self.not_following_back:
            # Go to his page
            self.driver.get('https://instagram.com/' + user)
            sleep(6)
            # Acess the possible actions
            self.driver.find_element_by_xpath("//button[contains(text(), 'Seguindo')]")\
            .click()
            sleep(2)
            # Stop following
            self.driver.find_element_by_xpath("//button[contains(text(), 'Deixar de seguir')]")\
            .click()
            sleep(2)

    def save_info(self):
        """
        Save the info on a json file.
        This info contains the following, followers and not following back usernames

        """
        # Save the info
        self._get_info()
        # Creates the dict
        data = {}
        data['Following users'] = self.following
        data['Followers users'] = self.followers
        data['Not following back users'] = self.not_following_back
        # Saves the file
        with open(f'info_user_{self.username}.json', 'w') as file:
            json.dump(data, file)
