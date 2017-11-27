import pickle

from pypinyin import lazy_pinyin
from pyexcel_xlsx import get_data


def get_no(zone, community):
    return ''.join([s[0].upper() for s in lazy_pinyin(zone + community)])

def get_pump_house():
    all_data = get_data('二次供水设施档案核对整理汇总（霍工）.xlsx')['Sheet1']
    for index, row in enumerate(all_data[4:-1], start=4):
        if not row or row[0] is None:
            continue
            
        _dict = {}
        _dict['title'] = ''.join(['{:0>3}'.format(row[0]), row[2]])
        print('start ', _dict['title'])
        
        if row[8] is None:
            top = row[6] if row[6] is not None else 12
        else:
            top = row[8]
        _dict['No'] = ''.join([get_no('拱北', row[2]), '{:0>3}'.format(row[0]), '{:0>2}'.format(str(top)), 'B1'])
        
        _dict['小区名称'] = row[2]
        _dict['加压设施地址'] = row[3]
        _dict['设施竣工时间'] = ''
        _dict['设施接收时间'] = ''
        try:
            _dict['独立电表表号'] = int(row[67])
        except (TypeError, ValueError, IndexError):
            _dict['独立电表表号'] = ''
        
        _dict['供水所:单位名称'] = '珠海水务集团拱北供水所'
        _dict['供水所:联系人'] = ''
        _dict['供水所:联系电话'] = ''
        _dict['维护单位:单位名称'] = '多特机电设备有限公司'
        _dict['维护单位:联系人'] = ''
        _dict['维护单位:联系电话'] = ''
        _dict['建设单位:单位名称'] = ''
        _dict['建设单位:联系人'] = ''
        _dict['建设单位:联系电话'] = ''
        _dict['物管单位:单位名称'] = row[62] if row[62] is not None else ''
        _dict['物管单位:联系人'] = row[63] if row[63] is not None else ''
        _dict['物管单位:联系电话'] = row[64] if row[64] is not None else ''
        
        _dict['加压总户数'] = row[66] if row[66] is not None else ''
        
        _dict['PLC:型号'] = row[56] if row[56] is not None else ''
        _dict['PLC:品牌'] = row[57] if row[57] is not None else ''
        
        _dict['VFD:型号'] = row[53] if row[53] is not None else ''
        _dict['VFD:品牌'] = row[54] if row[54] is not None else ''
        
        if all_data[index + 1][0] is not None:
         
            _dict['直供:临界'] = row[4] if row[4] is not None else 0
            _dict['一区:临界'] = row[6] if row[6] is not None else ''
            _dict['二区:临界'] = row[8] if row[8] is not None else ''
            
            if row[8]:
                _dict['分区'] = 2
            else:
                _dict['分区'] = 1
            
            _dict['一区:设定压力'] = row[19] if row[19] is not None else ''
            
            _dict['一区:主泵:数量'] = _dict['一区:电机:数量'] = row[18] if row[18] is not None else ''
            _dict['一区:主泵:型号'] = row[9] if row[9] is not None else ''
            _dict['一区:主泵:品牌'] = row[10] if row[10] is not None else ''
            _dict['一区:电机:型号'] = row[13] if row[13] is not None else ''
            _dict['一区:电机:品牌'] = row[14] if row[14] is not None else ''
            
            _dict['一区:辅泵:数量'] = _dict['一区:电机_f:数量'] = row[29] if row[29] is not None else ''
            _dict['一区:辅泵:型号'] = row[20] if row[20] is not None else ''
            _dict['一区:辅泵:品牌'] = row[21] if row[21] is not None else ''
            _dict['一区:电机_f:型号'] = row[24] if row[24] is not None else ''
            _dict['一区:电机_f:品牌'] = row[25] if row[25] is not None else ''
            
            _dict['一区:气压罐:数量'] = 1 if row[58] is not None else ''
            _dict['一区:气压罐:型号'] = row[58] if row[58] is not None else ''
            _dict['一区:气压罐:品牌'] = row[59] if row[59] is not None else ''
            _dict['一区:气压罐:V'] = row[58] if row[58] is not None else ''
            
            _dict['一区:控制:数量'] = 1 if row[57] is not None else ''
            _dict['一区:控制:型号'] = row[56] if row[56] is not None else ''
            _dict['一区:控制:品牌'] = row[57] if row[57] is not None else ''
            
            _dict['一区:控制:PLC'] = row[56] if row[56] is not None else ''
            _dict['一区:控制:VFD'] = row[53] if row[53] is not None else ''
            _dict['一区:控制:U'] = 380 if row[56] is not None else ''
            _dict['一区:控制:N'] = row[27] if row[56] is not None else ''

            _dict['一区:主泵:H'] = row[11] if row[11] is not None else ''
            _dict['一区:主泵:Q'] = row[12] if row[12] is not None else ''
            
            _dict['一区:电机:U'] = 380 if row[16] is not None else ''
            _dict['一区:电机:N'] = row[16] if row[16] is not None else ''
            _dict['一区:电机:n'] = row[17] if row[17] is not None else ''
            _dict['一区:电机:密封'] = row[15] if row[15] is not None else ''
            
            _dict['一区:辅泵:H'] = row[22] if row[22] is not None else ''
            _dict['一区:辅泵:Q'] = row[23] if row[23] is not None else ''
            
            _dict['一区:电机_f:U'] = 380 if row[27] is not None else ''
            _dict['一区:电机_f:N'] = row[27] if row[27] is not None else ''
            _dict['一区:电机_f:n'] = row[28] if row[28] is not None else ''
            _dict['一区:电机_f:密封'] = row[26] if row[26] is not None else ''
            
            _dict['一区:总出水管径(mm)'] = row[60] if row[60] is not None else ''
            _dict['一区:管材'] = row[61] if row[61] is not None else ''
            _dict['一区:供水方式'] = row[65] if row[65] is not None else ''
            _dict['一区:泵组流量上限Q'] = _dict['一区:主泵:Q'] * _dict['一区:主泵:数量'] if _dict['一区:主泵:Q'] and _dict['一区:主泵:数量'] else ''
            _dict['一区:泵组扬程上限H'] = _dict['一区:主泵:H'] if _dict['一区:主泵:H'] else ''
            _dict['一区:供水户数'] = _dict['加压总户数'] // _dict['分区']  if _dict['加压总户数'] else ''

            # ------------------------------------------------------------------------------------------
            if _dict['分区'] == 2:
                
                _dict['二区:设定压力'] = row[19  + 22] if row[19  + 22] is not None else ''
                
                _dict['二区:主泵:数量'] = _dict['二区:电机:数量'] = row[18 + 22] if row[18 + 22] is not None else ''
                _dict['二区:主泵:型号'] = row[9 + 22] if row[9 + 22] is not None else ''
                _dict['二区:主泵:品牌'] = row[10 + 22] if row[10 + 22] is not None else ''
                _dict['二区:电机:型号'] = row[13 + 22] if row[13 + 22] is not None else ''
                _dict['二区:电机:品牌'] = row[14 + 22] if row[14 + 22] is not None else ''
                
                _dict['二区:辅泵:数量'] = _dict['二区:电机_f:数量'] = row[29 + 22] if row[29 + 22] is not None else ''
                _dict['二区:辅泵:型号'] = row[20 + 22] if row[20 + 22] is not None else ''
                _dict['二区:辅泵:品牌'] = row[21 + 22] if row[21 + 22] is not None else ''
                _dict['二区:电机_f:型号'] = row[24 + 22] if row[24 + 22] is not None else ''
                _dict['二区:电机_f:品牌'] = row[25 + 22] if row[25 + 22] is not None else ''


                _dict['二区:主泵:H'] = row[11 + 22] if row[11 + 22] is not None else ''
                _dict['二区:主泵:Q'] = row[12 + 22] if row[12 + 22] is not None else ''
                
                _dict['二区:电机:U'] = 380 if row[16 + 22] is not None else ''
                _dict['二区:电机:N'] = row[16 + 22] if row[16 + 22] is not None else ''
                _dict['二区:电机:n'] = row[17 + 22] if row[17 + 22] is not None else ''
                _dict['二区:电机:密封'] = row[15 + 22] if row[15 + 22] is not None else ''
                
                _dict['二区:辅泵:H'] = row[22 + 22] if row[22 + 22] is not None else ''
                _dict['二区:辅泵:Q'] = row[23 + 22] if row[23 + 22] is not None else ''
                
                _dict['二区:电机_f:U'] = 380 if row[27 + 22] is not None else ''
                _dict['二区:电机_f:N'] = row[27 + 22] if row[27 + 22] is not None else ''
                _dict['二区:电机_f:n'] = row[28 + 22] if row[28 + 22] is not None else ''
                _dict['二区:电机_f:密封'] = row[26 + 22] if row[26 + 22] is not None else ''
                        
                _dict['二区:气压罐:数量'] = 1 if row[58] is not None else ''
                _dict['二区:气压罐:型号'] = row[58] if row[58] is not None else ''
                _dict['二区:气压罐:品牌'] = row[59] if row[59] is not None else ''
                _dict['二区:气压罐:V'] = row[58] if row[58] is not None else ''
                
                _dict['二区:控制:数量'] = 1 if row[57 ] is not None else ''
                _dict['二区:控制:型号'] = row[56] if row[56] is not None else ''
                _dict['二区:控制:品牌'] = row[57] if row[57] is not None else ''
                

                _dict['二区:总出水管径(mm)'] = _dict['一区:总出水管径(mm)']
                _dict['二区:管材'] = _dict['一区:管材']
                _dict['二区:供水方式'] = _dict['一区:供水方式']
                _dict['二区:泵组流量上限Q'] = _dict['二区:主泵:Q'] * _dict['二区:主泵:数量'] if _dict['二区:主泵:Q'] and _dict['二区:主泵:数量'] else ''
                _dict['二区:泵组扬程上限H'] = _dict['二区:主泵:H'] if _dict['二区:主泵:H'] else ''
                _dict['二区:供水户数'] = _dict['加压总户数'] // _dict['分区']  if _dict['加压总户数'] else ''
            
        else:
            _next_row = all_data[index + 1]
            _dict['分区'] = 3
            _dict['直供:临界'] = row[4] if row[4] is not None else 0
            _dict['一区:临界'] = _next_row[6] if _next_row[6] is not None else ''
            _dict['二区:临界'] = row[6] if row[6] is not None else ''
            _dict['三区:临界'] = row[8] if row[8] is not None else 0
        
            # ------------------------------------------------------------------------
        
            _dict['一区:设定压力'] = _next_row[19] if _next_row[19] is not None else ''
            
            _dict['一区:主泵:数量'] = _dict['一区:电机:数量'] = _next_row[18] if _next_row[18] is not None else ''
            _dict['一区:主泵:型号'] = _next_row[9] if _next_row[9] is not None else ''
            _dict['一区:主泵:品牌'] = _next_row[10] if _next_row[10] is not None else ''
            _dict['一区:电机:型号'] = _next_row[13] if _next_row[13] is not None else ''
            _dict['一区:电机:品牌'] = _next_row[14] if _next_row[14] is not None else ''
            
            _dict['一区:辅泵:数量'] = _dict['一区:电机_f:数量'] = _next_row[29] if _next_row[29] is not None else ''
            _dict['一区:辅泵:型号'] = _next_row[20] if _next_row[20] is not None else ''
            _dict['一区:辅泵:品牌'] = _next_row[21] if _next_row[21] is not None else ''
            _dict['一区:电机_f:型号'] = _next_row[24] if _next_row[24] is not None else ''
            _dict['一区:电机_f:品牌'] = _next_row[25] if _next_row[25] is not None else ''
            
            _dict['一区:气压罐:数量'] = 1 if _next_row[58] is not None else ''
            _dict['一区:气压罐:型号'] = _next_row[58] if _next_row[58] is not None else ''
            _dict['一区:气压罐:品牌'] = _next_row[59] if _next_row[59] is not None else ''
            _dict['一区:气压罐:V'] = _next_row[58] if _next_row[58] is not None else ''
            
            _dict['一区:控制:数量'] = 1 if _next_row[57] is not None else ''
            _dict['一区:控制:型号'] = _next_row[56] if _next_row[56] is not None else ''
            _dict['一区:控制:品牌'] = _next_row[57] if _next_row[57] is not None else ''

            _dict['一区:主泵:H'] = _next_row[11] if _next_row[11] is not None else ''
            _dict['一区:主泵:Q'] = _next_row[12] if _next_row[12] is not None else ''
            
            _dict['一区:电机:U'] = 380 if _next_row[16] is not None else ''
            _dict['一区:电机:N'] = _next_row[16] if _next_row[16] is not None else ''
            _dict['一区:电机:n'] = _next_row[17] if _next_row[17] is not None else ''
            _dict['一区:电机:密封'] = _next_row[15] if _next_row[15] is not None else ''
            
            _dict['一区:辅泵:H'] = _next_row[22] if _next_row[22] is not None else ''
            _dict['一区:辅泵:Q'] = _next_row[23] if _next_row[23] is not None else ''
            
            _dict['一区:电机_f:U'] = 380 if _next_row[27] is not None else ''
            _dict['一区:电机_f:N'] = _next_row[27] if _next_row[27] is not None else ''
            _dict['一区:电机_f:n'] = _next_row[28] if _next_row[28] is not None else ''
            _dict['一区:电机_f:密封'] = _next_row[26] if _next_row[26] is not None else ''
            
            _dict['一区:总出水管径(mm)'] = row[60] if row[60] is not None else ''
            _dict['一区:管材'] = row[61] if row[61] is not None else ''
            _dict['一区:供水方式'] = row[65] if row[65] is not None else ''
            _dict['一区:泵组流量上限Q'] = _dict['一区:主泵:Q'] * _dict['一区:主泵:数量'] if _dict['一区:主泵:Q'] and _dict['一区:主泵:数量'] else ''
            _dict['一区:泵组扬程上限H'] = _dict['一区:主泵:H'] if _dict['一区:主泵:H'] else ''
            _dict['一区:供水户数'] = _dict['加压总户数'] // _dict['分区']  if _dict['加压总户数'] else ''

            # ------------------------------------------------------------------------------
            
            _dict['二区:设定压力'] = row[19] if row[19] is not None else ''
            
            _dict['二区:主泵:数量'] = _dict['二区:电机:数量'] = row[18] if row[18] is not None else ''
            _dict['二区:主泵:型号'] = row[9] if row[9] is not None else ''
            _dict['二区:主泵:品牌'] = row[10] if row[10] is not None else ''
            _dict['二区:电机:型号'] = row[13] if row[13] is not None else ''
            _dict['二区:电机:品牌'] = row[14] if row[14] is not None else ''
            
            _dict['二区:辅泵:数量'] = _dict['二区:电机_f:数量'] = row[29] if row[29] is not None else ''
            _dict['二区:辅泵:型号'] = row[20] if row[20] is not None else ''
            _dict['二区:辅泵:品牌'] = row[21] if row[21] is not None else ''
            _dict['二区:电机_f:型号'] = row[24] if row[24] is not None else ''
            _dict['二区:电机_f:品牌'] = row[25] if row[25] is not None else ''
            
            _dict['二区:气压罐:数量'] = 1 if row[58] is not None else ''
            _dict['二区:气压罐:型号'] = row[58] if row[58] is not None else ''
            _dict['二区:气压罐:品牌'] = row[59] if row[59] is not None else ''
            _dict['二区:气压罐:V'] = row[58] if row[58] is not None else ''
            
            _dict['二区:控制:数量'] = 1 if row[57] is not None else ''
            _dict['二区:控制:型号'] = row[56] if row[56] is not None else ''
            _dict['二区:控制:品牌'] = row[57] if row[57] is not None else ''

            _dict['二区:主泵:H'] = row[11] if row[11] is not None else ''
            _dict['二区:主泵:Q'] = row[12] if row[12] is not None else ''
            
            _dict['二区:电机:U'] = 380 if row[16] is not None else ''
            _dict['二区:电机:N'] = row[16] if row[16] is not None else ''
            _dict['二区:电机:n'] = row[17] if row[17] is not None else ''
            _dict['二区:电机:密封'] = row[15] if row[15] is not None else ''
            
            _dict['二区:辅泵:H'] = row[22] if row[22] is not None else ''
            _dict['二区:辅泵:Q'] = row[23] if row[23] is not None else ''
            
            _dict['二区:电机_f:U'] = 380 if row[27] is not None else ''
            _dict['二区:电机_f:N'] = row[27] if row[27] is not None else ''
            _dict['二区:电机_f:n'] = row[28] if row[28] is not None else ''
            _dict['二区:电机_f:密封'] = row[26] if row[26] is not None else ''
            
            _dict['二区:总出水管径(mm)'] = row[60] if row[60] is not None else ''
            _dict['二区:管材'] = row[61] if row[61] is not None else ''
            _dict['二区:供水方式'] = row[65] if row[65] is not None else ''
            _dict['二区:泵组流量上限Q'] = _dict['二区:主泵:Q'] * _dict['二区:主泵:数量'] if _dict['二区:主泵:Q'] and _dict['二区:主泵:数量'] else ''
            _dict['二区:泵组扬程上限H'] = _dict['二区:主泵:H'] if _dict['二区:主泵:H'] else ''
            _dict['二区:供水户数'] = _dict['加压总户数'] // _dict['分区']  if _dict['加压总户数'] else ''

            
            # ------------------------------------------------------------------------------------------
            
            _dict['三区:设定压力'] = row[19  + 22] if row[19  + 22] is not None else ''
            
            _dict['三区:主泵:数量'] = _dict['三区:电机:数量'] = row[18 + 22] if row[18 + 22] is not None else ''
            _dict['三区:主泵:型号'] = row[9 + 22] if row[9 + 22] is not None else ''
            _dict['三区:主泵:品牌'] = row[10 + 22] if row[10 + 22] is not None else ''
            _dict['三区:电机:型号'] = row[13 + 22] if row[13 + 22] is not None else ''
            _dict['三区:电机:品牌'] = row[14 + 22] if row[14 + 22] is not None else ''
            
            _dict['三区:辅泵:数量'] = _dict['三区:电机_f:数量'] = row[29 + 22] if row[29 + 22] is not None else ''
            _dict['三区:辅泵:型号'] = row[20 + 22] if row[20 + 22] is not None else ''
            _dict['三区:辅泵:品牌'] = row[21 + 22] if row[21 + 22] is not None else ''
            _dict['三区:电机_f:型号'] = row[24 + 22] if row[24 + 22] is not None else ''
            _dict['三区:电机_f:品牌'] = row[25 + 22] if row[25 + 22] is not None else ''


            _dict['三区:主泵:H'] = row[11 + 22] if row[11 + 22] is not None else ''
            _dict['三区:主泵:Q'] = row[12 + 22] if row[12 + 22] is not None else ''
            
            _dict['三区:电机:U'] = 380 if row[16 + 22] is not None else ''
            _dict['三区:电机:N'] = row[16 + 22] if row[16 + 22] is not None else ''
            _dict['三区:电机:n'] = row[17 + 22] if row[17 + 22] is not None else ''
            _dict['三区:电机:密封'] = row[15 + 22] if row[15 + 22] is not None else ''
            
            _dict['三区:辅泵:H'] = row[22 + 22] if row[22 + 22] is not None else ''
            _dict['三区:辅泵:Q'] = row[23 + 22] if row[23 + 22] is not None else ''
            
            _dict['三区:电机_f:U'] = 380 if row[27 + 22] is not None else ''
            _dict['三区:电机_f:N'] = row[27 + 22] if row[27 + 22] is not None else ''
            _dict['三区:电机_f:n'] = row[28 + 22] if row[28 + 22] is not None else ''
            _dict['三区:电机_f:密封'] = row[26 + 22] if row[26 + 22] is not None else ''
                    
            _dict['三区:气压罐:数量'] = 1 if row[58] is not None else ''
            _dict['三区:气压罐:型号'] = row[58] if row[58] is not None else ''
            _dict['三区:气压罐:品牌'] = row[59] if row[59] is not None else ''
            _dict['三区:气压罐:V'] = row[58] if row[58] is not None else ''
            
            _dict['三区:控制:数量'] = 1 if row[57 ] is not None else ''
            _dict['三区:控制:型号'] = row[56] if row[56] is not None else ''
            _dict['三区:控制:品牌'] = row[57] if row[57] is not None else ''
            

            _dict['三区:总出水管径(mm)'] = _dict['二区:总出水管径(mm)']
            _dict['三区:管材'] = _dict['二区:管材']
            _dict['三区:供水方式'] = _dict['一区:供水方式']
            _dict['三区:泵组流量上限Q'] = _dict['三区:主泵:Q'] * _dict['三区:主泵:数量'] if _dict['三区:主泵:Q'] and _dict['三区:主泵:数量'] else ''
            _dict['三区:泵组扬程上限H'] = _dict['三区:主泵:H'] if _dict['三区:主泵:H'] else ''
            _dict['三区:供水户数'] = _dict['加压总户数'] // _dict['分区']  if _dict['加压总户数'] else ''
        
        
        
        with open('./pickle_folder/{}'.format(_dict['title']), 'wb') as wf:
            pickle.dump(_dict, wf)
        # break
        
