#编写一个图形界面，包含两个输入框，第一个输入框是'姓名'，第二个输入框是'年龄'，校验'姓名'不能为数字，校验'年龄'必须为数字不能超过三位。包含两个提交按钮，第一个是'确认保存'，第二个是'取消' 。

import tkinter as tk
from tkinter import messagebox

def validate_name(name):
    # 校验姓名不能为数字
    if name.isdigit():
        return False
    return True

def validate_age(age):
    # 校验年龄必须为数字且不能超过三位
    if not age.isdigit() or len(age) > 3:
        return False
    return True

def save_data():
    name = name_entry.get()
    age = age_entry.get()
    
    if not validate_name(name):
        messagebox.showerror("错误", "姓名不能为数字")
        return
    
    if not validate_age(age):
        messagebox.showerror("错误", "年龄必须是数字且不能超过三位")
        return
    
    messagebox.showinfo("保存成功", f"姓名：{name}\n年龄：{age}")

def cancel():
    root.quit()

# 创建主窗口
root = tk.Tk()
root.title("数据输入")

# 创建姓名输入框
name_label = tk.Label(root, text="姓名")
name_label.pack()
name_entry = tk.Entry(root)
name_entry.pack()

# 创建年龄输入框
age_label = tk.Label(root, text="年龄")
age_label.pack()
age_entry = tk.Entry(root)
age_entry.pack()

# 创建确认保存按钮
save_button = tk.Button(root, text="确认保存", command=save_data)
save_button.pack()

# 创建取消按钮
cancel_button = tk.Button(root, text="取消", command=cancel)
cancel_button.pack()

# 运行主循环
root.mainloop()



