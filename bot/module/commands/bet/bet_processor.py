import os
import sqlite3
import logging
import math
from operator import itemgetter

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
        self.cotes = [1.5, 1.5]

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
            self.cotes = [1, 1]
            for i in range(0, 2):
                for better in self.bets[i]:
                    self.total[i] += self.bets[i][better][1]

            if self.total[0] != 0:
                self.cotes[0] += float(self.total[1] + 10)/self.total[0]
            else:
                self.cotes[0] = 0


            if self.total[1] != 0:
                self.cotes[1] += float(self.total[0] + 10)/self.total[1]
            else:
                self.cotes[1] = 0

            self.get_irc().send_msg('Fin des bets [W|L]: [{0}|{1}] bets, [{2}|{3}] points, retour sur mise de [{4:.2f}|{5:.2f}] monkaHmm'.format(
                len(self.bets[0]), len(self.bets[1]), self.total[0], self.total[1], self.cotes[0], self.cotes[1]
            ))
        elif params[0].lower() in ['win', 'lose']:
            if not self.is_open:
                return
            if len(params) != 2: return
            if not(params[1].lower() == 'all' or params[1].isdigit()) or params[1] == '0': return

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
            if params[1].lower() == 'all':
                bet_value = points.points
            else:
                bet_value = min(int(params[1]), points.points)
            bet_value = max(1, bet_value)

            self.bets[index][sender] = [points.points, bet_value]

            self.get_irc().send_msg("/w {0} Vous avez bet {1} points sur {2}. Vous pouvez modifier tant que le bet est ouvert.".format(sender, bet_value, params[0].lower()))

        elif params[0] == 'result':
            if not is_admin:
                return
            if self.is_open or self.bets is None:
                return
            if len(params) != 2: return
            if params[1].lower() not in ['win', 'lose']: return

            index = 0 if params[1].lower() == 'win' else 1
            counter_index = (index + 1) % 2

            losers = []
            winners = []

            session = self.get_bot().database_sessions()
            for better in self.bets[counter_index]:
                points = session.query(UserPoints).filter(UserPoints.username == better).one_or_none()
                points.points = max(self.bets[counter_index][better][0] - self.bets[counter_index][better][1], 0)
                losers.append({ 'name': better, 'value': points.points - self.bets[counter_index][better][0] })
            for better in self.bets[index]:
                points = session.query(UserPoints).filter(UserPoints.username == better).one_or_none()
                points.points += math.ceil((self.cotes[index]-1)*self.bets[index][better][1])
                winners.append({ 'name': better, 'value': points.points - self.bets[index][better][0] })
            session.commit()

            winners.sort(key=itemgetter('value'), reverse=True)
            if len(winners) > 3: winners = winners[:3]
            losers.sort(key=itemgetter('value'))
            if len(losers) > 3: losers = losers[:3]

            if len(winners) == 0:
                self.get_irc().send_msg("Top pertes: {0}".format(
                    ', '.join(['{0} ({1})'.format(x['name'], x['value']) for x in losers])
                ))
            elif len(losers) == 0:
                self.get_irc().send_msg("Top gains: {0}".format(
                    ', '.join(['{0} (+{1})'.format(x['name'], x['value']) for x in winners])
                ))
            else:
                self.get_irc().send_msg("Tops: {0} / {1}".format(
                    ', '.join(['{0} (+{1})'.format(x['name'], x['value']) for x in winners]),
                    ', '.join(['{0} ({1})'.format(x['name'], x['value']) for x in losers])
                ))

            self.bets = None
            self.total = [0, 0]
            self.cotes = [1.5, 1.5]

    def points(self, param_line, sender, is_admin):
        """Returns players points."""
        session = self.get_bot().database_sessions()
        points = session.query(UserPoints).filter(UserPoints.username == sender).one_or_none()
        if points is None:
            points = UserPoints(sender, 1)
            session.add(points)
            session.commit()

        self.get_irc().send_msg("/w {0} Vous avez {1} points.".format(sender, points.points))

