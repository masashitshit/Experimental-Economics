from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        yield (views.Introduction)

        if self.case == 'both_A':
            yield (views.Decide, {"decision": 'A'})
            if self.player.role() == 'player1':
                assert self.player.payoff == Constants.A_player1_payoff
            else:
                assert self.player.payoff == Constants.A_player2_payoff

        if self.case == 'mismatch':
            if self.player.role() == 'player1':
                yield (views.Decide, {"decision": 'A'})
            else:
                yield (views.Decide, {"decision": 'B'})
            assert self.player.payoff == Constants.mismatch_payoff

        yield (views.MyPage)
        yield (views.Results)
