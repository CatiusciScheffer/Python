import unittest
from criptoControl import create_app, db
from criptoControl.models import WalletBalance, Transaction
from criptoControl.routes.transactions_routes import realizar_venda
from datetime import datetime

class TestTransactions(unittest.TestCase):
    
    def setUp(self):
        # Configurar o app e o banco de dados para testes
        self.app = create_app('testing')  # Certifique-se de que a configuração 'testing' está no __init__.py
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Criar dados iniciais no banco
        self.wallet_1 = WalletBalance(balance_wallet_id=23, balance_crypto_id=4, balance=50)
        self.wallet_2 = WalletBalance(balance_wallet_id=23, balance_crypto_id=47, balance=1000)
        db.session.add(self.wallet_1)
        db.session.add(self.wallet_2)
        db.session.commit()

    def tearDown(self):
        # Limpar o banco após cada teste
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_realizar_venda_sucesso(self):
        # Teste para transação de venda bem-sucedida
        with self.client:
            response = self.client.post('/reslizar_venda', json={  # Certifique-se de que esta URL é a correta
                'transaction_date': '2024-09-25',
                'payment_wallet_id': 23,
                'receiving_wallet_id': 23,
                'crypto_payment_id': 47,
                'crypto_payment_price': 10.0,
                'crypto_payment_quantity': 1.0,
                'total_paid': 10.0,
                'crypto_receive_id': 4,
                'crypto_receive_price': 0.04,
                'crypto_receive_quantity': 40.0,
                'total_received': 40.0,
                'crypto_fee_id': 47,
                'crypto_fee_price': 0.001,
                'crypto_fee_quantity': 0.001,
                'total_fee': 0.001,
                'transaction_type': 'Venda'
            })

            # Verifique o status da resposta
            self.assertEqual(response.status_code, 200, f"Status Code: {response.status_code}, Response: {response.data}")

            # Verificar que a transação foi registrada
            transaction = Transaction.query.filter_by(crypto_payment_id=47).first()
            self.assertIsNotNone(transaction, "A transação não foi registrada no banco de dados.")



    def test_realizar_venda_sem_saldo(self):
        # Teste para caso de saldo insuficiente
        with self.client:
            result = self.client.post('/route/to/realizar_venda', json={
                'transaction_date': '2024-09-25',
                'payment_wallet_id': 23,
                'receiving_wallet_id': 23,
                'crypto_payment_id': 47,
                'crypto_payment_price': 10.0,
                'crypto_payment_quantity': 2000.0,  # Valor maior que o saldo
                'total_paid': 20000.0,
                'crypto_receive_id': 4,
                'crypto_receive_price': 0.04,
                'crypto_receive_quantity': 80000.0,
                'total_received': 80000.0,
                'crypto_fee_id': 47,
                'crypto_fee_price': 0.001,
                'crypto_fee_quantity': 0.001,
                'total_fee': 0.001,
                'transaction_type': 'Venda'
            })

            # Verificar que a transação não foi registrada
            transaction = Transaction.query.filter_by(crypto_payment_quantity=2000.0).first()
            self.assertIsNone(transaction)

if __name__ == '__main__':
    unittest.main()

