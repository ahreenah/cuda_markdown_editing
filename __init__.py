a='''
currently working:
* lists
  + bulleted lists
* doubling next symbols: # , ~ , ' , "
* strikethrough by clicking Ctrl + ~
'''
import os
from cudatext import *

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_MarkdownEditor.ini')

option_int = 100
option_bool = True

def bool_to_str(v): return '1' if v else '0'
def str_to_bool(s): return s=='1'

class Command:
    
    def __init__(self):
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

    def on_caret(self, ed_self):
    	#print('c')
    	curArr = ed_self.get_carets()[0]
    	#print(curArr)
    	y = curArr[1]
    	x = curArr[0]
    	#y2 = curArr[3]
    	#x1, y1, x2, y2 = curArr
    	#print(ed_self.get_text_line(y))
    	pass
    def on_change(self, ed_self):
        pass
    def on_key(self, ed_self, key, state):
    	
    	'''curArr = ed_self.get_carets()[0]
    	print(curArr)
    	y1 = curArr[1]
    	y2 = curArr[3]
    	#x1, y1, x2, y2 = curArr
    	print(str(y1)+' '+str(y2))'''
    	print('k '+str(key))
    	if key==192:
    		if 's' in state:
    			print('stroking')
    		car = ed_self.get_carets()[0]
    		if (car[2] != -1) or (car[3] != -1):
    		    print('caret for stroking is : '+str(car))
    		    ed_self.insert(car[2],car[3],'~~')
    		    ed_self.insert(car[0],car[1],'~~')
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
    			ed_self.set_caret(indent,caret[1]+1)
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
    					ed_self.set_caret(i+2+len(str(nm+1)),car[1]+1)
    					return False
    			print('counted num is: '+str(s))
    		else:
    			print('not numbered')
    	
    	if key==9:
    		#tab#
    		strOldNum=ed_self.get_carets()[0][1]
    		strOld=ed_self.get_text_line(strOldNum)
    		strIndent=''
    		while len(strOld)>0 and (strOld[0]==' ' or strOld[0]=='\t'):
    			strIndent+=strOld[0]
    			strOld=strOld[1:]
    		if strOld[0]=='*':
    			curArr = ed_self.get_carets()[0]
    			print('Writing the -')
    			y = curArr[1]
    			x = curArr[0]
    			ed_self.insert(x,y,"-")
    			strIndent+='\t'
    			strN=strIndent+'+'
    			ed_self.set_text_line(y,strN)
    			ed_self.set_caret(x+1,y)
    		if strOld[0]=='+':
    			curArr = ed_self.get_carets()[0]
    			print('Writing the -')
    			y = curArr[1]
    			x = curArr[0]
    			ed_self.insert(x,y,"-")
    			strIndent+='\t'
    			strN=strIndent+'-'
    			ed_self.set_text_line(y,strN)
    			ed_self.set_caret(x+1,y)
    		if strOld[0]=='-':
    			curArr = ed_self.get_carets()[0]
    			print('Writing the -')
    			y = curArr[1]
    			x = curArr[0]
    			ed_self.insert(x,y,"-")
    			strIndent+='\t'
    			strN=strIndent+'*'
    			ed_self.set_text_line(y,strN)
    			ed_self.set_caret(x+1,y)
    		return False
    		
    def on_insert(self, ed_self, text):
    	print('inserted '+text)
    	if text in ['"',"'",'#','~']:
    		#print('doubling')
    		
    		curArr = ed_self.get_carets()[0]
    		y = curArr[1]
    		x = curArr[0]
    		ed_self.insert(x,y,text)
    	else:
    		print('not doubling')
    	'''
        *
        *
        *
        *
        	+
        	+
        		-
        		-
        		-
        			*
        			*
        #sdf#*
        ##sdfsve##
        ###sdferge###
        ####sdfsrege####
        
        ~~asdsf~~
        ~~poiuytrewq~~
    	'''