from record_manager import MiscChecks, RecordManager
#from collections import UserDict
      
class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    DEFAULT = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ContactBook(): #UserDict
    def __init__(self):
        self.data = {}
        self.priority_ids = []
        self.record_cnt = 0
        self.generated_ids = 0
        self.file = "storage.bin"
        self.update_file("load",0)

        self.opnng = f"Введіть, будь ласка, "
        self.non_obligatory = f"( або '{bcolors.RED}N{bcolors.GREEN}', якщо бажаєте додати пізніше)"
        self.opnng_en = f"Please, enter the "
        self.non_obligatory_en = f"( or '{bcolors.RED}N{bcolors.GREEN}', if you want to add it later)"
        self.method_table = {'__localization_insert':{'name':{'en':"of the contact manager", 'uk':"менеджера контактів"},'description':{'en':"contact manager", 'uk':"менеджер контактів та записів"}},
                            'contact_create':{'class':'ContactBook', 'description':{'en':"Adds a new record to the contact book. You can add a name, a phone, a birthday, an address, an an email - either when creating a record, or later.",'uk':"Додає новий запис до книги контактів. Можна додати ім'я, телефони, день народження, адресу та email одразу, а можна й пізніше."}, 'methods':{self.add_contact:{'name':{'en':f"{self.opnng_en}name{self.non_obligatory_en}",'uk':f"{self.opnng}ім'я{self.non_obligatory}"},'phone':{'en':f"{self.opnng_en}phone number{self.non_obligatory_en}",'uk':f"{self.opnng}номер телефону{self.non_obligatory}"}, 'birthday':{'en':f"{self.opnng_en}birthday{self.non_obligatory_en}",'uk':f"{self.opnng}день народження контакта{self.non_obligatory}"}, 'email':{'en':f"{self.opnng_en}email{self.non_obligatory_en}",'uk':f"{self.opnng}електронну пошту контакта{self.non_obligatory}"}, 'address':{'en':f"{self.opnng_en}address{self.non_obligatory_en}",'uk':f"{self.opnng}адресу контакта{self.non_obligatory}"}}}}}

    def test_printer(self,*args):
        print(args)

    # Prepares self.data[id] to be saved.
    # Explanation: operates in one mode: 'add' (requires record id). returns prepared dict with record variables. 
    # Used to add new lines to the file.bin
    def prepare_data(self,mode:str,record_id=None):
        if mode == "add":
            for rid,record in self.data.items():
                if rid == record_id:
                    return {'Name':record.name,'Phones':record.phones,'Birthday':record.birthday,'Email':record.email,'Address':record.address}
    
    
    # Dynamicly adds new records, deletes records, creates file.bin, etc.
    # If mode == add, adding record to file (with correct persistent id). If mode == 'del', removes the record by id, overwrites saved data with the new parsed self.data. 
    # With "ed", overwrites saved data with the new parsed self.data
    def update_file(self,mode:str,r_id=None):
        import pickle
        from pathlib import Path
        file = Path(self.file)
        if not file.exists():
            with open(file, 'wb') as storage:
                print("No data to load! Creating new file!")
                return

        if mode == "add":
            with open(file, 'ab') as storage:
                st_r_id = self.generated_ids
                class PersPickler(pickle.Pickler):
                    def persistent_id(self, obj):
                        return st_r_id if st_r_id else None

                PersPickler(storage).dump(self.prepare_data("add",record_id=r_id))
                self.generated_ids += 1
        elif mode == "del":
            with open(file, 'wb') as storage:
                if r_id in self.data:
                    del self.data[r_id]

                if len(self.data) > 0:
                    id_generator = 0
                    class PersPickler(pickle.Pickler):
                        def persistent_id(self, obj):
                            return id_generator if id_generator else None
                    
                    for id,record in self.data.items():
                        PersPickler(storage).dump({'Name':record.name,'Phones':record.phones,'Birthday':record.birthday,'Email':record.email,'Address':record.address})
                        id_generator += 1
                    self.generated_ids = id_generator
                else:
                    print("ERROR!\nNo such record exists!")
        elif mode == "ed":
            with open(file, 'wb') as storage:
                if len(self.data) > 0:
                    id_generator = 0
                    class PersPickler(pickle.Pickler):
                        def persistent_id(self, obj):
                            """Return a persistent id for the `bar` object only"""
                            return id_generator if id_generator else None
                    
                    for id,record in self.data.items():
                        PersPickler(storage).dump({'Name':record.name,'Phones':record.phones,'Birthday':record.birthday,'Email':record.email,'Address':record.address})
                        id_generator += 1
                    self.generated_ids = id_generator
        elif mode == "load":
            with open(file, 'rb') as storage:
                class PersUnpickler(pickle.Unpickler):
                    def persistent_load(self, pers_id):
                        try:
                            if int(pers_id) or int(pers_id) == 0:
                                return pers_id
                        except TypeError(f'{pers_id} Cant be converted into int!'):
                            raise pickle.UnpicklingError("Persistent id is not number in string!")
                
                if file.stat().st_size != 0:
                    id_generator = 0
                    try:
                        while True:  
                            record = PersUnpickler(storage).load()
                            # print(record)
                            self.data[id_generator] = RecordManager()
                            self.data[id_generator].load_data(name=record['Name'],phones=record['Phones'],birthday=record['Birthday'],email=record['Email'],address=record['Address'])
                            id_generator += 1
                    except EOFError:
                        self.generated_ids = id_generator
                        self.record_cnt = id_generator
                        print('Reached the end of file!')
            #print(self.data)


    #Saves self.data and some technical variables. Can be used, although everything should be saved automatically. may be used to ensure, that nothing will be lost.
    def save_changes(self):
        self.update_file("ed")

    def add_contact(self,name,phone,birthday,email,address):
        new_record = RecordManager()
        if self.dialogue_check(name):
            new_record.add_name(name)
        if self.dialogue_check(phone):
            new_record.add_phone(phone)
        if self.dialogue_check(birthday):
            new_record.add_birthday(birthday)
        if self.dialogue_check(email):
            new_record.add_email(email)
        if self.dialogue_check(address):
            new_record.add_address(address)

        self.id_assign(mode="add",record=new_record)
        self.update_file("add",self.generated_ids)
        print(new_record)
    
    def dialogue_check(self,variable):
        if variable.lower() != 'n':
            return True
        return False

    def id_assign(self,mode:str,record:RecordManager):
        if mode == "add":
            if len(self.priority_ids) > 0:
                self.data[self.priority_ids[0]] = record
                del self.priority_ids[0]
            else:
                self.data[self.record_cnt] = record
                self.record_cnt += 1
        elif mode == "del":
            for k,v in self.data.items():
                if v == record:
                    self.priority_ids.append(k)
