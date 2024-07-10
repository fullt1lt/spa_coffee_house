from django.core.mail import send_mail
from spa.settings import DEFAULT_FROM_EMAIL

class SendMail:

    @staticmethod
    def send_email_to_client(record):
        if record.client:
            subject = 'Ваше замовлення прийнято'
            message = (
                f'Вітаю, {record.client.first_name} {record.client.last_name}, ваше замовлення на процедуру '
                f'{record.procedure.type_category.name} підтверджено. Дата і час: {record.schedule.day} {record.start_time}.'
            )
            send_mail(
                subject,
                message,
                DEFAULT_FROM_EMAIL,
                [record.client.email],
                fail_silently=False,
            )

    @staticmethod
    def send_email_to_therapist(record):
        subject = 'Нова запис на процедуру'
        message = (
            f'Вітаю, {record.schedule.therapist.user.first_name} {record.schedule.therapist.user.last_name}, у вас новий запис '
            f'на процедуру {record.procedure.type_category.name}. Клієнт: {record.client.get_full_name()}. Дата і час: '
            f'{record.schedule.day} {record.start_time}.'
        )
        send_mail(
            subject,
            message,
            DEFAULT_FROM_EMAIL,
            [DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
