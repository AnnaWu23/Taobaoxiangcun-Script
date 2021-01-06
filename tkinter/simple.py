import tkinter as tk

window = tk.Tk()

window.title('淘宝秒杀')

window.geometry('500x300')
# navigation bar
var = tk.StringVar()
var.set('欢迎~')
l = tk.Label(window, textvariable=var, bg='bisque', font=('Arial', 12), width=30, height=2)
l.pack()

# receive message
time_start = tk.Entry(window, show=None, font=('Arial', 14))
time_start.pack()

# hit button
on_hit = False
def hit_me():
    global on_hit
    if on_hit == False:
        on_hit = True
        var.set('冲鸭！！！！')
    else:
        on_hit = False
        var.set('别点了，在冲了在冲了')

b = tk.Button(window, text='开始',font=('Arial', 12), width=6, height=1, command=hit_me)
b.pack()

# 文本框
e = tk.Entry()
e.pack()

def insert_end():
    var = e.get()
    t.insert('end', var)

thought = tk.Button(window, text='发表感言', width=10, height=2, command=insert_end)
thought.pack()

t = tk.Text(window, height=3, width=40)
t.pack()


window.mainloop()