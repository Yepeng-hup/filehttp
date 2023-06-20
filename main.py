import os
import hashlib
import traceback
from flask import Flask, request, redirect, render_template, url_for, send_file
from werkzeug.utils import secure_filename

CONTAINER = "C:\\Users\\XuanQu\\Desktop\\github\\Flask-FileServer\\upload"
DOWNLOAD_FIEL_DIR = "C:\\Users\\XuanQu\\Desktop\\github\\Flask-FileServer\\file.txt"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = CONTAINER
app.config["DOWNLOAD_FIEL_DIR"] = DOWNLOAD_FIEL_DIR
app.config['MAX_CONTENT_LENGTH'] = 10 * 1000 * 1000 * 1000


@app.route('/', methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        try:
            if 'file' not in request.files:
                print('No file part')
                return "err"
            file = request.files['file']
            if file.filename == '':
                print('No selected file')
                return "err"
            if file:
                filename = secure_filename(file.filename)
                dirSize = sum(os.path.getsize(f) for f in os.listdir('.') if os.path.isfile(f))
                if dirSize < app.config['MAX_CONTENT_LENGTH']:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    fileSha1 = hashlib.sha1(filename.encode('utf-8'))
                    fileCode = fileSha1.hexdigest()[:6]
                    return fileCode
                else:
                    print("save file error.")
                    return "err"
        except Exception as e:
            print(e)
            return "err"

    return render_template("upload.html")


@app.route('/link', methods=["GET"])
def linkGen():
    code = request.args.get("code")
    file_name = check_file(code)
    write_file(code, file_name)
    try:
        if code.isalnum() and len(code) == 6:
            return render_template("link.html", content=code)
    except:
        return redirect("/")
    return redirect("/")


@app.route('/receive', methods=["GET", "POST"])
@app.route('/receive/<file>', methods=["GET"])
def receive_file(file=""):
    if request.method == "POST":
        try:
            fileCode = request.form.get("fileCode")
            fileName = check_file(fileCode)
            if fileName == "":
                print("error not is file.")
                return redirect(url_for('upload_file'))
            return render_template("download.html", content=fileName)
        except:
            return redirect("/")
    if file != "":
        fileName = check_file(file)
        if fileName == "":
            print("error not is file.")
            return redirect(url_for('upload_file'))
        return render_template("download.html", content=fileName)
    else:
        return render_template("receive.html")


@app.route('/download', methods=["GET"])
def download():
    # 浏览器下载链接: http://ip:port/download?file_name=1.sh&file_dir=test
    # linux下载链接: curl -# -o 1.txt http://ip:port/download?file_name=1.sh&file_dir=test
    file_name = request.args.get('file_name')
    # file_dir = request.args.get('file_dir')
    # path = app.config["UPLOAD_FOLDER"] + file_dir + '/' + '%s' % file_name
    path = app.config["UPLOAD_FOLDER"] + '/' + '%s' % file_name
    return send_file(path, as_attachment=True)


@app.route("/catfile", methods=["GET"])
def cat_file():
    file_list = list()
    with open(app.config["DOWNLOAD_FIEL_DIR"], "r", encoding='utf8') as f:
        file_text = f.read()
        # 以什么分割
        textAll = file_text.split(',')
        # list反转
        # textAll.reverse()
        for i in textAll:
            i = ''.join(i.rsplit("\n", 1))
            if i != '':
                file_list.append(i)
        file_l = file_list[1::2]
        code_l = file_list[::2]
        str_dict = dict(zip(code_l, file_l))
    return render_template("filelist.html", file_name=str_dict)


@app.route("/delete", methods=["POST"])
def delete_file():
    file_name = request.form.get("name")
    textList = file_name.split('\t')
    file_name = textList[2]
    rel = del_dir_file(file_name)
    if rel == "ok":
        print(f"file delete ok -----> {file_name}")
    try:
        with open(app.config["DOWNLOAD_FIEL_DIR"], 'r', encoding='utf-8') as f:
            lines = f.readlines()
            new_as_lines = list()
            for i in lines:
                bools = file_name in i.replace('\n', '')
                if bools != True:
                    new_as_lines.append(i)
                else:
                    continue
        with open(app.config["DOWNLOAD_FIEL_DIR"], 'w', encoding='utf-8') as f:
            f.writelines(new_as_lines)
        return ""
    except Exception:
        print(traceback.format_exc())
        return ""


def write_file(file_code: str = None, file_name: str = None):
    f_dict = dict()
    f_dict["file_code"] = file_code
    f_dict["file_name"] = file_name
    with open(app.config["DOWNLOAD_FIEL_DIR"], 'a', encoding='utf8') as f:
        for k, v in f_dict.items():
            f.write(f"{v},")
        f.write("\n")


def check_file(fileCode):
    if len(fileCode) == 6:
        try:
            int(fileCode, 16)
        except:
            return ""
        files = os.listdir(CONTAINER)
        for i in files:
            fileSha1 = hashlib.sha1(i.encode('utf-8'))
            if fileSha1.hexdigest()[:6] == fileCode:
                return i
        return ""
    return ""


def del_dir_file(file_name: str):
    try:
        os.remove(app.config["UPLOAD_FOLDER"] + f"\\{file_name}")
        return "ok"
    except:
        print(traceback.format_exc())


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=1880)