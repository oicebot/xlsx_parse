#!/usr/bin/python
# -*- coding:utf-8 -*-
#
# Debug on Python 3.5.2
# 2017.04.17 by Oicebot 
#
#运行方法，用 Python IDLE 打开，按 F5 运行
import re

def parse_sonography_result(intext=''):
    intext = intext.replace('\n',' ')    #先把所有回车替换成空格。
    full_text=intext.split('。')         #将整个字符串用句号分割开，每个句子变成数组里的一个元素
    
    #TODO: 提取诊断结果 US-Birads 等级
    

def parse_operation(intext=''):
    intext = intext.replace('\n',' ')    #先把所有回车替换成空格。
    full_text=intext.split('。')         #将整个字符串用句号分割开，每个句子变成数组里的一个元素
    
    #TODO：提取手术过程切了些什么
    
    
def parse_pathology(intext='',div='$',replace_data='',outputemptyvalue=True):
    '''
    函数功能：提取分析结果是什么细胞
    接受4个参数： intext 是需处理的字符串本身， div 是分割多个诊断字符串的标记(可选)
                          replace_data 是替换的标记及其对应的全称(可选)，
                          outputemptyvalue 是否吐空值(可选)，默认”是“
    '''
    intext = intext.replace('\n',' ')    #先把所有回车替换成空格。
    full_text=intext.split(div)         #将整个字符串用 div 分割开，每个元素中将包含一个完整的病理诊断描述
        
    if not replace_data:
        #默认的替换标记及对应的全称
        replace_data = {'wz':'位置','dx':'定性','fj':'分级','dz':'单发/多灶','bs':'伴随病变的情况','lj':'累及周围组织情况','ln':'淋巴结转移情况'}
        
    output_list = []
        
    for detail_info in full_text:
        tokens = str(detail_info)
        tokens = tokens.split("[")[1:]

        info_data = {}  #初始化一个空字典
        if outputemptyvalue:
            for k,j in replace_data.items(): #为输出空值，则应先初始化空字典的值
                info_data[j] = ''  #字典的 key 来自替换标记的全称
        
        for tok in tokens:
            if tok:
                info_token = tok.split("]")[0]
                tag = info_token.split(" ")[0]
                try:
                    describe_name = replace_data[tag]
                except KeyError:
                    raise RuntimeError('没找到能用的tag啊！')
                else:
                    describe_text = ' '.join(info_token.split(" ")[1:])
                    info_data[describe_name] = describe_text
                    
        output_list.append(info_data)
        
    return output_list
    

