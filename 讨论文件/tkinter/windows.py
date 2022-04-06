from tkinter import *
#################窗口实例化######################
# 第1步，实例化object，建立窗口window
window = Tk()

# 第2步，给窗口的可视化起名字
window.title('淘宝抢购软件')

# 第3步，设定窗口的大小(长 * 宽)
window.geometry('600x400')

####################设置欢迎内容#####################
# 第4步，在图形界面上设定标签
title = Label(window, text='欢迎使用淘宝秒杀~', bg='bisque', font=('Arial', 18),width = 400, height=2)
# 说明： bg为背景，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
title.pack()
# 放置标签

Label(window, text='点击“添加商品”可批量添加商品及其相关信息', font=('Arial', 12),width = 40, height=2).place(x=45, y=60)


####################按钮########################

#开始秒杀按钮
# 第1步，创建函数功能
def addGoods():
    pass

# 第2步，在窗口界面设置放置Button按键
Button(window, text="添加商品", font=('Arial', 12), width=10, height=1, command=addGoods).place(x=400, y=66)


# 主窗口循环显示
window.mainloop()