import psycopg2, random
from psycopg2.extras import DictCursor
class User:
    def __init__(self,id,name,surname,age,dob,country):
        self.id = id
        self.name = name
        self.surname = surname
        self.age = age
        self.dob = dob
        self.country = country
    def __str__(self):
        return f'ID: {self.id}\nName: {self.name}\nSurname: {self.surname}\nAge: {self.age}\nDate of birth: {self.dob}\nCountry: {self.country}'
class CreditCard:
    def __init__(self,nums,exp,cvc,holder_name,holder_surname,pin,balance):
        self.nums = nums
        self.exp = exp
        self.cvc = cvc
        self.holder_name = holder_name
        self.holder_surname = holder_surname
        self.pin = pin
        self.balance = balance
    def __str__(self):
        return f'Nums: {self.nums}\nExp: {self.exp}\nCVC: {self.cvc}\nHolder name: {self.holder_name} {self.holder_surname}\nPIN: {self.pin}\nBalance: {self.balance} BYN'
def menu_transactions_funct(user,card):
    while True:
        print('==========TRANSACTIONS MENU==========\n1.P2P\n2.Put money\n3.Back')
        trans_choice = input("Enter:")
        match trans_choice:
            case '3':
                print('Returning you to main menu...')
                return
            case '2':
                print('Enter amount of money that you want to put.\nExample: 5,10,15,20,25,30,35,40,45,50 etc...')
                try:
                    amount = int(input('Enter:'))
                except ValueError:
                    print('You had to input NUMBERS not LETTERS!')
                    continue
                if amount % 5 == 0:
                    card.balance += amount
                    print(f'Now your balance is {card.balance} BYN!')
                    with psycopg2.connect(host = 'localhost',user = 'postgres',dbname = 'postgres',port = 5432,password = 'MY_PASSWORD') as conn:
                        with conn.cursor(cursor_factory = DictCursor) as cursor:
                            sql_insert = 'UPDATE user_cards SET balance = %s WHERE user_id = %s'
                            cursor.execute(sql_insert,(card.balance,user.id))
                else:
                    print('Enter correct amount.')
            case '1':
                while True:
                    print('===========P2P==========')
                    print('What payment method you want to use?\n1.Name,surname\n2.Card nums\n3.Back')
                    p2p_choice = input("Enter method:")
                    match p2p_choice:
                        case '3':
                            print('Returning you back to transactions menu...')
                            break
                        case '2':
                            p2p_nums = input('Enter card numbers.(example: 4255 1901 2282 1993)')
                            try:
                                p2p_amount = int(input("Enter amount that you want to transact:"))
                            except ValueError:
                                print("You had to put AMOUNT of your money! Not letters!")
                                continue
                            if p2p_amount > card.balance:
                                print('You dont have this amount on your card!')
                            else:
                                with psycopg2.connect(host = 'localhost',user = 'postgress',dbname = 'postgres',port = 5432,password = 'MYPASSWORD') as conn:
                                    with conn.cursor(cursor_factory = DictCursor) as cursor:
                                        sql_insert = 'UPDATE user_cards SET balance = balance + %s WHERE nums = %s'
                                        cursor.execute(sql_insert,(p2p_amount,p2p_nums))
                                        if cursor.rowcount == 0:
                                            print('Card that you typed is not EXISTS!')
                                            continue
                                        card.balance -=p2p_amount
                                        sql_insert = 'UPDATE user_cards SET balance = %s WHERE user_id = %s'
                                        cursor.execute(sql_insert,(card.balance,user.id))
                                        print(f'Payment success!\nCheck:\n============\nOperation: P2P\nNumbers: {p2p_nums}\nAmount: {p2p_amount} BYN\n==========')
                        case '1':
                            print('Enter name and surname that you want to trancast money. Example: Alexander Drachou')
                            p2p_name = input('Enter NAME:').strip().capitalize()
                            p2p_surname = input('Enter SURNAME:').strip().capitalize()
                            try:
                                p2p_amount = int(input('Enter amount that you want to transact:'))
                            except ValueError:
                                print("You had to put AMOUNT of your money! Not letters!")
                                continue
                            if p2p_amount > card.balance:
                                print('You dont have this amount on your card!')
                            else:
                                with psycopg2.connect(host = 'localhost',user = 'postgres',dbname = 'postgres',port = 5432,password = 'MY_PASSWORD') as conn:
                                    with conn.cursor(cursor_factory = DictCursor) as cursor:
                                        sql_insert = 'UPDATE user_cards SET balance = user_cards.balance + %s FROM user_info WHERE user_cards.user_id = user_info.id AND user_info.name = %s AND user_info.surname = %s'
                                        cursor.execute(sql_insert,(p2p_amount,p2p_name,p2p_surname))
                                        if cursor.rowcount == 0:
                                            print('A person with this name,surname is not EXISTS!')
                                            continue
                                        card.balance -=p2p_amount
                                        sql_insert = 'UPDATE user_cards SET balance = %s WHERE user_id = %s'
                                        cursor.execute(sql_insert,(card.balance,user.id))
                                        print(f'Payment success!\nCheck:\n============\nOperation: P2P\nName/Surname: {p2p_name} {p2p_surname}\nAmount: {p2p_amount} BYN\n==========')
