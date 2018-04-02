
import qrcode
import time
from PIL import Image

from tkinter import * 
import qrcode
import image
import webbrowser

class QRCreator:

    separator = '0x1D'
    notFound = 'NULL'
    end_of_message = 'EOT'
    null_check = str(-1)
    message = '[]>'
    message_block = ''

    def __init__(self, odometerRead, fuelEconomy, fuelLevel1,engineHours,fuelUsed,DataPlate):
        self.odometerRead = odometerRead
        self.fuelEconomy = fuelEconomy
        self.fuelLevel1 = fuelLevel1
        self.engineHours = engineHours
        self.fuelUsed = fuelUsed
        self.niin = DataPlate.niin
        self.serialNumber = DataPlate.serial_number
        niin = str(self.niin)
        self.niin_string = niin[0:9]
        self.headers = ['SN','N','VO','FU','FE','EH','FL']
        self.ends = ['','','DH','G','DHG','HR','P1']
        
        self.data = [str(self.serialNumber),self.niin_string,str(self.odometerRead),str(self.fuelUsed),str(self.fuelEconomy),str(self.engineHours),str(self.fuelLevel1)]

        

        #self.data = [str(self.odometerRead),str(self.fuelEconomy),str(self.fuelLevel1), str(self.engineHours),str(self.fuelUsed),self.niin_string,str(self.serialNumber)]

    def display(self):
        print(qrcode.constants.ERROR_CORRECT_H)
        qr = qrcode.QRCode(version=4, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)

        for x in range(0, 7):
            if self.data[x] == '-1':
                self.data[x] = self.notFound

        for x in range(0, 7):
            length = len(self.data[x])
            if x != 0:
                zero_count = 9 - length
                self.message_block = self.message_block + self.headers[x]
                for y in range(0, zero_count):
                    self.message_block = self.message_block + '0'
                self.message_block = self.message_block + self.data[x] + self.ends[x]
            else:
                zero_count = 6 - length
                self.message_block = self.message_block + self.headers[x]
                for y in range(0, zero_count):
                    self.message_block = self.message_block + '0'
                self.message_block = self.message_block + self.data[x] + self.ends[x]
            self.message = self.message + self.message_block
            if x != 6:
                self.message = self.message + self.separator
            else:
                self.message = self.message + self.end_of_message
            self.message_block = ''

        print(self.message)

        qr.add_data(self.message)
        qr.make(fit=True)

        img = qr.make_image()

        img.save("image.jpg")
        #img.show()

        filename = "image.jpg"
        webbrowser.open(filename)

        data1 = "Vehicle Odometer: " + str(self.odometerRead) + " Miles"
        data2 = "Total Engine Hours: " + str(self.engineHours) + " Hours"
        data3 = "Total Fuel Used: " + str(self.fuelUsed) + " Gallons"
        data4 = "Fuel Economy: " + str(self.fuelEconomy) + " Miles per Gallon"
        data5 = "Fuel Level 1: " + str(self.fuelLevel1) + " %"
        data6 = "Serial Number: " + str(self.serialNumber)
        data7 = "NIIN: " + self.niin_string

        totalData = data6 + '\n' + data7 + '\n' + data1 + '\n' + data2 + '\n' + data3 + '\n' + data4 + '\n' + data5

        f = open('backupinfo.txt','w')
        f.write(totalData)
        f.close()

        

class DataPlate:

    serial_number = -1
    niin = -1
    tamcn = -1
    test = -1

    def __init__(self, filename):
        self.file_name = filename

    def openFile(self):
        f = open(self.file_name)

        file_info = f.read()

        data = (file_info.splitlines())

        self.serial_number = data[1]
        
        self.niin = data[3]

        self.tamcn = data[5]

        self.test = data[7]
        

        print(self.test)

    def display(self):
        data1 = "Serial Number: " + str(self.serial_number)
        data2 = "NIIN: " + str(self.niin)
        totalData = data1 + '\n' + data2 
        root = Tk()
        root.geometry('250x150+1000+100')
        label = Label(root, text= totalData, width=40, height = 50, font=(None,15))
        label.pack()


# Class for human readable data
class TextDisplay:



    def __init__(self, odometerRead, fuelEconomy, fuelLevel1,engineHours,fuelUsed,plate):
        self.serial_number = plate.serial_number
        self.niin = plate.niin
        self.odometerRead = odometerRead
        self.fuelEconomy = fuelEconomy
        self.fuelLevel1 = fuelLevel1
        self.engineHours = engineHours
        self.fuelUsed = fuelUsed
        self.tamcn = plate.tamcn
        self.test = plate.test
        
        
  

    def display(self):
        
        Data = [str(self.serial_number), str(self.niin),str(self.tamcn),str(self.test),"","   Value:", "   " + str(self.odometerRead), "   " + str(self.engineHours), "   " + str(self.fuelUsed), "   " + str(self.fuelEconomy), "   " + str(self.fuelLevel1)]
        Labels = ["Serial Number:","NIIN:","TAMCN:","ID Number:","","Parameter:","Vehicle Odometer:","Total Engine Hours:","Total Fuel Used:","Fuel Economy:","Fuel Level 1:"]
        Units = ["","","","","","Units:","Miles","Hours","Gallons","Miles per Gallon","%"]
        height = len(Data)
        width = 3

        root = Tk()
        for i in range(height):
            for j in range(width):
                if j == 1:
                    label = Label(root, text = Data[i],font=(None,15))
                    label.grid(row=i,column =j,sticky = W)
                elif j == 2:
                    label = Label(root, text = Units[i],font=(None,15))
                    label.grid(row=i,column =j,sticky = W)
                else:
                    label = Label(root, text = Labels[i],font=(None,15))
                    label.grid(row=i,column =j,sticky = W) 
        #height = 8
        #width = 3
        root.geometry('500x350+650+350')
        #label = Label(root, text= totalData, width=150, font=(None,15))
        #label.pack()
