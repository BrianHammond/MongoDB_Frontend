# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(957, 787)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u":/images/ms_icon.jpg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"")
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"action_about")
        self.action_about_qt = QAction(MainWindow)
        self.action_about_qt.setObjectName(u"action_about_qt")
        self.action_dark_mode = QAction(MainWindow)
        self.action_dark_mode.setObjectName(u"action_dark_mode")
        self.action_dark_mode.setCheckable(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_4 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.line_server = QLineEdit(self.groupBox_2)
        self.line_server.setObjectName(u"line_server")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.line_server.sizePolicy().hasHeightForWidth())
        self.line_server.setSizePolicy(sizePolicy1)
        self.line_server.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_4.addWidget(self.line_server)

        self.line_username = QLineEdit(self.groupBox_2)
        self.line_username.setObjectName(u"line_username")
        sizePolicy1.setHeightForWidth(self.line_username.sizePolicy().hasHeightForWidth())
        self.line_username.setSizePolicy(sizePolicy1)
        self.line_username.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_4.addWidget(self.line_username)

        self.line_password = QLineEdit(self.groupBox_2)
        self.line_password.setObjectName(u"line_password")
        sizePolicy1.setHeightForWidth(self.line_password.sizePolicy().hasHeightForWidth())
        self.line_password.setSizePolicy(sizePolicy1)
        self.line_password.setMinimumSize(QSize(150, 0))
        self.line_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.horizontalLayout_4.addWidget(self.line_password)

        self.line_cluster = QLineEdit(self.groupBox_2)
        self.line_cluster.setObjectName(u"line_cluster")
        self.line_cluster.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.line_cluster)

        self.radio_mongo_cloud = QRadioButton(self.groupBox_2)
        self.radio_mongo_cloud.setObjectName(u"radio_mongo_cloud")

        self.horizontalLayout_4.addWidget(self.radio_mongo_cloud)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.line_database = QLineEdit(self.groupBox_2)
        self.line_database.setObjectName(u"line_database")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.line_database.sizePolicy().hasHeightForWidth())
        self.line_database.setSizePolicy(sizePolicy2)
        self.line_database.setMinimumSize(QSize(300, 0))

        self.horizontalLayout_6.addWidget(self.line_database)

        self.line_collection = QLineEdit(self.groupBox_2)
        self.line_collection.setObjectName(u"line_collection")
        sizePolicy2.setHeightForWidth(self.line_collection.sizePolicy().hasHeightForWidth())
        self.line_collection.setSizePolicy(sizePolicy2)
        self.line_collection.setMinimumSize(QSize(300, 0))

        self.horizontalLayout_6.addWidget(self.line_collection)

        self.button_connect = QPushButton(self.groupBox_2)
        self.button_connect.setObjectName(u"button_connect")
        sizePolicy2.setHeightForWidth(self.button_connect.sizePolicy().hasHeightForWidth())
        self.button_connect.setSizePolicy(sizePolicy2)
        self.button_connect.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_6.addWidget(self.button_connect)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)


        self.verticalLayout_4.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.line_firstname = QLineEdit(self.groupBox)
        self.line_firstname.setObjectName(u"line_firstname")

        self.horizontalLayout.addWidget(self.line_firstname)

        self.line_middlename = QLineEdit(self.groupBox)
        self.line_middlename.setObjectName(u"line_middlename")

        self.horizontalLayout.addWidget(self.line_middlename)

        self.line_lastname = QLineEdit(self.groupBox)
        self.line_lastname.setObjectName(u"line_lastname")

        self.horizontalLayout.addWidget(self.line_lastname)

        self.line_age = QLineEdit(self.groupBox)
        self.line_age.setObjectName(u"line_age")

        self.horizontalLayout.addWidget(self.line_age)

        self.line_title = QLineEdit(self.groupBox)
        self.line_title.setObjectName(u"line_title")

        self.horizontalLayout.addWidget(self.line_title)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.line_address1 = QLineEdit(self.groupBox)
        self.line_address1.setObjectName(u"line_address1")

        self.horizontalLayout_2.addWidget(self.line_address1)

        self.line_address2 = QLineEdit(self.groupBox)
        self.line_address2.setObjectName(u"line_address2")

        self.horizontalLayout_2.addWidget(self.line_address2)

        self.line_country = QLineEdit(self.groupBox)
        self.line_country.setObjectName(u"line_country")

        self.horizontalLayout_2.addWidget(self.line_country)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.line_misc = QLineEdit(self.groupBox)
        self.line_misc.setObjectName(u"line_misc")

        self.verticalLayout_3.addWidget(self.line_misc)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.button_send = QPushButton(self.groupBox)
        self.button_send.setObjectName(u"button_send")
        sizePolicy2.setHeightForWidth(self.button_send.sizePolicy().hasHeightForWidth())
        self.button_send.setSizePolicy(sizePolicy2)
        self.button_send.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_3.addWidget(self.button_send)

        self.button_update = QPushButton(self.groupBox)
        self.button_update.setObjectName(u"button_update")
        sizePolicy2.setHeightForWidth(self.button_update.sizePolicy().hasHeightForWidth())
        self.button_update.setSizePolicy(sizePolicy2)
        self.button_update.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_3.addWidget(self.button_update)

        self.button_delete = QPushButton(self.groupBox)
        self.button_delete.setObjectName(u"button_delete")
        sizePolicy2.setHeightForWidth(self.button_delete.sizePolicy().hasHeightForWidth())
        self.button_delete.setSizePolicy(sizePolicy2)
        self.button_delete.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_3.addWidget(self.button_delete)

        self.button_query = QPushButton(self.groupBox)
        self.button_query.setObjectName(u"button_query")
        sizePolicy2.setHeightForWidth(self.button_query.sizePolicy().hasHeightForWidth())
        self.button_query.setSizePolicy(sizePolicy2)
        self.button_query.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_3.addWidget(self.button_query)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.verticalLayout_4.addWidget(self.groupBox)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMinimumSize(QSize(12, 58))
        self.verticalLayout = QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.line_firstname_search = QLineEdit(self.groupBox_3)
        self.line_firstname_search.setObjectName(u"line_firstname_search")

        self.horizontalLayout_5.addWidget(self.line_firstname_search)

        self.line_lastname_search = QLineEdit(self.groupBox_3)
        self.line_lastname_search.setObjectName(u"line_lastname_search")

        self.horizontalLayout_5.addWidget(self.line_lastname_search)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.button_search = QPushButton(self.groupBox_3)
        self.button_search.setObjectName(u"button_search")
        sizePolicy2.setHeightForWidth(self.button_search.sizePolicy().hasHeightForWidth())
        self.button_search.setSizePolicy(sizePolicy2)
        self.button_search.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_7.addWidget(self.button_search)

        self.button_import_csv = QPushButton(self.groupBox_3)
        self.button_import_csv.setObjectName(u"button_import_csv")
        sizePolicy2.setHeightForWidth(self.button_import_csv.sizePolicy().hasHeightForWidth())
        self.button_import_csv.setSizePolicy(sizePolicy2)
        self.button_import_csv.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_7.addWidget(self.button_import_csv)

        self.button_export_csv = QPushButton(self.groupBox_3)
        self.button_export_csv.setObjectName(u"button_export_csv")
        sizePolicy2.setHeightForWidth(self.button_export_csv.sizePolicy().hasHeightForWidth())
        self.button_export_csv.setSizePolicy(sizePolicy2)
        self.button_export_csv.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_7.addWidget(self.button_export_csv)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_7)


        self.verticalLayout_4.addWidget(self.groupBox_3)

        self.table = QTableWidget(self.centralwidget)
        self.table.setObjectName(u"table")
        self.table.setRowCount(0)
        self.table.verticalHeader().setVisible(False)

        self.verticalLayout_4.addWidget(self.table)

        self.label_connection = QLabel(self.centralwidget)
        self.label_connection.setObjectName(u"label_connection")

        self.verticalLayout_4.addWidget(self.label_connection)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 957, 22))
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.line_server, self.line_username)
        QWidget.setTabOrder(self.line_username, self.line_password)
        QWidget.setTabOrder(self.line_password, self.line_cluster)
        QWidget.setTabOrder(self.line_cluster, self.radio_mongo_cloud)
        QWidget.setTabOrder(self.radio_mongo_cloud, self.line_database)
        QWidget.setTabOrder(self.line_database, self.line_collection)
        QWidget.setTabOrder(self.line_collection, self.button_connect)
        QWidget.setTabOrder(self.button_connect, self.line_firstname)
        QWidget.setTabOrder(self.line_firstname, self.line_middlename)
        QWidget.setTabOrder(self.line_middlename, self.line_lastname)
        QWidget.setTabOrder(self.line_lastname, self.line_age)
        QWidget.setTabOrder(self.line_age, self.line_title)
        QWidget.setTabOrder(self.line_title, self.line_address1)
        QWidget.setTabOrder(self.line_address1, self.line_address2)
        QWidget.setTabOrder(self.line_address2, self.line_country)
        QWidget.setTabOrder(self.line_country, self.line_misc)
        QWidget.setTabOrder(self.line_misc, self.button_send)
        QWidget.setTabOrder(self.button_send, self.button_update)
        QWidget.setTabOrder(self.button_update, self.button_delete)
        QWidget.setTabOrder(self.button_delete, self.button_query)
        QWidget.setTabOrder(self.button_query, self.line_firstname_search)
        QWidget.setTabOrder(self.line_firstname_search, self.line_lastname_search)
        QWidget.setTabOrder(self.line_lastname_search, self.button_search)
        QWidget.setTabOrder(self.button_search, self.button_import_csv)
        QWidget.setTabOrder(self.button_import_csv, self.button_export_csv)
        QWidget.setTabOrder(self.button_export_csv, self.table)

        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuHelp.addAction(self.action_about)
        self.menuHelp.addAction(self.action_about_qt)
        self.menuSettings.addAction(self.action_dark_mode)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MongoDB Frontend", None))
        self.action_about.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.action_about_qt.setText(QCoreApplication.translate("MainWindow", u"About Qt", None))
        self.action_dark_mode.setText(QCoreApplication.translate("MainWindow", u"Dark Mode", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Server Info", None))
        self.line_server.setText("")
        self.line_server.setPlaceholderText(QCoreApplication.translate("MainWindow", u"MongoDB IP", None))
        self.line_username.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Username", None))
        self.line_password.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Password", None))
#if QT_CONFIG(statustip)
        self.line_cluster.setStatusTip(QCoreApplication.translate("MainWindow", u"Used only for MongoDB Cloud", None))
#endif // QT_CONFIG(statustip)
        self.line_cluster.setPlaceholderText(QCoreApplication.translate("MainWindow", u"MongoDB Cluster", None))
#if QT_CONFIG(statustip)
        self.radio_mongo_cloud.setStatusTip(QCoreApplication.translate("MainWindow", u"Will connect to MongoDB Cloud if checked", None))
#endif // QT_CONFIG(statustip)
        self.radio_mongo_cloud.setText(QCoreApplication.translate("MainWindow", u"MongoDB Cloud", None))
        self.line_database.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Database", None))
        self.line_collection.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Collection", None))
        self.button_connect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Employee Information", None))
        self.line_firstname.setPlaceholderText(QCoreApplication.translate("MainWindow", u"First Name", None))
        self.line_middlename.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Middle Name", None))
        self.line_lastname.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Last Name", None))
        self.line_age.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Age", None))
        self.line_title.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Title", None))
        self.line_address1.setText("")
        self.line_address1.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Address 1", None))
        self.line_address2.setText("")
        self.line_address2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Address 2", None))
        self.line_country.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Country", None))
        self.line_misc.setText("")
        self.line_misc.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Misc Info", None))
#if QT_CONFIG(statustip)
        self.button_send.setStatusTip(QCoreApplication.translate("MainWindow", u"Send to MongoDB", None))
#endif // QT_CONFIG(statustip)
        self.button_send.setText(QCoreApplication.translate("MainWindow", u"Send", None))
#if QT_CONFIG(statustip)
        self.button_update.setStatusTip(QCoreApplication.translate("MainWindow", u"Update MongoDB", None))
#endif // QT_CONFIG(statustip)
        self.button_update.setText(QCoreApplication.translate("MainWindow", u"Update", None))
#if QT_CONFIG(statustip)
        self.button_delete.setStatusTip(QCoreApplication.translate("MainWindow", u"Delete from MongoDB", None))
#endif // QT_CONFIG(statustip)
        self.button_delete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
#if QT_CONFIG(statustip)
        self.button_query.setStatusTip(QCoreApplication.translate("MainWindow", u"Query MongoDB", None))
#endif // QT_CONFIG(statustip)
        self.button_query.setText(QCoreApplication.translate("MainWindow", u"Query DB", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Search", None))
        self.line_firstname_search.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search First Name", None))
        self.line_lastname_search.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search Last Name", None))
#if QT_CONFIG(statustip)
        self.button_search.setStatusTip(QCoreApplication.translate("MainWindow", u"Search MongoDB", None))
#endif // QT_CONFIG(statustip)
        self.button_search.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.button_import_csv.setText(QCoreApplication.translate("MainWindow", u"Import CSV", None))
        self.button_export_csv.setText(QCoreApplication.translate("MainWindow", u"Export to CSV", None))
        self.label_connection.setText(QCoreApplication.translate("MainWindow", u"MongoDB Connection Status Label", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
    # retranslateUi

