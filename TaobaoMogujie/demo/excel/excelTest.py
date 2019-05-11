import xlrd
import xlwt

file = 'orders.xls'
row_list = []
res_list = []

def read_excel():
    wb = xlrd.open_workbook(filename=file)#打开文件
    print(wb.sheet_names())#获取所有表格名字

    sheet1 = wb.sheet_by_index(0)#通过索引获取表格
    print(sheet1.name,'   行数：', sheet1.nrows, '   列数：',sheet1.ncols)
    # 获取行数
    nrows = sheet1.nrows
    # 获取列数
    ncols = sheet1.ncols
    print ('nrows: ', nrows, ' ncols: ', ncols)
    #print(sheet1.row(1)[0].value)

    # 获取各行数据
    for i in range(1, nrows):
        row_data = sheet1.row(i)[0].value
        row_list.append(row_data)
        res_list.append('sf:89000')

    for row_data in row_list:
       print ('orid:', row_data)

#设置表格样式
def set_style(name,height,bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

#写Excel
def write_excel():
    f = xlwt.Workbook()
    sheet1 = f.add_sheet('结果',cell_overwrite_ok=True)
    row0 = ["订单ID","物流"]
    #写第一行
    for i in range(0,len(row0)):
        sheet1.write(0,i,row0[i],set_style('Times New Roman',220,True))
    #写数据
    for i in range(0, len(row_list)):
        sheet1.write(i+1, 0, row_list[i])
        sheet1.write(i+1, 1, res_list[i])
    f.save('orders_res.xls')

if __name__ == '__main__':
    read_excel()
    write_excel()