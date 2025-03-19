import sys
import qdarkstyle
import datetime
import pymongo
import csv
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog
from PySide6.QtCore import QSettings
from main_ui import Ui_MainWindow as main_ui
from about_ui import Ui_Dialog as about_ui
from cryptography.fernet import Fernet

class MainWindow(QMainWindow, main_ui): # used to display the main user interface
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # loads main_ui
        self.settings_manager = SettingsManager(self)  # Initializes SettingsManager
        self.settings_manager.load_settings()  # Load settings when the app starts
        self.mongo_db = MongoDB()  # Initialize MongoDB instance

        self.label_connection.setText("Not Connected to MongoDB")

        # buttons
        self.button_send.clicked.connect(self.mongo_send) # Send button is pressed
        self.button_update.clicked.connect(self.mongo_update) # Update button is pressed
        self.button_query.clicked.connect(self.mongo_query) # Query button is pressed
        self.button_delete.clicked.connect(self.mongo_delete) # Delete button is pressed
        self.button_connect.clicked.connect(self.connect_to_mongo) # Connect button is pressed
        self.button_search.clicked.connect(self.mongo_search) # Search button is pressed
        self.button_csv.clicked.connect(self.export_to_csv) # Export to CSV button is pressed

        # menubar
        self.action_dark_mode.toggled.connect(self.dark_mode) # Dark mode is toggled
        self.action_about_qt.triggered.connect(lambda: QApplication.aboutQt()) # Displays the about Qt dialog
        self.action_about.triggered.connect(lambda: AboutWindow(dark_mode=self.action_dark_mode.isChecked()).exec()) # Displays the about dialog

        # radio button
        self.radio_mongo_cloud.toggled.connect(lambda checked: self.line_cluster.setEnabled(checked)) # Enables the cluster field when MongoDB Cloud radio button is toggled

    def mongo_send(self): # sends data to MongoDB (send button is pressed)
        db_collection = self.line_collection.text()
        id = datetime.datetime.now().strftime("%m%d%Y%H%M%S")

        # Get the values from the QLineEdits
        firstname = self.line_firstname.text()
        middlename = self.line_middlename.text()
        lastname = self.line_lastname.text()
        age = self.line_age.text()
        title = self.line_title.text()
        address1 = self.line_address1.text()
        address2 = self.line_address2.text()
        country = self.line_country.text()
        misc = self.line_misc.text()

        row = self.table.rowCount()
        self.populate_table(row, id, firstname, middlename, lastname, age, title, address1, address2, country, misc)

        # Prepare the data dictionary
        data = {
            "_id": id,
            "Name": {
                "First Name": firstname,
                "Middle Name": middlename,
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

    def mongo_update(self): # updates data in MongoDB (update button is pressed)
        db_collection = self.line_collection.text()
        # Get the selected row from the table
        selected_row = self.table.currentRow()  # Get the selected row index

        if selected_row != -1:  # If a row is selected
            # Retrieve the data from the table
            id = self.table.item(selected_row, 0).text()  # Get the ID from the first column
            firstname = self.table.item(selected_row, 1).text()
            middlename = self.table.item(selected_row, 2).text()
            lastname = self.table.item(selected_row, 3).text()
            age = self.table.item(selected_row, 4).text()
            title = self.table.item(selected_row, 5).text()
            address1 = self.table.item(selected_row, 6).text()
            address2 = self.table.item(selected_row, 7).text()
            country = self.table.item(selected_row, 8).text()
            misc = self.table.item(selected_row, 9).text()

            # Prepare the updated data
            updated_data = {
                "Name": {
                    "First Name": firstname,
                    "Middle Name": middlename,
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

    def mongo_query(self): # queries data from MongoDB (query button is pressed)
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
                self.table.setItem(row, 2, QTableWidgetItem(doc.get('Name', {}).get('Middle Name', '')))
                self.table.setItem(row, 3, QTableWidgetItem(doc.get('Name', {}).get('Last Name', '')))
                self.table.setItem(row, 4, QTableWidgetItem(str(doc.get('Age', ''))))
                self.table.setItem(row, 5, QTableWidgetItem(doc.get('Title', '')))
                self.table.setItem(row, 6, QTableWidgetItem(doc.get('Address', {}).get('Address 1', '')))
                self.table.setItem(row, 7, QTableWidgetItem(doc.get('Address', {}).get('Address 2', '')))
                self.table.setItem(row, 8, QTableWidgetItem(doc.get('Address', {}).get('Country', '')))
                self.table.setItem(row, 9, QTableWidgetItem(doc.get('Misc', '')))

            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()

        else:
            print("MongoDB is not connected. Cannot query data.")

    def mongo_delete(self): # deletes data from MongoDB (delete button is pressed)
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

    def mongo_search(self): # searches data in MongoDB (search button is pressed)
        db_collection = self.line_collection.text()
        firstname_search = self.line_firstname_search.text()
        lastname_search = self.line_lastname_search.text()

        query = {}
        if firstname_search:
            query["Name.First Name"] = {"$regex": firstname_search, "$options": "i"} # case-insensitive search
        if lastname_search:
            query["Name.Last Name"] = {"$regex": lastname_search, "$options": "i"} # case-insensitive search

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
                self.table.setItem(row, 2, QTableWidgetItem(doc.get('Name', {}).get('Middle Name', '')))
                self.table.setItem(row, 3, QTableWidgetItem(doc.get('Name', {}).get('Last Name', '')))
                self.table.setItem(row, 4, QTableWidgetItem(str(doc.get('Age', ''))))
                self.table.setItem(row, 5, QTableWidgetItem(doc.get('Title', '')))
                self.table.setItem(row, 6, QTableWidgetItem(doc.get('Address', {}).get('Address 1', '')))
                self.table.setItem(row, 7, QTableWidgetItem(doc.get('Address', {}).get('Address 2', '')))
                self.table.setItem(row, 8, QTableWidgetItem(doc.get('Address', {}).get('Country', '')))
                self.table.setItem(row, 9, QTableWidgetItem(doc.get('Misc', '')))

            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()

        else:
            print("MongoDB is not connected. Cannot query data.")

    def export_to_csv(self):  # exports data to CSV (export to CSV button is pressed)
        self.filename = QFileDialog.getSaveFileName(self, 'Export File', '', 'Data File (*.csv)')

        if not self.filename[0]:
            return

        try:
            with open(self.filename[0], 'w', newline='') as file:
                writer = csv.writer(file)
                
                # Write the header row (column names from the table)
                headers = [self.table.horizontalHeaderItem(col).text() for col in range(self.table.columnCount())]
                writer.writerow(headers)

                # Write the data rows from the table
                for row in range(self.table.rowCount()):
                    row_data = []
                    for col in range(self.table.columnCount()):
                        item = self.table.item(row, col)
                        # Append the text if the item exists, otherwise append an empty string
                        row_data.append(item.text() if item else '')
                    writer.writerow(row_data)

            QMessageBox.information(self, "Export Successful", f"Table data exported to {self.filename[0]}")
        
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export to CSV: {str(e)}")

    def connect_to_mongo(self): # connects to MongoDB (connect button is pressed)
        server_url = self.line_server.text()
        username = self.line_username.text()
        password = self.line_password.text()
        database = self.line_database.text()
        cluster = self.line_cluster.text()

        if any(not field for field in [server_url, username, password, database]):
            QMessageBox.warning(self, "Input Error", "Please fill in all fields: Server URL, Username, Password, and Database.")
            return

        # Create MongoDB instance with provided details
        self.mongo_db = MongoDB(
            server_url=server_url, 
            username=username, 
            password=password, 
            database=database,
            cluster=cluster,
            parent=self)
        
        self.mongo_db.connect()  # Try to connect

        #self.mongo_query()

    def initialize_table(self):
        self.table.setRowCount(0) # clears the table
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels(['ID', 'First Name', 'Middle Name', 'Last Name', 'Age', 'Title', 'Address 1', 'Address 2', 'Country', 'Misc'])
        self.table.setSelectionMode(QTableWidget.MultiSelection)

    def populate_table(self, row, id, firstname, middlename, lastname, age, title, address1, address2, country, misc):
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(str(id)))
        self.table.setItem(row, 1, QTableWidgetItem(firstname))
        self.table.setItem(row, 2, QTableWidgetItem(middlename))
        self.table.setItem(row, 3, QTableWidgetItem(lastname))
        self.table.setItem(row, 4, QTableWidgetItem(age))
        self.table.setItem(row, 5, QTableWidgetItem(title))
        self.table.setItem(row, 6, QTableWidgetItem(address1))
        self.table.setItem(row, 7, QTableWidgetItem(address2))
        self.table.setItem(row, 8, QTableWidgetItem(country))
        self.table.setItem(row, 9, QTableWidgetItem(misc))
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def clear_fields(self):
        self.line_firstname.clear()
        self.line_middlename.clear()
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

    def closeEvent(self, event):  # Save settings when closing the app
        self.settings_manager.save_settings()  # Save settings using the manager
        event.accept()

class MongoDB: # Connect to MongoDB Cloud
    def __init__(self, server_url=None, port=27017, username=None, password=None, database=None, cluster=None, parent=None):
        self.server_url = server_url
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.client = None
        self.db = None
        self.cluster = cluster
        self.is_connected = False
        self.parent = parent

    def connect(self):
        try:
            # Check radio button state and use appropriate URI
            if self.parent and self.parent.radio_mongo_cloud.isChecked():
                uri = f"mongodb+srv://{self.username}:{self.password}@{self.server_url}/?retryWrites=true&w=majority&appName={self.cluster}"
                self.client = MongoClient(uri, server_api=ServerApi('1'))
            else:
                # Local MongoDB connection
                uri = f"mongodb://{self.username}:{self.password}@{self.server_url}:{self.port}/"
                self.client = MongoClient(uri)
            
            # Set the default database to use after connection is established
            self.db = self.client[self.database]
            
            # Try to send a ping to the server to check if it's alive
            self.client.admin.command('ping')  # Pings the MongoDB server
            self.is_connected = True
            QMessageBox.information(None, "MongoDB", f"Successfully connected {self.server_url}")

            if self.parent:
                self.parent.label_connection.setText("Connected to MongoDB")
            print("Ping to MongoDB server successful")

            self.parent.mongo_query()
            
        except pymongo.errors.OperationFailure as e:
            if self.parent:
                self.parent.label_connection.setText("Failed to connect to MongoDB")
            # Authentication failed, show message box with a simplified message
            QMessageBox.critical(None, "FAILED TO CONNECT", "Please check your credentials\nIf your credentials are fine then check the database and collections and try again.")
        except Exception as e:
            if self.parent:
                self.parent.label_connection.setText("Failed to connect to MongoDB")
            QMessageBox.critical(None, "Connection Error", f"Error connecting to MongoDB: {e}")

class SettingsManager: # used to load and save settings when opening and closing the app
    def __init__(self, main_window):
        self.main_window = main_window
        self.settings = QSettings('settings.ini', QSettings.IniFormat)
        self.key = self.settings.value('encryption_key', None)
        if self.key is None:
            self.key = Fernet.generate_key()
            self.settings.setValue('encryption_key', self.key.decode())
        self.cipher = Fernet(self.key)

    def encrypt_text(self, text):
        if not text:
            return None
        return self.cipher.encrypt(text.encode()).decode()
    
    def decrypt_text(self, encrypted_text):
        if not encrypted_text:
            return None
        try:
            return self.cipher.decrypt(encrypted_text.encode()).decode()
        except Exception as e:
            print(f"Decryption error: {e}")
            return None

    def load_settings(self):
        size = self.settings.value('window_size', None)
        pos = self.settings.value('window_pos', None)
        dark = self.settings.value('dark_mode')
        server_url = self.settings.value('server_url')
        username = self.settings.value('username')
        database = self.settings.value('database')
        collection = self.settings.value('collection')
        encrypted_password = self.settings.value('password')
        on_cloud = self.settings.value('on_cloud')
        cluster = self.settings.value('cluster')
        
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

        if encrypted_password is not None:
            password = self.decrypt_text(encrypted_password)
            if password:
                self.main_window.line_password.setText(password)
            else:
                self.main_window.line_password.setText("")
        if on_cloud == 'true':
            self.main_window.radio_mongo_cloud.setChecked(True)
            self.main_window.line_cluster.setEnabled(True)

        if cluster is not None:
            self.main_window.line_cluster.setText(cluster)

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
        self.settings.setValue('on_cloud', self.main_window.radio_mongo_cloud.isChecked())
        self.settings.setValue('cluster', self.main_window.line_cluster.text())

        password = self.main_window.line_password.text()
        self.settings.setValue('password', self.encrypt_text(password))

class AboutWindow(QDialog, about_ui): 
    def __init__(self, dark_mode=False):
        super().__init__()
        self.setupUi(self)
        if dark_mode:
            self.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
        self.button_ok.clicked.connect(self.accept)

if __name__ == "__main__":
    app = QApplication(sys.argv)  # needs to run first
    main_window = MainWindow()  # Instance of MainWindow
    main_window.show()
    sys.exit(app.exec())