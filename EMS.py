# GUI Application for Employee Management System

from tkinter import *
import math
from datetime import datetime
import tkinter.messagebox as messagebox
from tkinter.scrolledtext import *
from sqlite3 import *
import matplotlib.pyplot as plt
import requests


root = Tk()
root.title("Employee Management System")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry('%dx%d+0+0' % (w, h))
root.configure(background="thistle")
f = ("Times New Roman", 25, "bold")




#===============================================================================================
# Validation for ID


def validateId(inputValue):

	if not inputValue:
		messagebox.showerror("Error", "ID cannot be empty.")
		return False

	if " " in inputValue:
		messagebox.showerror("Error", "ID cannot contain spaces.")
		return False

	if not inputValue.isalnum():  
		messagebox.showerror("Error", "ID cannot contain special characters.")
		return False

		value = float(inputValue)  # Convert to float for numerical checks

	if not inputValue.isdigit():
        	messagebox.showerror("Error", "ID must not be a text.")
        	return False

	return True


#===============================================================================================
# Validation for Name


def validateName(inputValue):

	if not inputValue:
		messagebox.showerror("Error", "Name cannot be empty.")
		return False

	if " " in inputValue:
		messagebox.showerror("Error", "Name cannot contain spaces.")
		return False

	if not inputValue.isalnum():  
		messagebox.showerror("Error", "Name cannot contain special characters.")
		return False

		value = float(inputValue)  # Convert to float for numerical checks

	if not inputValue.isalpha():
        	messagebox.showerror("Error", "Name must not be a number.")
        	return False

	return True


#===============================================================================================
# Validation for Salary


def validateSalary(inputValue, min_value=1000, max_value=1000000):
	if not inputValue:
		messagebox.showerror("Error", "Salary cannot be empty.")
		return False

	if " " in inputValue:
		messagebox.showerror("Error", "Salary cannot contain spaces.")
		return False

	if not inputValue.replace(".", "", 1).replace("-", "", 1).isalnum():  
		messagebox.showerror("Error", "Salary cannot contain special characters.")
		return False

		value = float(inputValue)  # Convert to float for numerical checks

	if not inputValue.replace(".", "", 1).replace("-", "", 1).isdigit():
        	messagebox.showerror("Error", "Salary must not be a text.")
        	return False

	if float(inputValue) < min_value:
		messagebox.showerror("Error", f"Salary must be greater than or equal to {min_value}")
		return False

	if float(inputValue) > max_value:
		messagebox.showerror("Error", f"Salary must be less than or equal to {max_value}")
		return False

	return True




#===============================================================================================
# Back to Main


def f1():
	root.deiconify()
	add.withdraw()

def f2():
	root.deiconify()
	view.withdraw()

def f3():
	root.deiconify()
	update.withdraw()

def f4():
	root.deiconify()
	delete.withdraw()

def f5():
	root.deiconify()
	plt.close()
	charts.withdraw()




#===============================================================================================
# Displaying the employee list


def viewData():
	view.deiconify()
	root.withdraw()

	empData.delete(1.0, END)
	con = None
	
	try:
		con = connect("EMS.db")
		cursor = con.cursor()
		sql = "select * from emp"
		cursor.execute(sql)
		data = cursor.fetchall()
		info = ""
		for d in data:
			info += "Id: " + str(d[0]) + "\t" + "Name: " + str(d[1]) + "\t     " + "Salary: " + str(d[2]) + "\n"
		empData.insert(INSERT, info)
	
	except Exception as e:
		showerror("Issue: ", e)
	
	finally:
		if con is not None:
			con.close()




#===============================================================================================
# Main Window


labTitle = Label(root, text="Employee Management System", font=f)
labTitle.place(x=580, y=20)

def add():
	add.deiconify()
	root.withdraw()

def delete():
	delete.deiconify()
	root.withdraw()

def update():
	update.deiconify()
	root.withdraw()

def charts():
	charts.deiconify()
	root.withdraw()


btnAdd = Button(root, text = "Add", font = f, width = 13, command = add)
btnAdd.place(x=670, y=130)
btnView = Button(root, text = "View", font = f, width = 13, command = viewData)
btnView.place(x=670, y=230)
btnUpdate = Button(root, text = "Update", font = f, width = 13, command = update)
btnUpdate.place(x=670, y=330)
btnDelete = Button(root, text = "Delete", font = f, width = 13, command = delete)
btnDelete.place(x=670, y=430)
btnCharts = Button(root, text = "Charts", font = f, width = 13, command = charts)
btnCharts.place(x=670, y=530)

