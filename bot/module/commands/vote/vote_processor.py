import os
import sqlite3
import logging

from bot.module.commands.processor import Processor


class VoteProcessor(Processor):
    """Processor for all vote commands.

    Attributes:
        choices: choices in a vote.
        votes: all user votes.
    """

    def __init__(self):

        self.choices = None
        self.votes = None

    def is_vote_open(self):
        """Helper to test if a vote is currently running.

        Returns:
            True if a vote is running, False otherwise.
        """
        return self.choices is not None

    def vote_open(self, param_line, sender, is_admin):
        """Open a vote."""
        if not is_admin:
            return

        if self.is_vote_open():
            self.get_irc().send_msg("Un vote est déjà en cours.")
            return

        choices = [choice.strip() for choice in param_line.split(',')]
        choices = list(filter(None, choices))
        if len(choices) == 0:
            return

        self.choices = choices
        self.votes = {}

        line = 'Votez avec !choix x || {}'.format(
            ', '.join('{0} => {1}'.format((index+1), value)
            for index, value in enumerate(self.choices)))
        self.get_irc().send_msg(line)

    def vote(self, param_line, sender, is_admin):
        """Register a vote of a user."""
        if not self.is_vote_open() or param_line is None or sender is None:
            return

        # Check if the choice exists
        try:
            value = int(param_line)
        except (ValueError, TypeError):
            return
        if value > len(self.choices):
            return

        self.votes[sender] = value-1

    def vote_close(self, param_line, sender, is_admin):
        """Close the vote in progress (if there is one)."""
        if not is_admin or not self.is_vote_open():
            return

        total_votes = max(1, len(self.votes))
        vote_counts = [0 for i in self.choices]
        for vote in self.votes.values():
            vote_counts[vote-1] += 1

        sorted_indexes = sorted(range(len(vote_counts)), key=lambda k: vote_counts[k], reverse=True)

        line = "Résultats: {}.".format(
            ', '.join(['{}. {} ({:.1f}%)'.format(index,
                                                self.choices[index],
                                                100.0 * vote_counts[index]/total_votes)
                       for index in sorted_indexes])
        )
        self.choices = None
        self.votes = None
        self.get_irc().send_msg(line)

    def vote_info(self, param_line, sender, is_admin):
        """Give info about current vote.."""
        if not self.is_vote_open():
            return

        line = 'Votez avec !choix x || {}'.format(
            ', '.join('{0} => {1}'.format((index+1), value)
            for index, value in enumerate(self.choices)))
        self.get_irc().send_msg(line)

