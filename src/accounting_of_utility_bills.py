import flet as ft
from  sqlite3 import connect, Error
import ctypes
import logging
import os
import datetime



if os.path.exists("accounting_of_utility_bills.log"):
    logging.basicConfig(level=logging.ERROR, filename="accounting_of_utility_bills.log",filemode="a", format="%(asctime)s %(levelname)s %(message)s")

else:
    logging.basicConfig(level=logging.ERROR, filename="accounting_of_utility_bills.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")



def sqlite_create_db():


    try:
        with connect('bills.db') as db:
            cur = db.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS gas (
               id INTEGER PRIMARY KEY,
               accountnumber TEXT,
               date TEXT,
               previousreadings TEXT,
               currentreadings TEXT,
               sum TEXT,
               payment TEXT
               )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS gasdelivery (
                       id INTEGER PRIMARY KEY,
                       accountnumber TEXT,
                       date TEXT,
                       previousreadings TEXT,
               currentreadings TEXT,
               sum TEXT,
               payment TEXT
                       )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS electro (
                    id INTEGER PRIMARY KEY,
               accountnumber TEXT,
               date TEXT,
               previousreadings TEXT,
               currentreadings TEXT,
               sum TEXT,
               payment TEXT

                   )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS water (
                    id INTEGER PRIMARY KEY,
               accountnumber TEXT,
               date TEXT,
               previousreadings TEXT,
               currentreadings TEXT,
               sum TEXT,
               payment TEXT
               
                   )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS trash (
                   id INTEGER PRIMARY KEY,
               accountnumber TEXT,
               date TEXT,
               
               sum TEXT
               
                   )''')


    except Error as er:
        ctypes.windll.user32.MessageBoxW(0, str(er), "Ошибка создания БД", 0x40) # вызов предупреждающего окна с ошибкой средствами Windows
        logging.exception(er, exc_info=True)


    db.commit()



def main(page: ft.Page):
    page.title = "Bills utility" # наименование окна программы

    #page.scroll = True                  # разрешения вертикальной прокрутки  в основном окне
    page.window_resizable = False       # запрет расстягивания основного окна по ширине и высоте
    page.auto_scroll = True

    # функция закрытия предупреждающего баннера вывода ошибок
    def close_banner(e):
        page.banner.open = False
        page.update()

    # баннер ошибок
    def alert_banner(message):
        page.banner = ft.Banner(
            bgcolor=ft.colors.AMBER_100,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content=ft.Text(message),
            actions=[ft.TextButton("Закрыть", on_click=close_banner), ])
        page.banner.open = True
        page.update()



    def clear_fields():
        account_number.value = ""
        until_price.value = ""
        previous_readings.value = ""
        current_readings.value = ""
        payment.value = ""
        date.value = ""
        sum.value = ""
        page.update()


    def disable_fields():
        date.disabled = True
        until_price.disabled = True
        previous_readings.disabled = True
        current_readings.disabled = True
        sum.disabled = True
        payment.disabled = True
        account_number.disabled = True
        page.update()

    def enable_fields():
        date.disabled = False
        until_price.disabled = False
        previous_readings.disabled = False
        current_readings.disabled = False
        sum.disabled = False
        payment.disabled = False
        account_number.disabled = False
        page.update()


    def disable_value_chekboxes():
        gas.value = False
        gas_delivery.value = False
        water.value = False
        electro.value = False
        trash.value = False

        page.update()

    def enable_chekboxes():
        gas.disabled = False
        gas_delivery.disabled = False
        water.disabled = False
        electro.disabled = False
        trash.disabled = False
        page.update()


    def checkboxes_changed(e):
        if gas.value == True:
            account_number.value = "990312758"
            until_price.value = "7.95689"
            gas_delivery.disabled = True
            water.disabled = True
            electro.disabled = True
            trash.disabled = True
            date_button.disabled = False

            #enable_fields()

            page.update()

        elif gas_delivery.value == True:
            account_number.value = "13-14703"
            until_price.value = "1.416"
            gas.disabled = True
            water.disabled = True
            electro.disabled = True
            trash.disabled = True
            date_button.disabled = False
            #enable_fields()
            page.update()


        elif electro.value == True:
            account_number.value = "210414112"
            until_price.value = "2.64"
            gas_delivery.disabled = True
            water.disabled = True
            gas.disabled = True
            trash.disabled = True
            date_button.disabled = False
            #enable_fields()
            page.update()


        elif water.value == True:
            account_number.value = "39441"
            until_price.value = "20.22"
            gas_delivery.disabled = True
            gas.disabled = True
            electro.disabled = True
            trash.disabled = True
            date_button.disabled = False
            #enable_fields()

            page.update()


        elif trash.value == True:
            account_number.value = "149426"
            payment.value = "46.04"
            enable_fields()
            gas_delivery.disabled = True
            water.disabled = True
            electro.disabled = True
            gas.disabled = True
            date_button.disabled = False
            current_readings.disabled = True
            previous_readings.disabled = True
            sum.disabled = True
            until_price.disabled = True
            #if date.value !="":
            add_btn.disabled = False
                #page.update()


            page.update()


        else:
            clear_fields()
            #payment.value = ""
            gas.disabled = False
            gas_delivery.disabled = False
            water.disabled = False
            electro.disabled = False
            trash.disabled = False
            date_button.disabled = True
            current_readings.disabled = False
            previous_readings.disabled = False
            sum.disabled = False
            until_price.disabled = False
            add_btn.disabled = True
            disable_fields()

            page.update()

    #функция получения всех записей из таблицы
    def sqlite_get_all_data(name_table):
        lst = []
        lv.controls.clear()
        page.update()
        #page.add(lv)
        try:
            with connect('bills.db') as db:
                cur = db.cursor()

            cur.execute(
                f'SELECT * FROM {name_table}')

        except Error as er:
            logging.exception(er, exc_info=True)
            alert_banner(er)
            #print(er)

        rows = cur.fetchall()

        if  gas.value == True:#director.value == "":
            for row in rows:
                lst.append(row)
                text_id.value = row[0]
                text_account.value = row[1]
                text_data.value = row[2]
                text_previus.value = row[3]
                #text_director.value = row[4]
                text_sum.value = row[4]
                text_payment.value = row[5]

                lv.controls.append(ft.Text(
                    f"{text_id.value}         {text_account.value}                       {text_data.value}    {text_previus.value}       {text_sum.value}                                                     {text_payment.value}"))

                page.update()

        elif gas_delivery.value == True:#aktors.disabled == True:
            for row in rows:
                lst.append(row)
                text_id.value = row[0]
                text_account.value = row[1]
                text_data.value = row[2]
                text_previus.value = row[3]
                text_curent.value = row[4]

                text_payment.value = row[5]

                lv.controls.append(ft.Text(
                    f"{text_id.value}   {text_account.value}   {text_data.value}    {text_previus.value}     {text_curent.value}     {text_payment.value}"))

                page.update()

        elif electro.value ==True:
            for row in rows:
                lst.append(row)
                text_id.value = row[0]
                text_account.value = row[1]
                text_data.value = row[2]
                text_previus.value = row[3]

                text_payment.value = row[4]

                lv.controls.append(ft.Text(
                    f"{text_id.value}   {text_account.value}   {text_data.value}    {text_previus.value}   {text_payment.value}"))

                page.update()


        elif trash.value == True:
            for row in rows:
                #lst.append(row)
                text_id.value = row[0]
                text_account.value = row[1]
                text_data.value = row[2]

                text_payment.value = row[3]

                lv.controls.append(ft.Text(
                    f"{text_id.value}   {text_account.value}   {text_data.value}   {text_payment.value}"))

                page.update()

        elif water.value == True:
            for row in rows:
                lst.append(row)
                text_id.value = row[0]
                text_account.value = row[1]
                text_data.value = row[2]
                text_previus.value = row[3]
                text_curent.value = row[4]
                text_sum.value = row[5]
                text_payment.value = row[6]


                lv.controls.append(ft.Text(
                            f"{text_id.value}   {text_account.value}   {text_data.value}    {text_previus.value}    {text_curent.value}   {text_sum.value}   {text_payment.value}"))

                page.update()

        gas.value = False
        electro.value = False
        water.value = False
        trash.value = False
        gas_delivery.value = False
        gas.disabled = False
        gas_delivery.disabled = False
        electro.disabled = False
        water.disabled = False
        trash.disabled = False
        add_btn.disabled = True
        clear_fields()

        page.update()



    def get_value(e):

        lv.controls.clear()
        page.update()
        if gas.value == True:
            sub_selection_condition("gas")

            page.update()


        elif gas_delivery.value == True:

            sub_selection_condition("gasdelivery")

            page.update()



        elif water.value == True:
            sub_selection_condition("water")

            page.update()



        elif electro.value == True:
            sub_selection_condition("electro")

            page.update()



        elif trash.value == True:
           sub_selection_condition("trash")

           page.update()


    def sub_selection_condition (table):
        if account_number.value != "":

            get_sql_data(table, "accountnumber",account_number.value)
            clear_fields()


        elif date.value != "":
            get_sql_data(table,"date",date.value)
            clear_fields()
            date.value = ""


        elif previous_readings.value != "" :
            get_sql_data(table,"previousreadings",previous_readings.value)
            clear_fields()

        elif current_readings.value != "":
            get_sql_data(table,"currentreadings",current_readings.value)
            clear_fields()

        elif sum.value != "":
            get_sql_data(table,"sum",sum.value)
            clear_fields()

        elif payment.value != "":
            get_sql_data(table,"payment",payment.value)
            clear_fields()



        # else:
        #     pass
        #
        #     sqlite_get_all_data(table)

    def get_sql_data(name_table,name_column,value_column):
        lv.controls.clear()
        page.update()
        try:
            with connect('bills.db') as db:
                cur = db.cursor()

            cur.execute(
                f'SELECT * FROM {name_table}  WHERE  {name_column} LIKE "%{value_column}%"')
        except Error as er:
            logging.exception(er, exc_info=True)
            alert_banner(er)

        rows = cur.fetchall()


        if rows == []:

            page.snack_bar = ft.SnackBar(content=ft.Text("По данному запросу ничего не найдено"), open=False)
            page.snack_bar.open = True
            clear_fields()

            page.update()


        else:
            if gas.value == True:
                for row in rows:

                    text_id.value = row[0]
                    text_account.value = row[1]
                    text_data.value = row[2]
                    text_previus.value = row[3]

                    text_curent.value = row[4]
                    text_sum.value = row[5]
                    text_payment.value = row[6]

                    lv.controls.append(ft.Text(
                        f"                       {text_id.value}     {text_data.value}         {text_account.value}                            {text_previus.value}                                        {text_curent.value}                                       {text_sum.value}                   {text_payment.value}"))

                    page.update()


            elif gas_delivery.value == True:
                for row in rows:

                    text_id.value = row[0]
                    text_account.value = row[1]
                    text_data.value = row[2]
                    text_previus.value = row[3]

                    text_curent.value = row[4]
                    text_sum.value = row[5]
                    text_payment.value = row[6]

                    lv.controls.append(ft.Text(
                        f"                       {text_id.value}     {text_data.value}         {text_account.value}                            {text_previus.value}                                        {text_curent.value}                                       {text_sum.value}                                           {text_payment.value}"))

                    page.update()

            elif electro.value == True:
                for row in rows:

                    text_id.value = row[0]
                    text_account.value = row[1]
                    text_data.value = row[2]
                    text_previus.value = row[3]

                    text_curent.value = row[4]
                    text_sum.value = row[5]
                    text_payment.value = row[6]

                    lv.controls.append(ft.Text(
                        f"                       {text_id.value}     {text_data.value}         {text_account.value}                            {text_previus.value}                                        {text_curent.value}                                       {text_sum.value}                                           {text_payment.value}"))

                    page.update()


            elif water.value == True:
                for row in rows:

                    text_id.value = row[0]
                    text_account.value = row[1]
                    text_data.value = row[2]
                    text_previus.value = row[3]

                    text_curent.value = row[4]
                    text_sum.value = row[5]
                    text_payment.value = row[6]

                    lv.controls.append(ft.Text(
                        f"                       {text_id.value}     {text_data.value}         {text_account.value}                            {text_previus.value}                                        {text_curent.value}                                       {text_sum.value}                                                  {text_payment.value}"))

                    page.update()


            elif trash.value == True:
                for row in rows:

                    text_id.value = row[0]
                    text_account.value = row[1]
                    text_data.value = row[2]
                    text_payment.value = row[3]


                    lv.controls.append(ft.Text(
                        f"                        {text_id.value}      {text_data.value}         {text_account.value}                                                                                                                                                                                  {text_payment.value}"))

                    page.update()

        disable_fields()
        disable_value_chekboxes()
        enable_chekboxes()




        add_btn.disabled = True
        date_button.disabled = True


    def sql_add(e):
        lv.controls.clear()
        page.update()

        try:
            with connect('bills.db') as db:
                cur = db.cursor()

                if gas.value == True:


                    cur.execute(f'INSERT INTO gas VALUES(NULL,"{account_number.value}","{date.value}","{previous_readings.value}","{current_readings.value}","{sum.value}", "{payment.value}")')


                elif water.value == True:

                    cur.execute(f'INSERT INTO water VALUES(NULL,"{account_number.value}","{date.value}","{previous_readings.value}","{current_readings.value}","{sum.value}", "{payment.value}")')


                elif trash.value == True:

                    cur.execute(f'INSERT INTO trash VALUES(NULL,"{account_number.value}","{date.value}","{payment.value}")')


                elif electro.value == True:

                    cur.execute(f'INSERT INTO electro VALUES(NULL,"{account_number.value}","{date.value}","{previous_readings.value}","{current_readings.value}","{sum.value}", "{payment.value}")')


                elif gas_delivery.value == True:

                    cur.execute(f'INSERT INTO gasdelivery VALUES(NULL,"{account_number.value}","{date.value}","{previous_readings.value}","{current_readings.value}","{sum.value}", "{payment.value}")')


            db.commit()
        except Error as er:

            # print(type(er))
            alert_banner(er)
            logging.exception(er, exc_info=True)

        page.snack_bar.open = True
        clear_fields()
        disable_fields()
        disable_value_chekboxes()
        enable_chekboxes()
        # date.value = ""
        # gas.value = False
        # electro.value = False
        # water.value = False
        # trash.value = False
        # gas_delivery.value = False
        # gas.disabled = False
        # gas_delivery.disabled = False
        # electro.disabled = False
        # water.disabled = False
        # trash.disabled = False
        add_btn.disabled = True
        date_button.disabled = True
        # date.disabled = True
        # until_price.disabled = True
        # previous_readings.disabled = True
        # current_readings.disabled = True
        # sum.disabled = True
        # payment.disabled = True
        # account_number.disabled = True
        page.update()




    def validate(e):
        if account_number.value  and until_price.value  and previous_readings.value and current_readings.value and date.value != "":#all([account_number.value,until_price,previous_readings,current_readings,date.value]):
            add_btn.disabled = False
            #difference = int(current_readings.value) - int(previous_readings.value)
            sum.value = int(current_readings.value) - int(previous_readings.value)
            payment.value = (int(current_readings.value) - int(previous_readings.value))*float(until_price.value)


        else:
            add_btn.disabled = True


        page.update()





    def change_date(e):
        dd = date_picker.value.date()
        date.value = dd
        enable_fields()
        page.update()



    def date_picker_dismissed(e):

        return date_picker.value



    date_picker = ft.DatePicker(
        on_change=change_date,
        on_dismiss=date_picker_dismissed,
        first_date=datetime.datetime(1989, 6, 1),
        last_date=datetime.datetime(2177, 10, 1),)

    page.overlay.append(date_picker)

    page.snack_bar = ft.SnackBar(content=ft.Text("Данные добавлены"), open=False)
    lv = ft.ListView(expand=1, spacing=10, padding=0, auto_scroll=True, divider_thickness=1)


    gas = ft.Checkbox(label="Газ", value= False, on_change=checkboxes_changed)  # ,col={"sm": 6, "md": 4, "xl": 2})
    gas_delivery = ft.Checkbox(label="Доставка газа", value= False, on_change= checkboxes_changed)
    electro = ft.Checkbox(label="Электроснобжение", value= False,on_change= checkboxes_changed )
    water = ft.Checkbox(label="Водоснабжение", value= False, on_change= checkboxes_changed)
    trash = ft.Checkbox(label="вывоз мусора", value= False,on_change= checkboxes_changed )

    account_number = ft.TextField(label="номер счёта", width=130,
                         input_filter=ft.InputFilter(allow=True, replacement_string="",
                                                     regex_string=r"[0-9,.-\s/]+"),on_change= validate,disabled= True)

    until_price = ft.TextField(label="цена(грн.) за 1 (м3,кВт)", width=150,
                         input_filter=ft.InputFilter(allow=True, replacement_string="",
                                                     regex_string=r"[0-9.-\s/]+"),on_change=validate,disabled= True)

    previous_readings = ft.TextField(label="предыдущие показания счётчика", width=150,input_filter=ft.InputFilter(allow=True, replacement_string="",regex_string=r"[0-9,.-\s/]+"),on_change=validate,disabled=True)


    current_readings = ft.TextField(label="текущие показания счётчика", width=150,input_filter=ft.InputFilter(allow=True, replacement_string="",regex_string=r"[0-9,.-\s/]+"),on_change=validate,disabled=True)

    payment = ft.TextField(label="сумма оплаты(грн.)", width=175,input_filter=ft.InputFilter(allow=True, replacement_string="",regex_string=r"[0-9,.-\s/]+"),disabled=True)

    date = ft.TextField(label= "дата", width=110,input_filter=ft.InputFilter(allow=True, replacement_string="",
                                                     regex_string=r"[0-9,.-\s/]+"),disabled= True)

    sum = ft.TextField(label="израсходовано", width=145,input_filter=ft.InputFilter(allow=True, replacement_string="",regex_string=r"[0-9,.-\s/]+"),disabled=True)
    text_id = ft.Text(value="")
    text_account = ft.Text(value="TEST_NAME")
    text_data = ft.Text(value="TEST_DATE")
    text_previus = ft.Text(value="TEXT_GENRE")
    text_curent = ft.Text(value="TEST_DIRECTOR")
    text_sum = ft.Text(value="TEXT_ACTORS")
    text_payment = ft.Text(value="TEST_STATE")

    results_panel = ft.Row(
        [ft.Text("                       ", weight=ft.FontWeight.BOLD), ft.Text("дата", weight=ft.FontWeight.BOLD),
         ft.Text("номер счёта", weight=ft.FontWeight.BOLD),
         ft.Text("предыдущие показания", weight=ft.FontWeight.BOLD),
         ft.Text("текущие показания", weight=ft.FontWeight.BOLD),
         ft.Text("израсходавано(кВт,м3)", weight=ft.FontWeight.BOLD),
         ft.Text("сумма оплаты(грн.)", weight=ft.FontWeight.BOLD)], wrap=True, spacing=50,)


    date_button = ft.ElevatedButton(
        "Pick date",
        icon=ft.icons.CALENDAR_MONTH,
        on_click= lambda _: date_picker.pick_date(),disabled= True)

    add_btn = ft.ElevatedButton(text= "Добавить в БД",on_click=sql_add,disabled=True)
    get_btn = ft.OutlinedButton(text="Получить из БД", width=200, on_click=get_value)

    input_panel = ft.Row([ft.Column([gas,gas_delivery,electro,water,trash]),date,account_number,until_price,previous_readings,current_readings,sum,payment])
    buttons_panel = ft.Row([date_button,add_btn,get_btn])


    page.add(input_panel,buttons_panel,results_panel,lv)#ft.Container([lv]))



if __name__ == "__main__":

    sqlite_create_db()
    ft.app(main)
