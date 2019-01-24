
import os
from cudatext import *

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_markdown_editing.ini')#full path to config

default_config_text='''[op]
list_indent_bullets=*-+
match_header_hashes=0'''
def bool_to_str(v): return '1' if v else '0'
def str_to_bool(s): return s=='1'

class Command:
    
    def __init__(self):
        self.MAX_HASHES=6
        self.DOUBLE_MAX_HASHES=self.MAX_HASHES*2
        self.bullets=ini_read('cuda_markdown_editing.ini','op','list_indent_bullets','*+-')
        self.match_header_hashes=str_to_bool(ini_read('cuda_markdown_editing.ini','op','match_header_hashes','0'))
        self.need_doubling_res=self.match_header_hashes
        if self.bullets=='':
            self.bullets='*'
        self.bullets+=self.bullets[0]
        for i in '*-+':
            if not i in self.bullets:
                self.bullets+=i+i
        barr=[]
        for i in self.bullets:
            barr.append(i)
        self.barr=barr

    def config(self):
        def _config_exists():
            return os.path.exists(fn_config)
        if not _config_exists():
            config_file = open(fn_config,'w+')
            config_file.write(default_config_text)
            config_file.close()
        file_open(fn_config)
        
    def run(self):
        s = '''
        file lines count: {cnt}
        '''.format(
             cnt = ed.get_line_count()
             )
        msg_box(s, MB_OK)
        
    def on_key(self, ed_self, key, state):
        if key==51:
            # hash symnol
            if 's' in state:
                x1,y1,x2,y2=ed_self.get_carets()[0]
                if y2!=-1 and  x2!=-1:
                    if x2>x1:
                        x2+=1
                    else:
                        x1+=1
                    if x2<x1:
                        x1,x2=x2,x1
                    if self.need_doubling_res:
                        ed_self.insert(x2-1,y2,'#')
                    ed_self.insert(0,y2,'#')
                    ln=ed_self.get_text_line(y1)
                    i=0
                    for ch in ln:
                        if ch=='#':
                            i+=1
                        else:
                            break
                    if i<=self.MAX_HASHES:
                        ed_self.set_caret(i,y1,len(ln)-i,y1)
                    else:
                        while(len(ln)>0):
                            if ln[0]=='#':
                                ln=ln[1:]
                            elif ln[-1]=='#':
                                ln=ln[:-1]
                            else:
                                break
                            ed_self.set_text_line(y1,ln)
                            ed_self.set_caret(0,y1,len(ln),y1)
                    return False
                else:
                    y   = ed_self.get_carets()[0][1]
                    st  = ed_self.get_text_line(y)
                    sto = st
                    if len(st)>0:
                        while (len(st)>0)  and (st[0] in [' ','\t','#']):
                            st=st[1:]
                    i=0
                    numres=0
                    st  = ed_self.get_text_line(y)
                    while(i<len(st)):
                        if st[i]=='#':
                            numres+=1
                            i+=1
                        else:
                            break
                    if((numres>=self.MAX_HASHES) and (not self.need_doubling_res)) or (numres>=self.DOUBLE_MAX_HASHES):
                        ed_self.set_text_line(y,' ')
                        ed_self.set_caret(0,y)
                        return False
                    else:
                        pass
        if key==192:
            # ~   simbol
            if 's' in state:
                symm='~~'
            else:
                symm='`'
            x1,y1,x2,y2 = ed_self.get_carets()[0]
            if (x2<x1 and y2==y1) or y2<y1:
                if x2!=-1 or y2!=-1:
                    x2,x1=x1,x2
                    y2,y1=y1,y2
            print('h1')
            if (x2 != -1) or (y2 != -1):
                print(str(x2)+' '+str(y2))
                if (y2>y1) or ((y2==y1) and (x2>x1)):
                    ed_self.insert(x2,y2,symm)
                    ed_self.insert(x1,y1,symm)      
                else:
                    ed_self.insert(x2,y2,symm)
                    ed_self.insert(x1,y1,symm)
                if symm=='`':
                    if y2==y1:
                        ed_self.set_caret(x1+1,y1, x2+1,y2)
                    else:
                        ed_self.set_caret(x1+1,y1, x2,y2)
                else:
                    if y2==y1:
                        ed_self.set_caret(x1+2,y1, x2+2,y2)
                    else:
                        ed_self.set_caret(x1+2,y1, x2,y2)
                return False
        if key==13:
            # enter
            str_old=ed_self.get_text_line(ed_self.get_carets()[0][1])
            str_add_f=''
            indent=1
            while len(str_old)>0 and (str_old[0]==' ' or str_old[0]=='\t'):
                str_add_f+=str_old[0]
                str_old=str_old[1:]
                indent+=1
            if not str_old:
                return True
            if str_old[0] in '-+*':
                is_gfm = (str_old[2:5] in ['[ ]','[X]','[x]'])
                if len(str_old)==1 and str_old[0]=='-':
                    return True
                if str_old[0]=='-' and not str_old[1]==' ':
                    return True
                if str_old[0]=='*':
                    if '*' in str_old[1:]:
                        return True
                x,y = ed_self.get_carets()[0][:2]
                empty=True
                for i in str_old:
                    if not i in [' ','\t']:
                        if not i in '*-+':
                            empty=False
                if empty:
                    ed_self.set_text_line(y,' '*x)
                    ed_self.set_caret(x-2,y)
                    return False
                x,y = ed_self.get_carets()[0][:2]
                ggf=(' [ ]' if is_gfm else ' ')
                ed_self.insert(x,y,'\n'+str_add_f+str_old[0]+ggf)
                ed_self.set_caret(indent+len(ggf),ed_self.get_carets()[0][1]+1)
                return False
            num_arr=['1','2','3','4','5','6','7','8','9','0']
            if str_old[0] in num_arr:
                s=''
                i=0
                ll=len(str_old)
                str_old+=' '
                while(str_old[i] in num_arr) and (i<ll):
                    s=s+str_old[i]
                    i = i+1
                if (i<ll):
                    if(str_old[i]=='.'):
                        nm=int(s)
                        car = ed_self.get_carets()[0]
                        ed_self.insert(car[0],car[1],'\n'+str_add_f+str(nm+1)+'.')
                        ed_self.set_caret(len(str_add_f+str(nm+1)+'.'),car[1]+1)
                        return False
        if key==190:
            # > symbol
            if 's' in state:
                x1,y1,x2,y2=ed_self.get_carets()[0]
                if y2<y1:
                    y1, y2 = y2, y1
                for i in range(y1, y2+1):
                    ed_self.insert(0,i,'> ')
                return False
        if key==32:
            # space
            x,y,x1,y1 = ed_self.get_carets()[0]
            if x==0:
                return
            strt=ed_self.get_text_substr(x-1,y,x+1,y)
            if len(strt)<2:
                return True
            if strt[0]=='*' and strt[1]=='*':
                ed_self.delete(x,y,x+1,y)
            if strt[0] in['"',"'","`"] and strt[0]==strt[1]:
                ed_self.delete(x,y,x+1,y)
            if strt[0:2] in ['()','[]','{}']:
                ed_self.delete(x,y,x+1,y)
        if key==8:
            # backspace
            x,y,x1,y1 = ed_self.get_carets()[0]
            subst=ed_self.get_text_substr(x-1,y,x+1,y)
            if subst in ["''" , '""' , '{}' , '[]' , '()', '**','``']:
                ed_self.delete(x-1,y,x+1,y)
                ed_self.set_caret(x-1,y)
                return False
        if key==9:
            #tab symbol
            str_old_num=ed_self.get_carets()[0][1]
            str_old=ed_self.get_text_line(str_old_num)
            if 's' in state:
                #str_old=str_old=ed_self.get_text_line(str_old_num)
                if str_old[0]==' ' or str_old[0]=='\t':
                    if str_old[0]==' ':
                        str_old=str_old[1:]
                    str_old=str_old[1:]
                    i=''
                    while str_old [0] in [' ','\t']:
                        i=i+str_old[0]
                        str_old=str_old[1:]
                    sym=str_old[0]
                    if len(str_old)>0:
                        while str_old[0] in '0123456789':
                            str_old=str_old[1:]
                            if len(str_old)==0:
                                break
                    wt=str_old[1:]
                    if sym in '*-+':
                        j=len(self.barr)-1
                        while self.barr[j]!=sym:
                            j-=1
                        sym=self.barr[j-1]
                    else:
                        sym=self.bullets[0]+' '
                    ed_self.set_text_line(str_old_num,i+sym+wt)
                    ed_self.set_caret(len(i)+2, str_old_num)
                i=0
                return False
            if len(str_old)==0:
                return True
            if str_old[0] in '-=' :
                if not len(str_old)>=2:
                    same=True
                    for i in str_old:
                        if not i in [' ','\t','-','='] :
                            same=False
                    if same:
                        str_old=str_old[:1]
                        x,y = ed_self.get_carets()[0][:2]
                        for i in range(len(ed_self.get_text_line(str_old_num)), len(ed_self.get_text_line(str_old_num-1))):
                            str_old+=str_old[0]
                        ed_self.set_text_line(y,str_old)
                        ed_self.set_caret(len(str_old)+1,y)
                        return False
            str_syms='1234567890.'
            str_indent=''
            while len(str_old)>0 and (str_old[0]==' ' or str_old[0]=='\t'):
                str_indent+=str_old[0]
                str_old=str_old[1:]
            is_numbered=False
            if len(str_old)>0:              
                while str_old[0] in str_syms:
                    is_numbered=True
                    str_old=str_old[2:]
                    if len(str_old)==0:
                        break
            if is_numbered:
                ed_self.set_text_line(str_old_num,str_indent+' '*ed_self.get_prop(PROP_INDENT_SIZE)+'1.'+str_old)
            ed_self.set_caret(len(ed_self.get_text_line(str_old_num)),str_old_num)
            return False
            #barr=['*','-','+','\\']
            def nextb(curb):
                i=0
                for j in self.barr:
                    if j==curb:
                        return self.barr[(i+1)%len(self.barr)]
                    else:
                        i+=1
                return barr[0]
            if len(str_old)==0:return
            if str_old[0]in self.barr:
                if str_old[0]=='*':
                    x,y=ed_self.get_carets()[0][:2]
                    strt=ed_self.get_text_line(y)
                    while(strt[0] in [' ','\t']):
                        strt=strt[1:]
                    strt=strt[1:]
                    if '*' in strt:
                        return False
                    else:
                        ed_self.insert(0,y,' '*ed_self.get_prop(PROP_INDENT_SIZE))
                x,y = ed_self.get_carets()[0][:2]
                if str_old[2:]=='':
                    ed_self.set_text_line(y,str_indent+' '*ed_self.get_prop(PROP_INDENT_SIZE)+nextb(str_old[0])+' '+str_old[2:])
                ed_self.set_caret(x+2,y)
            return False
        elif key==56:
        # * symbol
            if 's' in state:
                x1,y1,x2,y2=ed_self.get_carets()[0]
                if (x2!=-1 and y2!=-1) and((x2<x1 and y2==y1) or y2<y1):
                    x1,x2=x2,x1
                    y2,y1=y1,y2
                if x2==-1 and y2==-1:
                    #ed_self.insert(x1,y1,'**')
                    print('h2')
                    return True
                print('h2')
                ed_self.insert(x2,y2,'*')
                ed_self.insert(x1,y1,'*')
                if y2==y1:
                    ed_self.set_caret(x1+1,y1,x2+1,y2)
                else:
                    ed_self.set_caret(x1+1,y1,x2,y2)
                return False
        elif key==189:
            # _ symbol
            print(189)
            if 's' in state:
                x1,y1,x2,y2=ed_self.get_carets()[0]
                if x2==-1 and y2==-1:
                    ed_self.insert(x1,y1,'_')
                    return True
                if (x2<x1 and y2==y1) or y2<y1:
                    x1,x2=x2,x1
                    y1,y2=y2,y1
                ed_self.insert(x2,y2,'_')
                ed_self.insert(x1,y1,'_')
                if (y2==-1) and (x2==-1):
                    return True
                if y2==y1:
                    ed_self.set_caret(x1+1,y1,x2+1,y2)
                else:
                    ed_self.set_caret(x1+1,y1,x2,y2)
                return False
        else:
            print(key)
    def on_insert(self, ed_self, text):
        if text in ['"',"'",'#',
        '~','*','`']:
            print('dd')
            if text=='#' and not self.need_doubling_res:
                return
            x,y = ed_self.get_carets()[0][:2]
            ed_self.insert(x,y,text)
