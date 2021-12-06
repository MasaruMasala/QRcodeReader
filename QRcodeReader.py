#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
try:
    from pyzbar.pyzbar import decode
    from PIL import ImageGrab, Image
except ImportError:
    print("ImportError! You need to run the 'pip install -r requirements.txt' command")
    exit()
from datetime import datetime
import os, tkinter, tkinter.filedialog, argparse, pprint

use_clipboard=True
this_dir=os.path.dirname(os.path.abspath(__file__))

def main():
    opt=get_option()
    if opt.clipboard:
        image = ImageGrab.grabclipboard()
        data=qr_decode(image)
        if len(data)>0:
            nowtime=datetime.now().strftime('%Y%d%m_%H%M%S')
            os.makedirs('output',exist_ok=True)
            print(this_dir)
            filepath=f'{this_dir}{os.sep}output{os.sep}{nowtime}'
            for k,v in data.items():
                filepath+=f'_{v.get("type")}'
            filepath+='.png'
            print(f'save image file:{filepath}')
            image.save(f'{filepath}')
            data_save(filepath,data)
            
    else:
        root = tkinter.Tk()
        root.withdraw()
        fTyp = [("png","*.png")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        filepath = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
        root.destroy()
        if filepath:
            image = Image.open(filepath)
            data=qr_decode(image)
            data_save(filepath,data)


def get_option():
    argparser = argparse.ArgumentParser(prog='QRcodeReader')
    argparser.add_argument('-c', '--clipboard', default=False,
                  action="store_true",
                  help='use clipboard image data')
    return argparser.parse_args()


def data_save(filepath,data):
    if len(data)>0:
        file_dir,file_nameext=os.path.split(os.path.abspath(filepath))
        file_name,file_ext=os.path.splitext(file_nameext)
        textfilepath=f'{file_dir}{os.sep}{file_name}.txt'
        with open(textfilepath,mode='w') as f:
            f.write(pprint.pformat(data))
        print(f'save data file :{textfilepath}')


def qr_decode(image):
    result={}
    if isinstance(image, Image.Image):
        count=0
        decoded = decode(image)
        for row in decoded:
            _result={}
            _result['type'] = row.type
            _result['data'] = row.data.decode('utf-8','ignore')
            _result['rect'] = row.rect
            _result['polygon']=row.polygon
            print(f'type={_result.get("type")} data={_result.get("data")}')
            result[count]=_result
            count+=1
    if len(result)==0:
        print('no barcode image')
    return result


if __name__ == '__main__':
    main()
    