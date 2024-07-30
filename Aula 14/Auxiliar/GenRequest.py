import openpyxl
from win32com import client
import pythoncom
import os

class GENREQUEST:
    
    def __init__(self, dados: list):
        self.dados = list(dados)
    
    def manage_request(self):
        
        if len(self.dados[0]) == 19:
            try:
                try:
                    if self.dados[0][18] > 1:
                        iva = self.dados[0][18]/100
                    
                    else:
                        iva = self.dados[0][18]
                
                except:
                    iva = 0
                
                worksheet = openpyxl.load_workbook('Modelos/requisicao.xlsx')
                request = worksheet['Requisicao']
                
                index = 19
                request[f'C{index}'] = int(self.dados[0][1])
                request[f'D{index}'] = self.dados[0][4]
                request[f'G{index}'] = float(self.dados[0][6])
                request[f'H{index}'] = 'Un'
                request[f'I{index}'] = float(self.dados[0][7])
                request[f'K{index}'] = float(self.dados[0][8])
                request[f'L{index}'] = float(iva)
                
                request['L3'] = int(self.dados[0][1])
                request['L4'] = self.dados[0][12]
                request['L9'] = self.dados[0][14]
                request['L10'] = self.dados[0][15]
                request['L11'] = self.dados[0][16]
                request['L12'] = self.dados[0][17]
                
                request['C62'] = self.dados[0][5]
                request['C66'] = self.dados[0][13]
                request['G72'] = float(self.dados[0][8])
                request['H72'] = float(iva)
                request['I72'] = float(request['G72'].value * request['H72'].value)
                
                request['L71'] = request['G72'].value
                request['L73'] = request['L71'].value
                request['L75'] = request['I72'].value
                
                if self.dados[0][14] != '':
                    request['L8'] = 'Exmos Srs.'
                    request['C77'] = f'Obs. Requisição a {self.dados[0][14]}'
                
                else:
                    request['L8'] = ''
                    request['C77'] = ''
                
                request['L77'] = request['L73'].value + request['L75'].value
                
                path = os.path.join(os.path.expanduser('~'), 'Documents')
                file_path = os.path.abspath(os.path.join(path, 'Requisições'))
                worksheet.save(f'{file_path}/Requisição nº {self.dados[0][1]}.xlsx')
                worksheet.close()
                
                pythoncom.CoInitialize()
                try:
                    app = client.DispatchEx("Excel.Application")
                    app.Interactive = False
                    app.Visible = False
                    
                    workbook = app.Workbooks.open(f'{file_path}/Requisição nº {self.dados[0][1]}.xlsx')
                    output = os.path.splitext(f'{file_path}/Requisição nº {self.dados[0][1]}.xlsx')[0]
                    
                    workbook.ActiveSheet.ExportAsFixedFormat(0, output)
                    workbook.Close()
                    
                    os.remove(f'{file_path}/Requisição nº {self.dados[0][1]}.xlsx')
                    os.startfile(f'{file_path}/Requisição nº {self.dados[0][1]}.pdf')
                
                finally:
                    pythoncom.CoUninitialize()
                    
                return True
            
            except Exception as e:
                return e
        
        else:
            return False