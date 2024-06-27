from pypayment import PayOkPayment, PayOkPaymentType, PayOkCurrency, PaymentStatus
import config

PayOkPayment.authorize(config.PAYOK_KEY, config.API_ID, config.SHOP_ID, config.SECRET_KEY,
                       payment_type=PayOkPaymentType.CARD,
                       currency=PayOkCurrency.RUB,
                       success_url="https://buchma.ru/pay/success.html")

def create_pay(amount, description):
    global payment
    payment = PayOkPayment(amount=amount,
                        description=description,
                        payment_type=PayOkPaymentType.CARD,
                        currency=PayOkCurrency.RUB,
                        success_url="https://buchma.ru/pay/success.html")

    return payment.url

def check_pay():
    if payment.status == PaymentStatus.PAID:
        return "Успешно!"

    if payment.status == PaymentStatus.WAITING:
        return "Платеж ожидает оплаты"

    if payment.status == PaymentStatus.REJECTED:
        return "Платеж был отклонен"

    if payment.status == PaymentStatus.EXPIRED:
        return "Срок действия платежа истек"

