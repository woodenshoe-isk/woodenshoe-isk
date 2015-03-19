import braintree
import datetime
from decimal import Decimal

class CreditCardProcessing(object):

    braintree.Configuration.configure(
        braintree.Environment.Sandbox,
        "r37tq3rht8wbgwfr",     #merchant_id
        "nywnhm2x4sdn3cpk",     #public_key
        "86wvwtc7zzc44c9x"      #private_key
    )
    
    #wrapper for submitting charges. Submits for settlement
    #automatically.
    @classmethod
    def submit_settlement( cls, transaction_amount='0.0', credit_card_number='', credit_card_expiration=''):
        result = braintree.Transaction.sale({
                "amount": transaction_amount,
            "credit_card": {
                "number": credit_card_number,
                "expiration_date": credit_card_expiration
            },
            "options": {
                "submit_for_settlement": True
            }
        })
        return result
       
    @classmethod
    def get_settlement_batch_totals_today(cls):
        search_results=braintree.Transaction.search( 
            braintree.TransactionSearch.status.in_list( 
                braintree.Transaction.Status.SubmittedForSettlement, 
                braintree.Transaction.Status.Settled, 
                braintree.Transaction.Status.SettlementFailed), 
            braintree.TransactionSearch.created_at >= datetime.datetime.today())
        total= Decimal(0)
        for trans in search_results.items:
            total += trans.amount
        return total
        
            