labLocation = Label(root, text="Location:", font=f)
labLocation.place(x=300, y=650)
labTemp = Label(root, text="Temperature:", font=f)
labTemp.place(x=1000, y=650)




def get_location():
	try:
		response = requests.get('https://ipinfo.io/json')
		data = response.json()
		return data.get('city'), data.get('country')
	except Exception as e:
		print(f"Error fetching location: {e}")
		return None, None


def get_temperature(city):
	try:
		api_key = '661fde5f508fb99f18d46c5a329b0c96'
		url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
		response = requests.get(url)
		data = response.json()

		# Print the entire data for debugging
		print(data)

		if 'main' not in data:
			raise Exception("Missing 'main' key in response data")

		temperature = data['main']['temp']
		return temperature
	except Exception as e:
		print(f"Error fetching temperature: {e}")
		return None


# Update the location and temperature labels
def update_labels():
	city, country = get_location()
	temperature = get_temperature(city)
	labLocation.config(text=f"Location: {city}, {country}")
	labTemp.config(text=f"Temperature: {temperature}°C")

# Call the update_labels function initially to update the labels
update_labels()




#===============================================================================================
# Storing employee details in the database


def save():
	id = entId_add.get()
	name = entName_add.get()
	salary = entSalary_add.get()
	if validateId(id) and validateName(name) and validateSalary(salary): 
		id1 = int(id)
		salary1 = int(salary)
		con = None
		try:
			con = connect("EMS.db")
			cursor = con.cursor()

			sql = "SELECT * FROM emp WHERE id = ?"
			cursor.execute(sql, (id,))
			result = cursor.fetchone()
			if result:
				messagebox.showerror("Error", "ID already exists.")
			else:

				sql = "insert into emp(id, name, salary) values('%d', '%s', '%d')"
				cursor.execute(sql%(id1, name, salary1))
				con.commit()
				messagebox.showinfo("Done", "Congrats")

				entId_add.delete(0, END)
				entName_add.delete(0, END)
				entSalary_add.delete(0, END)
		except Exception as e:
			msg = "issue: " + str(e)
			messagebox.showerror("Problem", msg)
		finally:
			if con is not None:
				con.close()




#===============================================================================================
# Add Window


add = Toplevel(root)
add.title("Add Employee")
w, h = add.winfo_screenwidth(), root.winfo_screenheight()
add.geometry('%dx%d+0+0' % (w, h))
add.configure(background="thistle")
f = ("Times New Roman", 25, "bold")

labTitle = Label(add, text="Add Employee Details", font=f)
labTitle.place(x=580, y=20)

labId_add = Label(add, text="Enter Emp ID:", font=f, width = 15)
entId_add = Entry(add, font=f)

labName_add = Label(add, text="Enter Emp Name:", font=f, width = 15)
entName_add = Entry(add, font=f)

labSalary_add = Label(add, text="Enter Emp Salary:", font=f, width = 15)
entSalary_add = Entry(add, font=f)

labId_add.place(x=300, y=200)
entId_add.place(x=850, y=200)
labName_add.place(x=300, y=270)
entName_add.place(x=850, y=270)
labSalary_add.place(x=300, y=340)
entSalary_add.place(x=850, y=340)

btnSave = Button(add, text="Save", font=f, width = 10, command=save)
btnSave.place(x=670, y=500)

btnBack = Button(add, text = "Back to Main", font = f, width = 10, command = f1)
btnBack.place(x=670, y=600)

add.withdraw()




#===============================================================================================
# View Window


view = Toplevel(root)
view.title("View Employee")
w, h = view.winfo_screenwidth(), root.winfo_screenheight()
view.geometry('%dx%d+0+0' % (w, h))
view.configure(background="thistle")
f = ("Times New Roman", 25, "bold")

labTitle = Label(view, text="View Employee Details", font=f)
labTitle.place(x=620, y=20)

empData = ScrolledText(view, width = 45, height = 10, font = f)
empData.place(x=400, y=170)

btnBack = Button(view, text = "Back to Main", font = f, width = 10, command = f2)
btnBack.place(x=670, y=600)

view.withdraw()




#===============================================================================================
# Updating employee details in the database


