import tkinter as tk
import tkinter.ttk as ttk
import datetime as da
import calendar as ca
import pymysql
from tkinter import *
from tkinter import messagebox, ttk

WEEK = ['日', '月', '火', '水', '木', '金', '土']
WEEK_COLOUR = ['red', 'black', 'black', 'black','black', 'black', 'blue']

#------------------------------------------------------------------
# 予定種別を取得
#
# actions = ('学校','試験', '課題', '行事', '就活', 'アルバイト','旅行')
connection = pymysql.connect(host='127.0.0.1',
                            user='root',
                            password='',
                            db='apr01',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
# トランザクション開始
connection.begin()
with connection.cursor() as cursor:
  cursor = connection.cursor()

  # クエリの作成
  sql = 'select category_name from categories'

  # クエリの実行
  cursor.execute(sql)

  # 実行結果の受け取り
  results = cursor.fetchall()

  # 実行結果をリストに格納
  actions = []
  for row in results:
    actions.append(row['category_name'])
# トランザクション終了
connection.close()



#-----------------------------------
# ログイン機能
#
class LetsLogin:

  def __init__(self, root):
    self.createWidget(root)

  def createWidget(self, root):
    self.root = root
    self.root.title("ログイン")
    frame1 = ttk.Frame(self.root, padding=(20))
    frame1.grid()

    # infoラベル
    self.lbl_info = ttk.Label(frame1, text='ユーザー名とパスワードを入力してください。')
    self.lbl_info.grid(row=0, column=0, pady=15, columnspan=2)

    # ユーザー名ラベル
    self.lbl_UserName = ttk.Label(frame1, text='ユーザー名', padding=(10, 2))
    self.lbl_UserName.grid()

    # ユーザー名エントリ
    self.username = StringVar()
    self.username_entry = ttk.Entry(frame1, textvariable=self.username, width=30)
    self.username_entry.grid(row=1, column=1)

    # パスワードラベル
    lbl_Password = ttk.Label(frame1, text='パスワード', padding=(10, 2))
    lbl_Password.grid(row=2, column=0, pady=2)

    # パスワードエントリ
    self.password = StringVar()
    self.password_entry = ttk.Entry(frame1, textvariable=self.password, width=30, show='*')
    self.password_entry.grid(row=2, column=1, pady=2)

    # ログインボタン
    btn_login = ttk.Button(frame1, text='ログイン', command=lambda:self.Login())
    btn_login.grid(row=3, column=0, pady=3, columnspan=2)

    # 新規登録ボタン
    btn_register = ttk.Button(frame1, text='新規登録', command=lambda:self.SignUp())
    btn_register.grid(row=4, column=0, pady=1, columnspan=2)

    self.root.mainloop()


  #--------------------------------------------------------------
  # 新規登録
  #
  def SignUp(self):

    # 入力された情報をエントリから取得
    in_UserName = self.username_entry.get()
    in_PassWord = self.password_entry.get()
    if self.CheckForSignUp(in_UserName) == True:

      # DBに保存
      connection = pymysql.connect(host='127.0.0.1',
                                user='root',
                                password='',
                                db='apr01',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
      connection.begin()
      with connection.cursor() as cursor:
        cursor = connection.cursor()
        record_data = [(in_UserName, in_PassWord)]
        cursor.executemany("insert into users(user_name, password) values(%s, %s)", record_data)
      connection.commit()
      connection.close()

      self.lbl_info['text'] = '登録成功。ログインしてください。'

    else:
      self.lbl_info['text'] = 'このユーザー名は使われています。'


  #--------------------------------------------------------------
  # データベースに検索してユーザー名の重複チェック
  #
  def CheckForSignUp(self, user_name):

    # DB接続のための情報定義
    connection = pymysql.connect(host='127.0.0.1',
                                user='root',
                                password='',
                                db='apr01',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    # トランザクション開始
    connection.begin()
    with connection.cursor() as cursor:
      cursor = connection.cursor()

    # クエリの作成
    sql = 'select * from users where user_name = \'{}\''.format(user_name)

    # クエリの実行
    cursor.execute(sql)

    # 実行結果の受け取り
    result = cursor.fetchall()

    if result == ():
      return True
    else:
      return False


  #--------------------------------------------------------------
  # ログイン実行
  #
  def Login(self):

    # 入力された情報をエントリから取得
    in_UserName = self.username_entry.get()
    in_PassWord = self.password_entry.get()

    # 認証結果をinfoラベルに表示
    CertResult = self.CheckForLogin(in_UserName, in_PassWord)
    if CertResult == 'WrongPassword':
      self.lbl_info['text'] = 'パスワードが違います。'
    elif CertResult == 'NotExist':
      self.lbl_info['text'] = 'アカウントが存在しません'
    else:
      self.lbl_info['text'] = 'ログイン成功'
      self.root.destroy()
      print(CertResult)
      self.CertResult = CertResult


  #--------------------------------------------------------------
  # データベースに問い合わせ認証を行う
  def CheckForLogin(self, in_username, in_password):

    # DB接続のための情報定義
    connection = pymysql.connect(host='127.0.0.1',
                                user='root',
                                password='',
                                db='apr01',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    # トランザクション開始
    connection.begin()
    with connection.cursor() as cursor:
      cursor = connection.cursor()

      # クエリの作成
      sql = 'select * from users where user_name = \'{}\''.format(in_username)

      # クエリの実行
      cursor.execute(sql)

      # 実行結果の受け取り
      result = cursor.fetchall()

      # ユーザ認証
      if result == ():
        return 'NotExist'
      else:
        result = result[0]
        if in_username == result['user_name'] and in_password == result['password']:
          user_id = result['user_id']
          user_name = result['user_name']
          return user_id, user_name
        else:
          return 'WrongPassword'

    # トランザクション終了
    connection.close()


#-----------------------------------------------------------------
# メインアプリ
#
class YicDiary:
  def __init__(self, root, usr_info):
    root.title('予定管理アプリ')
    root.geometry('520x280')
    root.resizable(0, 0)
    root.grid_columnconfigure((0, 1), weight=1)
    self.sub_win = None

    self.year  = da.date.today().year
    self.mon = da.date.today().month
    self.today = da.date.today().day

    self.user_id = usr_info[0]
    self.user_name = usr_info[1]

    self.title = None
    # 左側のカレンダー部分
    leftFrame = tk.Frame(root)
    leftFrame.grid(row=0, column=0)
    self.leftBuild(leftFrame)

    # 右側の予定管理部分
    rightFrame = tk.Frame(root)
    rightFrame.grid(row=0, column=1)
    self.rightBuild(rightFrame)

    # カレンダー下にログイン中ユーザー表示
    lbl_LoginUser = tk.Label(root, text = '{} がログイン中'.format(self.user_name), font=('', 12))
    lbl_LoginUser['foreground'] = 'green'
    lbl_LoginUser.place(x=40, y=200)


  #-----------------------------------------------------------------
  # アプリの左側の領域を作成する
  #
  # leftFrame: 左側のフレーム
  def leftBuild(self, leftFrame):
    self.viewLabel = tk.Label(leftFrame, font=('', 10))
    beforButton = tk.Button(leftFrame, text='＜', font=('', 10), command=lambda:self.disp(-1))
    nextButton = tk.Button(leftFrame, text='＞', font=('', 10), command=lambda:self.disp(1))

    self.viewLabel.grid(row=0, column=1, pady=10, padx=10)
    beforButton.grid(row=0, column=0, pady=10, padx=10)
    nextButton.grid(row=0, column=2, pady=10, padx=10)

    self.calendar = tk.Frame(leftFrame)
    self.calendar.grid(row=1, column=0, columnspan=3)
    self.disp(0)


  #-----------------------------------------------------------------
  # アプリの右側の領域を作成する
  #
  # rightFrame: 右側のフレーム
  def rightBuild(self, rightFrame):
    r1_frame = tk.Frame(rightFrame)
    r1_frame.grid(row=0, column=0, pady=10)

    temp = '{}年{}月{}日の予定'.format(self.year, self.mon, self.today)
    self.title = tk.Label(r1_frame, text=temp, font=('', 12))
    self.title.grid(row=0, column=0, padx=20)

    button = tk.Button(rightFrame, text='追加', command=lambda:self.add())
    button.grid(row=0, column=1)

    self.r2_frame = tk.Frame(rightFrame)
    self.r2_frame.grid(row=1, column=0)

    self.schedule()


  #-----------------------------------------------------------------
  # アプリの右側の領域に予定を表示する
  #
  def schedule(self):
    # ウィジットを廃棄
    for widget in self.r2_frame.winfo_children():
      widget.destroy()

    # データベースに予定の問い合わせを行う
    pass


  #-----------------------------------------------------------------
  # カレンダーを表示する
  #
  # argv: -1 = 前月
  #        0 = 今月（起動時のみ）
  #        1 = 次月
  def disp(self, argv):
    self.mon = self.mon + argv
    if self.mon < 1:
      self.mon, self.year = 12, self.year - 1
    elif self.mon > 12:
      self.mon, self.year = 1, self.year + 1

    self.viewLabel['text'] = '{}年{}月'.format(self.year, self.mon)

    cal = ca.Calendar(firstweekday=6)
    cal = cal.monthdayscalendar(self.year, self.mon)

    # ウィジットを廃棄
    for widget in self.calendar.winfo_children():
      widget.destroy()

    # 見出し行
    r = 0
    for i, x in enumerate(WEEK):
      label_day = tk.Label(self.calendar, text=x, font=('', 10), width=3, fg=WEEK_COLOUR[i])
      label_day.grid(row=r, column=i, pady=1)

    # カレンダー本体
    r = 1
    for week in cal:
      for i, day in enumerate(week):
        if day == 0: day = ' '
        label_day = tk.Label(self.calendar, text=day, font=('', 10), fg=WEEK_COLOUR[i], borderwidth=1)
        if (da.date.today().year, da.date.today().month, da.date.today().day) == (self.year, self.mon, day):
          label_day['relief'] = 'solid'
        label_day.bind('<Button-1>', self.click)
        label_day.grid(row=r, column=i, padx=2, pady=1)
      r = r + 1

    # 画面右側の表示を変更
    if self.title is not None:
      self.today = 1
      self.title['text'] = '{}年{}月{}日の予定'.format(self.year, self.mon, self.today)


  #-----------------------------------------------------------------
  # 予定を追加したときに呼び出されるメソッド
  #
  def add(self):
    if self.sub_win == None or not self.sub_win.winfo_exists():
      self.sub_win = tk.Toplevel()
      self.sub_win.geometry("300x300")
      self.sub_win.resizable(0, 0)

      # ラベル
      sb1_frame = tk.Frame(self.sub_win)
      sb1_frame.grid(row=0, column=0)
      temp = '{}年{}月{}日　追加する予定'.format(self.year, self.mon, self.today)
      title = tk.Label(sb1_frame, text=temp, font=('', 12))
      title.grid(row=0, column=0)

      # 予定種別（コンボボックス）###########################
      sb2_frame = tk.Frame(self.sub_win)
      sb2_frame.grid(row=1, column=0)
      label_1 = tk.Label(sb2_frame, text='種別 : 　', font=('', 10))
      label_1.grid(row=0, column=0, sticky=tk.W)
      self.combo = ttk.Combobox(sb2_frame, state='readonly', values=actions)
      self.combo.current(0)
      self.combo.grid(row=0, column=1)

      # テキストエリア（垂直スクロール付）\###########################
      sb3_frame = tk.Frame(self.sub_win)
      sb3_frame.grid(row=2, column=0)
      self.text = tk.Text(sb3_frame, width=40, height=15)
      self.text.grid(row=0, column=0)
      scroll_v = tk.Scrollbar(sb3_frame, orient=tk.VERTICAL, command=self.text.yview)
      scroll_v.grid(row=0, column=1, sticky=tk.N+tk.S)
      self.text["yscrollcommand"] = scroll_v.set

      # 保存ボタン
      sb4_frame = tk.Frame(self.sub_win)
      sb4_frame.grid(row=3, column=0, sticky=tk.NE)
      button = tk.Button(sb4_frame, text='保存', command=lambda:self.done())
      button.pack(padx=10, pady=10)
    elif self.sub_win != None and self.sub_win.winfo_exists():
      self.sub_win.lift()


  #-----------------------------------------------------------------
  # 予定追加ウィンドウで「保存」を押したときに呼び出されるメソッド
  #
  def done(self):
	# 日付
    days = '{}-{}-{}'.format(self.year, self.mon, self.today)
    print(days)

	# 種別
    category = self.combo.get()
    print(category)
	# ID化 (学校','試験', '課題', '行事', '就活', 'アルバイト','旅行) →1, 2, 3, 4, 5, 6, 7
    def getkey(category):
      if category == '学校':
        return 1
      elif category == '試験':
        return 2
      elif category == '課題':
        return 3
      elif category == '行事':
        return 4
      elif category == '就活':
        return 5
      elif category == 'アルバイト':
        return 6
      elif category == '旅行':
        return 7

    category_id = getkey(category)



	# 予定
    schedule = self.text.get('1.0', 'end-1c')
    print(schedule)


    connection = pymysql.connect(host='127.0.0.1',
                                user='root',
                                password='',
                                db='apr01',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    try:
  # トランザクション開始
      connection.begin()

      with connection.cursor() as cursor:
        cursor = connection.cursor()

        # データベースに保存
        record_data = [(self.user_id, category_id, days, schedule)]
        cursor.executemany("insert into schedules(user_id, category_id, days, schedule) values(%s, %s, %s, %s)", record_data)

      connection.commit()

    #except:
      #print('error')

    finally:
      connection.close()

    self.sub_win.destroy()



  #-----------------------------------------------------------------
  # 日付をクリックした際に呼びだされるメソッド（コールバック関数）
  #
  # event: 左クリックイベント <Button-1>
  def click(self, event):
    day = event.widget['text']
    if day != ' ':
      self.title['text'] = '{}年{}月{}日の予定'.format(self.year, self.mon, day)
      self.today = day

    #-----------------------------
    # 右側にその日の予定を表示
    #
    # 種別IDから種類を取得するgetCategory()
    def getCategory(category_id):
      if category_id == 1:
        return '学校'
      elif category_id == 2:
        return '試験'
      elif category_id == 3:
        return '課題'
      elif category_id == 4:
        return '行事'
      elif category_id == 5:
        return '就活'
      elif category_id == 6:
        return 'アルバイト'
      elif category_id == 7:
        return '旅行'

    #-----------------------------
    #
    # ユーザーIDからユーザー名を取得
    def getUserName(user_id):
      connection = pymysql.connect(host='127.0.0.1',
                                  user='root',
                                  password='',
                                  db='apr01',
                                  charset='utf8mb4',
                                  cursorclass=pymysql.cursors.DictCursor)
      connection.begin()
      with connection.cursor() as cursor:
        cursor = connection.cursor()
        sql = 'select user_name from users where user_id = {}'.format(user_id)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
          return row['user_name']

    # 表示済みの予定を削除
    lbl_schedule = tk.Label(text = '予定なし　　　　　　　　　　　　　　　　　　\n\n\n\n\n\n\n\n\n')
    lbl_schedule.place(x=260, y=120)

    # DB接続のための情報定義
    connection = pymysql.connect(host='127.0.0.1',
                                user='root',
                                password='',
                                db='apr01',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    # トランザクション開始
    connection.begin()
    with connection.cursor() as cursor:
      cursor = connection.cursor()

      # クエリの作成
      sql = 'select * from schedules where days = \'{}-{}-{}\''.format(self.year, self.mon, day)

      # クエリの実行
      cursor.execute(sql)

      # 実行結果の受け取り
      results = cursor.fetchall()
      # 実行結果の編集
      for i, row in enumerate(results):
        text = '{}の予定\n種類:{}   『{}』\n'.format(getUserName(row['user_id']), getCategory(row['category_id']), row['schedule'])
        # ラベルに予定を表示
        lbl_schedule = tk.Label(text = text)
        lbl_schedule.place(x=260, y=120+i*40)

    # トランザクション終了
    connection.close()


def Main():
  root = tk.Tk()
  logined = LetsLogin(root)
  user_info = logined.CertResult
  root = tk.Tk()
  YicDiary(root, user_info)
  root.mainloop()

if __name__ == '__main__':
  Main()
