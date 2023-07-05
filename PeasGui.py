import tkinter as tk
import time
from tkinter import ttk
import subprocess
import argparse

def execute_command(command):
    # 执行命令并捕获输出
    result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
    peas_text = r''' _ __   ___  __ _ ___
| '_ \ / _ \/ _' / __|
| |_) |  __/ (_| \__ \
| .__/ \___|\__._|___/
|_| - Probe ActiveSync
'''
    # 在结果中将peas_text替换成空
    result.stdout = result.stdout.replace(peas_text, '')
    # 删除掉以Listing开头的行
    result.stdout = '\n'.join([line for line in result.stdout.split('\n') if not line.startswith('Listing')])
    # 检查命令是否成功执行
    if result.returncode == 0:
        # 返回命令的输出结果
        return result.stdout.strip().split('\n')
    else:
        # 返回错误信息
        return [result.stderr.strip()]


def expand_row(event):
    # 获取选中的行
    selected_item = treeview.focus()

    # 判断是否已经展开
    if treeview.item(selected_item, option='tags') == ('expanded',):
        # 收起行
        treeview.item(selected_item, tags=())
    else:
        # 展开行
        treeview.item(selected_item, tags=('expanded',))

def execute_selected_command(file_path):
    # print(file_path)
    exec_text = "python2 -m peas --list-unc=\'{list_unc}\' -u \'{email_user}\' -p \'{email_pass}\'  {ip}".format(
        list_unc=file_path,
        email_user=args.u,
        email_pass=args.p,
        ip=args.ip
    )
    print(peas_command)


    # 执行选中的命令
    output = execute_command(exec_text)

    # 获取选中的行
    selected_item = treeview.focus()

    # 删除子项
    children = treeview.get_children(selected_item)
    for child in children:
        treeview.delete(child)

    # 添加子项
    for line in output:
        file_data = list(filter(None, line.split(' ')))
        file_name = " ".join(file_data[5:]) #解决文件名包含空格的情况
        file_size = file_data[4]
        file_type = file_data[3]
        Creation_time = " ".join(file_data[1:2])
        Modification_time = " ".join(file_data[2:3])
        Notkonw = file_data[0]
        treeview.insert(selected_item , "end", text=file_name, values=(file_size, file_type, Creation_time, Modification_time, Notkonw, file_name))

def execute_download_command(file_name):
    exec_text = "python2 -m peas --dl-unc=\'{dl_unc}\' -o \'{output}\' -u \'{email_user}\' -p \'{email_pass}\'  {ip}".format(
        dl_unc=file_name,
        output=str(int(time.time())) + '_' + str(list(file_name.split("\\"))[-1]),
        email_user=args.u,
        email_pass=args.p,
        ip=args.ip
    )
    print(exec_text)
    # 执行选中的命令
    execute_command(exec_text)

def add_column(treeview):
    # 添加列
    treeview["columns"] = ("file_size", "file_type", "Creation_time", "Modification_time", "notknow", "path")

    # 设置列的标题
    treeview.heading("#0", text="File_Name")
    treeview.heading("file_size", text="file_size")
    treeview.heading("file_type", text="file_type")
    treeview.heading("Creation_time", text="Creation_time")
    treeview.heading("Modification_time", text="Modification_time")
    treeview.heading("notknow", text="notknow")

    # 隐藏路径列
    treeview.column("path", width=0, stretch=False)

def add_data(treeview, output):
    # 添加数据
    for line in output:
        file_data = list(filter(None, line.split(' ')))
        # print(file_data)
        file_name = " ".join(file_data[5:]) #解决文件名包含空格的情况
        file_size = file_data[4]
        file_type = file_data[3]
        Creation_time = " ".join(file_data[1:2])
        Modification_time = " ".join(file_data[2:3])
        Notkonw = file_data[0]
        treeview.insert("", "end", text=file_name, values=(file_size, file_type, Creation_time, Modification_time, Notkonw, file_name))

if __name__ == '__main__':
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", help="Email User", required=True)
    parser.add_argument("-p", help="Email Password", required=True)
    parser.add_argument("--list-unc", help="Unc List", required=True)
    parser.add_argument("-ip", help="Download UncPath", required=True)
    args = parser.parse_args()

    peas_command = "python2 -m peas --list-unc=\'{list_unc}\' -u \'{email_user}\' -p \'{email_pass}\' {ip}".format(
        list_unc=args.list_unc,
        email_user=args.u,
        email_pass=args.p,
        ip=args.ip
    )
    print(peas_command)

    # 创建窗口
    window = tk.Tk()

    # 设置窗口标题
    window.title("File Selection")

    # 设置窗口大小
    window.geometry("1620x540")

    # 执行命令
    output = execute_command(peas_command)

    # 创建Treeview
    treeview = ttk.Treeview(window)
    treeview.pack(fill="both", expand=True)


    # 添加列
    add_column(treeview)


    # 添加数据
    add_data(treeview, output)

    # 绑定展开事件
    treeview.bind("<Double-1>", expand_row)

    """
        查询目录模块
    """

    # 创建右键菜单1
    show_menu = tk.Menu(window, tearoff=False)
    show_menu.add_command(label="Execute", command=lambda: execute_selected_command(treeview.item(treeview.focus())['values'][-1]))

    def menu_exec_fuc(event):
        # 在鼠标位置显示右键菜单1
        show_menu.post(event.x_root, event.y_root)

    # 绑定右键点击事件1
    treeview.bind("<Button-3>", menu_exec_fuc)

    """
        文件下载模块
    """

    # 创建右键菜单2
    show_menu.add_command(label="Download", command=lambda: execute_download_command(treeview.item(treeview.focus())['values'][-1]))

    def menu_download_fuc(event):
        # 在鼠标位置显示右键菜单2
        show_menu.post(event.x_root, event.y_root)

    # 绑定右键点击事件2
    treeview.bind("<Button-3>", menu_download_fuc)


    def close_menu(event):
        # 关闭右键菜单
        show_menu.unpost()


    # 绑定左键点击事件
    treeview.bind("<Button-1>", close_menu)

    # 运行窗口主循环
    window.mainloop()
