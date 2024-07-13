import logging
import re
import psycopg2
from psycopg2 import Error
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import os
import subprocess
from dotenv import load_dotenv

import paramiko

load_dotenv()


host1 = os.getenv('RM_HOST')
port2 = os.getenv('RM_PORT')
username3 = os.getenv('RM_USER')
password4 = os.getenv('RM_PASSWORD')


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host1, username=username3, password=password4, port=port2)



TOKEN = os.getenv('TOKEN')

# Подключаем логирование
logging.basicConfig(filename='logfile.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Start Program')
logger = logging.getLogger(__name__)

# LESSION 1:
def LinuxGetRelease(update: Update, context):
    stdin, stdout, stderr = client.exec_command('lsb_release -a')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    logging.info(data)
    update.message.reply_text(data)
def LinuxGetUname(update: Update, context):
    stdin, stdout, stderr = client.exec_command('uname')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    logging.info(data)
    update.message.reply_text(data)
def LinuxGetUptime(update: Update, context):
    stdin, stdout, stderr = client.exec_command('uptime')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    logging.info(data)
    update.message.reply_text(data)
def LinuxGetDF(update: Update, context):
    stdin, stdout, stderr = client.exec_command('df')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    logging.info(data)
    update.message.reply_text(data)
def LinuxGetFree(update: Update, context):
    stdin, stdout, stderr = client.exec_command('free')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    logging.info(data)
    update.message.reply_text(data)
def LinuxGetMpstat(update: Update, context):
    stdin, stdout, stderr = client.exec_command('mpstat')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    logging.info(data)
    update.message.reply_text(data)
def LinuxGetW(update: Update, context):
    stdin, stdout, stderr = client.exec_command('w')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    logging.info(data)
    update.message.reply_text(data)
def LinuxGetAuths(update: Update, context):
    stdin, stdout, stderr = client.exec_command('tail /var/log/auth.log --lines=10')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    logging.info(data)
    update.message.reply_text(data)
def LinuxGetCritical(update: Update, context):
    stdin, stdout, stderr = client.exec_command("tail /var/log/kern.log --lines=5")
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    logging.info(data)
    update.message.reply_text(data)
def LinuxGetPS(update: Update, context):
    stdin, stdout, stderr = client.exec_command('ps -s')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    logging.info(data)
    update.message.reply_text(data)
def LinuxGetSS(update: Update, context):
    stdin, stdout, stderr = client.exec_command('ss -s')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    logging.info(data)
    update.message.reply_text(data)
def VerifyGetAptList(update: Update, context):
    update.message.reply_text('Type 1 to print out all upgradable programs or enter a name of a specific program to check its status')

    return 'LinuxGetAptList'
def LinuxGetAptList(update: Update, context):
    user_input = update.message.text

    if user_input == '1':
        stdin, stdout, stderr = client.exec_command('apt list --upgradable')
        data = stdout.read() + stderr.read()
        data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
        logging.info(data)
        update.message.reply_text(data)
        return ConversationHandler.END
    else:
        user_input2 = update.message.text
        variable = "apt list " + user_input2
        stdin, stdout, stderr = client.exec_command(variable)
        data = stdout.read() + stderr.read()
        data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
        logging.info(data)
        update.message.reply_text(data)
        return ConversationHandler.END
def LinuxGetServices(update: Update, context):
    stdin, stdout, stderr = client.exec_command('systemctl list-units --state=failed')
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    logging.info(data)
    update.message.reply_text(data)
def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!')
def helpCommand(update: Update, context):
    update.message.reply_text('Help!')
def VerifyPasswordCommand(update: Update, context):
    update.message.reply_text('Give me the password to check its security: ')

    return 'VerifyPassword'
def VerifyPassword(update: Update, context):
    user_input = update.message.text
    passregex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
    passlist = passregex.findall(user_input)
    logging.info(passlist)
    if not passlist:
        update.message.reply_text('Weak password. Try again.')
        return
    else:
        update.message.reply_text('Strong password! Good to go!')
        return ConversationHandler.END
