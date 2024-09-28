from reader import Reader
from writer import Writer
class Table:
    def __init__(self):
        self.table = []
        self.headers = []
    def load(self,reader:Reader):
        self.table = []
        self.headers = reader.readline()
        temp = reader.readline()
        while temp:
            self.table.append(temp)
            temp = reader.readline()
    def __init__(self):
        self.table = []
        self.headers = []
    def get_id_by_header(self,header):
        try:
            return self.headers.index(header)
        except ValueError:
            return -1
    def get_header_by_id(self,id):
        try:
            return self.headers[id]
        except:
            return None
    def add_new_column(self,header,initval=""):
        self.table = [column + [initval] for column in self.table]
        self.headers.append(header)
    def add_new_row(self,values):
        self.table.append(values)
    def alter(self,columnid1,columnid2):
        for column in range(len(self.table)):
            temp = self.table[column][columnid1]
            self.table[column][columnid1] = self.table[column][columnid2]
            self.table[column][columnid2] = temp
        temp = self.headers[columnid1]
        self.headers[columnid1] = self.headers[columnid2]
        self.headers[columnid2] = temp
    def swap(self,rowid1,rowid2):
        temp = self.table[rowid1]
        self.table[rowid1] = self.table[rowid2]
        self.table[rowid2] = temp
    def delete_row(self,rowid):
        self.table.pop(rowid)
    def delete_column(self,columnid):
        self.headers.pop(columnid)
        for row in range(len(self.table)):
            self.table[row].pop(columnid)
    def save(self,writer:Writer):
        writer.writeline(self.headers)
        for column in self.table:
            writer.writeline(column)
        return writer