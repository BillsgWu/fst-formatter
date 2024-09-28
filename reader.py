# from openpyxl import load_workbook
class Reader:
    def readline(self):
        pass
class CSVReader(Reader):
    def __init__(self,file,encoding="UTF-8",sep=","):
        self.file = open(file,encoding=encoding)
        self.columnlen = None
        self.sep = sep
    def readline(self):
        raw = self.file.readline()
        if not raw:
            return None
        raw = raw.strip("\n")
        buffer = ""
        res = []
        qstat = 0
        for char in raw:
            if qstat == 0 and char == self.sep:
                res.append(buffer)
                buffer = ""
            elif qstat == 2 and char == '"':
                qstat = 0
            elif qstat == 1 and char == "'":
                qstat = 0
            elif qstat == 0 and char == '"':
                qstat = 2
            elif qstat == 0 and char == "'":
                qstat = 1
            else:
                buffer += char
        res.append(buffer)
        if not self.columnlen:
            self.columnlen = len(res)
        else:
            for i in range(max(self.columnlen-len(res),0)):
                res.append(None)
            for i in range(max(len(res)-self.columnlen,0)):
                res.pop()
        return res
    def readraw(self):
        raw = self.file.readline()
        if not raw:
            return None
        return raw
# class XLSReader(Reader):
#     pass