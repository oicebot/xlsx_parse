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
    
    
def parse_pathology(intext=''):
    intext = intext.replace('\n',' ')    #先把所有回车替换成空格。
    full_text=intext.split('。')         #将整个字符串用句号分割开，每个句子变成数组里的一个元素
    
    #TODO：提取分析结果是什么细胞

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
        
        #构建一个字典，描述就是句子的第一个小分句  info_list[0] 相当于 数组 info_list 的第0个元素
        
        info_data = {'描述':'',
                     '位置':'',
                     '大小':'',
                     '形态':'',
                     '生长方向':'',
                     '边缘':'',
                     '分布':'',
                     '内部回声':'',
                     '钙化':'',
                     '后方回声':'', }
                     
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
            elif ('边缘' in detail_info or '边界' in detail_info ) and (not '可见' in detail_info) and (not 'CDFI' in detail_info):
                info_data['边缘'] = detail_info
            #后方回声
            elif any(word in detail_info for word in ['后方回声','后方伴声衰减']): 
                info_data['后方回声'] = detail_info
            #内部回声  
            elif '内部' in detail_info:
                info_data['内部回声'] = detail_info
            #钙化
            elif any(a in detail_info for a in['钙化','状强回声',]):
                info_data['钙化'] = detail_info


        for i in range(len(positions)):
            #有多个值的时候，就生成多个位置、大小不同，但其他描述共享的字典对象
            info_data['位置'] = positions[i]
            info_data['大小'] = sizes[i % len(sizes)] #预防下标越界
            info_data['描述'] = describes[i % len(describes)]
            output_list.append(dict(info_data))  #将字典对象逐个加入输出的列表里
            
        
    return output_list  #输出
    
    
if __name__ == '__main__':
    #改成从文件中读取，你可以试着把超声检查的内容复制到文本文件中测试
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
        index += 1
        
#运行方法，用 Python IDLE 打开，按 F5 运行
        



