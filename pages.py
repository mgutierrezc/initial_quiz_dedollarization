import math
from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants, Player, Group

from django.conf import settings
import string
import random
import time

debug = True
"""docstring format

Method

Description:

Input:

Output:


Class

Description:

Input:

Output:

"""

"""Instructions Pages"""

# TODO: Create an introductory page that explains they are going to be on a payed quiz about the game
# (ser más detallado)

# TODO: Testear timeouts en MTurk

# Por lo demás, ya funciona este quiz

class InitialPage(Page):
    pass

class GeneralRules(Page):
    pass


class Introduction(Page):
    def vars_for_template(self):
        exchange_rate = self.session.config['real_world_currency_per_point']
        # If you don't create a session inside a room, there won't be any label, but a participant unique code only
        foreign_tax = self.session.config['foreign_tax']
        perc_f_tax_consumer = self.session.config['percent_foreign_tax_consumer']
        perc_f_tax_producer = self.session.config['percent_foreign_tax_producer']
        store_cost_hom = self.session.config['token_store_cost_homogeneous']
        store_cost_het = self.session.config['token_store_cost_heterogeneous']
        show_foreign_transactions = self.session.config['show_foreign_transactions']

        # Treatment variable: 0 if baseline, 1 if tax treatment, 2 if cost treatment, 3 show foreign trans treatment
        # Baseline Treatment
        treatment = 0
        # Tax Treatment
        if perc_f_tax_consumer != 0 and perc_f_tax_producer != 0 and foreign_tax != 0:
            treatment = 1
        # 2 Cost Treatment
        elif store_cost_hom != 0 or store_cost_het != 0:
            treatment = 2
        # 3 Show Foreign Trans Treatment
        elif show_foreign_transactions is True:
            treatment = 3

        return dict(participant_id=self.participant.label,
                    exchange_rate=exchange_rate,
                    perc_f_tax_consumer=perc_f_tax_consumer,
                    perc_f_tax_producer=perc_f_tax_producer,
                    foreign_tax=foreign_tax,
                    store_cost_hom=store_cost_hom,
                    store_cost_het=store_cost_het,
                    show_foreign_transactions=show_foreign_transactions,
                    treatment=treatment)


class QuizPage(Page):
    _allow_custom_attributes = True
    form_model = 'player'
    # timeout_seconds = Constants.timer

    def get_form_fields(self):
        return [self.player.current_field()]

    # A dynamic error message is necessary

    def error_message(self, values):
        player = self.player
        language = self.session.config['language']
        current_field = player.current_field()
        correct_answer = Constants.quiz_fields[current_field]
        if values[current_field] != correct_answer:
            player.q_incorrect_attempts += 1
            if language == 0:
                self.player.quiz_incorrect_answer = 'Incorrect. The correct answer is "'\
                                                    + str(Constants.quiz_answers[player.quiz_page_counter]) + '"'
                return self.player.quiz_incorrect_answer

            elif language == 1:
                self.player.quiz_respuesta_incorrecta = 'Incorrecto. La respuesta correcta es "' \
                                                    + str(Constants.respuestas_quiz[player.quiz_page_counter]) + '"'
                return self.player.quiz_respuesta_incorrecta

            else:
                return 'Undefined'

    def vars_for_template(self):
        player = self.player
        quiz_questions = Constants.quiz_questions
        preguntas_quiz = Constants.preguntas_quiz
        language = self.session.config['language']

        index = player.quiz_page_counter
        return {'participant_id': self.participant.label, 'question': quiz_questions[index],
                'pregunta': preguntas_quiz[index],
                'page_number': index + 1, 'incorrect_answer': player.quiz_incorrect_answer,
                'respuesta_incorrecta': player.quiz_respuesta_incorrecta,
                'language': language}

    def before_next_page(self):
        player = self.player
        player.quiz_page_counter += 1

        if self.timeout_happened:
            player.q_timeout = 1
        if player.q_timeout == 1 and player.q_incorrect_attempts == 0:
            player.q_validation = 1
        if player.q_incorrect_attempts == 0 and self.timeout_happened is False:
            player.num_correct += 1
            player.quiz_earnings += Constants.payment_per_answer

        self.participant.vars['quiz_earnings'] += player.quiz_earnings
        player.error_sequence += str(player.q_incorrect_attempts)
        player.timeout_sequence += str(player.q_timeout)
        player.q_timeout = 0
        player.q_incorrect_attempts = 0

    def is_displayed(self):
        if self.participant.vars['MobilePhones'] is False:
            return True
        else:
            return False


class QuizResults(Page):
    form_model = 'player'
    form_fields = ['quiz_dec_2']

    def vars_for_template(self):
        language = self.session.config['language']
        quiz_earnings = self.player.quiz_earnings
        return {'participant_id': self.participant.label, 'language': language,
                'quiz_earnings': quiz_earnings,
                'dollar_amount': self.player.quiz_earnings.to_real_world_currency(self.session)
                }  # Shows subject how much they earned from the quiz

    def before_next_page(self):
        # Adds quiz earnings to player's payoff
        self.participant.vars['quiz_earnings'] = self.player.quiz_earnings.to_real_world_currency(self.session)
        self.participant.vars['quiz_questions_correct'] = self.player.num_correct
        self.player.payoff = self.player.quiz_earnings

    def is_displayed(self):
        if self.participant.vars['MobilePhones'] is False:
            return True
        else:
            return False


class QuizTimeout(Page):
    _allow_custom_attributes = True

    def vars_for_template(self):
        player = self.player
        quiz_questions = Constants.quiz_questions
        preguntas_quiz = Constants.preguntas_quiz
        language = self.session.config['language']

        index = player.quiz_page_counter - 1
        return {'question': quiz_questions[index], 'pregunta': preguntas_quiz,
                'answer': Constants.quiz_answers[index], 'language': language}

    def is_displayed(self):
        player = self.player
        if player.q_validation == 1 and self.participant.vars['MobilePhones'] is False:
            return True
        else:
            return False

    def before_next_page(self):
        self.player.q_validation = 0


# DYNAMIC QUIZ WITH TIMEOUTS
page_sequence = [
    InitialPage,
    GeneralRules,
    Introduction,
    QuizPage,
    QuizPage,
    QuizPage,
    QuizPage,
    QuizResults,
]