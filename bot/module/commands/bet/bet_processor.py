import os
import sqlite3
import logging
import math

from bot.module.commands.processor import Processor
from bot.models.Points import UserPoints

class BetProcessor(Processor):
    """Processor for all bet commands.

    Attributes:
        bets: all user bets.
        is_open: if bet is open or closed.
    """

    def __init__(self):
        self.bets = None
        self.is_open = False
        self.total = [0, 0]

        if self.bot.config['BET'].getboolean('enabled', False):
            self.commands.extend([{
                'aliases': ['bet', 'b'],
                'command': self.bet
            },{
                'aliases': ['points', 'p'],
                'command': self.points
            },{
                'aliases': ['top'],
                'command': self.top
            }])

    def top(self, param_line, sender, is_admin):
        """Display top 5 betters."""

        session = self.get_bot().database_sessions()
        top_result = []
        for points in session.query(UserPoints).order_by(UserPoints.points.desc()).limit(5):
            top_result.append('{0} ({1})'.format(points.username, points.points))
        self.get_irc().send_msg('Les meilleurs oracles sont {0}'.format(', '.join(top_result)))

    def bet(self, param_line, sender, is_admin):
        """Register a bet of a user."""
        if param_line is None:
            return

        params = param_line.split(' ', maxsplit=1)
        if params[0] == 'open':
            if not is_admin:
                return
            if self.bets is not None:
                self.get_irc().send_msg('Bet non disponible, annulez ou complétez les bets en cours DansGame')
                return
            self.bets = [{}, {}]
            self.is_open = True
            self.get_irc().send_msg('Bet ouvert, utilisez "!bet win/lose X" PogChamp')
        elif params[0] == 'cancel':
            if not is_admin:
                return
            self.bets = None
            self.is_open = False
            self.get_irc().send_msg('Bet annulés Jebaited')
        elif params[0] == 'close':
            if not is_admin:
                return
            self.is_open = False
            self.total = [0, 0]
            for i in range(0, 2):
                for better in self.bets[i]:
                    self.total[i] += self.bets[i][better][1]
            self.get_irc().send_msg('Fin des bets: {0} win de {2} points et {1} lose de {3} points monkaHmm'.format(
                len(self.bets[0]), len(self.bets[1]), self.total[0], self.total[1]
            ))
        elif params[0].lower() in ['win', 'lose']:
            if not self.is_open:
                return
            if len(params) != 2: return
            if not(params[1].lower() == 'all' or params[1].isdigit()): return

            index = 0 if params[0].lower() == 'win' else 1
            counter_index = (index + 1) % 2
            if sender in self.bets[counter_index]:
                self.bets[counter_index].pop(sender)

            session = self.get_bot().database_sessions()
            points = session.query(UserPoints).filter(UserPoints.username == sender).one_or_none()
            if points is None:
                points = UserPoints(sender, 1)
                session.add(points)
                session.commit()
            to_add = points.points
            if params[1].isdigit():
                to_add = min(int(params[1]), points.points)
            self.bets[index][sender] = [points.points, to_add]

            self.get_irc().send_msg("/w {0} Vous avez bet {1} points sur {2}. Vous pouvez modifier tant que le bet est ouvert.".format(sender, to_add, params[0].lower()))

        elif params[0] == 'result':
            if not is_admin:
                return
            if self.is_open or self.bets is None:
                return
            if len(params) != 2: return
            if params[1].lower() not in ['win', 'lose']: return

            index = 0 if params[1].lower() == 'win' else 1
            counter_index = (index + 1) % 2

            session = self.get_bot().database_sessions()
            for better in self.bets[counter_index]:
                points = session.query(UserPoints).filter(UserPoints.username == better).one_or_none()
                points.points = self.bets[counter_index][better][0] - self.bets[counter_index][better][1]

            for better in self.bets[index]:
                points = session.query(UserPoints).filter(UserPoints.username == better).one_or_none()
                points.points += 1
                if self.total[index]!= 0:
                    points.points += math.ceil(self.bets[index][better][1] * self.total[counter_index] / self.total[index])
            session.commit()
            self.bets = None


    def points(self, param_line, sender, is_admin):
        """Returns players points."""
        session = self.get_bot().database_sessions()
        points = session.query(UserPoints).filter(UserPoints.username == sender).one_or_none()
        if points is None:
            points = UserPoints(sender, 1)
            session.add(points)
            session.commit()

        self.get_irc().send_msg("/w {0} Vous avez {1} points.".format(sender, points.points))

