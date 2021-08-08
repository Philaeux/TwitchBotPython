import math
from operator import itemgetter

from bot.models.Points import UserPoints


class BetProcessor:
    """Processor for all bet commands."""

    def __init__(self, bot):
        self.bot = bot
        if not self.bot.config['STRATEGY_BET'].getboolean('enabled', False):
            return

        self.status = 'BET_READY'
        self.bet_type = 'PLAYER'
        self.bet_choices = {
            'PLAYER': ['win', 'lose'],
            'SPECTATOR': ['radiant', 'dire']
        }
        self.bets = None
        self.total = [0, 0]
        self.cotes = [1, 1]

        self.bot.strategy.command_handlers["bet"] = self.bet
        self.bot.strategy.command_handlers["top"] = self.top
        self.bot.strategy.command_handlers["points"] = self.points

    def top(self, sender, is_admin, is_sub, command, arguments):
        """Display top 5 betters."""
        session = self.bot.database.sessions()
        top_result = []
        if arguments == "":
            for points in session.query(UserPoints).order_by(UserPoints.points.desc()).limit(5):
                top_result.append('{0} ({1})'.format(points.username, points.points))
            self.bot.irc.send_msg('Les meilleurs oracles sont {0}'.format(', '.join(top_result)))
        else:
            if not is_admin or not arguments.isdigit():
                return
            offset = int(arguments)
            for points in session.query(UserPoints).order_by(UserPoints.points.desc()).offset(offset-1).limit(5):
                top_result.append('{0} ({1})'.format(points.username, points.points))
            if len(top_result) == 0:
                return
            self.bot.irc.send_msg('Les oracles {0} à {1} sont {2}'.format(offset, offset+len(top_result)-1, ', '.join(top_result)))

    def bet(self, sender, is_admin, is_sub, command, arguments):
        """Register a bet of a user."""
        if arguments is None:
            return

        params = arguments.split(' ', maxsplit=1)
        if params[0] == 'open':
            if not is_admin:
                return
            if self.status != 'BET_READY':
                self.bot.irc.send_msg('Bet non disponible, annulez ou complétez les bets en cours DansGame')
                return
            if len(params) == 2 and params[1] == 'spec':
                self.bet_type = 'SPECTATOR'
            else:
                self.bet_type = 'PLAYER'
            self.bets = [{}, {}]
            self.status = 'BET_OPEN'
            self.bot.irc.send_msg('Bet ouvert, utilisez "!bet {0} X" PogChamp'.format('/'.join(self.bet_choices[self.bet_type])))
        elif params[0] == 'cancel':
            if not is_admin:
                return
            if self.status == 'BET_READY':
                return
            self.bets = None
            self.status = 'BET_READY'
            self.total = [0, 0]
            self.cotes = [1, 1]
            self.bot.irc.send_msg('Bet annulés Jebaited')
        elif params[0] == 'close':
            if not is_admin:
                return
            if self.status != 'BET_OPEN':
                return
            self.status = 'BET_WAITING_RESULT'
            self.total = [0, 0]
            self.cotes = [1 + 0.5, 1 + 0.5]
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

            self.bot.irc.send_msg('Fin des bets: [{0}|{1}] bets, [{2}|{3}] points, retour sur mise de [{4:.2f}|{5:.2f}] monkaHmm'.format(
                len(self.bets[0]), len(self.bets[1]), self.total[0], self.total[1], self.cotes[0], self.cotes[1]
            ))
        elif params[0].lower() in self.bet_choices[self.bet_type]:
            if self.status != 'BET_OPEN':
                return
            if len(params) != 2:
                return
            if not(params[1].lower() == 'all' or params[1].isdigit()) or params[1] == '0':
                return

            index = 0 if params[0].lower() in ['win', 'radiant'] else 1
            counter_index = (index + 1) % 2
            if sender in self.bets[counter_index]:
                return

            session = self.bot.database.sessions()
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

            if sender in self.bets[index] and self.bets[index][sender][1] >= bet_value:
                return
            else:
                self.bets[index][sender] = [points.points, bet_value]

            # Too much bets make it impossible for the bot to send that much private messages.
            self.bot.irc.send_msg("{0} a bet {1} points sur {2}.".format(sender, bet_value, params[0].lower()))
        elif params[0] == 'result':
            if not is_admin:
                return
            if self.status != 'BET_WAITING_RESULT':
                return
            if len(params) != 2:
                return
            if params[1].lower() not in self.bet_choices[self.bet_type]:
                return

            index = 0 if params[1].lower() in ['win', 'radiant'] else 1
            counter_index = (index + 1) % 2

            losers = []
            winners = []

            session = self.bot.database.sessions()
            for better in self.bets[counter_index]:
                points = session.query(UserPoints).filter(UserPoints.username == better).one_or_none()
                points.points = max(self.bets[counter_index][better][0] - self.bets[counter_index][better][1], 1)
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
                self.bot.irc.send_msg("Top pertes: {0}".format(
                    ', '.join(['{0} ({1})'.format(x['name'], x['value']) for x in losers])
                ))
            elif len(losers) == 0:
                self.bot.irc.send_msg("Top gains: {0}".format(
                    ', '.join(['{0} (+{1})'.format(x['name'], x['value']) for x in winners])
                ))
            else:
                self.bot.irc.send_msg("Tops: {0} / {1}".format(
                    ', '.join(['{0} (+{1})'.format(x['name'], x['value']) for x in winners]),
                    ', '.join(['{0} ({1})'.format(x['name'], x['value']) for x in losers])
                ))

            self.status = 'BET_READY'
            self.bets = None
            self.total = [0, 0]
            self.cotes = [1, 1]
        elif params[0] == 'reset_database':
            if not is_admin:
                return
            if self.status != 'BET_READY':
                self.bot.irc.send_msg("Impossible de nettoyer la matrice lorsqu'un bet est en cours Pepega")
                return
            session = self.bot.database.sessions()
            session.query(UserPoints).delete()
            session.commit()
            self.bot.irc.send_msg("Un modo a reset les points NotLikeThis")

    def points(self, sender, is_admin, is_sub, command, arguments):
        """Returns players points."""
        if arguments == "":
            session = self.bot.database.sessions()
            points = session.query(UserPoints).filter(UserPoints.username == sender).one_or_none()
            if points is None:
                points = UserPoints(sender, 1)
                session.add(points)
                session.commit()

            self.bot.irc.send_msg("{0} a {1} points.".format(sender, points.points))
        else:
            if not is_admin:
                return
            player = arguments.lower()
            session = self.bot.database.sessions()
            points = session.query(UserPoints).filter(UserPoints.username == player).one_or_none()
            if points is None:
                return
            else:
                self.bot.irc.send_msg("{0} a {1} points.".format(arguments, points.points))
