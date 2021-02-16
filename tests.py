from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from otree.api import SubmissionMustFail
from .models import Constants
import test_cases as tc
import random as r


# FOR ALPHA/BETA TESTING
class PlayerBot(Bot): 
    """"This class represents a virtual player that will input the values that each page requires and that allows to
        test if there are errors in a specific page or field.

        -Yield statements will change the value of the fields
        -Assert statements check if the field values have a specific value or not
        -SubmissionMustFail stops the game if an invalid value submitted has been accepted
        
        There are two main modes for the bots

        *alpha: They check if the game runs with values that shouldn't be accepted by each variable. It checks:
            **inside the boundaries: checks for errors using inside the boundaries
            **in the boundaries: checks for errors using the boundary values (Because this task has fixed values
            predefined as answers, the fields should not accept this values unless the fixed answer is a bound. This is
            not the case for the Collateral Game task)
            **outside the boundaries: checks for errors using values outside the boundaries
            **different types of values: checks if the values that has been inputted are the same type of the respective
             variables

        *beta: They check how the game would run in a real environment with a big amount of players. To do this testing,
            its only needed to run a huge number of bots.
    """

    def play_round(self):

        yield (pages.WelcomePage)
        yield (pages.TaskOverview)
        yield (pages.RoleAssignment)
        yield (pages.LoanAgreement)
        yield (pages.LoanFulfillment)
        yield (pages.LoanRemediation)
        yield (pages.TaskRepayment)
        yield (pages.ScoreSheetOverview)

        if self.player.role() == 'lender':
            # VARIABLE: prac_loan_input
            # Invalid value of the same type
            boundaries = tc.bounds_practice
            if self.player.prac_loan not in boundaries:
                for bound in boundaries:
                    yield SubmissionMustFail(pages.PracLoanOffer,
                                             {'prac_loan_input': bound})

            out_of_bounds = tc.out_of_bounds_practice
            for out in out_of_bounds:
                yield SubmissionMustFail(pages.PracLoanOffer,
                                         {'prac_loan_input': out})

            # Invalid value from a different type
            invalids = tc.type_errors_integer
            for invalid in invalids:
                yield SubmissionMustFail(pages.PracLoanOffer,
                                         {'prac_loan_input': invalid})

            # Valid answer
            yield (pages.PracLoanOffer, {'prac_loan_input': self.player.prac_loan})
            assert self.player.prac_loan_input == self.player.prac_loan

            if Constants.contract_enforcement is False:

                # VARIABLE: prac_collateral_decision
                # Invalid value of the same type
                bounds_and_out_of_bounds = ['No', 'a']
                for bound_and_out in bounds_and_out_of_bounds:
                    yield SubmissionMustFail(pages.PracCollateralDecision,
                                             {'prac_collateral_decision': bound_and_out})

                # Invalid value from a different type
                invalids = tc.type_errors_char
                for invalid in invalids:
                    yield SubmissionMustFail(pages.PracCollateralDecision,
                                             {'prac_collateral_decision': invalid})

                # Valid answer
                yield (pages.PracCollateralDecision,
                       {'prac_collateral_decision': 'Yes'})
                assert self.player.prac_collateral_decision == 'Yes'

                # VARIABLE: prac_recovered_collateral_input
                # Invalid value of the same type
                boundaries = [1, self.player.prac_project_return]
                if self.player.prac_recovered_collateral not in boundaries:
                    for bound in boundaries:
                        yield SubmissionMustFail(pages.PracCollateralSeizure,
                                                 {'prac_recovered_collateral_input': bound})

                out_of_bounds = [0, self.player.prac_project_return + 1]
                for out in out_of_bounds:
                    yield SubmissionMustFail(pages.PracCollateralSeizure,
                                             {'prac_recovered_collateral_input': out})

                # Invalid value from a different type
                invalids = tc.type_errors_integer
                for invalid in invalids:
                    yield SubmissionMustFail(pages.PracCollateralSeizure,
                                             {'prac_recovered_collateral_input': invalid})

                # Valid answer
                yield (pages.PracCollateralSeizure,
                       {'prac_recovered_collateral_input': self.player.prac_recovered_collateral})
                assert self.player.prac_recovered_collateral == self.player.prac_recovered_collateral

            else:
                yield (pages.PracCollateralDecision)
                yield (pages.PracCollateralSeizure)

        else:
            # VARIABLE: prac_collateral_input
            # Invalid value of the same type
            boundaries = tc.bounds_practice
            if self.player.prac_collateral not in boundaries:
                for bound in boundaries:
                    yield SubmissionMustFail(pages.PracCollateralOffer,
                                             {'prac_collateral_input': bound})

            out_of_bounds = tc.out_of_bounds_practice
            for out in out_of_bounds:
                yield SubmissionMustFail(pages.PracCollateralOffer,
                                         {'prac_collateral_input': out})

            # Invalid value from a different type
            invalids = tc.type_errors_integer
            for invalid in invalids:
                yield SubmissionMustFail(pages.PracCollateralOffer,
                                         {'prac_collateral_input': invalid})

            # Valid answer
            yield (pages.PracCollateralOffer,
                   {'prac_collateral_input': self.player.prac_collateral})
            assert self.player.prac_collateral_input == self.player.prac_collateral

            # VARIABLE: prac_loan_package_decision
            # Invalid value of the same type
            bounds_and_out_of_bounds = ['No', 'a']
            for bound_and_out in bounds_and_out_of_bounds:
                yield SubmissionMustFail(pages.PracLoanPackageDecision,
                                         {'prac_loan_package_decision': bound_and_out})

            # Invalid value from a different type
            invalids = tc.type_errors_char
            for invalid in invalids:
                yield SubmissionMustFail(pages.PracLoanPackageDecision,
                                         {'prac_loan_package_decision': invalid})

            # Valid answer
            yield (pages.PracLoanPackageDecision,
                   {'prac_loan_package_decision': 'Yes'})
            assert self.player.prac_loan_package_decision == 'Yes'

            # VARIABLE: prac_repayment_input
            # Invalid value of the same type
            boundaries = [1, self.player.prac_project_return]
            if self.player.prac_repayment not in boundaries:
                for bound in boundaries:
                    yield SubmissionMustFail(pages.PracReturnRealization,
                                             {'prac_repayment_input': bound})

            out_of_bounds = [0, self.player.prac_project_return + 1]
            for out in out_of_bounds:
                yield SubmissionMustFail(pages.PracReturnRealization,
                                         {'prac_repayment_input': out})

            # Invalid value from a different type
            invalids = tc.type_errors_integer
            for invalid in invalids:
                yield SubmissionMustFail(pages.PracReturnRealization,
                                         {'prac_repayment_input': invalid})

            # Valid answer
            yield (pages.PracReturnRealization, {'prac_repayment_input': self.player.prac_repayment})
            assert self.player.prac_repayment_input == self.player.prac_repayment

        yield (pages.PracResults)

        # Values for Quiz
        for i in range(1, 7):
            # VARIABLE: 'question_{}_response'.format(i)
            # Invalid value of the same type

            out_of_bounds = tc.out_of_bounds_quiz
            for out in out_of_bounds:
                yield SubmissionMustFail(pages.QuizPage,
                                         {'question_{}_response'.format(i): out})

            # Invalid value from a different type
            if i != 1:
                invalids = tc.type_errors_integer
            else:
                invalids = tc.type_errors_boolean

            for invalid in invalids:
                yield SubmissionMustFail(pages.QuizPage,
                                         {'question_{}_response'.format(i): invalid})

            # Valid answer
            yield (pages.QuizPage, {'question_{}_response'.format(i): tc.correct_quiz_answers['correct{}'.format(i)]})

        yield (pages.QuizResults)

# TODO: Use the following code template to create a function that does the alpha testing


"""
# CODE TEMPLATE FOR BOTS

                # VARIABLE: 
                # Invalid value of the same type
                boundaries = 
                if self.player. not in boundaries:
                    for bound in boundaries:
                        yield SubmissionMustFail(pages.,
                                                 {'': bound})

                out_of_bounds = 
                for out in out_of_bounds:
                    yield SubmissionMustFail(pages.,
                                             {'': out})

                # Invalid value from a different type
                invalids = 
                for invalid in invalids:
                    yield SubmissionMustFail(pages.,
                                             {'': invalid})

                # Valid answer
"""