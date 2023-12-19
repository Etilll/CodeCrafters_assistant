# Зберігає в собі методи перевірки значень класу RecordManager. Окремо не використовується.
class MiscChecks:
    def month_check(self,month:str):
        if len(month) > 2:
            error_text = {'en':"Wrong month format. Should be exactly two characters.",'ua':"Некоректний формат місяця: має складатись рівно з двох символів."}
            raise ValueError(error_text[self.language])
        if month[:1] == "0":
            month = month[:1]
        if int(month) <= 12:
            return True
        else:
            error_text = {'en':"Wrong month format: there can't be more than 12 of them. Correct format: MM-DD-YYYY.",'ua':"Некоректний формат місяця: їх не може бути більше дванадцяти. Правильний формат: ММ-ДД-РРРР."}
            raise ValueError(error_text[self.language])

    def p_check(self,phone:str):
        from re import search
        map = {' ':''}
        phone.translate(map)
        if len(phone) == 10 and search(r'\d{10}', phone) != None:
            return phone
        else:
            error_text = {'en':"Incorrect phone number. Must be exactly 10 characters, digits only.",'ua':"Некорректний номер телефону. Має складатись виключно з цифр, і цифр має бути 10. Не більше і не менше."}
            raise ValueError(error_text[self.language])

    def birthday_check(self,birthday):
        from re import search
        # Format: MM-DD-YYYY
        if birthday == None:
            return None
        elif (search(r'\d{2}\D\d{2}\D\d{4}', birthday) != None and len(birthday) == 10):
            tmp = birthday[0:2]
            if self.month_check(tmp):
                return birthday
        elif search(r'\d{8}', birthday) != None and len(birthday) == 8:
            tmp = birthday[0:2]
            if self.month_check(tmp):
                tmp = birthday[0:2] + "-" + birthday[2:4] + "-" + birthday[4:6] + birthday[6:8]
                return tmp
        else:
            error_text = {'en':"Wrong birthday format. The correct format would be: MM-DD-YYYY",'ua':"Некоректний формат дня народження. Правильний формат: ММ-ДД-РРРР."}
            raise ValueError(error_text[self.language])
        
    def email_check(self,email):
        from re import search
        # Format: text@text.text
        if email == None:
            return None
        elif (search(r'\S{3,}@[a-zA-Z]{2,}.[a-zA-Z]{2,}', email) != None):
            return email
        else:
            error_text = {'en':"Wrong email format. The correct format would be: text@text.text",'ua':"Некоректний формат електронної пошти. Правильний формат: текст@текст.текст"}
            raise ValueError(error_text[self.language])
        
    def has_phone(self,phone:str):
        for i in self.phones:
            if i.value == phone:
                return True
           
        return False 

# Екземпляр класу. Відповідає за зберігання усіх змінних запису. Створюється у ContactBook. Необов'язкові поля можуть бути пропущені символами "n"/"N".
# У самому класі зберігається лише функціонал запису/зміни/видалення. Все інше наслідується від MiscChecks.
class RecordManager(MiscChecks):
    def __init__(self):
        self.language = None
        self.phones = []
        self.name = "Unnamed contact"
        self.birthday = None
        self.email = None
        self.address = None

    def __str__(self):
        return f"Record name: {self.name}, Birthday: {self.birthday}, phones: {'; '.join(p for p in self.phones)}"

    def add_phone(self,phone):
        if type(self.p_check(phone)) == str:
            phone = self.p_check(phone)
            self.phones.append(phone)

    def add_birthday(self,birthday):
        if self.birthday_check(birthday):
            self.birthday = self.birthday_check(birthday)

    def add_name(self,name:str):
        self.name = name

    def add_email(self,email:str):
        if self.email_check(email):
            self.email = email

    def add_address(self,address:str):
        self.address = address

    def edit_phone(self,phone:str,new_phone:str):
        if self.has_phone(phone):
            if type(self.p_check(new_phone)) == str:
                self.phones.remove(phone)
                self.phones.append(new_phone)
                return
        
        error_text = {'en':"Haven't found this phone number in the chosen contact!",'ua':"Цей телефон у обраному контакті не знайдено!"}
        raise ValueError(error_text[self.language])
    
    def edit_birthday(self,new_birthday:str):
        if self.birthday != None:
            if type(self.birthday_check(new_birthday)) == str:
                self.birthday = self.birthday_check(new_birthday)
                return
        
        error_text = {'en':"Birthday is not set in this record. Please, use the function for adding birthday instead.",'ua':"День народження у записі відсутній. Будь ласка, скористайтеся функцією додавання дня народження!"}
        raise ValueError(error_text[self.language])
            
    def edit_email(self,new_email:str):
        if self.email != None:
            if type(self.email_check(new_email)) == str:
                self.email = new_email
                return

        error_text = {'en':"Email is not set in this record. Please, use the function for adding email instead.",'ua':"Електронна пошта у записі відсутня. Будь ласка, скористайтеся функцією додавання дня електронної пошти!"}
        raise ValueError(error_text[self.language])
        
    def edit_name(self,name:str):
        self.name = name

    def edit_address(self,address:str):
        self.address = address

    def remove_phone(self,phone:str):
        if self.has_phone(phone):
            self.phones.remove(phone)
            return
        
        error_text = {'en':"Haven't found this phone number in the chosen contact!",'ua':"Цей телефон у обраному контакті не знайдено!"}
        raise ValueError(error_text[self.language])
    
    def remove_birthday(self):
        self.birthday = None
    
    def remove_name(self):
        self.name = "Unnamed contact"

    def remove_email(self):
        self.email = None

    def remove_address(self):
        self.address = None

    def load_data(self,name,phones,birthday,email,address): # To avoid reoccurring checks when loading from storage.bin
        self.phones = phones
        self.name = name
        self.birthday = birthday
        self.email = email
        self.address = address