# import modules
import sys

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QTableWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QTableWidgetItem,
)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import QDate


# App Class
class ExpenseApp(QWidget):
    def __init__(self):
        """Main App Objects & Settings"""
        super().__init__()
        self.resize(550, 500)
        self.setWindowTitle("Expense Tracker 2.0")

        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        # self.date_box.setDisplayFormat("dd-MM-yyyy")
        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()

        self.add_button = QPushButton("Add Expense")
        self.delete_button = QPushButton("Delete Expense")
        self.add_button.clicked.connect(self.add_expense)

        self.table = QTableWidget()
        self.table.setColumnCount(5)  # ID, Date, Category, Amount, Description
        header_names = ["ID", "Date", "Category", "Amount", "Description"]
        self.table.setHorizontalHeaderLabels(header_names)

        # Design App with Layouts
        self.dropdown.addItems(
            [
                "Food",
                "Transportation",
                "Rent",
                "Shopping",
                "Entertainment",
                "Bills",
                "Other",
            ]
        )

        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()

        # row1
        self.row1.addWidget(QLabel("Date:"))
        self.row1.addWidget(self.date_box)
        self.row1.addWidget(QLabel("Category:"))
        self.row1.addWidget(self.dropdown)
        # row2
        self.row2.addWidget(QLabel("Amount:"))
        self.row2.addWidget(self.amount)
        self.row2.addWidget(QLabel("Description:"))
        self.row2.addWidget(self.description)
        # row3
        self.row3.addWidget(self.add_button)
        self.row3.addWidget(self.delete_button)

        # add layout
        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        self.master_layout.addLayout(self.row3)

        self.master_layout.addWidget(self.table)

        # set layout
        self.setLayout(self.master_layout)

        self.load_table()

    def load_table(self):
        self.table.setRowCount(0)

        query = QSqlQuery("SELECT * FROM expenses")
        row = 0
        while query.next():
            expense_id = query.value(0)
            date = query.value(1)
            category = query.value(2)
            amount = query.value(3)
            description = query.value(4)

            # add values to Table
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(str(expense_id)))
            self.table.setItem(row, 1, QTableWidgetItem(date))
            self.table.setItem(row, 2, QTableWidgetItem(category))
            self.table.setItem(row, 3, QTableWidgetItem(str(amount)))
            self.table.setItem(row, 4, QTableWidgetItem(description))

            row += 1

    def add_expense(self):
        date = self.date_box.date().toString("dd-MM-yyyy")
        category = self.dropdown.currentText()
        amount = self.amount.text()
        description = self.description.text()

        query = QSqlQuery()
        query.prepare(
            """
            INSERT INTO expenses (date, category, amount, description)
            VALUES (?, ?, ?, ?)
            """
        )
        query.addBindValue(date)
        query.addBindValue(category)
        query.addBindValue(amount)
        query.addBindValue(description)
        query.exec_()

        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()

        self.load_table()


# create database
database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName("expense.db")
if not database.open():
    QMessageBox.critical(None, "Error", "Could not open your Database")
    sys.exit(1)

query = QSqlQuery()
query.exec_(
    """
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        amount REAL,
        description TEXT
    )
    """
)


# Run App
if __name__ in "__main__":
    app = QApplication([])
    main = ExpenseApp()
    main.show()
    app.exec_()
