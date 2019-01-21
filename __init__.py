
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

class Command:
    
    def __init__(self):
        self.bullets=ini_read('cuda_markdown_editing.ini','op','list_indent_bullets','*+-')
        self.match_header_hashes=str_to_bool(ini_read('cuda_markdown_editing.ini','op','match_header_hashes','0'))
        self.needDoublingRes=self.match_header_hashes
        if self.bullets=='':
        	self.bullets='*'
        barr=[]
        for i in self.bullets:
        	barr.append(i)
        self.barr=barr
        global option_int, option_bool
        option_int = int(ini_read(fn_config, 'op', 'option_int', str(option_int)))
        option_bool = str_to_bool(ini_read(fn_config, 'op', 'option_bool', bool_to_str(option_bool)))

    def config(self):
    	def _config_exists():
        	return os.path.exists(fn_config)
    	if not _config_exists():
        	config_file = open(fn_config,'w+')
        	config_file.write(default_config_text)
        	config_file.close()
    	ini_write(fn_config, 'op', 'option_int', str(option_int))
    	ini_write(fn_config, 'op', 'option_bool', bool_to_str(option_bool))
    	file_open(fn_config)
        
    def run(self):
        s = '''
        file lines count: {cnt}
        option_int: {i}
        option_bool: {b}
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
    				if((numres>=6) and (not self.needDoublingRes)) or (numres>=12):
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
    		if x2<x1 and  x2!=-1:
    			x2,x1=x1,x2
    		if (x2 != -1) or (y2 != -1):
    		    if (y2>y1) or ((y2==y1) and (x2>x1)):
    		    	ed_self.insert(x2,y2,symm)
    		    	ed_self.insert(x1,y1,symm)
    		    else:
    		    	ed_self.insert(x2,y2,symm)
    		    	ed_self.insert(x1,y1,symm)	
    		    return False
    	if key==13:
    		#enter#
    		strOld=ed_self.get_text_line(ed_self.get_carets()[0][1])
    		straddF=''
    		indent=1
    		while len(strOld)>0 and (strOld[0]==' ' or strOld[0]=='\t'):
    			straddF+=strOld[0]
    			strOld=strOld[1:]
    			indent+=1
    		if not strOld:
    			return True
    		if strOld[0] in self.bullets:
    			if len(strOld)==1 and strOld[0]=='-':
    				return True
    			if strOld[0]=='-' and not strOld[1]==' ':
    				return True
    			x,y = ed_self.get_carets()[0][:2]
    			ed_self.insert(x,y,'\n'+straddF+strOld[0])
    			ed_self.set_caret(indent+1,ed_self.get_carets()[0][1]+1)
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
    		if strt[0] in['"',"'","`"] and strt[0]==strt[1]:
    			ed_self.delete(x,y,x+1,y)
    	if key==9:
    		#tab symbol
    		strOldNum=ed_self.get_carets()[0][1]
    		strOld=ed_self.get_text_line(strOldNum)
    		if 's' in state:
    			#strOld=strOld=ed_self.get_text_line(strOldNum)
    			if strOld[0]==' ' or strOld[0]=='\t':
    				if strOld[0]==' ':
    					strOld=strOld[1:]
    				strOld=strOld[1:]
    				i=''
    				while strOld [0] in [' ','\t']:
    					i=i+strOld[0]
    					strOld=strOld[1:]
    				sym=strOld[0]
    				if len(strOld)>0:
    					while strOld[0] in '0123456789':
    						strOld=strOld[1:]
    						if len(strOld)==0:
    							break
    				wt=strOld[1:]
    				if sym in self.barr:
    					j=0
    					while self.barr[j]!=sym:
    						j+=1
    					sym=self.barr[j-1]
    				else:
    					sym='* '
    				ed_self.set_text_line(strOldNum,i+sym+wt)
    				ed_self.set_caret(len(i)+2, strOldNum)
    			i=0
    			return False
    		if len(strOld)==0:
    			return True
    		if strOld[0] in '-=' :
    			if not len(strOld)>=2:
    				print('lining')
    				same=True
    				for i in strOld:
    					if not i in [' ','\t','-','='] :
    						same=False
    				if same:
    					strOld=strOld[:1]
    					x,y = ed_self.get_carets()[0][:2]
    					for i in range(len(ed_self.get_text_line(strOldNum)), len(ed_self.get_text_line(strOldNum-1))):
    						strOld+=strOld[0]
    					ed_self.set_text_line(y,strOld)
    					return False
    		strSyms='1234567890.'
    		strIndent=''
    		while len(strOld)>0 and (strOld[0]==' ' or strOld[0]=='\t'):
    			strIndent+=strOld[0]
    			strOld=strOld[1:]
    		isNumbered=False
    		while strOld[0] in strSyms:
    			isNumbered=True
    			strOld=strOld[2:]
    			if len(strOld)==0:
    				break
    		if isNumbered:
    			ed_self.set_text_line(strOldNum,strIndent+'\t1.'+strOld)
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
    		if len(strOld)==0:return
    		if strOld[0]in self.barr:
    			x,y = ed_self.get_carets()[0][:2]
    			ed_self.set_text_line(y,strIndent+'\t'+nextb(strOld[0])+' '+strOld[2:])
    			ed_self.set_caret(x+2,y)
    		return False
    	elif key==56:
    		if 's' in state:
    			print(ed_self.get_carets()[0])
    			x1,y1,x2,y2=ed_self.get_carets()[0]
    			if x2<x1:
    				x1,x2=x2,x1
    			if x2==-1 and y2==-1:
    				return True
    				
    			print('inserting... %s %s %s %s'%(x1,y1,x2,y2))
    			ed_self.insert(x2,y2,'*')
    			ed_self.insert(x1,y1,'*')
    			ed_self.set_sel_rect(x1+1,y1,x2+1,y2)
    			return False
    def on_insert(self, ed_self, text):
    	if text in ['"',"'",'#',
    	'~','*','`']:
    		if text=='#' and not self.needDoublingRes:
    			return
    		x,y = ed_self.get_carets()[0][:2]
    		ed_self.insert(x,y,text)
