
def logger(message, answer):
    print("\n ------ ")
    from datetime import datetime
    print(datetime.now())
    print("Сообщение от {0} {1}. (id = {2}) \n Текст - {3} \n ID сообщения: {4}".format(message.from_user.first_name, message.from_user.username, str(message.from_user.id), message.text, message.message_id))
    print(answer)

def auth_user(message):
    from datetime import datetime
    userId = str(message.from_user.id)
    userLogin = message.from_user.username


def generate_log_message(message, answer=None):
    msg = "Сообщение от: {0} {1} id: {2} Текст: {3} ID сообщения: {4} Ответ: {5}".format(message.from_user.first_name, message.from_user.username, str(message.from_user.id), message.text, message.message_id, answer)
    return msg