import os
import json
import random

from bot.module.commands.processor import Processor


class InfoProcessor(Processor):
    """Processor for all information that a viewer may request.

    Attributes:
        motd_data: message of the day.
        who_data: information about the current streamer.
        toolmix_data: placeholder for toolmix links.
        twitter_accounts: list of twitter accounts loaded from file
    """

    def __init__(self):
        self.motd_data = 'Aucun message.'
        self.who_data = 'Aucune info sur le streamer actuel.'
        self.toolmix_data = 'Aucun lien.'
        self.dota_heroes = ['Abaddon', 'Alchemist', 'Ancient Apparition', 'Anti-Mage', 'Arc Warden', 'Axe', 'Bane',
                            'Batrider', 'Beastmaster', 'Bloodseeker', 'Bounty Hunter', 'Brewmaster', 'Bristleback',
                            'Broodmother', 'Centaur Warruner', 'Chaos Knight', 'Chen', 'Clinkz', 'Clockwerk',
                            'Crystal Maiden', 'Dark Seer', 'Dark Willow', 'Dazzle', 'Death Prophet', 'Disruptor',
                            'Doom','Dragon Knight', 'Drow Ranger', 'Earth Spirit', 'Earthshaker', 'Elder Titan',
                            'Ember Spirit', 'Enchantress', 'Enigma', 'Faceless Void', 'Gyrocopter', 'Huskar', 'Invoker',
                            'Io', 'Jakiro', 'Juggernaut', 'Keeper of the Light', 'Kunkka', 'Legion Commander',
                            'Leshrac', 'Lich', 'Lifestealer', 'Lina', 'Lion', 'Lone Druid', 'Luna', 'Lycan', 'Magnus',
                            'Medusa', 'Meepo', 'Mirana', 'Monkey King', 'Morphling', 'Naga Siren', "Nature's Prophet",
                            'Necrophos', 'Night Stalker', 'Nyx Assassin', 'Ogre Magi', 'Omniknight', 'Oracle',
                            'Outworld Devourer', 'Pangolier', 'Phantom Assassin', 'Phantom Lancer', 'Phoenix', 'Puck',
                            'Pudge', 'Pugna', 'Queen of Pain', 'Razor', 'Riki', 'Rubick', 'Sand King', 'Shadow Demon',
                            'Shadow Fiend', 'Shadow Shaman', 'Silencer', 'Skywrath Mage', 'Slardar', 'Slark', 'Sniper',
                            'Spectre', 'Spirit Breaker', 'Storm Spirit', 'Sven', 'Techies', 'Templar Assassin',
                            'Terrorblade', 'Tidehunter', 'Timbersaw', 'Tinker', 'Tiny', 'Treant Protector',
                            'Troll Warlord', 'Tusk', 'Underlord', 'Undying', 'Ursa', 'Vengeful Spirit', 'Venomancer',
                            'Viper', 'Visage', 'Warlock', 'Weaver', 'Windranger', 'Winter Wyvern', 'Witch Doctor',
                            'Wraith King', 'Zeus']
        with open(os.path.join(os.path.dirname(__file__),
                               'twitters.json')) as json_data:
            self.twitter_accounts = json.load(json_data)

    def help(self, param_line, sender, is_admin):
        """Returns all the commands the bot is listening to."""
        command_names = []

        for command in self.get_commands().commands:
            command_names.append(command['aliases'][0])

        line = "Les coassements que j'écoute sont: {0}.".format(
            ', '.join(sorted(command_names)))

        self.get_irc().send_msg(line)

    def motd(self, param_line, sender, is_admin):
        """Display an informative message for the viewers.

        Only admins are able to change the message.
        """
        if is_admin and param_line is not None:
            self.motd_data = 'Message du jour: {0}'.format(param_line)
        self.get_irc().send_msg(self.motd_data)

    def who(self, param_line, sender, is_admin):
        """Display current streamers.

        Only admins are able to change the message.
        """
        if is_admin and param_line is not None:
            self.who_data = 'Streamers actuels: {0}'.format(param_line)
        self.get_irc().send_msg(self.who_data)

    def toolmix(self, param_line, sender, is_admin):
        """Display toolmix links."""
        self.get_irc().send_msg('Trouvez des joueurs pour la league FTV https://www.frogged.tv/compte/toolmix/joueur '
                                'ou directement une team https://www.frogged.tv/compte/toolmix/equipe')

    def league(self, param_line, sender, is_admin):
        """Display league links."""
        self.get_irc().send_msg('Toutes les informations sur la league https://www.frogged.tv/league')

    def youtube(self, param_line, sender, is_admin):
        """Print the youtube official channel of the FroggedTV"""
        self.get_irc().send_msg('Le YouTube de la FroggedTV : '
                                'https://www.youtube.com/FroggedTV')

    def instagram(self, param_line, sender, is_admin):
        """Print the official Instagram account of the FroggedTV"""
        self.get_irc().send_msg('L\'Instagram de la FroggedTV : '
                                'https://www.instagram.com/froggedtv')

    def twitter(self, param_line, sender, is_admin):
        """Display the Twitter acco unt of the asked streamer."""
        if param_line is not None:
            twitter = self.find_twitter(param_line.lower())
        else:
            twitter = self.find_twitter('froggedtv')

        if twitter is not None:
            line = '{0} : {1}'.format(twitter['pretty_name'], twitter['link'])
            self.get_irc().send_msg(line)

    def find_twitter(self, name):
        """Find the twitter account linked to a streamer name.

        Args:
            name: name of the twitter account requested.
        Returns:
            The twitter account information with name as one of it aliases,
            or None if no account is found.
        """
        for twitter_account in self.twitter_accounts:
            if name in twitter_account['aliases']:
                return twitter_account

        return None



    def random_hero(self, param_line, sender, is_admin):
        """Random a hero."""
        hero = random.choice(self.dota_heroes)
        self.get_irc().send_msg('@{0} has randomed {1}.'.format(sender, hero))
