from itertools import zip_longest

import xlsxwriter


class MyDict(dict):
    def get(self, key):
        if key == '直供:供水户数': 
            if super().get('直供:临界'):
                return 4 * int(super().get('直供:临界'))
            else:
                return 0
        return str(super().get(key, ''))


def sheet_one(data, filename=None,sheet1=True, sheet2=True, sheet3=True):
    DATA = MyDict(data)
    
    if filename is None:
        filename = './ph/{}.xlsx'.format(data.get('title', 'test'))
    
    with xlsxwriter.Workbook(filename) as wb:
        if sheet1:
            worksheet = wb.add_worksheet('供水设施档案')

            worksheet.set_column(0, 0, 12)
            worksheet.set_column(1, 1, 10)
            worksheet.set_column(2, 2, 5)
            worksheet.set_column(3, 3, 15)
            worksheet.set_column(4, 4, 10)
            worksheet.set_column(5, 5, 5)
            worksheet.set_column(6, 6, 6)
            worksheet.set_column(7, 7, 5)
            worksheet.set_column(8, 8, 6)
            worksheet.set_column(9, 9, 5)
            worksheet.set_column(10, 10, 10)
            worksheet.set_column(11, 11, 5)
            worksheet.set_column(12, 12, 10)
            worksheet.set_column(13, 14, 15)

            worksheet.set_row(0, 45)
            for r in range(1, 47):
                worksheet.set_row(r, 30)

            common_format = {
                'align': 'center',
                'valign': 'vcenter',
                'font_size': 12,
                'font_name': '仿宋',
                'border': 1,
            }

            title_format = wb.add_format({
                'bold': True,
                'align': 'center',
                'valign': 'vcenter',
                'font_size': 22,
                'font_name': '仿宋',
            })
            worksheet.merge_range('D1:M1', '珠海市二次供水设施基础档案信息表', title_format)

            worksheet.write_string('N1', '编号：',
                                   wb.add_format(
                                       {'align': 'right', 'valign': 'vcenter', 'font_size': 12, 'font_name': '仿宋', }))
            worksheet.write_string('O1', DATA.get('No'),
                                   wb.add_format({'valign': 'vcenter', 'font_size': 12, 'font_name': '仿宋', }))

            # -----------------------------------------------------------------------

            tmp = dict(common_format)
            tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'top': 2, 'left': 2})
            worksheet.merge_range('A2:C2', '小区名称', wb.add_format(tmp))

            for r, s in zip(range(3, 6), ['加压设施地址', '设施竣工时间', '设施接收时间']):
                tmp = dict(common_format)
                tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'left': 2})
                worksheet.merge_range('A{r}:C{r}'.format(r=r), s, wb.add_format(tmp))

            tmp = dict(common_format)
            tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'bottom': 2, 'left': 2})
            worksheet.merge_range('A6:C6', '独立电表表号', wb.add_format(tmp))

            # -----------------------------------------------------------------------

            tmp = dict(common_format)
            tmp.update({'top': 2, 'right': 2})
            worksheet.merge_range('D2:G2', DATA.get('小区名称'), wb.add_format(tmp))

            for r, s in zip(range(3, 6), ['加压设施地址', '设施竣工时间', '设施接收时间']):
                tmp = dict(common_format)
                tmp.update({'right': 2})
                worksheet.merge_range('D{r}:G{r}'.format(r=r), DATA.get(s), wb.add_format(tmp))

            tmp = dict(common_format)
            tmp.update({'bottom': 2, 'right': 2})
            worksheet.merge_range('D6:G6', DATA.get('独立电表表号'), wb.add_format(tmp))

            # -----------------------------------------------------------------------

            tmp = dict(common_format)
            tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'top': 2, 'left': 2})
            worksheet.merge_range('H2:I2', '责任单位', wb.add_format(tmp))

            for r, s in zip(range(3, 6), ['供水所', '维护单位', '建设单位']):
                tmp = dict(common_format)
                tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'left': 2})
                worksheet.merge_range('H{r}:I{r}'.format(r=r), s, wb.add_format(tmp))

            tmp = dict(common_format)
            tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'bottom': 2, 'left': 2})
            worksheet.merge_range('H6:I6', '物管单位', wb.add_format(tmp))

            tmp = dict(common_format)
            tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'top': 2})
            worksheet.merge_range('J2:M2', '单位名称', wb.add_format(tmp))
            worksheet.write_string('N2', '联系人', wb.add_format(tmp))

            tmp = dict(common_format)
            tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'top': 2, 'right': 2})
            worksheet.write_string('O2', '联系电话', wb.add_format(tmp))

            # -----------------------------------------------------------------------

            for r, s in zip(range(3, 6), ['供水所', '维护单位', '建设单位']):
                worksheet.merge_range('J{r}:M{r}'.format(r=r), DATA.get('{}:单位名称'.format(s)), wb.add_format(common_format))
                worksheet.write_string('N{}'.format(r), DATA.get('{}:联系人'.format(s)), wb.add_format(common_format))
                tmp = dict(common_format)
                tmp.update({'right': 2})
                worksheet.write_string('O{}'.format(r), DATA.get('{}:联系电话'.format(s)), wb.add_format(tmp))

            tmp = dict(common_format)
            tmp.update({'bottom': 2})
            worksheet.merge_range('J6:M6', DATA.get('物管单位:单位名称'), wb.add_format(tmp))
            worksheet.write_string('N6', DATA.get('物管单位:联系人'), wb.add_format(tmp))
            tmp.update({'right': 2})
            worksheet.write_string('O6', DATA.get('物管单位:联系电话'), wb.add_format(tmp))

            # -----------------------------------------------------------------------

            tmp = dict(common_format)
            tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'border': 2})
            for c, s in zip(['A', 'B', 'C', 'D', 'E'], ['分区', '设备名称', '数量', '型号', '品牌']):
                worksheet.merge_range('{c}7:{c}8'.format(c=c), s, wb.add_format(tmp))

            worksheet.merge_range('F7:M8', '主要技术参数', wb.add_format(tmp))

            tmp = dict(common_format)
            tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'border': 2, 'bottom': 1})
            worksheet.merge_range('N7:O7', '机组综合信息', wb.add_format(tmp))

            tmp = dict(common_format)
            tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'left': 2, 'bottom': 2})
            worksheet.write_string('N8', '加压总户数', wb.add_format(tmp))

            tmp = dict(common_format)
            tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'right': 2, 'bottom': 2})
            worksheet.write_string('O8', DATA.get('加压总户数'), wb.add_format(tmp))

            # -----------------------------------------------------------------------

            tmp = dict(common_format)
            tmp.update({'border': 2, 'right': 1})
            worksheet.write_string('A9', '直供', wb.add_format(tmp))

            tmp.update({'left': 1})
            worksheet.write_string('B9', '入泵房阀门', wb.add_format(tmp))
            worksheet.write_string('C9', DATA.get('直供:数量'), wb.add_format(tmp))
            worksheet.write_string('D9', DATA.get('直供:型号'), wb.add_format(tmp))

            tmp.update({'right': 2})
            worksheet.write_string('E9', DATA.get('直供:品牌'), wb.add_format(tmp))

            # -----------------------------------------------------------------------

            tmp = dict(common_format)
            tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'border': 2, 'right': 1, 'font_size': 9})
            worksheet.write_string('F9', '', wb.add_format(tmp))

            tmp = dict(common_format)
            tmp.update({'border': 2, 'right': 1, 'left': 1, 'font_size': 9})
            for i, c in enumerate(['G', 'H', 'I', 'J', 'K', 'L']):
                if i & 1:
                    _format = wb.add_format(tmp)
                    _format.set_pattern(1)
                    _format.set_bg_color('#B8B8B8')
                    if c == 'J':
                        worksheet.write_string('{}9'.format(c), 'D', _format)
                    elif c == 'L':
                        worksheet.write_string('{}9'.format(c), 'P', _format)
                    else:
                        worksheet.write_string('{}9'.format(c), '', _format)
                else:
                    if c == 'K':
                        worksheet.write_string('{}9'.format(c), DATA.get('直供:D'), wb.add_format(tmp))
                    else:
                        worksheet.write_string('{}9'.format(c), '', wb.add_format(tmp))

            tmp.update({'right': 2})
            worksheet.write_string('M9', DATA.get('直供:P'), wb.add_format(tmp))

            # -----------------------------------------------------------------------

            tmp = dict(common_format)
            tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'border': 2, 'right': 1})
            worksheet.write_string('N9', '供水户数', wb.add_format(tmp))

            tmp = dict(common_format)
            tmp.update({'border': 2, 'left': 1})
            worksheet.write_number('O9', DATA.get('直供:供水户数'), wb.add_format(tmp))

            # -----------------------------------------------------------------------

            for start_row, zone in zip(range(10, 40, 6), ['一区', '二区', '三区', '四区', '高位泵房']):
                tmp = dict(common_format)
                tmp.update({'top': 2, 'left': 2})
                worksheet.merge_range('A{}:A{}'.format(str(start_row), str(start_row + 1)), zone, wb.add_format(tmp))

                worksheet.write_string('A{}'.format(str(start_row + 2)), '设定压力', wb.add_format(tmp))
                worksheet.write_string('A{}'.format(str(start_row + 3)), DATA.get('{}:设定压力'.format(zone)),
                                       wb.add_format(tmp))

                tmp.update({'bg_color': '#B8B8B8', 'pattern': 1})
                worksheet.write_string('A{}'.format(str(start_row + 4)), '最不利点压力', wb.add_format(tmp))
                tmp.update({'bottom': 2})
                worksheet.write_string('A{}'.format(str(start_row + 5)), DATA.get('{}:最不利点压力'.format(zone)),
                                       wb.add_format(tmp))

                for r, item, detail in zip(range(start_row, start_row + 6),
                                           ['主泵', '电机', '辅泵', '电机_f', '气压罐', '控制'],
                                           ['总出水管径(mm)', '管材', '供水方式', '泵组流量上限Q', '泵组扬程上限H', '供水户数']):

                    if r == start_row:
                        tmp = dict(common_format)
                        tmp.update({'top': 2})
                        tmp2 = dict(common_format)
                        tmp2.update({'top': 2})
                        tmp3 = dict(common_format)
                        tmp3.update({'top': 2})
                    elif r == start_row + 5:
                        tmp = dict(common_format)
                        tmp.update({'bottom': 2})
                        tmp2 = dict(common_format)
                        tmp2.update({'bottom': 2})
                        tmp3 = dict(common_format)
                        tmp3.update({'bottom': 2})
                    else:
                        tmp = dict(common_format)
                        tmp2 = dict(common_format)
                        tmp3 = dict(common_format)
                    tmp2.update({'font_size': 9})

                    worksheet.write_string('B{}'.format(str(r)), item.replace('_f', ''), wb.add_format(tmp))
                    worksheet.write_string('C{}'.format(str(r)), DATA.get('{}:{}:数量'.format(zone, item)),
                                           wb.add_format(tmp))
                    worksheet.write_string('D{}'.format(str(r)), DATA.get('{}:{}:型号'.format(zone, item)),
                                           wb.add_format(tmp))
                    tmp.update({'right': 2})
                    worksheet.write_string('E{}'.format(str(r)), DATA.get('{}:{}:品牌'.format(zone, item)),
                                           wb.add_format(tmp))

                    # --------------------------------------------------------------------------------

                    _f_format = wb.add_format(tmp2)
                    _f_format.set_left(2)
                    _f_format.set_pattern(1)
                    _f_format.set_bg_color('#B8B8B8')

                    if item in ['主泵', '辅泵']:
                        worksheet.write_string('F{}'.format(str(r)), 'H', _f_format)
                        _f_format.set_left(1)
                        worksheet.write_string('H{}'.format(str(r)), 'Q', _f_format)
                        worksheet.write_string('J{}'.format(str(r)), 'D', _f_format)
                        worksheet.write_string('L{}'.format(str(r)), 'Δh', _f_format)

                        worksheet.write_string('G{}'.format(str(r)), DATA.get('{}:{}:H'.format(zone, item)),
                                               wb.add_format(tmp2))
                        worksheet.write_string('I{}'.format(str(r)), DATA.get('{}:{}:Q'.format(zone, item)),
                                               wb.add_format(tmp2))
                        worksheet.write_string('K{}'.format(str(r)), DATA.get('{}:{}:D'.format(zone, item)),
                                               wb.add_format(tmp2))
                        tmp2.update({'right': 2})
                        worksheet.write_string('M{}'.format(str(r)), DATA.get('{}:{}:Δh'.format(zone, item)),
                                               wb.add_format(tmp2))

                    elif item in ['电机', '电机_f']:  #
                        worksheet.write_string('F{}'.format(str(r)), 'U', _f_format)
                        _f_format.set_left(1)
                        worksheet.write_string('H{}'.format(str(r)), 'N', _f_format)
                        worksheet.write_string('J{}'.format(str(r)), 'n', _f_format)
                        worksheet.write_string('L{}'.format(str(r)), '密封', _f_format)

                        worksheet.write_string('G{}'.format(str(r)), DATA.get('{}:{}:U'.format(zone, item)),
                                               wb.add_format(tmp2))
                        worksheet.write_string('I{}'.format(str(r)), DATA.get('{}:{}:N'.format(zone, item)),
                                               wb.add_format(tmp2))
                        worksheet.write_string('K{}'.format(str(r)), DATA.get('{}:{}:n'.format(zone, item)),
                                               wb.add_format(tmp2))
                        tmp2.update({'right': 2})
                        worksheet.write_string('M{}'.format(str(r)), DATA.get('{}:{}:密封'.format(zone, item)),
                                               wb.add_format(tmp2))

                    elif item == '气压罐':
                        worksheet.write_string('F{}'.format(str(r)), 'V', _f_format)
                        _f_format.set_left(1)
                        worksheet.write_string('H{}'.format(str(r)), 'Vs', _f_format)
                        worksheet.write_string('J{}'.format(str(r)), 'D', _f_format)
                        worksheet.write_string('L{}'.format(str(r)), 'P', _f_format)

                        worksheet.write_string('G{}'.format(str(r)), DATA.get('{}:{}:V'.format(zone, item)),
                                               wb.add_format(tmp2))
                        worksheet.write_string('I{}'.format(str(r)), DATA.get('{}:{}:Vs'.format(zone, item)),
                                               wb.add_format(tmp2))
                        worksheet.write_string('K{}'.format(str(r)), DATA.get('{}:{}:D'.format(zone, item)),
                                               wb.add_format(tmp2))
                        tmp2.update({'right': 2})
                        worksheet.write_string('M{}'.format(str(r)), DATA.get('{}:{}:P'.format(zone, item)),
                                               wb.add_format(tmp2))

                    else:
                        worksheet.write_string('F{}'.format(str(r)), 'U', _f_format)
                        _f_format.set_left(1)
                        worksheet.write_string('H{}'.format(str(r)), 'N', _f_format)
                        worksheet.write_string('J{}'.format(str(r)), 'VFD', _f_format)
                        worksheet.write_string('L{}'.format(str(r)), 'PLC', _f_format)

                        worksheet.write_string('G{}'.format(str(r)), DATA.get('{}:{}:U'.format(zone, item)),
                                               wb.add_format(tmp2))
                        worksheet.write_string('I{}'.format(str(r)), DATA.get('{}:{}:N'.format(zone, item)),
                                               wb.add_format(tmp2))
                        worksheet.write_string('K{}'.format(str(r)), DATA.get('{}:{}:VFD'.format(zone, item)),
                                               wb.add_format(tmp2))
                        tmp2.update({'right': 2})
                        worksheet.write_string('M{}'.format(str(r)), DATA.get('{}:{}:PLC'.format(zone, item)),
                                               wb.add_format(tmp2))

                    _l_format = wb.add_format(tmp3)
                    _l_format.set_left(2)
                    _l_format.set_pattern(1)
                    _l_format.set_bg_color('#B8B8B8')
                    worksheet.write_string('N{}'.format(str(r)), detail, _l_format)
                    tmp3.update({'right': 2})
                    worksheet.write_string('O{}'.format(str(r)), DATA.get('{}:{}'.format(zone, detail)),
                                           wb.add_format(tmp3))

            # -----------------------------------------------------------------------

            for start_row, zone in zip(range(40, 46, 3), ['排污（地下）', '排污（屋顶）']):
                _t_format = wb.add_format(common_format)
                _t_format.set_border(2)
                _t_format.set_left(1)
                worksheet.merge_range('A{}:A{}'.format(start_row, start_row + 2), zone, _t_format)

                for r, item in zip(range(start_row, start_row + 3), ['水泵', '电机', '控制']):
                    tmp = dict(common_format)
                    tmp2 = dict(common_format)
                    tmp2.update({'font_size': 9})
                    if r == start_row:
                        tmp.update({'top': 2})
                        tmp2.update({'top': 2})
                    elif r == start_row + 2:
                        tmp.update({'bottom': 2})
                        tmp2.update({'bottom': 2})

                    worksheet.write_string('B{}'.format(str(r)), item, wb.add_format(tmp))
                    worksheet.write_string('C{}'.format(str(r)), DATA.get('{}:{}:数量'.format(zone, item)),
                                           wb.add_format(tmp))
                    worksheet.write_string('D{}'.format(str(r)), DATA.get('{}:{}:型号'.format(zone, item)),
                                           wb.add_format(tmp))
                    tmp.update({'right': 2})
                    worksheet.write_string('E{}'.format(str(r)), DATA.get('{}:{}:品牌'.format(zone, item)),
                                           wb.add_format(tmp))

                    _f_format = wb.add_format(tmp2)
                    _f_format.set_left(2)
                    _f_format.set_pattern(1)
                    _f_format.set_bg_color('#B8B8B8')

                    if item == '水泵':
                        worksheet.write_string('F{}'.format(str(r)), 'H', _f_format)
                        _f_format.set_left(1)
                        worksheet.write_string('H{}'.format(str(r)), 'Q', _f_format)
                        worksheet.write_string('J{}'.format(str(r)), 'D', _f_format)
                        worksheet.write_string('L{}'.format(str(r)), 'Δh', _f_format)

                        worksheet.write_string('G{}'.format(str(r)), DATA.get('{}:{}:H'.format(zone, item)),
                                               wb.add_format(tmp2))
                        worksheet.write_string('I{}'.format(str(r)), DATA.get('{}:{}:Q'.format(zone, item)),
                                               wb.add_format(tmp2))
                        worksheet.write_string('K{}'.format(str(r)), DATA.get('{}:{}:D'.format(zone, item)),
                                               wb.add_format(tmp2))
                        tmp2.update({'right': 2})
                        worksheet.write_string('M{}'.format(str(r)), DATA.get('{}:{}:Δh'.format(zone, item)),
                                               wb.add_format(tmp2))
                    elif item == '电机':
                        worksheet.write_string('F{}'.format(str(r)), 'U', _f_format)
                        _f_format.set_left(1)
                        worksheet.write_string('H{}'.format(str(r)), 'N', _f_format)
                        worksheet.write_string('J{}'.format(str(r)), 'n', _f_format)
                        worksheet.write_string('L{}'.format(str(r)), '密封', _f_format)

                        worksheet.write_string('G{}'.format(str(r)), DATA.get('{}:{}:U'.format(zone, item)),
                                               wb.add_format(tmp2))
                        worksheet.write_string('I{}'.format(str(r)), DATA.get('{}:{}:N'.format(zone, item)),
                                               wb.add_format(tmp2))
                        worksheet.write_string('K{}'.format(str(r)), DATA.get('{}:{}:n'.format(zone, item)),
                                               wb.add_format(tmp2))
                        tmp2.update({'right': 2})
                        worksheet.write_string('M{}'.format(str(r)), DATA.get('{}:{}:密封'.format(zone, item)),
                                               wb.add_format(tmp2))
                    else:
                        worksheet.write_string('F{}'.format(str(r)), 'U', _f_format)
                        _f_format.set_left(1)
                        worksheet.write_string('H{}'.format(str(r)), 'N', _f_format)
                        worksheet.write_string('J{}'.format(str(r)), 'VFD', _f_format)
                        worksheet.write_string('L{}'.format(str(r)), 'PLC', _f_format)

                        worksheet.write_string('G{}'.format(str(r)), DATA.get('{}:{}:U'.format(zone, item)),
                                               wb.add_format(tmp2))
                        worksheet.write_string('I{}'.format(str(r)), DATA.get('{}:{}:N'.format(zone, item)),
                                               wb.add_format(tmp2))
                        worksheet.write_string('K{}'.format(str(r)), DATA.get('{}:{}:VFD'.format(zone, item)),
                                               wb.add_format(tmp2))
                        tmp2.update({'right': 2})
                        worksheet.write_string('M{}'.format(str(r)), DATA.get('{}:{}:PLC'.format(zone, item)),
                                               wb.add_format(tmp2))

                _w_format = wb.add_format(common_format)
                _w_format.set_border(2)
                _w_format.set_bottom(1)
                _w_format.set_pattern(1)
                _w_format.set_bg_color('#B8B8B8')
                worksheet.merge_range('N{r}:O{r}'.format(r=start_row), '集水坑容积（长*宽*深）m³', _w_format)

                _w_format = wb.add_format(common_format)
                _w_format.set_border(2)
                _w_format.set_top(1)
                worksheet.merge_range('N{r}:O{r}'.format(r=start_row + 1), '', _w_format)

                _w_format.set_bottom(2)
                worksheet.merge_range('N{r}:O{r}'.format(r=start_row + 2), '', _w_format)

        if sheet2:
            chartsheet = wb.add_worksheet('分区情况表')
            chartsheet.set_column(0, 0, 10)
            chartsheet.set_column(1, 1, 5)
            chartsheet.set_column(2, 15, 8)
            chartsheet.set_row(0, 42)
            for r in range(1, 14):
                chartsheet.set_row(r, 24)
            
            title_format = wb.add_format({
                'bold': True,
                'align': 'center',
                'valign': 'vcenter',
                'font_size': 22,
                'font_name': '仿宋',
            })
            chartsheet.merge_range('A1:O1', '珠海市二次供水设施分区情况表', title_format)
            
            common_format = {
                'align': 'center',
                'valign': 'vcenter',
                'font_size': 12,
                'font_name': '仿宋',
                'border': 1,
            }
            
            _format = wb.add_format(common_format)
            _format.set_pattern(1)
            _format.set_bg_color('#B8B8B8')
            chartsheet.merge_range('A2:B2', '小区名字', _format)
            
            chartsheet.merge_range('F2:H2', '小区加压设施地址', _format)
            
            _format = wb.add_format(common_format)
            chartsheet.merge_range('C2:E2', DATA.get('小区名称'), _format)
            
            chartsheet.merge_range('I2:O2', DATA.get('加压设施地址'), _format)
            
            _format = wb.add_format(common_format)
            _format.set_pattern(1)
            _format.set_bg_color('#B8B8B8')
            chartsheet.merge_range('A3:A4', '分区', _format)
            chartsheet.merge_range('B3:B4', '方向', _format)
            
            for row, s in zip(range(5, 12), ['直供楼层', '一区楼层', '二区楼层', '三区楼层', '四区楼层', '楼顶', '总户数']):
                chartsheet.write_string('A{}'.format(row), s, _format)
            
            chartsheet.write_string('A12', '加压总户数', _format)
            
            _format = wb.add_format(common_format)
            
            for row, s in zip(range(5, 11), ['直供', '一区', '二区', '三区', '四区', '楼顶']):
                if DATA.get('{}:临界'.format(s)):
                    chartsheet.write_string('B{}'.format(row), '↑', _format)
                else:
                    chartsheet.write_string('B{}'.format(row), '', _format)
            
            for row in [11, 12]:
                chartsheet.write_string('B{}'.format(row), '', _format)
            
            chartsheet.merge_range('C3:E3', '全部', _format)
            for row, s in zip_longest(range(5, 13), ['直供', '一区', '二区', '三区', '四区', '楼顶']):
                if DATA.get('{}:临界'.format(s)):
                    chartsheet.write_number('C{}'.format(row), int(DATA.get('{}:临界'.format(s))), _format)
                else:
                    chartsheet.write_string('C{}'.format(row), DATA.get('{}:临界'.format(s)), _format)
                
                if DATA.get('{}:临界'.format(s)):
                    chartsheet.write_number('E{}'.format(row), int(DATA.get('{}:供水户数'.format(s))), _format)
                else:
                    chartsheet.write_string('E{}'.format(row), DATA.get('{}:供水户数'.format(s)), _format)

            _filled_format = wb.add_format(common_format)
            _filled_format.set_pattern(1)
            _filled_format.set_bg_color('#B8B8B8')
            for col, s in zip(['C', 'D', 'E'], ['临界层', '占据层数', '户数']):
                chartsheet.write_string('{}4'.format(col), s, _filled_format)

                
            chartsheet.write_formula('D5', '=C5-0', _filled_format)
            for row, s in zip_longest(range(6, 13), ['一区', '二区', '三区', '四区', '楼顶']):
                if DATA.get('{}:临界'.format(s)):
                    chartsheet.write_formula('D{}'.format(row), '=C{}-C{}'.format(row, row - 1), _filled_format)
                else:
                    chartsheet.write_string('D{}'.format(row), '', _filled_format)

            chartsheet.write_formula('E11', '=SUM(E5:E10)', _format)
            chartsheet.write_formula('E12', '=SUM(E6:E10)', _format)
            
            for col in [5, 8, 11]:
                chartsheet.merge_range(2, col, 2, col + 2, '', _format)
                for row in range(4, 12):
                    chartsheet.write_string(row, col, '', _format)
                    chartsheet.write_string(row, col + 2, '', _format)
                for offset, s in zip(range(3), ['临界层', '占据层数', '户数']):
                    chartsheet.write_string(3, col + offset, s, _filled_format)
                for row in range(4, 12):
                    chartsheet.write_string(row, col + 1, '', _filled_format)
                    
            chartsheet.merge_range('O3:O4', '总户数', _filled_format)
            for row in range(4, 13):
                chartsheet.write_formula('O{}'.format(row), '=E{}'.format(row), _format)
                
        if sheet3:
            equipment_sheet = wb.add_worksheet('控制柜配置清单')
            equipment_sheet.set_column(0, 1, 8)
            equipment_sheet.set_column(2, 2, 10)
            equipment_sheet.set_column(3, 3, 23)
            equipment_sheet.set_column(4, 4, 8)
            equipment_sheet.set_column(5, 5, 15)
            equipment_sheet.set_column(6, 6, 20)
            equipment_sheet.set_column(7, 7, 36)
            
            equipment_sheet.set_row(0, 42)
            equipment_sheet.set_row(1, 33)
            for r in range(2, 25):
                equipment_sheet.set_row(r, 25)
            
            title_format = wb.add_format({
                'bold': True,
                'align': 'center',
                'valign': 'vcenter',
                'font_size': 22,
                'font_name': '仿宋',
            })
            equipment_sheet.merge_range('A1:H1', '珠海市二次供水设施控制柜配置清单', title_format)
            
            common_format = {
                'align': 'center',
                'valign': 'vcenter',
                'font_size': 12,
                'font_name': '仿宋',
                'border': 1,
            }
            _format = wb.add_format(common_format)
            _format.set_bottom(2)
            
            equipment_sheet.merge_range('A2:C2', '对应加压设施编号', _format)
            equipment_sheet.write_string('D2', DATA.get('No'), _format)
            equipment_sheet.write_string('E2', '小区名称', _format)
            equipment_sheet.write_string('F2', DATA.get('小区名称'), _format)
            equipment_sheet.write_string('G2', '加压设施地址', _format)
            equipment_sheet.write_string('H2', DATA.get('小区加压设施地址'), _format)
            
            _format = wb.add_format(common_format)
            for col, s in enumerate(['序号', '加压分区', '英文代号', '名称', '数量', '型号规格', '品牌', '主要技术参数']):
                equipment_sheet.write_string(2, col, s, _format)
            
            _plc = DATA.get('一区:控制:PLC') or '0'
            _vfd = DATA.get('一区:控制:VFD') or '0'
            
            _tmp_list = []
            for i in [('PLC', '可编程控制器', _plc), ('VFD', '变频器', _vfd)]:
                if i[2] != '':
                    _tmp_list.append(i)
            
            for i, item in enumerate(_tmp_list, start=1):
                equipment_sheet.write_string(2 + i, 0, str(i),_format)
                equipment_sheet.write_string(2 + i, 1, '一区', _format)
                equipment_sheet.write_string(2 + i, 2, item[0], _format)
                equipment_sheet.write_string(2 + i, 3, item[1], _format)
                equipment_sheet.write_string(2 + i, 4, '1', _format)
                equipment_sheet.write_string(2 + i, 5, DATA.get('{}:型号'.format(item[0])), _format)
                equipment_sheet.write_string(2 + i, 6, DATA.get('{}:品牌'.format(item[0])), _format)    
                equipment_sheet.write_string(2 + i, 7, '', _format) 
                
