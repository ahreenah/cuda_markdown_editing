
import os
from cudatext import *

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_markdown_editing.ini')#full path to config

option_int = 100
option_bool = True
default_config_text='''[op]
list_indent_bullets=*-+
match_header_hashes=0'''
def bool_to_str(v): return '1' if v else '0'
def str_to_bool(s): return s=='1'
#
class Command:
    
    def __init__(self):
        def _config_exists():
        	return os.path.exists(fn_config)
        if not _config_exists():
        	config_file = open(fn_config,'w+')
        	config_file.write(default_config_text)
        	config_file.close()
        self.bullets=ini_read('cuda_markdown_editing.ini','op','list_indent_bullets','*+-')
        self.match_header_hashes=ini_read('cuda_markdown_editing.ini','op','match_header_hashes','0')
        if self.match_header_hashes=='1':
        	self.match_header_hashes=True
        else:
        	self.match_header_hashes=False
        self.needDoublingRes=self.match_header_hashes
        if self.bullets=='':
        	self.bullets='*'
        barr=[]
        for i in self.bullets:
        	barr.append(i)
        self.barr=barr
        print('bullet set '+self.bullets)
        global option_int
        global option_bool
        option_int = int(ini_read(fn_config, 'op', 'option_int', str(option_int)))
        option_bool = str_to_bool(ini_read(fn_config, 'op', 'option_bool', bool_to_str(option_bool)))

    def config(self):

        ini_write(fn_config, 'op', 'option_int', str(option_int))
        ini_write(fn_config, 'op', 'option_bool', bool_to_str(option_bool))
        file_open(fn_config)
        
    def run(self):
        s = '''
        file lines count: {cnt}
        option_int: {i}
        option_bool: {b}
        '''.format(
             cnt = ed.get_line_count(),
             i = option_int,
             b = option_bool,
             )
        msg_box(s, MB_OK)
    def toggle_cap(self):
    	strnum=ed.get_carets()[0][1]
    	curn=0
    	for i in ed.folding(FOLDING_GET_LIST):
    		if i[0]<=strnum<=i[1]:
    			break
    		curn+=1
    	ed.folding(FOLDING_FOLD, index=curn)
    def on_key(self, ed_self, key, state):
    	if key==51:
    		# hash symnol
    		if 's' in state:
    			x1,y1,x2,y2=ed_self.get_carets()[0]
    			if not y2==-1:
    				if not x2==-1:
    					if x2>x1:
    						x2+=1
    					else:
    						x1+=1
    					if x2<x1:
    						x1,x2=x2,x1
    					if self.needDoublingRes:
    						ed_self.insert(x2-1,y2,'#')
    					ed_self.insert(0,y2,'#')
    					ln=ed_self.get_text_line(y1)
    					i=0
    					for ch in ln:
    						if ch=='#':
    							i+=1
    						else:
    							break
    					if i<=6:
    						ed_self.set_sel_rect(i,y1,len(ln),y1)
    					else:
    						print('error?')
    						while(len(ln)>0):
    							if ln[0]=='#':
    								ln=ln[1:]
    							elif ln[-1]=='#':
    								ln=ln[:-1]
    							else:
    								break
    						ed_self.set_text_line(y1,ln)
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
    				print(numres)
    				if((numres>=6) and (not self.needDoublingRes)) or (numres>=12):
    					print('clearing')
    					ed_self.set_text_line(y,' ')
    					ed_self.set_caret(0,y)
    					return False
    				else:
    					print('not clearing')
    	if key==192:
    		# ~ simbol
    		if 's' in state:
    			car = ed_self.get_carets()[0]
    			if (car[2] != -1) or (car[3] != -1):
    			    if (car[3]>car[1]) or ((car[3]==car[1]) and (car[2]>car[0])):
    			    	ed_self.insert(car[2],car[3],'~~')
    			    	ed_self.insert(car[0],car[1],'~~')
    			    else:
    			    	ed_self.insert(car[0],car[1],'~~')
    			    	ed_self.insert(car[2],car[3],'~~')
    			    return False
    		else:
    			# ` symbol
    			x1,y1,x2,y2 = ed_self.get_carets()[0]
    			
    			if (y2>y1) or ((y2==y1) and (x2>x1)):
    				ed_self.insert(x2,y2,'`')
    				ed_self.insert(x1,y1,'`')
    			else:
    				ed_self.insert(x1,y1,'`')
    				ed_self.insert(x2,y2,'`')
    			return False	
    	if key==13:
    		#enter#
    		strOldNum=ed_self.get_carets()[0][1]
    		strOld=ed_self.get_text_line(strOldNum)
    		straddF=''
    		indent=1
    		while len(strOld)>0 and (strOld[0]==' ' or strOld[0]=='\t'):
    			straddF+=strOld[0]
    			strOld=strOld[1:]
    			indent+=1
    		if not strOld:
    			return True
    		if strOld[0] in ['*','+','-']:
    			x,y,t,p = ed_self.get_carets()[0]
    			ed_self.insert(x,y,'\n'+straddF+strOld[0])
    			caret=ed_self.get_carets()[0]
    			ed_self.set_caret(indent+1,caret[1]+1)
    			return False
    		numArr=['1','2','3','4','5','6','7','8','9','0']
    		if strOld[0] in numArr:
    			s=''
    			i=0
    			ll=len(strOld)
    			strOld+=' '
    			while(strOld[i] in numArr) and (i<ll):
    				s=s+strOld[i]
    				i = i+1
    			if (i<ll):
    				if(strOld[i]=='.'):
    					nm=int(s)
    					car = ed_self.get_carets()[0]
    					ed_self.insert(car[0],car[1],'\n'+straddF+str(nm+1)+'.')
    					ed_self.set_caret(len(straddF+str(nm+1)+'.'),car[1]+1)
    					return False
    	if key==190:
    		# > symbol
    		if 's' in state:
    			car=ed_self.get_carets()[0]
    			y1 = car[1]
    			y2 = car[3]
    			if y2<y1:
    				y1, y2 = y2, y1
    			for i in range(y1, y2+1):
    				ed_self.insert(0,i,'> ')
    			return False
    	if key==32:
    		# space
    		car = ed_self.get_carets()[0]
    		x   = car[0]
    		y   = car[1]
    		was = ed_self.get_text_substr(x-1,y,x,y)
    		now = ed_self.get_text_substr(x,y,x+1,y)
    		if was in['"',"'","`"]:
    			if now==was:
    				ed_self.delete(x,y,x+1,y)
    	if key==9:
    		#tab symbol
    		strOldNum=ed_self.get_carets()[0][1]
    		strOld=ed_self.get_text_line(strOldNum)
    		if 's' in state:
    			strOld=strOld=ed_self.get_text_line(strOldNum)
    			if strOld[0]==' ':
    				strOld=strOld[1:]
    				strOld=strOld[1:]
    				i=''
    				while(strOld [0] in [' ','\t']):
    					i=i+strOld[0]
    					strOld=strOld[1:]
    				sym=strOld[0]
    				wt=strOld[1:]
    				if sym in self.barr:
    					j=0
    					while not (self.barr[j]==sym):
    						j+=1
    					sym=self.barr[j-1]
    				else:
    					sym='*'
    				ed_self.set_text_line(strOldNum,i+sym+strOld+wt)
    			elif strOld[0]=='\t':
    				strOld=strOld[1:]
    				i=''
    				while(strOld [0] in [' ','\t']):
    					i=i+strOld[0]
    					strOld=strOld[1:]    				
    				sym=strOld[0]
    				if sym in self.barr:
    					j=0
    					while not (self.barr[j]==sym):
    						j+=1
    					sym=self.barr[j-1]
    				else:
    					sym='* '
    				ed_self.set_text_line(strOldNum,i+sym+strOld[1:])
    			i=0
    			return False
    		if(len(strOld)==0):
    			return True
    		if(strOld[0] in ['-','=']):
    			same=True
    			for i in strOld:
    				if not(i == strOld[0]):
    					same=False
    			if same:
    				car = ed_self.get_carets()[0]
    				x, y = car[0],car[1]
    				for i in range(len(ed_self.get_text_line(strOldNum)), len(ed_self.get_text_line(strOldNum-1))):
    					ed_self.insert(x,y,strOld[0])
    				return False
    		strSyms='1234567890'
    		strIndent=''
    		while len(strOld)>0 and (strOld[0]==' ' or strOld[0]=='\t'):
    			strIndent+=strOld[0]
    			strOld=strOld[1:]
    		olt=strOld[2:]
    		ed_self.set_text_line(strOldNum,strIndent+'\t1.'+olt)
    		ed_self.set_caret(len(ed_self.get_text_line(strOldNum)),strOldNum)
    		#barr=['*','-','+','\\']
    		def nextb(curb):
    			i=0
    			for j in self.barr:
    				if j==curb:
    					return self.barr[(i+1)%len(self.barr)]
    				else:
    					i+=1
    			return barr[0]
    		if strOld[0]in self.barr:
    			curArr = ed_self.get_carets()[0]
    			y = curArr[1]
    			x = curArr[0]
    			#ed_self.insert(x,y,"-")
    			strIndent+='\t'
    			strN=strIndent+nextb(strOld[0])+' '+olt
    			ed_self.set_text_line(y,strN)
    			ed_self.set_caret(x,y)
    		'''if strOld[0]=='*':
    			curArr = ed_self.get_carets()[0]
    			y = curArr[1]
    			x = curArr[0]
    			ed_self.insert(x,y,"-")
    			strIndent+='\t'
    			strN=strIndent+'+ '+olt
    			ed_self.set_text_line(y,strN)
    			ed_self.set_caret(x,y)
    		if strOld[0]=='-':
    			curArr = ed_self.get_carets()[0]
    			y = curArr[1]
    			x = curArr[0]
    			ed_self.insert(x,y,"-")
    			strIndent+='\t'
    			strN=strIndent+'* '+olt
    			ed_self.set_text_line(y,strN)
    			ed_self.set_caret(x,y)'''
    		return False
    	
    def on_insert(self, ed_self, text):
    	if text in ['"',"'",'#','~','*','`']:
    		if text=='#' and not self.needDoublingRes:
    			return
    		x,y = ed_self.get_carets()[0][:2]
    		ed_self.insert(x,y,text)