def menu_settings_funct(us_data,login):
     while True:
        print('==========SETTINGS MENU==========')
        print('1.Check profile card\n2.Back')
        settings_choice = input("Enter:")
        match settings_choice:
            case '2':
                return
            case '1':
                print('This your profile card. Want to redact?\n1.Yes\n2.Back')
                print(user)
                settings_profile_choice = input('Enter:')
                match settings_profile_choice:
                    case '2':
                        return
                    case '1':
                        name = input('Enter your name:')
                        surname = input("Enter your surname:")
                        try:
                            age = int(input('Enter your age:'))
                        except ValueError:
                            print("You have to type a NUMBERS!")
                            continue
                        dob = input('Enter your date of birth: (MM/DD/YYYY)')
                        country = input('Enter your country:')
                        us_data.name = name
                        us_data.surname = surname
                        us_data.age = age
                        us_data.dob = dob
                        us_data.country = country
                        with psycopg2.connect(host = 'localhost',user = 'postgres',dbname = 'postgres',port = 5432,password = 'MY_PASSWORD') as conn:
                                            with conn.cursor(cursor_factory = DictCursor) as cursor:
                                                sql_insert = 'UPDATE user_info SET name = %s, surname = %s,age = %s,dob = %s,country = %s WHERE user_login = %s;'
                                                cursor.execute(sql_insert,(us_data.name,us_data.surname,us_data.age,us_data.dob,us_data.country,login,))
                                                print('Changes accept!')
                        
def menu_my_cards(user,card):
    while True:
        print("==========YOUR CARDS=========")
        if user.name == None or user.surname == None:
            print("You have to create your profile card at first! Settings -> Create profile card")
            return
        if card.pin == 0:
            print('Looks like you dont have card!\nWant to create new one?\n1.Yes\n2.No')
            card_choice = input("Enter:")
            match card_choice:
                case '2':
                    print('Returning you to main menu...')
                    return
                case '1':
                    card.nums = f'4255 1901 {random.randint(1000,9999)} {random.randint(1000,9999)}'
                    card.exp = '10/30'
                    card.cvc = f'{random.randint(100,999)}'
                    card.holder_name = user.name
                    card.holder_surname = user.surname
                    card.pin = random.randint(100,999)
                    card.balance = 0
                    with psycopg2.connect(host='localhost',port=5432,password = 'MY_PASSWORD',dbname = 'postgres',user = 'postgres') as conn:
                                with conn.cursor(cursor_factory = DictCursor) as cursor:
                                    sql_insert = 'UPDATE user_cards SET nums = %s,exp = %s,cvc = %s,holder_name = %s,holder_surname = %s,pin = %s,balance = %s WHERE user_id = %s'
                                    cursor.execute(sql_insert,(card.nums,card.exp,card.cvc,card.holder_name,card.holder_surname,card.pin,card.balance,user.id))
                    print("Congratulations! You got your first card!")
                    print(card)
                    enter = input('Press enter to leave.')
                    return
        else:
            print(card)
            enter = input('Press enter to leave.')
            return
                                                         
def menu_leave_funct():
    while True:
        print('Do you really want to leave?\n1.Yes\n2.No')
        leave_choice = input('Enter:')
        match leave_choice:
            case '1':
                print('You left from main menu!')
                leave = True
                return leave
            case '2':
                leave = False
                return leave
            case _:
                print('Enter correct option!')
