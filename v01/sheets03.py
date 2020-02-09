import tkinter as tk
from tkinter import filedialog

from generate_pdf import *

#-----------LOADS THE OUTPUT PATH-------------#

def loadConfig():
    file = open('config.csv','r')
    reader = csv.reader(file)
    path = ""

    for row in reader:
        if row[0]: return row[1]

    file.close()
    return ""

#########################################################################################################
#                                       GLOBAL VARIABLES                                                #
#########################################################################################################


entries = [['01','01 NOV 19','02 NOV 19','PEAR','£50',2,'1234567',100,20,120],
['01','03 NOV 19','04 NOV 19','CLOGGY','£50',2,'1234568',100,20,120],
['01','05 NOV 19','06 NOV 19','PYTHON','£50',2,'1234569',100,20,120],
['01','07 NOV 19','08 NOV 19','WEB','£50',2,'1234570',100,20,120],
['01','09 NOV 19','10 NOV 19','GLOBB','£50',2,'1234571',100,20,120]]
output_path = loadConfig()
extra_lines = []
gselected = None
PO_number = None

##########################################################################################################

captions = ['ID','Start date','End date', 'Company', 'Rate','Days', 'Invoice No','Sum','VAT','Total']

#########################################################################################################
#                                       DICTIONARY VALUES                                               #
#########################################################################################################

dd = {'lm':100,
'rm' : 100,
'bh' : 100,
'rad' : 10,
'cap_font' : 'Helvetica 10',
'cap_font_bold' : 'Helvetica 10 bold',
'txt_font' : 'Helvetica 12 bold',
'ttl_font' : 'Helvetica 20 bold',
'bttn_font' : 'Helvetica 12 bold',
'ttl_clr' : '#fa4300',
'cap_row' : 10,
'cap_color' : 'gray80',
'cap_high' : 'white',
'cap_ttl' : 'gray70',
'bgclr' : '#2e343d',
'txt_row' : 75,
'txt_clr' : 'gray40',
'rect_bg' : 'white',
'rect_int' : 'gray95',
'rect_high' : '#fac000',
'rect_mover' : '#ffe89c',
'nw': 25,
'b_high': '#41bffa',
'tk_icon' : 'invoices.ico'}

#########################################################################################################
#                                       INITIATE TK WINDOW                                              #
#########################################################################################################

root = tk.Tk()
root.geometry('1400x800+100+100')
root.iconbitmap(dd['tk_icon'])
root.title("Invoice creator")
canvas = tk.Canvas(root,width = 1400, height = 1200, bg=dd['bgclr'])
canvas.pack()


#########################################################################################################
#                                       BUTTON METHODS                                                  #
#########################################################################################################

#---------------------------------------CHANGES THE OUTPUT PATH-----------------------------------------#
def change_path():
    global output_path
    output_path = filedialog.askdirectory(initialdir=output_path)
    file = open('config.csv')
    lines = file.read().splitlines()
    lines[0] = 'Output path,' + output_path
    file.close()
    file = open('config.csv', 'w')
    file.write('\n'.join(lines))
    file.close()

#---------------------------------------SPLASH SCREEN---------------------------------------------------#

