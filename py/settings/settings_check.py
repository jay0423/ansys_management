from . import settings
import os
import sys
import platform
import pprint


SLASH = os.path.normcase("a/")[-1]


### settings.pyのチェック

def dir_ignore():
    pass


def path_file_name():
    pass


def file_extension():
    pass


def abbrebiation():
    pass

def dir_ignore():
    pass

def omission():
    pass


def dir_structure():
    DIR_STRUCTURE = settings.DIR_STRUCTURE
    for dir in DIR_STRUCTURE:
        if SLASH not in dir: # スラッシュがwindowsまたはmacに対応していない場合．
            print("Settings error: DIR_STRUCTUREのスラッシュが'{}'になっていません．".format(SLASH))
            sys.exit()
        if dir[-1] != SLASH:
            print("Settings error: DIR_STRUCTUREのパスの最後にスラッシュを入れてください．")
            sys.exit()
        
    if len(DIR_STRUCTURE) > 1:
        # if DIR_STRUCTURE[0] != sorted(DIR_STRUCTURE)[0]: # 書き順
        #     print("Settings error: DIR_STRUCTUREの順番を入れ替えてください．")
        #     sys.exit()
        
        dir_0 = list(DIR_STRUCTURE.keys())[0].split(SLASH)[0]
        for dir in DIR_STRUCTURE:
            if dir.split(SLASH)[0] != dir_0:
                print("Settings error: DIR_STRUCTUREの初期バスのディレクトリ名が一致していません．")
                sys.exit()

    # DIR_STRUCTURE内のディレクトリ名がABBREVIATIONに含まれていない場合，エラーを発生させる．
    for path in DIR_STRUCTURE:
        for pair in DIR_STRUCTURE[path]:
            if pair[0] not in settings.ABBREVIATION:
                print("Settings error: DIR_STRUCTUREに含まれるディレクトリ名(変数)がABBREVIATIONに存在していません．ABBREVIATIONに追加してください．")
                print(": {}".format(pair[0]))
                sys.exit()


def base_file_name():
    pass


def write_extension():
    pass


def default_replace_word_dict():
    pass


def py_dir_path():
    if settings.PY_DIR_PATH[-1] == "/" or settings.PY_DIR_PATH[-1] == "\ ".replace(" ", ""):
        pass
    elif settings.PY_DIR_PATH == "":
        pass
    else:
        print("Settings error: settings.PY_DIR_PATH -> パスの最後にスラッシュをつけてください．")
        pprint.pprint(settings.PY_DIR_PATH)
        sys.exit()


def cwd_path():
    if platform.system() == "windows": # windowsのみ確認する．
        if not os.path.exists(settings.CWD_PATH):
            print("Settings error: {}のパスが存在していません．CWD_PATHを設定し直してください．".format(settings.CWD_PATH))
            sys.exit()


### 初期チェック
def _get_new_base_path(first_path):
    BASE_PATH = first_path + "{}.{}".format(settings.BASE_FILE_NAME, settings.WRITE_EXTENSION)
    while True:
        if os.path.isfile(BASE_PATH):
            break
        l = BASE_PATH.split(SLASH)[:-2] + [BASE_PATH.split("/")[-1]]
        BASE_PATH = os.path.join(*l) # base.ansysファイルの場所を一段下げる
    return BASE_PATH


def base_path(first_path):
    # BASE_PATHに入力されていない場合，そこにbase.ansysファイルがあるのかを検証．
    first_path = os.path.normcase(first_path)
    BASE_PATH = os.path.normcase(settings.BASE_PATH)
    if BASE_PATH == "": # ファーストパス直下にある場合
        try:
            BASE_PATH = _get_new_base_path(first_path)
        except:
            print("Settings error：{}が存在しません．settings.pyのBASE_PATHを正しく設定してください．".format(BASE_PATH))
            sys.exit()
    else:
        if not os.path.isfile(BASE_PATH):
            print("Settings error：{}が存在しません．settings.pyのBASE_PATHを正しく設定してください．".format(first_path))
            sys.exit()


def distance_time_length(first_path):
    # DISTANCE, TIME, LENGTH
    first_path = os.path.normcase(first_path)
    BASE_PATH = os.path.normcase(settings.BASE_PATH)
    if BASE_PATH == "": # ファーストパス直下にある場合
        BASE_PATH = _get_new_base_path(first_path)

    def find_data(word):
        with open(BASE_PATH, encoding="utf-8_sig") as f: # 読み取り
            data_lines = f.readlines()
        for line in data_lines:
            if word in line:
                try:
                    data = line.replace(" ", "")
                    data = data.split("=")[-1]
                    data = float(data.split("!")[0])
                    break
                except:
                    pass
        return data

    try:
        DISTANCE = float(find_data(settings.DISTANCE))
    except:
        print("Settings error: DISTANCEが{}.{}に存在していません．".format(settings.BASE_PATH, settings.WRITE_EXTENSION))
        sys.exit()
    try:
        TIME = float(find_data(settings.TIME))
    except:
        print("Settings error: TIMEが{}.{}に存在していません．".format(settings.BASE_PATH, settings.WRITE_EXTENSION))
        sys.exit()
    try:
        LENGTH = float(find_data(settings.LENGTH))
    except:
        print("Settings error: LENGTHが{}.{}に存在していません．".format(settings.BASE_PATH, settings.WRITE_EXTENSION))
        sys.exit()



def find_solve(first_path):
    # 引数のパスにあるbase.ansys内にSOLVEがないことを確認し，ある場合はエラーを発生させる．
    first_path = os.path.normcase(first_path)
    BASE_PATH = os.path.normcase(settings.BASE_PATH)
    if BASE_PATH == "":
        BASE_PATH = _get_new_base_path(first_path)
    with open(BASE_PATH, encoding="utf-8_sig") as f: # 読み取り
        data_lines = f.readlines()

    for line in data_lines:
        if "solve" in line.lower():
            print("Warning: {}に'SOLVE'が含まれておりバグの原因となります．'SOLVE'以降のansysコードを削除して再度実行してください．".format(os.path.basename(BASE_PATH)))
            a = input("0: やり直す(推奨)\n1: 警告を無視する\n入力：")
            if a == "0":
                print("'SOLVE'以降を削除してください．")
                sys.exit()
            else:
                print("生成したansysファイルには'SOLVE'が含まれています．")


def check_all():
    abbrebiation()
    dir_structure()
    default_replace_word_dict()
    # base_path()
    dir_ignore()
    path_file_name()
    file_extension()
    omission()
    base_file_name()
    write_extension()
    py_dir_path()
    cwd_path()