def login_function():
    while True:
        print('==========LOGIN==========')
        print("Input your data to login account!\nEnter your login. quit() - for quit")
        login_in = input("Type:")
        if login_in == 'quit()':
            print('You chase quit to hall!')
            account_found = False
            login = None
            return account_found,login
        print('Enter your password!')
        password_in = input('Type:')
        with psycopg2.connect(host='localhost',port=5432,password = 'MY_PASSWORD',dbname = 'postgres',user = 'postgres') as conn:
            with conn.cursor(cursor_factory = DictCursor) as cursor:
                sql_insert = 'SELECT user_login,user_password FROM user_info WHERE user_login = %s AND user_password = %s'
                try:
                    cursor.execute(sql_insert,(login_in,password_in))
                    login,password = cursor.fetchone()
                    if login_in == login and password_in == password:
                        account_found = True
                        return account_found,login
                except TypeError:
                    print('You ENTERED WRONG DATA! Try again.')
                    account_found = False
def register_function():
    while True:
        print("==========REGISTER==========")
        print("Input your login for new account.Type 'quit()' for quit!")
        login_in = input('Type:').strip()
        if login_in == 'quit()':
            print('You chase quit to hall.')
            return
        print("Input your password for new account.")
        password_in = input('Type:').strip()
        print('Input your password again.')
        password_check = input('Type:').strip()
        if password_check != password_in:
            print("You typed a wrong password! Do this options again!")
            continue
        else:
            try:
                with psycopg2.connect(host = 'localhost',port = 5432,password = 'MY_PASSWORD',dbname = 'postgres',user = 'postgres') as conn:
                    with conn.cursor(cursor_factory=DictCursor) as cursor:
                        sql_insert = 'INSERT INTO user_info(user_login,user_password) VALUES (%s,%s) RETURNING id;'
                        cursor.execute(sql_insert,(login_in,password_in))
                        gen_id = cursor.fetchone()['id']
                        sql_insert = 'INSERT INTO user_cards(user_id,nums,exp,cvc,holder_name,holder_surname,pin,balance) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);'
                        cursor.execute(sql_insert,(gen_id,f'NOT-OPENED-{gen_id}','0','0','0','0',0,0))
            except Exception:
                        print('This LOGIN is reserved! Type new!')
                        continue
            print(f'You registered succesefully!\nYour login: {login_in}\nYour password: {password_in}')
            return
while True:
    print('==========BEBRABANK HALL==========\n1.Login\n2.Register\n3.Quit')
    choice = input('Choose one option')
    match choice:
        case '3':
            print("You chase quit from BEBRABANK!")
            break
        case '2':
            print("You chase register new account!")
            register_function()
        case '1':
            print('You chase login!')
            account_found,login = login_function()
            if account_found:
                with psycopg2.connect(host = 'localhost',user = 'postgres',dbname = 'postgres',port = 5432,password = 'MY_PASSWORD') as conn:
                    with conn.cursor(cursor_factory = DictCursor) as cursor:
                        sql_insert = 'SELECT id,name,surname,age,dob,country FROM user_info WHERE user_login = %s'
                        cursor.execute(sql_insert,(login,))
                        data = cursor.fetchone()
                        user = User(**data)
                        sql_insert = 'SELECT nums,exp,cvc,holder_name,holder_surname,pin,balance FROM user_cards WHERE user_id = %s'
                        gen_id = data['id']
                        cursor.execute(sql_insert,(gen_id,))
                        card_data = cursor.fetchone()
                        card = CreditCard(**card_data)
                while True:
                        print(f'==========BEBRABANK MAIN MENU==========')
                        print('1.My cards\n2.Transactions\n3.Settings\n4.Leave from account')
                        leave = False
                        choice_menu = input("Pick one option:")
                        match choice_menu:
                            case '4':
                                leave = menu_leave_funct()
                                if leave:
                                    break
                            case '3':
                                menu_settings_funct(user,login)
                            case "1":
                                menu_my_cards(user,card)
                            case '2':
                                if card.pin == 0:
                                    print('You have to create card at first!')
                                else:
                                    menu_transactions_funct(user,card)