def splash(message):
    warning = tk.Toplevel(root, border = 0)

    s_w,s_h = 800,200

    parent_geo = [int(dim) for dim in root.winfo_geometry().replace('x',' ').replace('+',' ').split()]
    w,h = parent_geo[0],parent_geo[1]
    x,y = parent_geo[2],parent_geo[3]
    warning.geometry('{}x{}+{}+{}'.format(s_w,s_h,x + w//2-s_w//2,y + h//2 - s_h//2))
    warning.overrideredirect(True)
    warning.resizable(width=False, height=False)
    warning_canvas = tk.Canvas(warning,width=1400, height=1200, bg=dd['bgclr'])
    warning_canvas.pack()
    warning_canvas.bind('<Button-1>', lambda x :warning.destroy())
    x,y = warning_canvas.canvasx(400),warning_canvas.canvasx(100)

    warning_canvas.create_text(x,y, text = message, font = 'Helvetica 20 bold', fill = 'white')
    warning_canvas.create_text(x,y+85, text = 'Click to close', font = 'Helvetica 8', fill = 'white')


#---------------------------------------LOADS ADDRESSES FROM A CSV FILE--------------------------------#

def loadAddresses(): # Loads addresses from the cvs
    file = open('addresses.csv','r')
    reader = csv.reader(file)
    addresses = {}

    for row in reader:
        addresses[row[0]] = row[1::]

    file.close()
    return addresses

#---------------------------------------EVENT MANAGER FOR CANVAS---------------------------------------#

def event_manager(event, list_of_objects):

    x,y = event.x, event.y
    if event.type[0] == '6':
        for object in list_of_objects:

            bbox = object.bbox
            object.on_mouse_off()
            x1,y1,x2,y2 = bbox[0],bbox[1],bbox[2],bbox[3],
            if x1<=x<=x2 and y1<=y<=y2:

                object.on_mouse_over()
                return


    if event.type[0] == '4':

        for object in list_of_objects:

            bbox = object.bbox
            object.on_mouse_off()
            x1,y1,x2,y2 = bbox[0],bbox[1],bbox[2],bbox[3],
            if x1<=x<=x2 and y1<=y<=y2:

                object.on_click()
                return


#---------------------------------------CREATES A NICE INPUT BOX---------------------------------------#

def add_input_box(p_canvas, left, top, width, height, just='left'):
    item_entry = tk.Entry(p_canvas, font='Helvetica 18 bold', background=dd['bgclr'], borderwidth=0, foreground='white', insertbackground='white', justify=just) #dd['bgclr']
    item_window = p_canvas.create_window(left+5, top+5, anchor='nw', window=item_entry, width=width-10, height=height-10)
    round_rectangle(p_canvas, left, top, left + width, top+height, fill=dd['bgclr'], outline='', width=0)
    return item_entry

#---------------------------------------CREATES A LINE OF INPUT BOXES----------------------------------#

def add_input_line(p_canvas, left, top):
    input_line = []
    round_rectangle(p_canvas,left-5,top-5,780,top+45, fill = '#556070')
    input_line.append(add_input_box(p_canvas, left, top, 300, 40))
    input_line.append(add_input_box(p_canvas, left+520, top, 50, 40,'right'))
    p_canvas.create_text(left + 610,top+22, font = 'Helvetica 18 bold', fill = 'white', text = 'X')
    input_line.append(add_input_box(p_canvas, left + 650, top, 100, 40,'right'))
    return input_line


#---------------------------------------ADD ECTRA LINE SCREEN------------------------------------------#

def add_extra_lines_screen():
    add_extra = tk.Toplevel(root)
    add_extra.iconbitmap(dd['tk_icon'])
    add_extra.title("Add extra items")
    s_w, s_h = 800, 600

    parent_geo = [int(dim) for dim in root.winfo_geometry().replace('x', ' ').replace('+', ' ').split()]
    w, h = parent_geo[0], parent_geo[1]
    x, y = parent_geo[2], parent_geo[3]
    add_extra.geometry('{}x{}+{}+{}'.format(s_w, s_h, x + w // 2 - s_w // 2, y + h // 2 - s_h // 2))


    add_extra_canvas = tk.Canvas(add_extra, width=800, height=600, bg=dd['bgclr'])
    add_extra_canvas.pack()

    add_extra_canvas_objects = []
    x,y = add_extra_canvas.canvasx(0),add_extra_canvas.canvasy(0)

    inputs = []

    def get_lines(inputs_lst): # READS THE LINES, REMOVES EMPTY ONES
        read = [[box.get() for index,box in enumerate(line) ] for line in inputs_lst]
        read = [line for line in read if any(line)]

        read = [(line[0], int(line[1]), float(line[2])) for line in read]

        global extra_lines
        extra_lines =  read
        add_extra.destroy()

    done_button = {'text': 'Done', 'bg': '', 'fcl': 'white', 'size': 40, 'font': 'Helvetica 12 bold',
                        'callback': lambda: get_lines(inputs), 'hl': 'white', 'hlc': dd['b_high'], 'fhl': 'Helvetica 14 bold', 'fhlc': 'white', 'ftxt': 'Done'}
    add_extra_canvas_objects.append(canvas_button(add_extra_canvas,(x+300,y+500,x+500,y+550),done_button))

    add_extra_canvas.create_text(x+25,y+25, anchor = 'nw', fill = dd['cap_ttl'], font = 'Helvetica 14 bold', text = 'Items')
    add_extra_canvas.create_text(x + 25 + 520, y + 25, anchor='nw', fill=dd['cap_ttl'], font='Helvetica 14 bold', text='Units')
    add_extra_canvas.create_text(x + 25 + 650, y + 25, anchor='nw', fill=dd['cap_ttl'], font='Helvetica 14 bold', text='Price/Unit')


    for i in range(5):
        inputs.append(add_input_line(add_extra_canvas,x+25,y+75+(i*60)))



    add_extra_canvas.bind('<Button-1>', lambda event: event_manager(event, add_extra_canvas_objects) )
    add_extra_canvas.bind('<Motion>', lambda event: event_manager(event, add_extra_canvas_objects))

    return extra_lines


#----------------SCREEN THAT APPEARS AFTER GENERATE INVOICE BUTTON IS PRESSED--------------------------#

def generate_invoice_screen():
    global PO_number
    PO_number = None
    if gselected == None: # IF NO INVOICE HAS BEEN SELECTED EXIT
        splash('Please elect an invoice')
        return

#####################################################################################

    invoice_canvas_items = []

    invoice_info = tk.Toplevel(root)
    invoice_info.iconbitmap(dd['tk_icon'])
    invoice_info.title("Check the info before you proceed")

    invoice_info.geometry('1400x800+100+100')
    invoice_canvas = tk.Canvas(invoice_info,width=1400, height=1200, bg=dd['bgclr'])
    invoice_canvas.pack()

    sel = entries[gselected]
    dd['nw']=50
    header = entry_box(captions, sel, invoice_canvas)

    addresses = loadAddresses()

#------------------------------------FUNCTIONS--------------------------------------------------#

    def close_invoice_info(): # when back button is pressed
        invoice_info.destroy()

    def generate_invoice_call(): # CALLS generate_invoice() funtion from generate_pdf.py and closes the windwo
        addresses = loadAddresses()
        sel = entries[gselected]
        if sel[3] not in addresses.keys():
            splash('Please add the company address to the database')
        else:

            splash('Generating invoice')
            generate_invoice(sel,PO_number,extra_lines,output_path)
            invoice_canvas.delete('all')
            invoice_info.destroy()


    def add_address(address): # adds address of a company to the csv file
        if address:
            selected = entries[gselected]

            file = open('addresses.csv', 'a')
            file.write("\n{},{}".format(selected[3], address))
            file.close()

            splash('Addres for {} added'.format(selected[3]))

    def addPO(number): # assigns a PO number

        global PO_number
        if number !='PO NUMBER':
            PO_number = number
            splash('Purchase number {} added'.format(number))
        else: splash('Please enter a PO number')

    def add_extra_lines(): # when add custom lines is pressed
        add_extra_lines_screen()


    invoice_canvas.create_line(700,200,700,700, fill='gray50', width=1, capstyle = 'round') # Separator


    ########################################################################################################
    # ADDRESS SECTION
    ########################################################################################################

    left = 300

    invoice_canvas.create_text(left, 250, text='Address', font=dd['ttl_font'], fill = 'gray50', anchor='sw')
    invoice_canvas.create_text(left, 325, text=sel[3], font=dd['ttl_font'], fill='White', anchor='sw')

    if sel[3] in addresses.keys():


        l = 375
        for line in addresses[sel[3]]:
            invoice_canvas.create_text(left, l, text=line, font=dd['txt_font'], fill='White', anchor='sw')
            l += 25
        change_PO_button = {'text' : 'Change address', 'bg' :'', 'fcl':'white', 'size' : 40,'font' : 'Helvetica 12 bold',
            'callback' : addPO , 'hl' : 'white', 'hlc' : dd['b_high'], 'fhl' : 'Helvetica 14 bold', 'fhlc' : 'white', 'ftxt' : 'Change address'}
        invoice_canvas_items.append(canvas_button(invoice_canvas,(left,575,left+300,675),change_PO_button))
    else:

        address_entry = tk.Text(invoice_canvas, font='Helvetica 14 bold', background = dd['bgclr'], borderwidth=0, foreground = 'white',insertbackground='white')
        address_entry.insert('1.0','No address \nfor this company found')

        address_window = invoice_canvas.create_window(left+5,355,anchor = 'nw', window = address_entry, width = 295, height=200)
        round_rectangle(invoice_canvas, left, 350, left+300, 555, fill='', outline='white', width=1)

        add_address_button = {'text': 'Add address', 'bg': '', 'fcl': 'white', 'size': 40, 'font': 'Helvetica 12 bold',
                              'callback': lambda : add_address(address_entry.get('1.0','end-1c')), 'hl': 'white', 'hlc': dd['b_high'], 'fhl': 'Helvetica 14 bold', 'fhlc': 'white', 'ftxt': 'Add address'}
        invoice_canvas_items.append(canvas_button(invoice_canvas,(left,575,left+300,675),add_address_button))




    ########################################################################################################
    # ADD PO SECTION
    ########################################################################################################

    right = 800 # Alignment value

    # SECTION TITLE
    invoice_canvas.create_text(right, 250, text='Purchase order', font=dd['ttl_font'], fill='gray50', anchor='sw')

    # ENTRY BOX
    PO_entry = tk.Entry(invoice_canvas, font='Helvetica 22 bold', background=dd['bgclr'], borderwidth=0, foreground='white', justify='center', text='PO NUMBER')
    PO_entry.delete(0,'end')
    PO_entry.insert('0', 'PO NUMBER')

    PO_window = invoice_canvas.create_window(right + 5, 355, anchor='nw', window=PO_entry, width=290, height=50)
    round_rectangle(invoice_canvas, right, 350, right + 300, 410, fill='', outline='white', width=1)
    #


    # ADD PO BUTTON
    add_po_button = {'text' : 'Add PO', 'bg' :'', 'fcl':'white', 'size' : 40,'font' : 'Helvetica 12 bold',
            'callback' : lambda: addPO(PO_entry.get()) , 'hl' : 'white', 'hlc' : dd['b_high'], 'fhl' : 'Helvetica 14 bold', 'fhlc' : 'white', 'ftxt' : 'Add PO'}
    invoice_canvas_items.append(canvas_button(invoice_canvas, (right, 575, right+300, 675), add_po_button))



    # ADD EXTRA LINES
    add_line_button = {'text': 'Add custom lines', 'bg': '', 'fcl': 'white', 'size': 40, 'font': 'Helvetica 12 bold',
                     'callback': add_extra_lines, 'hl': 'white', 'hlc': dd['b_high'], 'fhl': 'Helvetica 14 bold', 'fhlc': 'white', 'ftxt': 'Add custom lines'}
    invoice_canvas_items.append(canvas_button(invoice_canvas, (left,700,right+300,750),add_line_button))
    #

    ########################################################################################################
    # BACK AND NEXT BUTTONS
    ########################################################################################################

    next_button = {'text': 'Next', 'bg': '', 'fcl': 'white', 'size': 40, 'font': 'Helvetica 12 bold',
                       'callback': generate_invoice_call, 'hl': 'white', 'hlc': dd['b_high'], 'fhl': 'Helvetica 14 bold', 'fhlc': 'white', 'ftxt': 'Next'}
    invoice_canvas_items.append(canvas_button(invoice_canvas,(right+400,350,right+500,400),next_button))
    back_button = {'text': 'Back', 'bg': '', 'fcl': 'white', 'size': 40, 'font': 'Helvetica 12 bold',
                   'callback': close_invoice_info, 'hl': 'white', 'hlc': dd['b_high'], 'fhl': 'Helvetica 14 bold', 'fhlc': 'white', 'ftxt': 'Back'}
    invoice_canvas_items.append(canvas_button(invoice_canvas, (100, 350, 200, 400), back_button))

    #########################################################################################################
    # BINDINGS
    #########################################################################################################

    invoice_canvas.bind('<Motion>', lambda event: event_manager(event,invoice_canvas_items))
    invoice_canvas.bind('<Button-1>', lambda event: event_manager(event, invoice_canvas_items))

#--------------------------------DRAWS A ROUNDED RECTANGLE-------------------------------------#
def round_rectangle(p_canvas,x1, y1, x2, y2, radius=10, **kwargs):
    points = [x1+radius, y1,x1+radius, y1,x2-radius, y1,x2-radius, y1,x2, y1,x2, y1+radius,x2, y1+radius,x2, y2-radius,x2, y2-radius,x2, y2,
    x2 - radius, y2,x2-radius, y2,x2-radius, y2,x2-radius, y2,x1+radius, y2,x1+radius, y2,x1, y2,x1, y2-radius,x1, y2-radius,x1, y1+radius,x1, y1+radius,x1, y1]
    return p_canvas.create_polygon(points, **kwargs, smooth=True)




def select(index):
    global selected
    selected = index
#############################################################################################################
#
#                                      CLASSES GFX ELEMENTS
#
#############################################################################################################




#############################################################################################################
#                   THIS ONE DISPLAYS INVOICE DATA ON THE FIRST PAGE
#############################################################################################################

class entry_box:

    def __init__(self,captions,entry,p_canvas):
        f = ['{}']*7 + ['£{:.0f}']*3
        self.canvas = p_canvas

        self.col = [dd['lm']+20,dd['lm']+75,dd['lm']+200,dd['lm']+325,dd['lm']+525,dd['lm']+600,dd['lm']+700,dd['lm']+825,dd['lm']+950,dd['lm']+1075]
        self.cap_size = [dd['cap_font']] *9 + [dd['cap_font_bold']]
        self.cap_clr = [dd['cap_color']] * 9 + [dd['cap_ttl']]
        self.clr = [dd['txt_clr']] * 9 + [dd['ttl_clr']]
        self.size = [dd['txt_font']] * 9 + [dd['ttl_font']]
        self.static_background = round_rectangle(p_canvas,dd['lm'], dd['nw'], 1300, dd['nw'] + 100, fill=dd['rect_int'])
        self.dynamic_background = p_canvas.create_rectangle(self.col[1] - 15, dd['nw'], self.col[-1] - 25, dd['nw'] + 100, fill=dd['rect_bg'], width=0)
        self.cap_list = [p_canvas.create_text(self.col[i], dd['nw'] + dd['cap_row'], anchor='nw', font=self.cap_size[i], text=cap,
                                       fill=self.cap_clr[i]) for i, cap in enumerate(captions)]

        self.data_list = [
            p_canvas.create_text(self.col[i], dd['nw'] + dd['txt_row'], anchor='sw', font=self.size[i], text=f[i].format(data), fill=self.clr[i]) for
            i, data in enumerate(entry)]
        self.bbox = (dd['lm'], dd['nw'], 1300, dd['nw'] + 100)
        self.callback = select
    def cap_style(self, color, font):
        for cap in self.cap_list[1:-1]:
            self.canvas.itemconfig(cap, fill = color, font = font)

    def entry_highlight(self, color):
        self.canvas.itemconfig(self.dynamic_background, fill = color)

    def remove_highlight(self):
        self.entry_highlight(dd['rect_bg'])
        self.cap_style(dd['cap_color'], dd['cap_font'])

    def mover(self, color):
        self.canvas.itemconfig(self.dynamic_background, fill = color)

#BUTTONS DECRIPTION

buttons = [{'text' : 'Invoices saved in: {}'.format(output_path), 'bg' :'#2e343d', 'fcl':'white', 'size' : 40,'font' : 'Helvetica 12 bold',
            'callback' : change_path , 'hl' : 'white', 'hlc' : dd['rect_mover'], 'fhl' : 'Helvetica 14 bold', 'fhlc' : '#ff9500', 'ftxt' : 'Change output path'},
{'text' : 'Generate invoice', 'bg' : '#2e343d', 'fcl':'white', 'size' : 60,'font' : 'Helvetica 20 bold',
            'callback' : generate_invoice_screen , 'hl' : '#aee887', 'hlc' : '#aee887','fhl' : 'Helvetica 22 bold', 'fhlc' : 'white','ftxt' : 'Generate invoice'}]


#############################################################################################################
#                   THIS ONE DISPLAYS A BUTTON ON THE CANVAS
#############################################################################################################

class canvas_button:

    def __init__(self,p_canvas,bbox, setup):
        self.canvas = p_canvas
        self.bgcolor = {'norm' : setup ['bg'], 'high' : setup ['hlc']}
        self.txtcolor = {'norm' : setup['fcl'], 'high' : setup['fhlc']}
        self.font = {'norm' : setup['font'],'high' : setup['fhl']}
        self.message = {'norm' : setup['text'], 'high':setup['ftxt']}
        x,y,xx,yy = bbox[0],bbox[1],bbox[2],bbox[3]


        self.dynamic_background = round_rectangle(p_canvas,x,y, xx, yy, fill=self.bgcolor['norm'], width=1, outline='white' )

        self.cap_list = [p_canvas.create_text((x+xx)/2,(y+yy)/2, font=self.font['norm'], text=self.message['norm'], fill=self.txtcolor['norm'])]
        self.bbox = bbox

        self.on_click = setup['callback']



    def on_click(self, color):
        self.on_click()


    def on_mouse_over(self):
        self.canvas.itemconfig(self.dynamic_background, fill=self.bgcolor['high'])
        self.canvas.itemconfig(self.cap_list[0], fill=self.txtcolor['high'], text=self.message['high'], font=self.font['high'])

    def on_mouse_off(self):
        self.canvas.itemconfig(self.dynamic_background, fill = self.bgcolor['norm'])
        self.canvas.itemconfig(self.cap_list[0], fill=self.txtcolor['norm'], text = self.message['norm'],font = self.font['norm'])

#############################################################################################################
#                   THIS ONE DISPLAYS A BUTTON THAT UPDATES IT'S TEXT
#############################################################################################################

class active_button:

    def __init__(self,p_canvas,title):
        self.canvas = p_canvas
        self.bgcolor = {'norm' : title['bg'], 'high' : title['hlc']}
        self.txtcolor = {'norm' : title['fcl'], 'high' : title['fhlc']}
        self.font = {'norm' : title['font'],'high' : title['fhl']}
        self.message = {'norm' : title['text'], 'high':title['ftxt']}



        self.dynamic_background = round_rectangle(p_canvas,dd['lm'], dd['nw'], 1300, dd['nw'] + title['size'], fill=self.bgcolor['norm'], width=1, outline='white' )

        self.cap_list = [p_canvas.create_text(650,dd['nw'] + title['size']/2, font=self.font['norm'], text=self.message['norm'], fill=self.txtcolor['norm'])]
        self.bbox = (dd['lm'], dd['nw'], 1300, dd['nw'] + title['size'])
        dd['nw'] += title['size']
        self.callback = title['callback']
        self.update = False

    def cap_style(self, color, font):
        for cap in self.cap_list[1:-1]:
            self.canvas.itemconfig(cap, fill = color, font = font)

    def entry_highlight(self, color):
        self.canvas.itemconfig(self.dynamic_background, fill = color)

    def update_f(self):

        self.message['norm'] = 'Invoices saved in: {}'.format(output_path)

        self.canvas.itemconfig(self.cap_list[0], fill=self.txtcolor['norm'], text=self.message['norm'], font=self.font['norm'])

    def on_click(self):
        self.callback()

        if self.update:
            self.update_f()

    def mover(self,color):
        self.canvas.itemconfig(self.dynamic_background, fill=self.bgcolor['high'])
        self.canvas.itemconfig(self.cap_list[0], fill=self.txtcolor['high'], text=self.message['high'], font=self.font['high'])

    def remove_highlight(self):
        self.canvas.itemconfig(self.dynamic_background, fill = self.bgcolor['norm'])
        self.canvas.itemconfig(self.cap_list[0], fill=self.txtcolor['norm'], text = self.message['norm'],font = self.font['norm'])






#############################################################################################################
#                  DRAWS THE FIRST PAGE
#############################################################################################################



def draw_all_entries(entries, buttons):
    entries_list = []
    for entry in entries:
        entries_list.append(entry_box(captions,entry,canvas))
        dd['nw'] += 125

    dd['nw'] += 10
    for button in buttons:
        entries_list.append(active_button(canvas,button))
        dd['nw'] += 10

    entries_list[-2].update = True


    return entries_list

#############################################################################################################
#                  EVENT MANAGER FOR THE FIRST PAGE HAS EXTRA OPTION FOR SELECTION
#############################################################################################################

def register_click(event, display_list):
    x,y = event.x,event.y
    global gselected
    selected = None

    for index,object in enumerate(display_list):
        x1,y1,x2,y2 = object.bbox[0],object.bbox[1],object.bbox[2],object.bbox[3]
        if  x1 <= x <= x2 and y1 <= y <= y2:

            if gselected == index:
                object.remove_highlight()
                gselected = None

                return
            selected = index
            if index in range(5): gselected = selected
            break
    if selected in range(5):
        for object in display_list[0:5]:
            object.entry_highlight(dd['rect_bg'])
            object.cap_style(dd['cap_color'], dd['cap_font'])
        object = display_list[selected]
        object.entry_highlight(dd['rect_high'])
        object.cap_style(dd['cap_high'], dd['cap_font_bold'])

    elif selected != None:
        for object in display_list[5::]:
            object.remove_highlight()
        object = display_list[selected]
        object.entry_highlight(dd['rect_high'])
        #object.callback()
        object.on_click()
        object.remove_highlight()

#############################################################################################################
#                  EVENT MANAGER FOR THE FIRST PAGE JUST FOR MOUSE MOVEMENT AND HIGHLIGHTS
#############################################################################################################

def register_mover(event,display_list):

    x, y = event.x, event.y
    for index,object in enumerate(display_list):
        if index == gselected: continue
        object.remove_highlight()


    for index,object in enumerate(display_list):
        x1, y1, x2, y2 = object.bbox[0], object.bbox[1], object.bbox[2], object.bbox[3]

        if x1 <= x <= x2 and y1 <= y <= y2:
            if index == gselected: continue
            object.mover(dd['rect_mover'])








#############################################################################################################
#                  HOLDS ALL OBJECTS OF THE MAIN PAGE
#############################################################################################################

display_list = draw_all_entries(entries, buttons) #+ draw_button(buttons)

#############################################################################################################
#                  BINDINGS FOR THE FIRST PAGE
#############################################################################################################

canvas.bind('<Button-1>', lambda event: register_click(event,display_list))
canvas.bind('<Motion>', lambda event: register_mover(event,display_list))



tk.mainloop()