def echo(update: Update, context):
    update.message.reply_text(update.message.text)

# LESSION 2:

def SQLGetReplicationLogs(update: Update, context: CallbackContext) -> None:
    try:
        # Выполнение команды для получения логов
        result = subprocess.run(
            ["bash", "-c", f"cat {LOG_FILE_PATH} | grep repl | tail -n 15"],
            capture_output=True,
            text=True,
            check=True  # Проверка наличия ошибок выполнения
        )
        logs = result.stdout
        if logs:
            update.message.reply_text(f"Последние репликационные логи:\n{logs}")
        else:
            update.message.reply_text("Репликационные логи не найдены.")
    except subprocess.CalledProcessError as e:
        update.message.reply_text(f"Ошибка при выполнении команды: {e}")
    except Exception as e:
        update.message.reply_text(f"Ошибка при получении логов: {str(e)}")


def SQLGetEmails(update: Update, contest):
    try:
        connection = psycopg2.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"), database=os.getenv("DB_DATABASE"))
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM email_table;")
        data = cursor.fetchall()
        for row in data:
            update.message.reply_text(row)
            logging.info(row)
            logging.info("Email_table grab success!")
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
def SQLGetPhoneNumbers(update: Update, contest):
    try:
        connection = psycopg2.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"), database=os.getenv("DB_DATABASE"))
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM phonenumber_table;")
        data = cursor.fetchall()
        for row in data:
            update.message.reply_text(row)
            logging.info(row)
            logging.info("Phone_table grab success!")
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')

    return 'findPhoneNumbers'
def findPhoneNumbers(update: Update, context):
    user_input = update.message.text
    global phoneNumberList

    phoneNumberList= re.findall(r"\+?7[ -]?\(?\d{3}\)?[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}|8[ -]?\(?\d{3}\)?[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}", user_input)
    logging.info(phoneNumberList)
    if not phoneNumberList:
        update.message.reply_text('Телефонные номера не найдены')
        return ConversationHandler.END

    phoneNumbers = ''
    for i in range(len(phoneNumberList)):
        phoneNumbers += f'{i + 1}. {phoneNumberList[i]}\n'

    update.message.reply_text(phoneNumbers)
    update.message.reply_text('Если вы хотите ввести найденные почты в базу данных нажмите 1, если нет нажмите 2')
    return 'SQLTIME2'

def SQLFindPhoneNumbers(update: Update, context):
    user_input = update.message.text
    phoneNumbers = ''
    if user_input == '1':
        try:
            connection = psycopg2.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"), database=os.getenv("DB_DATABASE"))
            cursor = connection.cursor()
            for i in range(len(phoneNumberList)):
                phoneNumbers = f'{phoneNumberList[i]}'
                print(type(phoneNumbers))
                execution_command = "INSERT INTO phonenumber_table (phone_number) VALUES ('" + phoneNumbers + "');"
                logging.info(phoneNumbers)
                cursor.execute(execution_command)
                connection.commit()
            update.message.reply_text('Данные успешно вписанны')
            logging.info("Команда успешно выполнена")
        except (Exception, Error) as error:
            logging.error("Ошибка при работе с PostgreSQL: %s", error)
            update.message.reply_text('Ошибка')
        finally:
            if connection is not None:
                cursor.close()
                connection.close()
                logging.info("Соединение с PostgreSQL закрыто")
                return ConversationHandler.END
    
    elif user_input == '2':
        update.message.reply_text('Exit')
        return ConversationHandler.END
def findEmailCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска Email: ')

    return 'findEmail'
def findEmail(update: Update, context):
    user_input = update.message.text

    global EmailList
    EmailList= re.findall(r"\w+\@\w+\.\w+", user_input)

    logging.info(EmailList)

    if not EmailList:
        update.message.reply_text('Emails Not Found')
        return ConversationHandler.END

    Emails = ''
    for i in range(len(EmailList)):
        Emails += f'{i + 1}. {EmailList[i]}\n'

    update.message.reply_text(Emails)

    update.message.reply_text('Если вы хотите ввести найденные почты в базу данных нажмите 1, если нет нажмите 2')
    return 'SQLTIME'
