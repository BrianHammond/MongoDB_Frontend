import sys
import qdarkstyle
import datetime
from pymongo import MongoClient
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTableWidgetItem, QMessageBox
from PySide6.QtCore import QSettings
from main_ui import Ui_MainWindow as main_ui
from about_ui import Ui_Form as about_ui

class MainWindow(QMainWindow, main_ui): # used to display the main user interface
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # loads main_ui
        self.settings_manager = SettingsManager(self)  # Initializes SettingsManager
        self.settings_manager.load_settings()  # Load settings when the app starts
        self.mongo_db = MongoDB()  # Initialize MongoDB instance

        # Update label_connection based on connection status
        self.update_connection_status()

        # buttons
        self.button_send.clicked.connect(self.mongo_send)
        self.button_update.clicked.connect(self.mongo_update)
        self.button_query.clicked.connect(self.mongo_query)
        self.button_delete.clicked.connect(self.mongo_delete)
        self.button_connect.clicked.connect(self.mongo_url)

        # menubar
        self.action_dark_mode.toggled.connect(self.dark_mode)
        self.action_about.triggered.connect(self.show_about)
        self.action_about_qt.triggered.connect(self.about_qt)

        self.initialize_table()

    def mongo_send(self):
        self.current_date = datetime.datetime.now().strftime("%m%d%Y%H%M%S")
        id = self.current_date

        # Get the values from the QLineEdits
        name = self.line_name.text()  # QLineEdit for Name
        age = self.line_age.text()    # QLineEdit for Age
        title = self.line_title.text()  # QLineEdit for Title
        address1 = self.line_address1.text()  # QLineEdit for Address 1
        address2 = self.line_address2.text()  # QLineEdit for Address 2
        misc = self.line_misc.text()  # QLineEdit for Misc

        row = self.table.rowCount()
        self.populate_table(row, id, name, age, title, address1, address2, misc)

        # Prepare the data dictionary
        data = {
            "_id": id,
            "Name": name,
            "Age": age,
            "Title": title,
            "Address": {
                "Address 1": address1,
                "Address 2": address2
            },
            "Misc": misc
        }

        # Insert data into MongoDB
        if self.mongo_db.is_connected:
            # Access the 'employees' collection in the 'employees' database
            collection = self.mongo_db.db['employees']  # Switch to the 'employees' collection
            collection.insert_one(data)  # Insert the data into the collection
            print("Data inserted into MongoDB 'employees' collection")
        else:
            print("MongoDB is not connected. Cannot insert data.")

        # Optionally, clear fields after insertion
        self.clear_fields()

    def mongo_update(self):
        # Get the selected row from the table
        selected_row = self.table.currentRow()  # Get the selected row index

        if selected_row != -1:  # If a row is selected
            # Retrieve the data from the table
            id = self.table.item(selected_row, 0).text()  # Get the ID from the first column
            name = self.table.item(selected_row, 1).text()
            age = self.table.item(selected_row, 2).text()
            title = self.table.item(selected_row, 3).text()
            address1 = self.table.item(selected_row, 4).text()
            address2 = self.table.item(selected_row, 5).text()
            misc = self.table.item(selected_row, 6).text()

            # Prepare the updated data
            updated_data = {
                "Name": name,
                "Age": age,
                "Title": title,
                "Address": {
                    "Address 1": address1,
                    "Address 2": address2
                },
                "Misc": misc
            }

            # Update the data in MongoDB
            if self.mongo_db.is_connected:
                collection = self.mongo_db.db['employees']
                # Update the document with the given ID
                result = collection.update_one({"_id": id}, {"$set": updated_data})

                if result.matched_count > 0:
                    print("Document updated successfully in MongoDB")
                else:
                    print("No matching document found to update")
            else:
                print("MongoDB is not connected. Cannot update data.")
        
        self.table.resizeColumnsToContents()

    def mongo_query(self):
        print("Querying MongoDB")

        if self.mongo_db.is_connected:
            # Access the 'employees' collection in the 'employees' database
            collection = self.mongo_db.db['employees']

            # Query to get all documents from the collection
            documents = collection.find()

            # Clear the existing data in the table
            self.table.setRowCount(0)

            # Populate the table with data from MongoDB
            for doc in documents:
                row = self.table.rowCount()  # Get the next empty row index
                self.table.insertRow(row)  # Add a new row

                # Insert data into respective columns
                self.table.setItem(row, 0, QTableWidgetItem(str(doc.get('_id'))))
                self.table.setItem(row, 1, QTableWidgetItem(doc.get('Name', '')))
                self.table.setItem(row, 2, QTableWidgetItem(str(doc.get('Age', ''))))
                self.table.setItem(row, 3, QTableWidgetItem(doc.get('Title', '')))
                self.table.setItem(row, 4, QTableWidgetItem(doc.get('Address', {}).get('Address 1', '')))
                self.table.setItem(row, 5, QTableWidgetItem(doc.get('Address', {}).get('Address 2', '')))
                self.table.setItem(row, 6, QTableWidgetItem(doc.get('Misc', '')))

            # Resize the table to fit the new data
            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()
            print("Table populated with MongoDB data")

        else:
            print("MongoDB is not connected. Cannot query data.")

    def mongo_delete(self):
        print("Deleting from MongoDB")

        # Get the selected rows from the table
        selected_rows = self.table.selectedIndexes()

        # Check if any rows are selected
        if not selected_rows:
            print("No rows selected. Please select rows to delete.")
            return  # Early return if no rows are selected

        # Collect IDs from the selected rows
        ids_to_delete = {self.table.item(index.row(), 0).text() for index in selected_rows}

        # Confirm deletion with the user (optional)
        confirmation = QMessageBox.question(self, "Confirm Deletion",
                                            f"Are you sure you want to delete the selected {len(ids_to_delete)} records?",
                                            QMessageBox.Yes | QMessageBox.No)

        # Proceed only if the user confirms
        if confirmation != QMessageBox.Yes:
            print("Deletion cancelled.")
            return  # Early return if deletion is cancelled

        # Check MongoDB connection
        if not self.mongo_db.is_connected:
            print("MongoDB is not connected. Cannot delete data.")
            return  # Early return if not connected to MongoDB

        # Perform the deletion
        collection = self.mongo_db.db['employees']
        result = collection.delete_many({"_id": {"$in": list(ids_to_delete)}})

        # Handle the result of the deletion
        if result.deleted_count > 0:
            print(f"{result.deleted_count} document(s) deleted successfully from MongoDB")
            
            # Remove the rows from the table UI
            for row in sorted([index.row() for index in selected_rows], reverse=True):
                self.table.removeRow(row)
        else:
            print("No documents found to delete in MongoDB")

    def update_connection_status(self):
        self.mongo_db.is_connected = self.mongo_db.check_connection()
        if self.mongo_db.is_connected:
            self.label_connection.setText("Connected to MongoDB")
        else:
            self.label_connection.setText("Failed to connect to MongoDB")

    def mongo_url(self):
        server_url = self.line_server.text()  # Get IP address from line_server
        username = self.line_user.text()       # Get username from line_user
        password = self.line_pass.text()       # Get password from line_pass

        if server_url:
            # Create MongoDB instance with provided details
            self.mongo_db = MongoDB(host=server_url, username=username, password=password)
            self.mongo_db.connect()  # Try to connect
            
            # Update the connection status label
            self.update_connection_status()  # Refresh the connection status
        else:
            print("No server URL entered")
            self.label_connection.setText("Please enter a server URL")

    def initialize_table(self):
        self.table.setRowCount(0) # clears the table
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Age', 'Title', 'Address 1', 'Address 2', 'Misc'])
        self.table.setSelectionMode(QTableWidget.MultiSelection)

    def populate_table(self, row, id, name, age, title, address1, address2, misc):
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(str(id)))
        self.table.setItem(row, 1, QTableWidgetItem(name))
        self.table.setItem(row, 2, QTableWidgetItem(age))
        self.table.setItem(row, 3, QTableWidgetItem(title))
        self.table.setItem(row, 4, QTableWidgetItem(address1))
        self.table.setItem(row, 5, QTableWidgetItem(address2))
        self.table.setItem(row, 6, QTableWidgetItem(misc))
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def clear_fields(self):
        self.line_name.clear()
        self.line_age.clear()
        self.line_title.clear()
        self.line_address1.clear()
        self.line_address2.clear()
        self.line_misc.clear()

    def dark_mode(self, checked):
        if checked:
            self.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
        else:
            self.setStyleSheet('')

    def show_about(self):  # loads the About window
        self.about_window = AboutWindow(dark_mode=self.action_dark_mode.isChecked())
        self.about_window.show()

    def about_qt(self):  # loads the About Qt window
        QApplication.aboutQt()

    def closeEvent(self, event):  # Save settings when closing the app
        self.settings_manager.save_settings()  # Save settings using the manager
        event.accept()