def sheet_two(data, filename=None):
    _data = MyDict(data)
    
    if filename is None:
        filename = './wt/{}.xlsx'.format(data.get('title', 'test'))
        
    with xlsxwriter.Workbook(filename) as wb:
        worksheet = wb.add_worksheet('水池')

        worksheet.set_column(0, 32, 4)

        worksheet.set_row(0, 50)
        for r in range(1, 15):
            worksheet.set_row(r, 27)

        worksheet.merge_range('A1:G1', '')

        common_format = {
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 12,
            'font_name': '仿宋',
            'border': 1,
        }

        title_format = wb.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 22,
            'font_name': '仿宋',
        })

        worksheet.merge_range('H1:X1', '珠海市二次供水水池(箱)档案信息表', title_format)

        tmp = wb.add_format({
            'align': 'right',
            'valign': 'vcenter',
            'font_size': 12,
            'font_name': '仿宋',
        })
        worksheet.merge_range('Y1:Z1', '编号:', tmp)

        tmp.set_align('left')
        worksheet.merge_range('AA1:AE1', _data.get('No'), tmp)

        # -------------------------------------------------------------------------

        tmp = dict(common_format)
        tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'top': 2, 'left': 2})
        worksheet.merge_range('A2:E2', '小区名称', wb.add_format(tmp))

        for r, s in zip(range(3, 6), ['设施地址', '设施竣工时间', '设施接收时间']):
            tmp = dict(common_format)
            tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'left': 2})
            worksheet.merge_range('A{r}:E{r}'.format(r=r), s, wb.add_format(tmp))

        tmp = dict(common_format)
        tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'bottom': 2, 'left': 2})
        worksheet.merge_range('A6:E6', '对应加压设施编号', wb.add_format(tmp))

        # -----------------------------------------------------------------------

        tmp = dict(common_format)
        tmp.update({'top': 2})
        worksheet.merge_range('F2:L2', _data.get('小区名称'), wb.add_format(tmp))

        for r, s in zip(range(3, 6), ['设施地址', '设施竣工时间', '设施接收时间']):
            if r == 3:
                tmp = dict(common_format)
                worksheet.merge_range('F{r}:K{r}'.format(r=r), _data.get(s), wb.add_format(tmp))
                worksheet.write_string('L{r}'.format(r=r), _data.get('position'), wb.add_format(tmp))
            else:
                tmp = dict(common_format)
                worksheet.merge_range('F{r}:L{r}'.format(r=r), _data.get(s), wb.add_format(tmp))

        tmp = dict(common_format)
        tmp.update({'bottom': 2})
        worksheet.write_string('F6', '', wb.add_format(tmp))
        worksheet.merge_range('G6:K6', _data.get('对应加压设施编号'), wb.add_format(tmp))
        worksheet.write_string('L6', '', wb.add_format(tmp))

        # -----------------------------------------------------------------------

        tmp = dict(common_format)
        tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'top': 2})
        worksheet.merge_range('M2:O2', '责任单位', wb.add_format(tmp))

        for r, s in zip(range(3, 6), ['供水所', '维护单位', '物业公司']):
            tmp = dict(common_format)
            tmp.update({'bg_color': '#B8B8B8', 'pattern': 1})
            worksheet.merge_range('M{r}:O{r}'.format(r=r), s, wb.add_format(tmp))

        tmp = dict(common_format)
        tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'bottom': 2})
        worksheet.merge_range('M6:O6', '建设单位', wb.add_format(tmp))

        tmp = dict(common_format)
        tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'top': 2})
        worksheet.merge_range('P2:V2', '单位名称', wb.add_format(tmp))
        worksheet.merge_range('W2:Z2', '联系人', wb.add_format(tmp))
        
        tmp.update({'right': 2})
        worksheet.merge_range('AA2:AE2', '联系电话', wb.add_format(tmp))

        # -----------------------------------------------------------------------

        for r, s in zip(range(3, 6), ['供水所', '维护单位', '物业公司']):
            worksheet.merge_range('P{r}:V{r}'.format(r=r), _data.get('{}:单位名称'.format(s)), wb.add_format(common_format))
            worksheet.merge_range('W{r}:Z{r}'.format(r=r), _data.get('{}:联系人'.format(s)), wb.add_format(common_format))
            tmp = dict(common_format)
            tmp.update({'right': 2})
            worksheet.merge_range('AA{r}:AE{r}'.format(r=r), _data.get('{}:联系电话'.format(s)), wb.add_format(tmp))

        tmp = dict(common_format)
        tmp.update({'bottom': 2})
        worksheet.merge_range('P6:V6', _data.get('建设单位:单位名称'), wb.add_format(tmp))
        worksheet.merge_range('W6:Z6', _data.get('建设单位:联系人'), wb.add_format(tmp))
        tmp.update({'right': 2})
        worksheet.merge_range('AA6:AE6', _data.get('建设单位:联系电话'), wb.add_format(tmp))

        # -----------------------------------------------------------------------
        
        tmp = dict(common_format)
        tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'border': 2, 'right': 1, 'text_wrap': 1})
        worksheet.merge_range('A7:C9', '水箱尺寸（m）\n（不规则水箱规格参考简图）', wb.add_format(tmp))

        for r, s in zip(range(7, 10), ['长', '宽', '高']):
            tmp = dict(common_format)
            tmp.update({'bg_color': '#B8B8B8', 'pattern': 1})
            tmp2 = dict(common_format)
            tmp2.update({'right': 2})
            if r == 7:
                tmp.update({'top': 2})
                tmp2.update({'top': 2})
            elif r == 9:
                tmp.update({'bottom': 2})
                tmp2.update({'bottom': 2})
                
            worksheet.merge_range('D{r}:E{r}'.format(r=r), s, wb.add_format(tmp))
            worksheet.merge_range('F{r}:L{r}'.format(r=r), _data.get(s), wb.add_format(tmp2))

        # -----------------------------------------------------------------------------
        
        for r, s in zip(range(10, 13), ['最大有效容积（m³）', '溢流口高度（m）', '设定水位（m）']):
            tmp = dict(common_format)
            tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'left': 2})
            tmp2 = dict(common_format)
            tmp2.update({'right': 2})
            if r == 10:
                tmp.update({'top': 2})
                tmp2.update({'top': 2})
            elif r == 12:
                tmp.update({'bottom': 2})
                tmp2.update({'bottom': 2})
            worksheet.merge_range('A{r}:E{r}'.format(r=r), s, wb.add_format(tmp))
            worksheet.merge_range('F{r}:L{r}'.format(r=r), _data.get(s), wb.add_format(tmp2))
        
        # -----------------------------------------------------------------------------
        
        for r, s in zip(range(7, 13), ['水箱材质', '控制方式', '进水口径', '出水口径', '排水状况', '消防水位（m）']):
            tmp = dict(common_format)
            tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'left': 2})
            tmp2 = dict(common_format)
            tmp2.update({'right': 2})
            if r == 7:
                tmp.update({'top': 2})
                tmp2.update({'top': 2})
            elif r == 12:
                tmp.update({'bottom': 2})
                tmp2.update({'bottom': 2})
            worksheet.merge_range('M{r}:O{r}'.format(r=r), s, wb.add_format(tmp))
            worksheet.merge_range('P{r}:V{r}'.format(r=r), _data.get(s), wb.add_format(tmp2))
        
        # -----------------------------------------------------------------------------
        
        for r, s in zip(range(7, 9), ['供水户数', '供水楼栋范围']):
            tmp = dict(common_format)
            tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'left': 2})
            tmp2 = dict(common_format)
            tmp2.update({'right': 2})
            if r == 7:
                tmp.update({'top': 2})
                tmp2.update({'top': 2})
            elif r == 8:
                tmp.update({'bottom': 2})
                tmp2.update({'bottom': 2})
                
            worksheet.merge_range('W{r}:Z{r}'.format(r=r), s, wb.add_format(tmp))
            worksheet.merge_range('AA{r}:AE{r}'.format(r=r), _data.get(s), wb.add_format(tmp2))
        
        # -----------------------------------------------------------------------------
        
        tmp = dict(common_format)
        tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'border': 2, 'right': 1})
        worksheet.merge_range('W9:Z12', '附属功能', wb.add_format(tmp))
        
        # -----------------------------------------------------------------------------
        
        for r, s in zip(range(9, 13), ['消防共用', '内外扶梯', '三孔防污', '集水坑']):
            tmp = dict(common_format)
            tmp.update({'bg_color': '#B8B8B8', 'pattern': 1})
            tmp2 = dict(common_format)
            tmp2.update({'right': 2})
            if r == 9:
                tmp.update({'top': 2})
                tmp2.update({'top': 2})
            elif r == 12:
                tmp.update({'bottom': 2})
                tmp2.update({'bottom': 2})
                
            worksheet.merge_range('AA{r}:AD{r}'.format(r=r), s, wb.add_format(tmp))
            worksheet.write_string('AE{r}'.format(r=r), _data.get(s), wb.add_format(tmp2))
        
        # -----------------------------------------------------------------------------
        
        for c, s in zip(((('A', 'E'), ('F', 'O')), (('P', 'V'), ('W', 'AE'))), ['资料核准人员', '现场核验时间']):
            tmp = dict(common_format)
            tmp.update({'bg_color': '#B8B8B8', 'pattern': 1, 'border': 2, 'right': 1})
            tmp2 = dict(common_format)
            tmp2.update({'border': 2, 'left': 1})
                
            worksheet.merge_range('{}13:{}13'.format(*c[0]), s, wb.add_format(tmp))
            worksheet.merge_range('{}13:{}13'.format(*c[1]), _data.get(s), wb.add_format(tmp2))
        
        
        # 画简图
        
        worksheet.set_row(15, 50)
        for r in range(16, 42):
            worksheet.set_row(r, 27)
            
        worksheet.merge_range('A16:G16', '')
        worksheet.merge_range('H16:X16', '珠海市二次供水水池(箱)大样图', title_format)
        
        tmp = wb.add_format({
            'align': 'right',
            'valign': 'vcenter',
            'font_size': 12,
            'font_name': '仿宋',
        })
        worksheet.merge_range('Y16:Z16', '编号:', tmp)

        tmp.set_align('left')
        worksheet.merge_range('AA16:AE16', _data.get('No'), tmp)
        

        for col in range(31):
            worksheet.write_string(17, col, '', wb.add_format({'top': 2}))
            worksheet.write_string(40, col, '', wb.add_format({'bottom': 2}))
        
        for row in range(17, 40 + 1):
            worksheet.write_string(row, 0, '', wb.add_format({'left': 2}))
            worksheet.write_string(row, 30, '', wb.add_format({'right': 2}))
        
        worksheet.write_string(17, 0, '', wb.add_format({'left': 2, 'top': 2}))
        worksheet.write_string(17, 30, '', wb.add_format({'right': 2, 'top': 2}))
        worksheet.write_string(40, 0, '', wb.add_format({'left': 2, 'bottom': 2}))
        worksheet.write_string(40, 30, '', wb.add_format({'right': 2, 'bottom': 2}))
        
        for row, key, value in zip(range(18, 21), ['高', '总容积', '有效容积'], ['高', '', '最大有效容积（m³）']):
            worksheet.merge_range('U{r}:V{r}'.format(r=row), '水箱', wb.add_format({'border': 2, 'align': 'center', 'valign': 'vcenter'}))
            worksheet.merge_range('W{r}:X{r}'.format(r=row), key, wb.add_format({'border': 2, 'align': 'center', 'valign': 'vcenter'}))
            if value:
                worksheet.merge_range('Y{r}:AE{r}'.format(r=row), _data.get(value), wb.add_format({'border': 2, 'align': 'center', 'valign': 'vcenter'}))
            else:
                worksheet.merge_range('Y{r}:AE{r}'.format(r=row), int(_data.get('长')) * int(_data.get('宽')) * int(_data.get('高')), wb.add_format({'border': 2, 'align': 'center', 'valign': 'vcenter'}))

        worksheet.merge_range('B{r}:H{r}'.format(r=19), '注：每个单元格表示为0.5×0.5m面积', wb.add_format({'align': 'center', 'valign': 'vcenter', 'font_size': 11}))
        worksheet.merge_range('I{r}:P{r}'.format(r=22), '俯瞰图', wb.add_format({'align': 'center', 'valign': 'vcenter', 'font_size': 11}))
        
        length = int(_data.get('长'))
        width = int(_data.get('宽'))
        
        start_col = (32 - length * 2) // 2
        
        worksheet.write_string(22, start_col + length, '{}m'.format(length), wb.add_format({'align': 'center', 'valign': 'vcenter', 'font_size': 11}))
        worksheet.write_string(23 + width, start_col - 1, '{}m'.format(width), wb.add_format({'align': 'center', 'valign': 'vcenter', 'font_size': 11}))
        
        worksheet.merge_range(23, start_col, 23 + width * 2, start_col + length * 2, '', wb.add_format({'border': 2}))
     

        
if __name__ == '__main__':
    # sheet_one({}, filename='charsheet.xlsx', sheet1=False, sheet2=False)
    sheet_two({'长': '5', '宽': '4', '高': '3'}, 'huatu.xlsx')