def SQLFindEmail(update: Update, context):
    user_input = update.message.text
    Emails = ''
    if user_input == '1':
        try:
            connection = psycopg2.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"), database=os.getenv("DB_DATABASE"))
            cursor = connection.cursor()
            for i in range(len(EmailList)):
                Emails = f'{EmailList[i]}'
                print(type(Emails))
                execution_command = "INSERT INTO email_table (email) VALUES ('" + Emails + "');"
                logging.info(Emails)
                cursor.execute(execution_command)
                connection.commit()
            update.message.reply_text('Данные успешно вписанны')
            logging.info("Команда успешно выполнена")
        except (Exception, Error) as error:
            logging.error("Ошибка при работе с PostgreSQL: %s", error)
            update.message.reply_text('Ошибка')
        finally:
            if connection is not None:
                cursor.close()
                connection.close()
                logging.info("Соединение с PostgreSQL закрыто")
                return ConversationHandler.END
    
    elif user_input == '2':
        update.message.reply_text('Exit')
        return ConversationHandler.END








def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('findPhoneNumbers', findPhoneNumbersCommand)],
        states={
            'findPhoneNumbers': [MessageHandler(Filters.text & ~Filters.command, findPhoneNumbers)],
            'SQLTIME2': [MessageHandler(Filters.text & ~Filters.command, SQLFindPhoneNumbers)],
        },
        fallbacks=[]
    )

    convHandlerFindEmail = ConversationHandler(
        entry_points=[CommandHandler('findEmail', findEmailCommand)],
        states={
            'findEmail': [MessageHandler(Filters.text & ~Filters.command, findEmail)],
            'SQLTIME': [MessageHandler(Filters.text & ~Filters.command, SQLFindEmail)],
        },
        fallbacks=[]
    )

    Passwordverifier = ConversationHandler(
        entry_points=[CommandHandler('verify_password', VerifyPasswordCommand)],
        states={
            'VerifyPassword': [MessageHandler(Filters.text & ~Filters.command, VerifyPassword)],
        },
        fallbacks=[]
    )
    convHandleraptget= ConversationHandler(
        entry_points=[CommandHandler('get_apt_list',  VerifyGetAptList)],
        states={
            'LinuxGetAptList': [MessageHandler(Filters.text & ~Filters.command, LinuxGetAptList)],
        },
        fallbacks=[]
    )

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpCommand))
    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerFindEmail)
    dp.add_handler(Passwordverifier)
    dp.add_handler(CommandHandler("get_release", LinuxGetRelease))
    dp.add_handler(CommandHandler("get_uname", LinuxGetUname))
    dp.add_handler(CommandHandler("get_uptime", LinuxGetUptime))
    dp.add_handler(CommandHandler("get_df", LinuxGetDF))
    dp.add_handler(CommandHandler("get_free", LinuxGetFree))
    dp.add_handler(CommandHandler("get_mpstat", LinuxGetMpstat))
    
    dp.add_handler(CommandHandler("get_w", LinuxGetW))
    dp.add_handler(CommandHandler("get_auths", LinuxGetAuths))
    dp.add_handler(CommandHandler("get_critical", LinuxGetCritical))
    dp.add_handler(CommandHandler("get_ps", LinuxGetPS))
    dp.add_handler(CommandHandler("get_ss", LinuxGetSS))
    dp.add_handler(convHandleraptget)
    dp.add_handler(CommandHandler("get_services", LinuxGetServices))
    #LESSION 2
    dp.add_handler(CommandHandler("get_repl_logs", SQLGetReplicationLogs))
    
    dp.add_handler(CommandHandler("get_emails", SQLGetEmails))
    dp.add_handler(CommandHandler("get_phone_numbers", SQLGetPhoneNumbers))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()