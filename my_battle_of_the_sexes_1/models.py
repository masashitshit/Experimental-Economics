from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = '高橋　雅士'

doc = """
audience treatment
"""


class Constants(BaseConstants):
    name_in_url = 'my_battle_of_the_sexes_1'
    players_per_group = 2
    num_rounds = 6


    instructions_template = 'my_battle_of_the_sexes_1/Instructions.html'

    # """Amount rewarded to husband if football is chosen"""
    A_player1_payoff = B_player2_payoff = c(300)

    # Amount rewarded to wife if football is chosen
    B_player1_payoff = A_player2_payoff = c(100)

    # amount rewarded to either if the choices don't match
    mismatch_payoff = c(0)

class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()    #セッションごとにランダムに組み合わせている



class Group(BaseGroup):
    def set_payoffs(self):
        player1 = self.get_player_by_role('player1')
        player2 = self.get_player_by_role('player2')

        if player1.decision != player2.decision:
            player1.payoff = Constants.mismatch_payoff
            player2.payoff = Constants.mismatch_payoff

        else:
            if player1.decision == 'A':
                player1.payoff = Constants.A_player1_payoff
                player2.payoff = Constants.A_player2_payoff
            else:
                player1.payoff = Constants.B_player1_payoff
                player2.payoff = Constants.B_player2_payoff

        for player in self.get_players():
            self.cumulative_1_payoff = sum([p.payoff for p in player1.in_all_rounds()])
            self.cumulative_2_payoff = sum([p.payoff for p in player2.in_all_rounds()])


class Player(BasePlayer):
    decision = models.CharField(
        choices=['A', 'B'],
        doc="""Either A or B""",
        widget=widgets.RadioSelect()
    )

    def other_player(self):
        """Returns other player in group"""
        return self.get_others_in_group()[0]

    def role(self):
        if self.id_in_group == 1:
            return 'player1'
        if self.id_in_group == 2:
            return 'player2'
