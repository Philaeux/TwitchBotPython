import os
import sqlite3
import logging

from bot.module.commands.processor import Processor


class CrsProcessor(Processor):
    """Processor for all crs commands.

    Attributes:
        connection: Database connection to the heroes names.
        cursor: cursor to request the database.

        hero_choices: hero choices in a vote.
        votes: all user votes.
    """

    def __init__(self):
        self.connection = sqlite3.connect(
            os.path.join(os.path.dirname(__file__),'heroes.db'))
        self.cursor = self.connection.cursor()

        self.hero_choices = None
        self.votes = None

    def find_hero(self, name):
        """Find the hero named on database.

        Args:
            name: on of the aliases of the hero
        Returns:
            xxx
        """
        self.cursor.execute(
            "SELECT * FROM heroes "
            "LEFT JOIN heroes_aliases ON heroes.id = heroes_aliases.id_hero "
            "WHERE heroes.name LIKE ?1 OR heroes_aliases.alias LIKE ?1", [name])

        return self.cursor.fetchone()

    def is_vote_open(self):
        """Helper to test if a vote is currently running.

        Returns:
            True if a vote is running, False otherwise.
        """
        return self.hero_choices is not None

    def crs(self, param_line, sender, is_admin):
        """Display information about CRS."""
        line = ('On a besoin de vos stratégies pour le prochain Chasse, '
                'Ragequit & Safari. Donnez vos idées sur bit.ly/taymaproie')
        self.get_irc().send_msg(line)

    def crs_open(self, param_line, sender, is_admin):
        """Open a CRS vote."""
        if not is_admin:
            return

        if self.is_vote_open():
            self.get_irc().send_msg("Un vote est déjà en cours.")
            return
        else:
            self.hero_choices = {}
            self.votes = {}

        list_of_heroes = [hero.strip() for hero in param_line.split(',')]

        if len(list_of_heroes) != 5:
            self.get_irc().send_msg("Il faut 5 héros pour ouvrir un vote CRS.")
            return

        for hero in list_of_heroes:
            hero_fetched = self.find_hero(hero)

            if hero_fetched is None:
                self.get_irc().send_msg(
                    "Impossible de trouver le héro '{}'.".format(hero))
                self.hero_choices = None
                return

            self.hero_choices[hero_fetched[0]] = {
                'id': hero_fetched[0],
                'name': hero_fetched[1],
                'votes': 0
            }

        line = 'Choix de la cible avec !crs_vote: {}'.format(
            ', '.join([hero['name'] for hero in self.hero_choices.values()]))
        self.get_irc().send_msg(line)

    def crs_vote(self, param_line, sender, is_admin):
        """Register a vote of a user."""
        if not self.is_vote_open() or param_line is None or sender is None:
            return

        # Check if the hero to vote for exists
        hero_to_vote = self.find_hero(param_line)

        if hero_to_vote is None:
            line = "Impossible de trouver le héro '{}'.".format(param_line)
            self.get_irc().send_private_msg(sender, line)
            return

        if hero_to_vote[0] in self.hero_choices:
            self.votes[sender] = hero_to_vote[0]
        else:
            line = "{} n'est pas disponible, héros disponibles: {}.".format(
                hero_to_vote[1],
                ', '.join([h['name'] for h in self.hero_choices.values()]))
            self.get_irc().send_private_msg(sender, line)

    def crs_close(self, param_line, sender, is_admin):
        """Close the vote in progress (if there is one)."""
        if not is_admin or not self.is_vote_open():
            return

        total_votes = len(self.votes)
        for vote in self.votes.values():
            self.hero_choices[vote]['votes'] += 1

        results = sorted(list(self.hero_choices.values()),
                         key=lambda hero: hero['votes'], reverse=True)
        self.hero_choices = None
        self.votes = None

        line = "Résultats: {}.".format(
            ', '.join(['{} ({:.1f}%)'.format(hero['name'],
                                             100.0 * hero['votes']/total_votes)
                       for hero in results])
        )
        self.get_irc().send_msg(line)
