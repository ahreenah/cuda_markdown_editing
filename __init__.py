
import os
from cudatext import *

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_MarkdownEditor.ini')

option_int = 100
option_bool = True

def bool_to_str(v): return '1' if v else '0'
def str_to_bool(s): return s=='1'

class Command:
    
    def __init__(self):
        self.needDoublingRes=False
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
    	print('toggling captions')
    	arr=ed.folding(FOLDING_GET_LIST)
    	print(str(arr))
    	strnum=ed.get_carets()[0][1]
    	print('line number is: '+str(strnum))
    	i=-1
    	curn=0
    	for i in arr:
    		print('procesing '+str(i)+'...')
    		if i[0]<=strnum<=i[1]:
    			i=curn
    			print('found!')
    			break
    		curn+=1
    	#print(str(i)+' '+str(arr[i][0]))
    	ed.folding(FOLDING_FOLD, index=i)
    def on_caret(self, ed_self):
    	#print('c')
    	curArr = ed_self.get_carets()[0]
    	#print(curArr)
    	y = curArr[1]
    	x = curArr[0]
    	pass
    def on_change(self, ed_self):
        pass
    def on_key(self, ed_self, key, state):
    	print('k '+str(key))
    	if key==51:
    		#reshetka
    		if 's' in state:
    			cur=ed_self.get_carets()[0]
    			if not cur[3]==-1:
    				if not cur[2]==-1:
    					x1,y1,x2,y2=cur[0],cur[1],cur[2],cur[3]
    					if x2>x1:
    						x2+=1
    					else:
    						x1+=1
    					print('selected text from '+str(x1))
    					if self.needDoublingRes:
    						ed_self.insert(x2,y2,'#')
    					ed_self.insert(0,y1,'#')
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
    							else:
    								break
    						ed_self.set_text_line(y1,ln)
    					return False
    			else:
    				car = ed_self.get_carets()[0]
    				y   = car[1]
    				st  = ed_self.get_text_line(y)
    				sto = st
    				while(st[0] in [' ','\t']):
    					st=st[1:]
    				i=0
    				numres=0
    				while(i<len(st)):
    					if st[i]=='#':
    						numres+=1
    						i+=1
    					else:
    						break
    				if(numres>=6):
    					for i in range(5):
    						sto=sto[1:]
    					while st[0]==' ':
    						sto=sto[1:]
    					ed_self.set_text_line(y,' ')
    					ed_self.set_caret(0,y)
    					return False
    	if key==192:
    		if 's' in state:
    			print('stroking')
    			car = ed_self.get_carets()[0]
    			if (car[2] != -1) or (car[3] != -1):
    			    print('caret for stroking is : '+str(car))
    			    if (car[3]>car[1]) or ((car[3]==car[1]) and (car[2]>car[0])):
    			    	ed_self.insert(car[2],car[3],'~~')
    			    	ed_self.insert(car[0],car[1],'~~')
    			    else:
    			    	ed_self.insert(car[0],car[1],'~~')
    			    	ed_self.insert(car[2],car[3],'~~')
    			    return False
    		else:
    			car = ed_self.get_carets()[0]
    			print('quoting')
    			if (car[3]>car[1]) or ((car[3]==car[1]) and (car[2]>car[0])):
    				ed_self.insert(car[2],car[3],'`')
    				ed_self.insert(car[0],car[1],'`')
    			else:
    				ed_self.insert(car[0],car[1],'`')
    				ed_self.insert(car[2],car[3],'`')
    			return False	
    		print('state '+state)
    				
    	if key==13:
    		#enter#
    		print('enter pressed' + str(ed_self.get_carets()[0][1]))
    		strOldNum=ed_self.get_carets()[0][1]
    		strOld=ed_self.get_text_line(strOldNum)
    		straddF=''
    		indent=1
    		while len(strOld)>0 and (strOld[0]==' ' or strOld[0]=='\t'):
    			straddF+=strOld[0]
    			strOld=strOld[1:]
    			indent+=1
    		print('Went from line '+strOld)
    		if not strOld:
    			return True
    		print('first symbol was: '+strOld[0]) 
    		if strOld[0] in ['*','+','-']:
    			curArr = ed_self.get_carets()[0]
    			y = curArr[1]
    			x = curArr[0]
    			print('inserted into '+str(x)+str(y+0))
    			ed_self.insert(x,y,'\n'+straddF+strOld[0])
    			caret=ed_self.get_carets()[0]
    			print(caret)
    			ed_self.set_caret(indent+1,caret[1]+1)
    			return False
    		numArr=['1','2','3','4','5','6','7','8','9','0']
    		if strOld[0] in numArr:
    			print('numbered list?')
    			s=''
    			i=0
    			ll=len(strOld)
    			strOld+=' '
    			while(strOld[i] in numArr) and (i<ll):
    				s=s+strOld[i]
    				i = i+1
    			if (i<ll):
    				if(strOld[i]=='.'):
    					print ('numbered list!!!')
    					nm=int(s)
    					print ('next number is '+str(nm+1)) 
    					car = ed_self.get_carets()[0]
    					print('went from line' +str(car[1]))
    					ed_self.insert(car[0],car[1],'\n'+straddF+str(nm+1)+'.')
    					ed_self.set_caret(len(straddF+str(nm+1)+'.'),car[1]+1)
    					return False
    			print('counted num is: '+str(s))
    		else:
    			print('not numbered')
    	
    	if key==190:
    		if 's' in state:
    			print('blockquote')
    			car=ed_self.get_carets()[0]
    			print(car)
    			y1 = car[1]
    			y2 = car[3]
    			if y2<y1:
    				y1, y2 = y2, y1
    			print('from %s to %s '%(y1, y2))
    			for i in range(y1, y2+1):
    				ed_self.insert(0,i,'> ')
    			return False
    	if key==32:
    		car = ed_self.get_carets()[0]
    		x   = car[0]
    		y   = car[1]
    		was = ed_self.get_text_substr(x-1,y,x,y)
    		now = ed_self.get_text_substr(x,y,x+1,y)
    		if was in['"',"'","`"]:
    			if now==was:
    				ed_self.delete(x,y,x+1,y)
    		print('w: '+was+' n: '+now)
    	if key==9:
    		#tab#
    		strOldNum=ed_self.get_carets()[0][1]
    		strOld=ed_self.get_text_line(strOldNum)
    		print(strOld)
    		if 's' in state:
    			strOld=strOld=ed_self.get_text_line(strOldNum)
    			print('unindenting!!'+strOld)
    			if strOld[0]==' ':
    				print('was:'+strOld)
    				strOld=strOld[1:]
    				strOld=strOld[1:]
    				print('set:'+strOld)
    				#print('bullet '+strOld[i])
    				i=''
    				while(strOld [0] in [' ','\t']):
    					i=i+strOld[0]
    					strOld=strOld[1:]
    				print('wt : '+strOld[1:])
    				sym=strOld[0]
    				wt=strOld[1:]
    				print('replacing')
    				if sym=='-':
    					sym='+'
    				elif sym=='+':
    					sym='*'
    				elif sym=='*':
    					sym='-'
    				ed_self.set_text_line(strOldNum,i+sym+strOld+wt)
    			elif strOld[0]=='\t':
    				print('tabs')
    				print('was:'+strOld)
    				print(strOld)
    				strOld=strOld[1:]
    				print('set:'+strOld)
    				print(strOld)
    				i=''
    				while(strOld [0] in [' ','\t']):
    					i=i+strOld[0]
    					strOld=strOld[1:]    				
    				print('bullet '+strOld[0])
    				sym=strOld[0]
    				if sym=='-':
    					sym='+'
    				elif sym=='+':
    					sym='*'
    				elif sym=='*':
    					sym='-'
    				ed_self.set_text_line(strOldNum,i+sym+strOld[1:])
    			i=0
    			return False
    		if(len(strOld)==0):
    			print('kp 1')
    			return True
    		if(strOld[0] in ['-','=']):
    			print('kp 2')
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
    		print('kp 3')
    		strSyms='1234567890'
    		print(strOld)
    		
    		strIndent=''
    		while len(strOld)>0 and (strOld[0]==' ' or strOld[0]=='\t'):
    			strIndent+=strOld[0]
    			strOld=strOld[1:]
    		olt=strOld[2:]
    		print('starting from nums: '+strOld+'!!!')
    		ed_self.set_text_line(strOldNum,strIndent+'\t1.')
    		ed_self.set_caret(len(ed_self.get_text_line(strOldNum)),strOldNum)
    		if strOld[0]=='+':
    			curArr = ed_self.get_carets()[0]
    			print('Writing the -')
    			y = curArr[1]
    			x = curArr[0]
    			ed_self.insert(x,y,"-")
    			strIndent+='\t'
    			print('inserting -')
    			strN=strIndent+'- '+olt
    			ed_self.set_text_line(y,strN)
    			ed_self.set_caret(x,y)
    		if strOld[0]=='*':
    			curArr = ed_self.get_carets()[0]
    			print('Writing the -')
    			y = curArr[1]
    			x = curArr[0]
    			ed_self.insert(x,y,"-")
    			strIndent+='\t'
    			print('inserting -')
    			strN=strIndent+'+ '+olt
    			ed_self.set_text_line(y,strN)
    			ed_self.set_caret(x,y)
    		if strOld[0]=='-':
    			curArr = ed_self.get_carets()[0]
    			print('Writing the -')
    			y = curArr[1]
    			x = curArr[0]
    			ed_self.insert(x,y,"-")
    			strIndent+='\t'
    			strN=strIndent+'* '+olt
    			ed_self.set_text_line(y,strN)
    			ed_self.set_caret(x,y)
    		return False
    	
    def on_insert(self, ed_self, text):
    	print('inserted '+text)
    	if text in ['"',"'",'#','~','*','`']:
    		#print('doubling')
    		if text=='#' and not self.needDoublingRes:
    			return
    		curArr = ed_self.get_carets()[0]
    		y = curArr[1]
    		x = curArr[0]
    		ed_self.insert(x,y,text)
    	else:
    		print('not doubling')
