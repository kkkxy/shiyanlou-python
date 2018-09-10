#!/usr/bin/env python3

import sys
import csv

class ArgsError(Exception):
    pass

class Args:
   
    def __init__(self, args):
        self. args = args
   
    def __parse_arg(self, arg):
        try:
            value = sys.argv[sys.argv.index(arg) + 1]
        except(ValueError, IndexError):
            value = None
        return value
   
    def get_arg(self, arg):
        value = self.__parse_arg(arg)
        if  value is None:
            raise ArgError('not found arg %s' % arg)
        return value

class SheBaoConfig:
    
    def __init__(self, file):   #file is a string 
        listconfig = self.__parse_config(file)
        self.jishulow = listconfig[0]
        self.jishuhigh= listconfig[1]
        self.totalrate = listconfig[2]
    
    def __parse_config(self, file):
        jishulow, jishuhigh, rate = 0, 0, 0
        with open(file) as f:
            for line in f:
                key, value = line.split('=')
                try:
                    key = key.strip()
                    value = float(value.strip())
                except(ValueError):
                    continue
                if key == 'JiShuL':
                    jishulow = value
                elif key == 'JiShuH':
                    jishuhigh = value 
                else:
                     rate += value
        listconfig = [jishulow, jishuhigh, rate]
        return listconfig 

class UserData:
 
    def __init__(self, file):
        self.data = self.__parse_userdata(file)
    def __parse_userdata(self, file):
        data = []
        with open(file) as f:
            for line in f:
                number, pay = line.split(',')
                data.append((number,pay))
        return data

    def __iter__(self):
        return iter(self.data)

class Calculator:
    startpoint = 3500
    tax_table = [
        (80000, 0.45, 15355),
        (55000, 0.35, 5505),
        (35000, 0.3, 2755),
        (9000, 0.25, 1005),
        (4500, 0.2, 555),
        (1500, 0.1, 105),
        (0, 0.03, 0),
    ]
    
    def __init__(self, config): #config is an example of SheBaoConfig
        self.config = config
    
    def calculate(self, data_item):
        number, pay = data_item
        pay = int(pay)
        if pay < self.config.jishulow:
            shebao = self.config.jishulow * self.config.totalrate
        elif pay > self.config.jishuhigh:
            shebao = self.config.jishuhigh * self.config.totalrate
        else:
            shebao = pay * self.config.totalrate
        leftpay = pay - shebao
        taxbase = leftpay - self.startpoint
        if taxbase < 0:
            tax = 0
        else:
            for item in self.tax_table:
                if taxbase > item[0]:
                    tax = taxbase * item[1] - item[2] 
                    break
                else:
                    continue
        lastpay = leftpay - tax
        return str(number), str(pay), '%.2f' % shebao, '%.2f' % tax, '%.2f' %lastpay

class Exporter:
    def __init__(self, file):
        self.file = file
 
    def export(self, data):     
        with open(self.file, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(data)

if __name__ == '__main__':
    args = Args(sys.argv[1:])
    config = SheBaoConfig(args.get_arg('-c'))
    userdata = UserData(args.get_arg('-d'))
    exporter = Exporter(args.get_arg('-o'))
    calculator = Calculator(config)
    
    results =[]
    for item in userdata:
        result = calculator.calculate(item)
        results.append(result)
    exporter.export(results)        



















