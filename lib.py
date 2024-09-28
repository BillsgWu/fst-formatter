from table_lib import Table
from reader import CSVReader
from writer import XLSXWriter
import logging as log
from templates import ThisTemplate
import sys
log.basicConfig(level=log.INFO,format="[%(levelname)-8s] - [%(asctime)s] : %(message)s")
logger = log.getLogger(__name__)
def scan_type(file):
    reader = CSVReader(file)
    reader.readraw()
    reader.readraw()
    dic = {}
    for i in range(3):
        mapping = reader.readraw().split(",")
        dic[eval(mapping[0])] = eval(mapping[1])
    return reader,dic
def process_file(ifile,ofile,logger):
    table = Table()
    reader,detail = scan_type(ifile)
    table.load(reader)
    wars = 0
    errs = 0
    
    # NXT: Module, Slot, Part Number, Feeder Name
    # XPF: Stage, Slot, Part Number, Feeder Name
    
    machtype = detail.get("MachineType","Unknown")
    if machtype == "NXT":
        headerkeeped = ["Module","Slot","Part Number","Feeder Name"]
    elif machtype == "XPF":
        headerkeeped = ["Stage","Slot","Part Number","Feeder Name"]
    else:
        errs += 1
        logger.error(f"Unknown Maching Type:{machtype}")
    for header in table.headers[:]:
        if not header in headerkeeped:
            table.delete_column(table.get_id_by_header(header))
    if table.headers != headerkeeped:
        wars += 1
        logger.warning(f"The file might be broken or miss some headers.")
    writer = XLSXWriter()
    writer.use_template(ThisTemplate)
    table.save(writer).workbook.save(ofile)
    return wars,errs