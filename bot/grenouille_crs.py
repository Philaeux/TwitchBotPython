import os
import sqlite3

class GrenouilleCRS:
    """The module of the bot responsible for the Chasse Ragequit & Safari interactions.

    Attributes
        grenouille_bot - The main class the module is linked to.
    """

    def __init__(self, grenouille_bot):
        self.grenouille_bot = grenouille_bot

        self.vote_opened = False
        self.vote_heroes = []
        self.vote_voters = []

        self.connection = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'heroes.db'))
        self.cursor = self.connection.cursor()

        self.actions = [
            {
                'name': 'open',
                'action': self.open
            },
            {
                'name': 'vote',
                'action': self.vote
            },
            {
                'name': 'close',
                'action': self.close
            }
        ]

    def find_action(self, name):
        """Find if asked action exists and returns it

        :return:
        """
        for action in self.actions:
            if (name == action['name']):
                return action

        return None

    def find_hero(self, name):
        """Find the hero named on database
        """

        self.cursor.execute('SELECT * FROM heroes LEFT JOIN heroes_aliases ON heroes.id = heroes_aliases.id_hero WHERE name LIKE ?1 OR heroes_aliases.alias LIKE ?1', [name])

        return self.cursor.fetchone()

    def execute(self, sender = None, is_admin = False, command = None, parameters = None):
        action = self.find_action(command)

        if action is not None:
            return action['action'](sender, is_admin, parameters)
        else:
            return

    def open(self, sender = None, is_admin = False, parameters = None):
        """Open a vote
        """

        if not is_admin:
            return

        if self.vote_opened:
            return ['Erreur : Un vote est déjà en cours !']

        list_of_heros = [hero.strip() for hero in parameters.split(',')]

        if len(list_of_heros) != 5:
            return ['Erreur : Il faut 5 héros pour ouvrir un vote !']

        for hero in list_of_heros:
            hero_fetched = self.find_hero(hero)

            if hero_fetched is None:
                return ['Erreur : Impossible de trouver le héro ' + hero]

            self.vote_heroes.append({
                'id': hero_fetched[0],
                'name': hero_fetched[1],
                'votes': 0
            })

        self.vote_opened = True

        return ['Le vote a été ouvert !', 'Liste des cibles : ' + ', '.join([hero['name'] for hero in self.vote_heroes]), 'Pour voter, tapez : !crs vote <nom de la cible> dans le chat !']

    def vote(self, sender = None, is_admin = False, parameters = None):
        """Register a vote
        """

        if (not self.vote_opened) or (parameters is None) or (sender is None):
            return

        # Check if user has already voted
        if sender in self.vote_voters:
            return

        hero_to_vote = self.find_hero(parameters)

        if hero_to_vote is None:
            return ['Impossible de trouver le héro ' + parameters]

        for hero in self.vote_heroes:
            if hero_to_vote[0] == hero['id']:
                hero['votes'] += 1

                self.vote_voters.append(sender)

                return

    def close(self, sender = None, is_admin = False, parameters = None):
        """Close the vote in progress (if there is one)
        """

        if not is_admin or not self.vote_opened:
            return

        selected_target = self.vote_heroes.pop()
        total_votes = selected_target['votes']

        for hero in self.vote_heroes:
            if hero['votes'] > selected_target['votes']:
                selected_target = hero

            total_votes += hero['votes']

        self.vote_opened = False
        self.vote_heroes = []

        return ['Info : Le vote a été fermé !', 'La cible est désignée est {} ({:.0f}% des voix)'.format(selected_target['name'], 100 * selected_target['votes'] / total_votes)]