class MongoDB:
    def __init__(self, host=None, port=27017, username=None, password=None, auth_db="admin"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.auth_db = auth_db
        self.client = None
        self.db = None

    def check_connection(self):
        try:
            # Try to send a ping to the server to check if it's alive
            self.client.admin.command('ping')  # Pings the MongoDB server
            return True
        except Exception:
            return False

    def connect(self):
        try:
            if self.username and self.password:
                # Connect to MongoDB with authentication using provided credentials
                self.client = MongoClient(self.host, self.port,
                                          username=self.username,
                                          password=self.password,
                                          authSource=self.auth_db)
                print(f"Connected to MongoDB at {self.host}:{self.port} with authentication")
            else:
                # Connect to MongoDB without authentication if no username/password is provided
                self.client = MongoClient(self.host, self.port)
                print(f"Connected to MongoDB at {self.host}:{self.port} without authentication")
            
            # Set the default database to use after connection is established
            self.db = self.client['employees']  # using the 'employees' database
            
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")

class SettingsManager: # used to load and save settings when opening and closing the app
    def __init__(self, main_window):
        self.main_window = main_window
        self.settings = QSettings('settings.ini', QSettings.IniFormat)

    def load_settings(self):
        size = self.settings.value('window_size', None)
        pos = self.settings.value('window_pos', None)
        dark = self.settings.value('dark_mode')
        
        if size is not None:
            self.main_window.resize(size)
        if pos is not None:
            self.main_window.move(pos)
        if dark == 'true':
            self.main_window.action_dark_mode.setChecked(True)
            self.main_window.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())

    def save_settings(self):
        self.settings.setValue('window_size', self.main_window.size())
        self.settings.setValue('window_pos', self.main_window.pos())
        self.settings.setValue('dark_mode', self.main_window.action_dark_mode.isChecked())

class AboutWindow(QWidget, about_ui): # Configures the About window
    def __init__(self, dark_mode=False):
        super().__init__()
        self.setupUi(self)

        if dark_mode:
            self.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())

if __name__ == "__main__":
    app = QApplication(sys.argv)  # needs to run first
    main_window = MainWindow()  # Instance of MainWindow
    main_window.show()
    sys.exit(app.exec())
