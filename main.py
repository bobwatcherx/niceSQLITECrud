import sqlite3
from nicegui import ui

conn = sqlite3.connect("db/mainan.db",check_same_thread=False)
cursor = conn.cursor()

name = ui.input(label="username").classes("w-full")
age = ui.input(label="you age").classes("w-full")

# CREATE ID TEXT FOR GET ID WHEN YOU CLICK EDIT AND DELETE BTN
get_id = ui.label()


# ADD NEW DATA
def addnewdata():
	try:
		cursor.execute('''INSERT INTO users (name,age) VALUES(?,?)''',(name.value,age.value))
		conn.commit()
		# SHOW NOTIF IF SUCCES ADD TO TABLE
		ui.notify(f"sucess add new data {name.value}",color="blue")

		# CLEAR INPUT NAME AND AGE
		name.value = ""
		age.value = ""
		# CLEAR ALL DATA IN LIST AND GET AGAIN
		list_alldata.clear()
		get_all_data()
	except Exception as e:
		print(e)

ui.button("add new data",
	on_click=addnewdata
	)

list_alldata = ui.column()


# FUNCTION FOR SAVE EDIT AFTER YOU CLICK SAVE IN DIALOG
def saveandedit(e):
	try:
		query = '''UPDATE users SET name=?,age=? WHERE id=?'''
		cursor.execute(query,(edit_name.value,edit_age.value,get_id.text))
		conn.commit()

		# AND SHOW NOTIF IF SUCCESS EDIT
		ui.notify("succes edit guys",color="green")
		# AND CLOSE EDIT DIALOG
		editdialog.close()

		# AND CLEAR list_alldata AND CALL FUNCTION GET TABLE AGAIN
		list_alldata.clear()
		get_all_data()
	except Exception as e:
		print(e)



# AND NOW CREATE DIALOG EDIT 
with ui.dialog() as editdialog:
	with ui.card():
		ui.label("Edit Data").classes("font-xl font-weight")

		# THIS INPUT IS GET VALUE FROM name textfield AND AUTO SET HERE
		edit_name = ui.input().bind_value_from(name,"value")
		edit_age = ui.input().bind_value_from(age,"value")
		
		# AND CREATE BUTTON SAVE EDIT AND CLOSE BUTTON
		with ui.row().classes("justify-between"):
			ui.button("save",on_click=lambda e:saveandedit(e))
			# FOR CLOSE DIALOG
			ui.button("close",on_click=editdialog.close).classes("bg-red")





# FOR EDIT FUNCTION
def editdata(x):
	# AND NOW GET ID FROM YOU CLICK EDIT BUTTON

	get_id.text = x.default_slot.children[0].text

	# AND SET NAME TEXTFIELD FROM YOU CLICK EDIT BUTTON
	name.value = x.default_slot.children[1].text
	age.value = x.default_slot.children[2].text

	# AND OPEN THE DIALOG EDIT 
	editdialog.open()
	ui.update()





# FOR DELETE
def deletebtn(x):
	# GET ID FROM YOU CLICK BUTTON DELETE

	get_id.text = x.default_slot.children[0].text
	cursor.execute('''DELETE FROM users WHERE id=?''',(get_id.text,))
	conn.commit()

	# AND CLEAR ALL DATA THEN CALL FUNCTION AGAIN FROM TABLE
	list_alldata.clear()
	get_all_data()

	# AND SHOW NOTIF IF YOU SUCCESS DELETE DATA FROM TABLE
	ui.notify("succes delete",color="red")	





# GET ALL DATA FROM TABLE
def get_all_data():
	cursor.execute('''SELECT * FROM users ''')
	res = cursor.fetchall()
	result = []
	for row in res:
		# AND CONVERT TO DICT JSON ARRAY
		data = {}
		for i,col in enumerate(cursor.description):
			data[col[0]] = row[i]
		result.append(data)
	print(result)

	# AND NOW AFTER GET ALL DATA FROM TABLE THEN CREATE CARD
	# FOR SEE DATA IN SCREEN APP
	for x in result:
		with list_alldata:
			# CREATE CARD FOR EDIT AND DELETE AND DATA
			with ui.card():
				with ui.column():
					with ui.row().classes("justify-between w-full") as carddata:
						ui.label(x['id'])
						ui.label(x['name'])
						ui.label(x['age'])
					with ui.row():
						# AND CREATE EDIT AND DELETE BUTTON
						ui.button("edit").on("click",lambda e, carddata=carddata : editdata(carddata))

						# AND DELETE
						ui.button("delete").on("click",lambda e, carddata=carddata : deletebtn(carddata)).classes("bg-red")


# AND CALL FUNCTION WHEN APP FIRST OPEN OR RUNNNING
get_all_data()


ui.run()