def updateName():
	id = entId_update.get()
	name = entName_update.get()

	if validateId(id): 
		id1 = int(id)
		con = None
		try:
			con = connect("EMS.db")
			cursor = con.cursor()

			sql = "SELECT * FROM emp WHERE id = ?"
			cursor.execute(sql, (id,))
			result = cursor.fetchone()
			if not result:
				messagebox.showerror("Error", "ID does not exist.")
			else:
				sql = "UPDATE emp SET name = ? WHERE id = ?"  # Update statement
				cursor.execute(sql, (name, id1))				
				con.commit()
				messagebox.showinfo("Success", "Employee data updated successfully!")

				entId_update.delete(0, END)
				entName_update.delete(0, END)
		except Exception as e:
			msg = "issue: " + str(e)
			messagebox.showerror("Problem", msg)
		finally:
			if con is not None:
				con.close()


def updateSalary():
	id = entId_update.get()
	salary = entSalary_update.get()

	if validateId(id): 
		id1 = int(id)
		salary1 = int(salary)
		con = None
		try:
			con = connect("EMS.db")
			cursor = con.cursor()

			sql = "SELECT * FROM emp WHERE id = ?"
			cursor.execute(sql, (id,))
			result = cursor.fetchone()
			if not result:
				messagebox.showerror("Error", "ID does not exist.")
			else:
				sql = "UPDATE emp SET salary = ? WHERE id = ?"  # Update statement
				cursor.execute(sql, (salary1, id1))				
				con.commit()
				messagebox.showinfo("Success", "Employee data updated successfully!")

				entId_update.delete(0, END)
				entSalary_update.delete(0, END)
		except Exception as e:
			msg = "issue: " + str(e)
			messagebox.showerror("Problem", msg)
		finally:
			if con is not None:
				con.close()


def updateBoth():
	id = entId_update.get()
	name = entName_update.get()
	salary = entSalary_update.get()

	if validateId(id): 
		id1 = int(id)
		salary1 = int(salary)
		con = None
		try:
			con = connect("EMS.db")
			cursor = con.cursor()

			sql = "SELECT * FROM emp WHERE id = ?"
			cursor.execute(sql, (id,))
			result = cursor.fetchone()
			if not result:
				messagebox.showerror("Error", "ID does not exist.")
			else:
				sql = "UPDATE emp SET name = ?, salary = ? WHERE id = ?"  # Update statement
				cursor.execute(sql, (name, salary1, id1))				
				con.commit()
				messagebox.showinfo("Success", "Employee data updated successfully!")

				entId_update.delete(0, END)
				entName_update.delete(0, END)
				entSalary_update.delete(0, END)
		except Exception as e:
			msg = "issue: " + str(e)
			messagebox.showerror("Problem", msg)
		finally:
			if con is not None:
				con.close()




#===============================================================================================
# Update Window


update = Toplevel(root)
update.title("Add Employee")
w, h = update.winfo_screenwidth(), root.winfo_screenheight()
update.geometry('%dx%d+0+0' % (w, h))
update.configure(background="thistle")
f = ("Times New Roman", 25, "bold")

labTitle = Label(update, text="Update Employee Details", font=f)
labTitle.place(x=580, y=20)

labId_update = Label(update, text="Enter Emp ID:", font=f, width = 15)
entId_update = Entry(update, font=f)

# Options for updating data
options = [ 
    "Name", 
    "Salary",
    "Both", 
] 

# Creating Options Dropdown
updateDropdown = StringVar(update)
updateDropdown.set("Name")  

labName_update = Label(update, text="Enter Emp Name:", font=f, width = 15)
entName_update = Entry(update, font=f)

labSalary_update = Label(update, text="Enter Emp Salary:", font=f, width = 15)
entSalary_update = Entry(update, font=f)

labId_update.place(x=300, y=200)
entId_update.place(x=850, y=200)


# Displaying the input labels when options changed


def updateData(*args):
	selectedOption = updateDropdown.get()

	if selectedOption == "Name":
		labName_update.place(x=300, y=320)
		entName_update.place(x=850, y=320)
    		
		labSalary_update.place_forget()
		entSalary_update.place_forget()

		btnSave.config(command=updateName)

	elif selectedOption == "Salary":
		labSalary_update.place(x=300, y=320)
		entSalary_update.place(x=850, y=320)

		labName_update.place_forget()
		entName_update.place_forget()

		btnSave.config(command=updateSalary)

	elif selectedOption == "Both":
		labName_update.place(x=300, y=320)
		entName_update.place(x=850, y=320)
		labSalary_update.place(x=300, y=370)
		entSalary_update.place(x=850, y=370)

		btnSave.config(command=updateBoth)
	else:
		labName_update.place_forget()
		entName_update.place_forget()
		labSalary_update.place_forget()
		entSalary_update.place_forget()