def parse_sonography(intext=''):
    intext = intext.replace('\n',' ')    #先把所有回车替换成空格。
    full_text=intext.split('。')         #将整个字符串用句号分割开，每个句子变成数组里的一个元素
    
    #所要提取信息的句子，同时包含'回声'   '可见'   '大小' 这三个词*
    #多个句子组成一个数组
    tumor_info=[i for i in full_text if ('回声' in i and '见' in i and ('边缘' in i or '边界' in i)) ]
    
    #调试用，打印显示有几个句子符合上面的要求
    #i=0
    #for k in tumor_info:
    #    print i,k
    #    i+=1
        
    #默认每个句子描述一个肿块
    
    output_list = []
    for each_tumor in tumor_info:
        
        info_list = each_tumor.split('，') #先将句子用逗号分隔成一串短语
        
        #构建一个字典
        
        info_data = {'描述':'',
                     '位置':'',
                     '大小':'',
                     '形态':'',
                     '生长方向':'',
                     '边缘':'',
                     '分布':'',
                     '内部回声':'',
                     '钙化':'',
                     '后方回声':'',
                     'CDFI':'',
                     }
                     
        sizes = []  #鉴于有可能一句话描述多个不同的尺寸，先建一个数组
        positions = []
        describes = []
        describe_text = ''
        pos_text = ''
        size_text = ''
        
        for detail_info in info_list:
            #综合描述
            if '侧' in detail_info and '见' in detail_info and any(a in detail_info for a in ['回声','团块']):
                describe_text = detail_info
               
            #位置
            if any(a in detail_info for a in ['点钟','副乳内','侧象限']):
                pos1 = detail_info.find('可见')
                pos2 = detail_info.find('大小')
                pos3 = detail_info.find('方向')
                if pos3 > 0:
                    pos3 += 2
                if any(a > 0 for a in [pos1,pos2,pos3]):
                    pos = min([n for n in [pos1,pos2,pos3] if n>0]) #取两者之间大于零的数字中较小的那个
                    pos_text = detail_info[:pos]  #裁掉后面一段
                else:
                    pos_text = detail_info          #找不到，自暴自弃，不裁剪了

            #大小
            if '大小' in detail_info or all(a in detail_info for a in ['×','mm']):
                pos1 = detail_info.find('大小')
                pos2 = detail_info.find('范围')
                if pos1 > 0 or pos2 > 0:
                    pos = min([n for n in [pos1,pos2] if n>0]) 
                    size_text = detail_info[pos:]    #裁去前面部分
                else:
                    size_text = detail_info          #找不到，自暴自弃，不裁剪了

                describes.append(describe_text)  #将当前描述加入数组
                positions.append(pos_text)       #将当前位置加入数组
                sizes.append(size_text)          #将当前尺寸加入数组
                
            #形态            
            elif '呈' in detail_info and '形' in detail_info:
                info_data['形态'] = detail_info
            #生长方向
            elif '生长' in detail_info:
                info_data['生长方向'] = detail_info
            #边界
            elif '分布' in detail_info:
                info_data['分布'] = detail_info
            #边缘
            elif any(a in detail_info for a in ['边缘','边界']) and (not any( a in detail_info for a in ['可见','CDFI','边缘型'])):
                info_data['边缘'] = detail_info
            #后方回声
            elif any(word in detail_info for word in ['后方回声','后方伴声衰减','后方伴回声增强']): 
                info_data['后方回声'] = detail_info
            #内部回声  
            elif '内部' in detail_info:
                info_data['内部回声'] = detail_info
            #钙化
            elif any(a in detail_info for a in['钙化','状强回声',]):
                info_data['钙化'] = detail_info
            #CDFI
            elif 'CDFI' in detail_info and '血流' in detail_info:
                info_data['CDFI'] = detail_info


        for i in range(len(positions)):
            #有多个值的时候，就生成多个位置、大小不同，但其他描述共享的字典对象
            info_data['位置'] = positions[i]
            info_data['大小'] = sizes[i % len(sizes)] #预防下标越界
            info_data['描述'] = describes[i % len(describes)]
            output_list.append(dict(info_data))  #将字典对象逐个加入输出的列表里
            
        
    return output_list  #输出
    
    
if __name__ == '__main__':
    #测试 parse_sonography
    #改成从文件中读取，你可以试着把超声检查的内容复制到文本文件中测试
    '''  
    testdata_file = open('testdata.txt',encoding="utf-8")
    #读取整个文件中的内容
    testdata = testdata_file.read()
        
    index = 0
    
    for i in parse_sonography(testdata):
        
        print('-----',index,'-----')
        print('描述：' + i['描述'])
        print('位置：' + i['位置'])
        print('大小：' + i['大小'])
        print('形态：' + i['形态'])
        print('生长方向：' + i['生长方向'])
        print('边缘：' + i['边缘'])
        print('分布：' + i['分布'])
        print('内部回声：' + i['内部回声'])
        print('钙化：' + i['钙化'])
        print('后方回声：' + i['后方回声'])
        print('CDFI：' + i['CDFI'])
        index += 1
    '''
    #测试 parse_pathology

    testdata_file = open('test_pathology.txt',encoding="utf-8")

    testdata = testdata_file.read()

    index = 0

    result = parse_pathology(testdata)

    for i in result:
        print('-----',index,'-----')
        for k,y in i.items():
            print("{} : {}".format(k,y))

        index += 1
        



