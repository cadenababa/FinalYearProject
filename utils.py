import xlrd
import openpyxl as xl

def sem_to_year(sem):
    return round((int(sem)/2))

def xlsx_to_xls(file):
    wb = xl.load_workbook(file)
    filepath = f"{file.rsplit('.', 1)[0]}.xls"
    wb.save(filepath)
    return filepath

def len_check(roll):
    if not isinstance(roll, str):
        roll = str(roll)
    if len(roll) == 1:
        return f"00{roll}"
    elif len(roll) == 2:
        return f"0{roll}"
    else:
        return roll

def create_roll(dept, batch, roll) -> str:
    return f"{dept}{batch}/{len_check(str(roll))}"

def generate_employee_id(cls):
    return f"RCC-TCHR-{len_check(cls.current_parameters.get('user_ptr_id'))}"