updateDropdown.trace("w", updateData) 

labOptions = Label(update, text="Select data to be updated:", font=f)
labOptions.place(x=300, y=250)

updateOptions = OptionMenu(update, updateDropdown, *options)
updateOptions.config(font=f)
updateOptions.place(x=850, y=250)

btnSave = Button(update, text="Save", font=f, width = 10, command=update)
btnSave.place(x=670, y=500)

btnBack = Button(update, text = "Back to Main", font = f, width = 13, command = f3)
btnBack.place(x=670, y=600)

update.withdraw()




#===============================================================================================
# Deleting employee details in the database


def deleteData():
	id = entId_delete.get()
	if validateId(id): 
		id1 = int(id)
		con = None
		try:
			con = connect("EMS.db")
			cursor = con.cursor()

			sql = "SELECT * FROM emp WHERE id = ?"
			cursor.execute(sql, (id,))
			result = cursor.fetchone()
			if not result:
				messagebox.showerror("Error", "ID does not exist.")
			else:

				sql = "DELETE FROM emp WHERE id = ?"  # Delete statement
				cursor.execute(sql, (id1,))
				con.commit()
				messagebox.showinfo("Success", "Employee data deleted successfully!")

				entId_delete.delete(0, END)
		except Exception as e:
			msg = "issue: " + str(e)
			messagebox.showerror("Problem", msg)
		finally:
			if con is not None:
				con.close()




#===============================================================================================
# Delete Window


delete = Toplevel(root)
delete.title("Delete Employee")
w, h = delete.winfo_screenwidth(), root.winfo_screenheight()
delete.geometry('%dx%d+0+0' % (w, h))
delete.configure(background="thistle")
f = ("Times New Roman", 25, "bold")

labTitle = Label(delete, text="Delete Employee", font=f)
labTitle.place(x=580, y=20)

labId_delete = Label(delete, text="Enter Emp ID:", font=f, width = 15)
entId_delete = Entry(delete, font=f)
labId_delete.place(x=300, y=200)
entId_delete.place(x=850, y=200)

btnDelete = Button(delete, text="Delete", font=f, width = 10, command=deleteData)
btnDelete.place(x=670, y=500)

btnBack = Button(delete, text = "Back to Main", font = f, width = 13, command = f4)
btnBack.place(x=670, y=600)

delete.withdraw()




#===============================================================================================
# Displaying the charts


def displayCharts():
	# Connect to the database
	conn = connect("EMS.db")
	cursor = conn.cursor()

	# Fetch the top 5 highest-earning salaried employees
	cursor.execute("SELECT name, salary FROM emp ORDER BY salary DESC LIMIT 5")
	results = cursor.fetchall()

	# Extract names and salaries from the results
	names = [result[0] for result in results]
	salaries = [result[1] for result in results]

	# Create the bar chart
	plt.figure(figsize=(7, 4))
	plt.bar(names, salaries, color='skyblue')
	plt.xlabel('Employee Name')
	plt.ylabel('Salary')
	plt.title('Top 5 Highest-Earning Salaried Employees')
	plt.xticks(rotation=45)
	plt.tight_layout()

	fig_manager = plt.get_current_fig_manager()
	fig_manager.window.wm_geometry("+450+130")

	# Show the bar chart
	plt.show()

	# Close the database connection
	conn.close()




#===============================================================================================
# Charts Window


charts = Toplevel(root)
charts.title("Add Employee")
w, h = charts.winfo_screenwidth(), root.winfo_screenheight()
charts.geometry('%dx%d+0+0' % (w, h))
charts.configure(background="thistle")
f = ("Times New Roman", 25, "bold")

labTitle = Label(charts, text="Top 5 Earnings", font=f)
labTitle.place(x=610, y=20)

btn_charts = Button(charts, text="Show Chart", font=f,  width = 13, command=displayCharts)
btn_charts.place(x=670, y=600)

btnBack = Button(charts, text = "Back to Main", font = f, width = 13, command = f5)
btnBack.place(x=670, y=700)

charts.withdraw()


root.mainloop()