def get_water_tank():
    all_data = get_data('water.xlsx')['Sheet1'][4:92]
    
    for row in all_data:
        _dict = {}
        _dict['No'] = 'GB-{}-{}-{}'.format(row[2], row[3], row[4])
        _dict['小区名称'] = row[9]
        _dict['设施地址'] = row[10]
        _dict['设施竣工时间'] = ''
        _dict['设施接收时间'] = ''
        _dict['对应加压设施编号'] = ''
        
        _dict['供水所:单位名称'] = '珠海水务集团拱北供水所'
        _dict['供水所:联系人'] = '胡小勇'
        _dict['供水所:联系电话'] = '8132985'
        
        _dict['维护单位:单位名称'] = '珠海水务集团水池清洗队'
        _dict['维护单位:联系人'] = ''
        _dict['维护单位:联系电话'] = ''
        
        _dict['物业公司:单位名称'] = row[11]
        _dict['物业公司:联系人'] = row[12]
        _dict['物业公司:联系电话'] = row[13]
        
        _dict['建设单位:单位名称'] = ''
        _dict['建设单位:联系人'] = ''
        _dict['建设单位:联系电话'] =''
        
        _dict['长'] = row[16]
        _dict['宽'] = row[17]
        _dict['高'] = row[18]
        
        _dict['水箱材质'] = row[23]
        _dict['控制方式'] = row[24]
        _dict['进水口径'] = row[25] if row[25] is not None else ''
        _dict['出水口径'] = row[26] if row[26] is not None else ''
        _dict['排水状况'] = '顺畅'
        _dict['消防水位（m）'] = ''
        
        _dict['供水户数'] = row[15]
        _dict['供水楼栋范围'] = ''
        
        _dict['最大有效容积（m³）'] = row[19]
        _dict['溢流口高度（m）'] = row[20] if row[20] is not None else ''
        _dict['设定水位（m）'] = row[21] if row[21] is not None else ''
        
        _dict['内外扶梯'] = '有'
        _dict['三孔防污'] = '有'
        _dict['集水坑'] = '有'
        
        _dict['资料核准人员'] = '敖荣健'
        
        with open('./pickle_folder/water/{}'.format(_dict['No']), 'wb') as wf:
            pickle.dump(_dict, wf)
        
        
if __name__ == '__main__':
    get_pump_house()
    # get_water_tank()
    