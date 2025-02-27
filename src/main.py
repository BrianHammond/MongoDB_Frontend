import sys
import qdarkstyle
import datetime
import pymongo
import json
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
        self.button_search.clicked.connect(self.mongo_search)

        # menubar
        self.action_dark_mode.toggled.connect(self.dark_mode)
        self.action_about.triggered.connect(self.show_about)
        self.action_about_qt.triggered.connect(self.about_qt)

    def mongo_send(self):
        db_collection = self.line_collection.text()
        self.current_date = datetime.datetime.now().strftime("%m%d%Y%H%M%S")
        id = self.current_date

        # Get the values from the QLineEdits
        firstname = self.line_firstname.text()
        lastname = self.line_lastname.text()
        age = self.line_age.text()
        title = self.line_title.text()
        address1 = self.line_address1.text()
        address2 = self.line_address2.text()
        country = self.line_country.text()
        misc = self.line_misc.text()

        row = self.table.rowCount()
        self.populate_table(row, id, firstname, lastname, age, title, address1, address2, country, misc)

        # Prepare the data dictionary
        data = {
            "_id": id,
            "Name": {
                "First Name": firstname,
                "Last Name": lastname
            },
            "Age": age,
            "Title": title,
            "Address": {
                "Address 1": address1,
                "Address 2": address2,
                "Country": country
            },
            "Misc": misc
        }

        # Insert data into MongoDB
        if self.mongo_db.is_connected:
            collection = self.mongo_db.db[db_collection]
            collection.insert_one(data)
        else:
            print("MongoDB is not connected. Cannot insert data.")

        self.clear_fields()

    def mongo_update(self):
        db_collection = self.line_collection.text()
        # Get the selected row from the table
        selected_row = self.table.currentRow()  # Get the selected row index

        if selected_row != -1:  # If a row is selected
            # Retrieve the data from the table
            id = self.table.item(selected_row, 0).text()  # Get the ID from the first column
            firstname = self.table.item(selected_row, 1).text()
            lastname = self.table.item(selected_row, 2).text()
            age = self.table.item(selected_row, 3).text()
            title = self.table.item(selected_row, 4).text()
            address1 = self.table.item(selected_row, 5).text()
            address2 = self.table.item(selected_row, 6).text()
            country = self.table.item(selected_row, 7).text()
            misc = self.table.item(selected_row, 8).text()

            # Prepare the updated data
            updated_data = {
                "Name": {
                    "First Name": firstname,
                    "Last Name": lastname
                },
                "Age": age,
                "Title": title,
                "Address": {
                    "Address 1": address1,
                    "Address 2": address2,
                    "Country": country
                },
                "Misc": misc
            }

            # Update the data in MongoDB
            if self.mongo_db.is_connected:
                collection = self.mongo_db.db[db_collection]
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
        db_collection = self.line_collection.text()
        self.initialize_table()

        if self.mongo_db.is_connected:
            collection = self.mongo_db.db[db_collection]

            # Query to get all documents from the collection
            documents = collection.find()

            self.table.setRowCount(0)

            # Populate the table with data from MongoDB
            for doc in documents:
                row = self.table.rowCount()  # Get the next empty row index
                self.table.insertRow(row)
                # Insert data into respective columns
                self.table.setItem(row, 0, QTableWidgetItem(str(doc.get('_id'))))
                self.table.setItem(row, 1, QTableWidgetItem(doc.get('Name', {}).get('First Name', '')))
                self.table.setItem(row, 2, QTableWidgetItem(doc.get('Name', {}).get('Last Name', '')))
                self.table.setItem(row, 3, QTableWidgetItem(str(doc.get('Age', ''))))
                self.table.setItem(row, 4, QTableWidgetItem(doc.get('Title', '')))
                self.table.setItem(row, 5, QTableWidgetItem(doc.get('Address', {}).get('Address 1', '')))
                self.table.setItem(row, 6, QTableWidgetItem(doc.get('Address', {}).get('Address 2', '')))
                self.table.setItem(row, 7, QTableWidgetItem(doc.get('Address', {}).get('Country', '')))
                self.table.setItem(row, 8, QTableWidgetItem(doc.get('Misc', '')))

            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()

        else:
            print("MongoDB is not connected. Cannot query data.")

    def mongo_delete(self):
        db_collection = self.line_collection.text()

        # Get the selected rows from the table
        selected_rows = self.table.selectedIndexes()

        # Check if any rows are selected
        if not selected_rows:
            return  # Early return if no rows are selected

        # Collect IDs from the selected rows
        ids_to_delete = {self.table.item(index.row(), 0).text() for index in selected_rows}

        # Confirm deletion with the user (optional)
        confirmation = QMessageBox.question(self, "Confirm Deletion",
                                            f"Are you sure you want to delete the selected {len(ids_to_delete)} records?",
                                            QMessageBox.Yes | QMessageBox.No)

        # Proceed only if the user confirms
        if confirmation != QMessageBox.Yes:
            return  # Early return if deletion is cancelled

        # Check MongoDB connection
        if not self.mongo_db.is_connected:
            return  # Early return if not connected to MongoDB

        # Perform the deletion
        collection = self.mongo_db.db[db_collection]
        result = collection.delete_many({"_id": {"$in": list(ids_to_delete)}})

        # Handle the result of the deletion
        if result.deleted_count > 0:
            # Remove the rows from the table UI
            for row in sorted([index.row() for index in selected_rows], reverse=True):
                self.table.removeRow(row)
        else:
            print("No documents found to delete in MongoDB")

    def mongo_search(self):
        db_collection = self.line_collection.text()
        firstname_search = self.line_firstname_search.text()
        lastname_search = self.line_lastname_search.text()

        query = {}
        if firstname_search:
            query["Name.First Name"] = firstname_search
        if lastname_search:
            query["Name.Last Name"] = lastname_search

        self.initialize_table()

        if self.mongo_db.is_connected:
            collection = self.mongo_db.db[db_collection]

            # Query to get documents based on search criteria
            documents = collection.find(query)

            # Clear the existing data in the table
            self.table.setRowCount(0)

            # Populate the table with data from MongoDB
            for doc in documents:
                row = self.table.rowCount()  # Get the next empty row index
                self.table.insertRow(row)  # Add a new row

                # Insert data into respective columns
                self.table.setItem(row, 0, QTableWidgetItem(str(doc.get('_id'))))
                self.table.setItem(row, 1, QTableWidgetItem(doc.get('Name', {}).get('First Name', '')))
                self.table.setItem(row, 2, QTableWidgetItem(doc.get('Name', {}).get('Last Name', '')))
                self.table.setItem(row, 3, QTableWidgetItem(str(doc.get('Age', ''))))
                self.table.setItem(row, 4, QTableWidgetItem(doc.get('Title', '')))
                self.table.setItem(row, 5, QTableWidgetItem(doc.get('Address', {}).get('Address 1', '')))
                self.table.setItem(row, 6, QTableWidgetItem(doc.get('Address', {}).get('Address 2', '')))
                self.table.setItem(row, 7, QTableWidgetItem(doc.get('Address', {}).get('Country', '')))
                self.table.setItem(row, 8, QTableWidgetItem(doc.get('Misc', '')))

            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()

        else:
            print("MongoDB is not connected. Cannot query data.")

    def update_connection_status(self):
        self.mongo_db.is_connected = self.mongo_db.check_connection()
        if self.mongo_db.is_connected:
            self.label_connection.setText("Connected to MongoDB")
        else:
            self.label_connection.setText("Failed to connect to MongoDB")

    def mongo_url(self):
        server_url = self.line_server.text()
        username = self.line_username.text()
        password = self.line_password.text()
        database = self.line_database.text()

        if any(not field for field in [server_url, username, password, database]):
            QMessageBox.warning(self, "Input Error", "Please fill in all fields: Server URL, Username, Password, and Database.")
            return

        # Create MongoDB instance with provided details
        self.mongo_db = MongoDB(host=server_url, username=username, password=password, database=database)
        self.mongo_db.connect()  # Try to connect

        # Update the connection status label
        self.update_connection_status()  # Refresh the connection status
        self.initialize_table()  # Initialize the table after connecting

    def initialize_table(self):
        self.table.setRowCount(0) # clears the table
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(['ID', 'First Name', 'Last Name', 'Age', 'Title', 'Address 1', 'Address 2', 'Country', 'Misc'])
        self.table.setSelectionMode(QTableWidget.MultiSelection)

    def populate_table(self, row, id, firstname, lastname, age, title, address1, address2, country, misc):
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(str(id)))
        self.table.setItem(row, 1, QTableWidgetItem(firstname))
        self.table.setItem(row, 2, QTableWidgetItem(lastname))
        self.table.setItem(row, 3, QTableWidgetItem(age))
        self.table.setItem(row, 4, QTableWidgetItem(title))
        self.table.setItem(row, 5, QTableWidgetItem(address1))
        self.table.setItem(row, 6, QTableWidgetItem(address2))
        self.table.setItem(row, 7, QTableWidgetItem(country))
        self.table.setItem(row, 8, QTableWidgetItem(misc))
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def clear_fields(self):
        self.line_firstname.clear()
        self.line_lastname.clear()
        self.line_age.clear()
        self.line_title.clear()
        self.line_address1.clear()
        self.line_address2.clear()
        self.line_country.clear()
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
    def __init__(self, host=None, port=27017, username=None, password=None, database=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
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
            self.client = MongoClient(self.host, self.port,
                                          username=self.username,
                                          password=self.password,
                                          authSource=self.database)  # Ensure 'authSource' is correct
           
            # Set the default database to use after connection is established
            self.db = self.client[self.database]
            
            # Try to send a ping to the server to check if it's alive
            self.client.admin.command('ping')  # Pings the MongoDB server
            print("Ping to MongoDB server successful")
        except pymongo.errors.OperationFailure as e:
            # Authentication failed, show message box with a simplified message
            QMessageBox.critical(None, "FAILED TO CONNECT", "Please check your credentials\nIf your credentials are fine then check the database and collections and try again.")
        except Exception as e:
            QMessageBox.critical(None, "Connection Error", f"Error connecting to MongoDB: {e}")

class SettingsManager: # used to load and save settings when opening and closing the app
    def __init__(self, main_window):
        self.main_window = main_window
        self.settings = QSettings('settings.ini', QSettings.IniFormat)

    def load_settings(self):
        size = self.settings.value('window_size', None)
        pos = self.settings.value('window_pos', None)
        dark = self.settings.value('dark_mode')
        server_url = self.settings.value('server_url')
        username = self.settings.value('username')
        database = self.settings.value('database')
        collection = self.settings.value('collection')
        
        if size is not None:
            self.main_window.resize(size)
        if pos is not None:
            self.main_window.move(pos)
        if dark == 'true':
            self.main_window.action_dark_mode.setChecked(True)
            self.main_window.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
        if server_url is not None:
            self.main_window.line_server.setText(server_url)
        if username is not None:
            self.main_window.line_username.setText(username)
        if database is not None:
            self.main_window.line_database.setText(database)
        if collection is not None:
            self.main_window.line_collection.setText(collection)

    def save_settings(self):
        self.settings.setValue('window_size', self.main_window.size())
        self.settings.setValue('window_pos', self.main_window.pos())
        self.settings.setValue('dark_mode', self.main_window.action_dark_mode.isChecked())
        self.settings.setValue('server_url', self.main_window.line_server.text())
        self.settings.setValue('username', self.main_window.line_username.text())
        self.settings.setValue('database', self.main_window.line_database.text())
        self.settings.setValue('collection', self.main_window.line_collection.text())

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