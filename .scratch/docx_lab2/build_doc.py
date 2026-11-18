# -*- coding: utf-8 -*-
"""按校园失物招领平台项目改写实验2模板（就地增量编辑 TARGET_DOCX）。"""
import copy
import sys
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

TARGET = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else TARGET
FIG = r"D:\code\lost-found-platform\.scratch\figs"
FIG2 = r"D:\code\lost-found-platform\.scratch\figs2"

doc = Document(TARGET)
body = doc.element.body
kids = list(body.iterchildren())


def par(i, expect=None):
    p = Paragraph(kids[i], doc)
    if expect is not None:
        t = p.text.strip().replace('\u3000', '')
        if expect not in t:
            raise AssertionError(f'[{i}] expect {expect!r} got {t[:50]!r}')
    return p


def tbl(i, expect=None):
    t = Table(kids[i], doc)
    if expect is not None:
        got = t.rows[0].cells[0].text.strip()
        if expect not in got:
            raise AssertionError(f'table [{i}] expect {expect!r} got {got[:30]!r}')
    return t


def set_text(p, text):
    runs = p.runs
    if runs:
        r0 = runs[0]
        for r in runs[1:]:
            r._element.getparent().remove(r._element)
        r0.text = text
    else:
        p.add_run(text)


def sub_text(p, old, new):
    for r in p.runs:
        if old in r.text:
            r.text = r.text.replace(old, new)
            return


def set_cell(cell, text):
    for p in cell.paragraphs[1:]:
        p._element.getparent().remove(p._element)
    p0 = cell.paragraphs[0]
    lines = str(text).split('\n')
    set_text(p0, lines[0])
    cur = p0._element
    for ln in lines[1:]:
        el = copy.deepcopy(p0._element)
        cur.addnext(el)
        cur = el
        set_text(Paragraph(el, doc), ln)


def fill_table(table, data, header=None):
    need = len(data) + 1
    while len(table.rows) < need:
        table._tbl.append(copy.deepcopy(table.rows[-1]._tr))
    while len(table.rows) > need:
        table._tbl.remove(table.rows[-1]._tr)
    if header:
        for j, v in enumerate(header):
            set_cell(table.rows[0].cells[j], v)
    for i, row in enumerate(data):
        for j, v in enumerate(row):
            set_cell(table.rows[i + 1].cells[j], v)


BODY_MODEL = 150      # 我的正文（首行缩进）
PLAIN_MODEL = 203     # 我的正文（无缩进）
H2_MODEL = 148
H3_MODEL = 149


def clone_par(model_idx, text):
    el = copy.deepcopy(kids[model_idx])
    p = Paragraph(el, doc)
    set_text(p, text)
    return el


def center_caption(text):
    el = copy.deepcopy(kids[PLAIN_MODEL])
    p = Paragraph(el, doc)
    set_text(p, text)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Pt(0)
    for r in p.runs:
        r.font.size = Pt(10.5)
        r.font.bold = False
    return el


def put_picture(p, path, width_in):
    for child in list(p._element):
        if child.tag != qn('w:pPr'):
            p._element.remove(child)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Pt(0)
    p.add_run().add_picture(path, width=Inches(width_in))


def new_table(rows, cols, data, header, width_in=5.9):
    t = doc.add_table(rows=rows, cols=cols)
    t.style = doc.styles['Grid Table 4 Accent 1']
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = t._tbl.tblPr
    tw = tblPr.find(qn('w:tblW'))
    if tw is None:
        tw = tblPr.makeelement(qn('w:tblW'), {})
        tblPr.append(tw)
    tw.set(qn('w:type'), 'dxa')
    tw.set(qn('w:w'), str(int(width_in * 1440)))
    each = int(width_in * 1440 / cols)
    for gc in t._tbl.tblGrid.findall(qn('w:gridCol')):
        gc.set(qn('w:w'), str(each))
    for j, v in enumerate(header):
        set_cell(t.rows[0].cells[j], v)
    for i, row in enumerate(data):
        for j, v in enumerate(row):
            set_cell(t.rows[i + 1].cells[j], v)
    return t


def insert_after(el, items):
    cur = el
    for it in items:
        cur.addnext(it)
        cur = it
    return cur


def drop(i):
    kids[i].getparent().remove(kids[i])


# ------------------------------------------------ 1. 基本信息
set_text(par(3, '小组号'), '小组号：2022级计算机科学与技术2班x组')
set_text(par(4, '组长'), '组长：xxx')
set_text(par(6, '班级'), '班级：信息科学与工程学院2022级计算机科学与技术2班')
set_text(par(9, '实验时间'), '实验时间：2026年 11 月 x 日   星期x')

score = tbl(33, '学号')
for i, row in enumerate(score.rows[1:], start=1):
    set_cell(row.cells[0], '000%d' % i)
    set_cell(row.cells[1], 'xxx')
    set_cell(row.cells[2], '')
    set_cell(row.cells[3], '')

sub_text(par(11, '在实验2基础上'), '在实验2基础上', '在实验一需求分析的基础上')
sub_text(par(16, '认真分析实验2的结果'), '认真分析实验2的结果', '认真分析实验一需求分析的结果')

# ------------------------------------------------ 2. 附件文档：标题 / 引言
set_text(par(38, '大学图书馆管理系统'), '校园失物招领平台设计文档')
set_text(par(40, '本说明书是结合'), '本说明书是结合对校园失物招领现状及现有失物招领模式的调研结果，经过需求分析，给出校园失物招领平台的基本描述与总体设计方案；内容包括系统体系结构、子系统与模块划分、模块详细设计、接口与数据库设计、开发与测试环境配置，相当于整个系统的总体设计说明书，同时作为后续编码实现与测试的依据。')
set_text(par(42, '结合之前'), '结合实验一对校园失物招领平台的需求分析，本说明书对系统的功能需求做结构化与细化说明，明确系统的体系结构与模块划分，给出主要模块的处理流程、接口数据结构与界面设计，作为程序设计人员编码和测试人员编写测试用例的参考依据。')
set_text(par(44, '待开发的软件系统的名称'), '待开发的软件系统的名称：校园失物招领平台（Lost & Found Platform，简称 LFP）')
set_text(par(45, '本项目的任务提出者'), '本项目的任务提出者：软件工程课程组')
set_text(par(46, '本项目的任务开发者'), '本项目的任务开发者：计科2班x组')
set_text(par(47, '本项目的任务用户'), '本项目的任务用户：在校学生、教职工（失主与拾取者），以及负责审核与维护的平台管理员')
set_text(par(49, '[1]'), '[1] 校园失物招领平台需求分析说明书（实验一提交文档）')
set_text(par(50, '[2]'), '[2] 王珊，萨师煊．数据库系统概论（第五版）．北京：高等教育出版社。')
set_text(par(51, '[3]'), '[3] GB/T 8567-2006 计算机软件文档编制规范')
set_text(par(52, '[4]'), '[4] 刘冰、赖涵等．软件工程实践教程。')
set_text(par(53, '[5]'), '[5] Spring Boot 3.5 Reference Documentation；MyBatis-Plus 3.5 官方文档')

# ------------------------------------------------ 3. 设计约束
set_text(par(57, '根据具体的系统描述'),
         '本系统遵循 GB/T 8567-2006 计算机软件文档编制规范；对外接口按 RESTful 风格设计，统一使用 JSON 报文与统一的响应结构；'
         '后端代码遵循《阿里巴巴 Java 开发手册》的分层与命名约定，前端代码遵循 ESLint + Prettier 规范；'
         '数据库设计遵循第三范式，仅在查询频繁的字段上做适度冗余；安全方面参照 OWASP Top 10，对输入校验、权限控制、文件上传统一管控。')
set_text(par(61, '主板'), '主板：云服务器主板（2 vCPU 起，可按并发弹性扩容）')
set_text(par(62, 'CPU'), 'CPU：4 核 x86_64，主频 2.4GHz 以上')
set_text(par(63, '内存'), '内存：8G DDR4（最低 4G，按并发量扩展）')
set_text(par(64, '硬盘'), '硬盘：100G SSD（系统盘 40G，数据盘 60G）')
set_text(par(65, '热插拔'), '备份：系统镜像 + 数据库每日定时逻辑备份')
set_text(par(66, '电源'), '网络：公网带宽 5Mbps 起，配置 HTTPS 证书')
set_text(par(68, '普通PC'), '普通 PC 或智能手机，通过浏览器访问，无需安装客户端')

set_text(par(71, '操作系统'), '操作系统：Linux（Ubuntu 22.04 LTS / CentOS 7.9）')
set_text(par(72, 'Web 服务器'), 'Web 服务器：Nginx 1.24（静态资源托管 + 反向代理）')
set_text(par(73, '数据库服务器'), '数据库服务器：MySQL 8.0（InnoDB 引擎，字符集 utf8mb4）')
set_text(par(74, '浏览器'), '应用运行环境：JDK 17 + Spring Boot 3.5.6（内嵌 Tomcat）')
set_text(par(75, '系统服务器运行环境'), '对象存储：阿里云 OSS（保存物品图片与头像，可切换本地 upload 目录）')
set_text(par(77, '浏览器'), '浏览器：Chrome / Edge 90 及以上版本')
set_text(par(78, '分辨率'), '分辨率：最佳运行效果 1440×900 像素，最小支持 1280×720 像素')

set_text(par(80, '学校图书馆管理系统中人员数据'),
         '本系统采用前后端分离架构，前端 Vue3 通过 Axios 调用后端 RESTful 接口，报文统一为 JSON，响应统一封装为 Result{code, message, data}；'
         '除注册、登录接口外，其余接口须在请求头携带 Authorization: Bearer <JWT>，由后端拦截器校验令牌有效性与用户角色。'
         '图片上传采用“先上传取 URL、再提交业务数据”的两步流程，后端把图片写入阿里云 OSS（开发环境写本地 upload 目录），物品表只保存图片 URL 列表，避免大字段入库。'
         '系统预留与学校统一身份认证、教务系统学号库的数据接口，用于学号与实名信息核验；当前版本以注册时手填学号、管理员审核认证状态的方式替代，接口层保持不变，后续接入无需改动业务代码。')

set_text(par(82, '窗口约束'), '页面约束')
set_text(par(83, '窗口支持最小化'), '页面在 1280×720 及以上分辨率自适应，内容区随浏览器窗口宽度伸缩')
set_text(par(84, '窗口上的控件'), '页面内的表格与图片随容器宽度等比缩放，正常浏览不出现横向滚动条')
set_text(par(85, '窗口的数据'), '页面数据可同时通过鼠标与键盘操作，表单支持 Enter 提交、Esc 关闭弹窗')
set_text(par(86, '窗口中按Tab'), '按 Tab 键移动焦点，顺序为先从左至右、再从上至下')
set_text(par(87, '与正在进行的操作'), '与当前操作无关的按钮置灰禁用，如未登录时“发布”“我要认领”按钮不可点击')
set_text(par(88, '按钮大小'), '按钮尺寸与页面空间协调，主操作与次操作用不同按钮样式区分')
set_text(par(89, '菜单约束'), '导航约束')
set_text(par(90, '菜单项的顺序'), '主导航固定在页面顶部，顺序为：首页、失物、招领、我的，逻辑关联项集中放置')
set_text(par(91, '菜单设置在'), '“我的”下集中“我的发布”“我的认领”“我的收藏”“消息中心”，不与其他入口交叉')
set_text(par(93, '选择合适的尺寸'), '图标统一采用 24×24（@1x）与 48×48（@2x）两种尺寸，保证高分屏清晰')
set_text(par(94, '图标放置在'), '图标置于导航文字左侧或按钮内，关键操作不用纯图标按钮代替文字')
set_text(par(95, '图标的外形'), '图标外形与实际功能语义一致，全站使用同一套线性图标，避免抽象化')
set_text(par(97, '对常用浏览器'), '对常用浏览器兼容性良好，包括 Chrome、Edge、Firefox、Safari 近两年主流版本，移动端适配 375px 及以上宽度')

# ------------------------------------------------ 4. 系统功能结构 / 部署结构
put_picture(par(99), FIG + r'\fig1_structure.png', 5.8)
set_text(par(100), '图 2-1  系统功能结构图')
c = par(100)
c.alignment = WD_ALIGN_PARAGRAPH.CENTER
c.paragraph_format.first_line_indent = Pt(0)
for r in c.runs:
    r.font.size = Pt(10.5)

put_picture(par(102), FIG2 + r'\fig_deploy.png', 5.85)
set_text(par(103), '图 2-2  系统部署结构图')
c = par(103)
c.alignment = WD_ALIGN_PARAGRAPH.CENTER
c.paragraph_format.first_line_indent = Pt(0)
for r in c.runs:
    r.font.size = Pt(10.5)

# ------------------------------------------------ 5. 子系统描述
set_text(par(105, '子系统清单'), '子系统按功能内聚、模块间低耦合的原则划分，清单如表 2-1 所示。')
fill_table(tbl(106, '子系统编号'), [
    ['SS1', 'LFP_Account\n账号与权限子系统',
     '用户注册与登录（签发 JWT）\n个人资料与头像维护\n修改密码与令牌失效\n角色与权限校验',
     '为其余子系统提供统一的身份认证与角色信息'],
    ['SS2', 'LFP_Item\n物品信息子系统',
     '发布失物 / 招领信息（含图片上传）\n列表浏览、分类与关键词检索\n物品详情展示\n我的发布（编辑、下架、删除）',
     '依赖 SS1 获取发布者身份；向 SS3 提供可认领的物品数据'],
    ['SS3', 'LFP_Claim\n认领管理子系统',
     '提交认领申请（凭证描述）\n我的认领进度查询\n发布者 / 管理员审核\n认领与物品状态联动流转',
     '依赖 SS2 的物品状态；审核结果驱动 SS4 生成消息'],
    ['SS4', 'LFP_FavMsg\n收藏与消息子系统',
     '收藏 / 取消收藏\n我的收藏列表\n系统通知与认领通知\n站内留言与未读提醒',
     '订阅 SS2、SS3 的业务事件，生成对应站内消息'],
    ['SS5', 'LFP_Admin\n后台管理子系统',
     '物品信息审核（通过 / 驳回）\n用户管理（封禁 / 解禁）\n物品分类管理\n平台数据统计',
     '调用 SS1 的角色权限，读取 SS2、SS3 的业务数据'],
])

# ------------------------------------------------ 6. 功能模块详细描述
set_text(par(108, '各模块清单'), '各模块及其子模块清单，如表 2-2 所示。')
fill_table(tbl(109, '模块编号'), [
    ['M1', '用户注册', 'M1-1', 'LFP_Account_Register', '新用户注册，校验账号与学号唯一性，默认角色 USER'],
    ['M2', '用户登录', 'M2-1', 'LFP_Account_Login', '账号密码登录，签发 JWT 令牌并返回角色'],
    ['M2', '用户登录', 'M2-2', 'LFP_Account_Logout', '退出登录，令牌加入黑名单立即失效'],
    ['M3', '个人资料', 'M3-1', 'LFP_Account_Profile', '查看与修改姓名、学号、学院、联系方式，修改密码'],
    ['M3', '个人资料', 'M3-2', 'LFP_Account_Avatar', '上传头像至 OSS 并更新用户头像地址'],
    ['M4', '发布物品', 'M4-1', 'LFP_Item_Publish', '发布失物 / 招领信息，录入隐藏特征与联系方式，提交后进入待审核'],
    ['M4', '发布物品', 'M4-2', 'LFP_Item_Image', '校验图片格式与大小，上传至 OSS 并返回访问 URL'],
    ['M5', '物品浏览', 'M5-1', 'LFP_Item_List', '按类型、分类、关键词与时间分页浏览物品列表'],
    ['M5', '物品浏览', 'M5-2', 'LFP_Item_Detail', '展示物品详情与图片，提示用隐藏特征核验物品归属'],
    ['M6', '我的发布', 'M6-1', 'LFP_Item_Mine', '查看本人发布记录及其审核、认领状态'],
    ['M6', '我的发布', 'M6-2', 'LFP_Item_Manage', '编辑、重新提交被驳回的信息、下架与删除'],
    ['M7', '认领申请', 'M7-1', 'LFP_Claim_Apply', '提交认领申请，填写认领凭证描述'],
    ['M7', '认领申请', 'M7-2', 'LFP_Claim_Mine', '查询本人认领申请的处理进度与结果'],
    ['M8', '认领审核', 'M8-1', 'LFP_Claim_Review', '发布者或管理员审核认领申请，通过或驳回并填写备注'],
    ['M8', '认领审核', 'M8-2', 'LFP_Claim_StateFlow', '认领与物品状态联动流转，自动关闭同物品其他待审申请'],
    ['M9', '收藏管理', 'M9-1', 'LFP_Favorite_Toggle', '收藏 / 取消收藏物品，按用户与物品唯一约束去重'],
    ['M9', '收藏管理', 'M9-2', 'LFP_Favorite_List', '查看我的收藏列表并可跳转物品详情'],
    ['M10', '消息通知', 'M10-1', 'LFP_Message_Notify', '生成系统通知、认领通知与站内留言，统计未读数量'],
    ['M11', '后台审核', 'M11-1', 'LFP_Admin_ItemAudit', '审核待审物品，通过置为 ACTIVE、驳回置为 CLOSED 并留存备注'],
    ['M12', '用户管理', 'M12-1', 'LFP_Admin_User', '查询用户、封禁 / 解禁账号，控制违规用户发布与认领'],
    ['M13', '分类管理', 'M13-1', 'LFP_Admin_Category', '维护物品分类的名称、图标与排序'],
    ['M14', '数据统计', 'M14-1', 'LFP_Admin_Stats', '统计物品总量、认领成功率、分类分布与近 7 日趋势'],
])

# ------------------------------------------------ 7. 权限设置
set_text(par(111, '系统权限设置'), '按“游客浏览、用户参与、管理员维护”的原则划分权限，如表 2-3 所示（“√”表示具备该权限）。')
fill_table(tbl(112, '功能描述'), [
    ['用户注册（校验账号、学号唯一）', 'M1-1', '', '√', '√'],
    ['登录并签发 / 注销 JWT 令牌', 'M2-1、M2-2', '√', '√', ''],
    ['维护个人资料、头像与密码', 'M3-1、M3-2', '√', '√', ''],
    ['发布失物 / 招领信息并上传图片', 'M4-1、M4-2', '√', '√', ''],
    ['浏览、检索物品与查看详情', 'M5-1、M5-2', '√', '√', '√'],
    ['管理我的发布（编辑 / 重提 / 下架）', 'M6-1、M6-2', '√', '√', ''],
    ['提交认领申请、查询认领进度', 'M7-1、M7-2', '√', '√', ''],
    ['审核收到的认领申请', 'M8-1、M8-2', '√', '√', ''],
    ['收藏物品与查看收藏列表', 'M9-1、M9-2', '√', '√', ''],
    ['查看系统 / 认领通知与站内留言', 'M10-1', '√', '√', ''],
    ['审核物品信息（通过 / 驳回）', 'M11-1', '√', '', ''],
    ['用户查询、封禁 / 解禁', 'M12-1', '√', '', ''],
    ['物品分类维护', 'M13-1', '√', '', ''],
    ['平台数据统计', 'M14-1', '√', '', ''],
], header=['功能描述', '对应模块', '管理员', '普通用户', '游客'])

# ------------------------------------------------ 8. 模块设计：四个子系统
set_text(par(116, '编目管理子系统'), '物品信息子系统')
set_text(par(117, 'IPO 表'), '1） 物品信息子系统 IPO 表（如表 2-4 所示）')
ipo1 = new_table(6, 4, [
    ['发布失物 / 招领', '类型、标题、分类、描述、发生时间、地点、隐藏特征、联系人及电话、图片 URL',
     '校验登录态与必填项 → 生成 item 记录（status = PENDING）→ 按类型、分类、关键词在相反类型中检索匹配候选',
     '发布结果提示、待审核物品记录、我的发布列表新增项'],
    ['图片上传', '图片文件（jpg / png / webp，单张 ≤ 5MB）、JWT 令牌',
     '校验文件类型与大小 → 按日期 + UUID 重命名 → 写入 OSS / 本地 upload 目录',
     '可访问的图片 URL 与文件名'],
    ['浏览与检索', '类型、分类编号、关键词、页码、每页条数',
     '按条件拼接查询 → 按发布时间倒序分页 → 过滤非 ACTIVE 记录',
     '物品列表（标题、分类、地点、时间、首图、状态）'],
    ['详情展示', '物品编号',
     '查询物品及其发布者信息 → 剔除隐藏特征字段 → 组装 VO',
     '物品详情（不含隐藏特征）、认领入口与收藏状态'],
    ['我的发布', '用户编号、状态筛选、页码',
     '按 user_id 与 status 组合查询 → 关联认领记录统计进度',
     '本人发布列表及审核、认领状态'],
], ['子模块', '输入', '处理', '输出'])
insert_after(kids[117], [ipo1._tbl])
for i in (118, 120, 121, 122, 123, 124):
    drop(i)
insert_after(kids[119], [
    clone_par(BODY_MODEL, '1. 物品列表页采用“顶部导航 + 左侧分类栏 + 右侧卡片列表”的布局：顶部为 Logo、失物 / 招领切换、搜索框与“发布”按钮；左侧为分类与筛选条件（时间范围、地点）；右侧以卡片流展示首图、标题、地点与时间，底部为分页器。'),
    clone_par(BODY_MODEL, '2. 发布页采用单列表单，按“类型—标题—分类—描述—时间地点—隐藏特征—图片—联系方式”顺序自上而下排列，必填项前标“*”；图片区支持拖拽上传并实时预览缩略图，提交按钮固定在底部，并提示“提交后需管理员审核”。'),
    clone_par(BODY_MODEL, '3. 详情页上半部分为图片轮播与关键信息，下半部分为描述与认领入口；点击“收藏”后图标即时变为已收藏状态；未登录用户点击任一操作均跳转登录页，并在登录后回填原页面地址。'),
])

set_text(par(125, '流通管理子系统'), '认领管理子系统')
set_text(par(126, '流通管理子系统  IPO 表'), '1） 认领管理子系统 IPO 表（如表 2-5 所示）')
ipo2 = new_table(4, 4, [
    ['提交认领申请', '物品编号、认领凭证描述、申请人 JWT 令牌',
     '校验物品状态为 ACTIVE、申请人非发布者、无重复待审申请 → 写 claim（PENDING）→ item 置为 PROCESSING → 写通知消息',
     '申请结果、待审认领记录、发布者通知'],
    ['认领审核', '认领编号、审核结论、审核备注、审核人编号',
     '校验认领为 PENDING → 更新 claim 状态 → 通过时 item 置为 COMPLETED 并批量驳回同物品其他申请',
     '认领状态、物品状态、双方通知消息'],
    ['我的认领进度', '用户编号、页码',
     '按 applicant_id 查询并关联物品标题与状态',
     '认领列表（物品、状态、审核备注、申请时间）'],
], ['子模块', '输入', '处理', '输出'])
insert_after(kids[126], [ipo2._tbl])
drop(127)

set_text(par(129, '1．借书模块'), '1．提交认领申请')
set_text(par(130, '借书模块 IPO 表'), '提交认领申请 界面设计')
drop(131)
insert_after(kids[130], [
    clone_par(BODY_MODEL, '1. 入口：物品详情页右下角固定“我要认领”按钮，物品状态不是 ACTIVE 时按钮置灰并提示原因。'),
    clone_par(BODY_MODEL, '2. 认领对话框：标题为“提交认领申请”，正文提示“请填写只有失主知道的特征（如内部物品、划痕、壁纸内容）”，输入框限 500 字并实时计数，底部为“取消 / 提交申请”。'),
    clone_par(BODY_MODEL, '3. 提交成功后对话框关闭，页面顶部提示“申请已提交，等待审核”，同时物品状态标签更新为“认领中”。'),
])

set_text(par(133, '借书模块 界面设计'), '2．认领审核')
drop(134)
set_text(par(135, '2．还书'), '认领审核 界面设计')
for i in (136, 137, 138, 139, 140):
    drop(i)
insert_after(kids[135], [
    clone_par(BODY_MODEL, '1. 审核页面从“收到的申请”进入，左侧为物品图片、描述与隐藏特征（仅审核人与发布者可见），右侧为申请人信息与认领凭证描述，便于逐条比对。'),
    clone_par(BODY_MODEL, '2. 底部为“通过 / 驳回”两个按钮：点击“通过”弹出二次确认；点击“驳回”必须填写驳回原因，否则提交按钮不可用。'),
    clone_par(BODY_MODEL, '3. 审核完成后列表即时刷新，已处理申请以“已通过 / 已驳回”标签展示，并向申请人推送站内消息。'),
])

set_text(par(141, '查询子系统'), '收藏与消息子系统')
set_text(par(142, 'IPO 图'), '1） 收藏与消息子系统 IPO 表（如表 2-6 所示）')
ipo3 = new_table(4, 4, [
    ['收藏 / 取消收藏', '用户编号、物品编号',
     '按唯一索引 uk_user_item 判断收藏状态 → 插入或删除 favorite 记录',
     '收藏状态（已收藏 / 未收藏）、收藏总数'],
    ['我的收藏列表', '用户编号、页码',
     '关联 item 查询 → 过滤已关闭物品 → 按收藏时间倒序',
     '收藏物品列表（标题、首图、状态、收藏时间）'],
    ['消息通知', '业务事件（审核、认领结果）、接收人编号',
     '按事件类型生成 message 记录（SYSTEM / CLAIM / CHAT）→ 维护未读标记',
     '站内消息列表、未读数量'],
], ['子模块', '输入', '处理', '输出'])
insert_after(kids[142], [ipo3._tbl])
insert_after(kids[143], [
    clone_par(BODY_MODEL, '1. 收藏列表复用物品卡片组件，按收藏时间倒序排列，卡片右上角为“取消收藏”图标，取消后卡片淡出并从列表移除。'),
    clone_par(BODY_MODEL, '2. 消息中心分为“系统通知 / 认领通知 / 站内留言”三个标签页，列表项显示类型图标、内容摘要、时间与未读标记；点击后标记已读并跳转到相关物品详情。'),
    clone_par(BODY_MODEL, '3. 导航栏“消息”图标以红色角标显示未读数量，数量为 0 时不显示角标。'),
])

set_text(par(144, '办理借阅证子系统'), '后台管理子系统')
set_text(par(145, 'IPO 图'), '1） 后台管理子系统 IPO 表（如表 2-7 所示）')
ipo4 = new_table(5, 4, [
    ['物品信息审核', '物品编号、审核结论、审核备注、审核人编号',
     '校验记录为 PENDING → 通过置为 ACTIVE / 驳回置为 CLOSED 并写入 audit_remark → 生成系统消息',
     '审核结果、物品状态、发布者通知'],
    ['用户管理', '用户编号 / 关键词、操作类型（封禁 / 解禁）',
     '校验操作人角色为 ADMIN → 更新 status → 拦截器拒绝被封禁用户访问受保护接口',
     '用户状态、操作日志记录'],
    ['分类管理', '分类名称、图标、排序值',
     '新增 / 修改 / 删除分类，校验名称不重复',
     '分类列表'],
    ['数据统计', '时间范围',
     '聚合 item、claim、user 三类数据，计算认领成功率与近 7 日趋势',
     '指标卡片与图表数据'],
], ['子模块', '输入', '处理', '输出'])
insert_after(kids[145], [ipo4._tbl])
insert_after(kids[146], [
    clone_par(BODY_MODEL, '1. 后台采用“左侧折叠菜单 + 右侧内容区”的管理端布局，菜单包含物品审核、用户管理、分类管理、数据统计四项。'),
    clone_par(BODY_MODEL, '2. 物品审核页左侧为待审列表（可切换待审 / 已审），右侧为选中物品的图片、描述与隐藏特征，底部为“通过 / 驳回”与备注输入框。'),
    clone_par(BODY_MODEL, '3. 数据统计页顶部为四张指标卡（物品总数、待审核数、认领成功率、新增用户），下方为按分类的柱状图与近 7 日发布趋势折线图。'),
])

print('module design done')

# ------------------------------------------------ 9. 模块详细设计（认领审核模块）
set_text(par(148, '借书模块详细设计'), '认领审核模块详细设计')
set_text(par(149, '借书模块功能描述'), '认领审核模块功能描述')
set_text(par(150, '用户填写图书借阅单'),
         '本模块负责处理失主对招领信息（或拾取者对失物信息）发起的认领申请，并给出审核结论。首先校验申请人登录状态与账号状态（1），账号被封禁则直接拒绝；'
         '随后读取物品记录，校验物品状态为 ACTIVE 且申请人不是发布者（2），若物品已处于 PROCESSING、COMPLETED 或 CLOSED，则提示“该物品已被认领或不可认领”；'
         '再按（申请人，物品）组合查询是否存在未处理的认领申请（3），存在则提示“请勿重复提交”。')
set_text(par(151, '完成（1）、（2）、（3）'),
         '完成（1）（2）（3）三项判断后，创建认领记录（status = PENDING），并把物品状态由 ACTIVE 置为 PROCESSING，避免并发重复认领，同时向发布者写入一条 CLAIM 类型消息。'
         '发布者或管理员在“收到的申请”中比对隐藏特征与凭证描述后作出审核结论：通过时把认领记录置为 APPROVED、物品置为 COMPLETED，并批量把同一物品下其他待审申请置为 REJECTED；'
         '驳回时把认领记录置为 REJECTED、物品恢复 ACTIVE，并把驳回原因写入 review_remark。两种结果均写入消息通知申请人。')
set_text(par(153, '说明对该模块程序的全部性能要求'), '本模块对精度、灵活性和时间特性的要求如下：')
set_text(par(154, '数据流量'), '数据流量： 认领申请 300 条 / 日（单校区约 1 万注册用户规模）')
set_text(par(155, '高峰流量'), '高峰流量： 1500 条 / 日（开学季、毕业季及大型活动之后）')

drop(157)
insert_after(kids[156], [
    clone_par(BODY_MODEL, '1. 入口：物品详情页右下角固定“我要认领”按钮，物品状态不是 ACTIVE 时按钮置灰并提示原因。'),
    clone_par(BODY_MODEL, '2. 审核界面：左侧展示物品图片、描述与隐藏特征（仅审核人与发布者可见），右侧展示申请人信息与凭证描述，底部为“通过 / 驳回”与驳回原因输入框。'),
    clone_par(BODY_MODEL, '3. 交互反馈：操作完成后列表即时刷新并弹出结果提示；被驳回的申请人可在“我的认领”中查看驳回原因并重新提交。'),
])

set_text(par(159, '读者信、借书证条码'), '物品编号、申请人编号、认领凭证描述、审核结论（通过 / 驳回）、审核备注、审核人编号与审核时间')
set_text(par(161, '读者信息、读者个别登记明细信息'), '认领记录状态、物品状态、审核结果提示、面向申请人与发布者的站内消息、我的认领列表更新')

put_picture(par(163), FIG2 + r'\fig_flow_claim.png', 5.0)

# ------------------------------------------------ 10. 物品发布模块详细设计 + 接口数据结构设计
iface = new_table(10, 4, [
    ['用户注册', 'POST /api/auth/register', 'username、password、realName、studentNo、college、phone', 'code、message'],
    ['用户登录', 'POST /api/auth/login', 'username、password', 'token、user{id, role, username}'],
    ['上传图片', 'POST /api/files/upload', 'multipart file、JWT 令牌', 'url、fileName'],
    ['发布物品', 'POST /api/items', 'type、title、categoryId、description、eventTime、location、secretFeature、contactName、contactPhone、images', 'id、status、createTime'],
    ['物品列表', 'GET /api/items', 'type、categoryId、keyword、page、pageSize', 'total、records[{id, title, cover, location, eventTime, status}]'],
    ['物品详情', 'GET /api/items/{id}', '路径参数 id', 'id、title、description、images、location、publisher{}、claimable'],
    ['提交认领', 'POST /api/claims', 'itemId、claimDesc', 'claimId、status'],
    ['认领审核', 'PUT /api/claims/{id}/review', 'status（APPROVED / REJECTED）、reviewRemark', 'claimId、claimStatus、itemStatus'],
    ['物品审核', 'PUT /api/admin/items/{id}/audit', 'result（PASS / REJECT）、auditRemark', 'itemId、status'],
], ['接口名称', '请求方法与路径', '主要请求参数', '主要返回字段'])

seq = [
    center_caption('图 3-1  认领审核模块程序流程图'),
    clone_par(H2_MODEL, '物品发布模块详细设计'),
    clone_par(H3_MODEL, '物品发布模块功能描述'),
    clone_par(BODY_MODEL, '用户登录后进入“发布”页面，按失物 / 招领两类填写物品信息：标题、分类、详细描述、丢失或拾取的时间与地点、隐藏特征（仅审核人可见）、联系人与联系电话，并上传不超过 3 张图片。前端先做必填项、字段长度与图片格式大小的校验（1），校验不通过则高亮对应字段并停留在当前页面。'),
    clone_par(BODY_MODEL, '校验通过后调用上传接口把图片写入 OSS 并取得访问 URL，随后携带 JWT 调用发布接口。后端依次校验登录态与角色、必填项与字段长度、图片 URL 是否由本系统上传、同一用户短时间内的发布次数（2），并依据“类型 + 分类 + 关键词”在相反类型（招领 ↔ 失物）中检索相似记录作为匹配候选。校验通过后写入 item 表，status 置为 PENDING（3），create_time 取服务器时间，并返回统一 Result 结构。'),
    clone_par(BODY_MODEL, '物品随后进入待审核队列：管理员在后台审核，通过则置为 ACTIVE 并进入前台列表，驳回则置为 CLOSED 并写入 audit_remark，同时向发布者推送系统消息，发布者可修改后重新提交。'),
    clone_par(H3_MODEL, '性能要求'),
    clone_par(PLAIN_MODEL, '本模块对精度、灵活性和时间特性的要求如下：'),
    clone_par(PLAIN_MODEL, '数据流量： 发布 200 条 / 日，图片上传 400 张 / 日'),
    clone_par(PLAIN_MODEL, '高峰流量： 1200 条 / 日；单张图片上限 5MB，上传接口响应时间 ≤ 3 秒'),
    clone_par(PLAIN_MODEL, '精度要求： 发生时间精确到分钟；图片 URL 与物品记录一一对应，不允许出现无效 URL'),
    clone_par(H3_MODEL, '模块人机交互设计—界面设计'),
    clone_par(BODY_MODEL, '1. 发布页为单列表单，顶部为“发布失物 / 发布招领”分段控件，中部依次为标题、分类（下拉选择）、描述（多行文本）、时间（日期时间选择器）、地点（文本输入 + 常用地点快选）、隐藏特征、图片（拖拽上传 + 缩略图预览）、联系人及电话，必填项前标“*”。'),
    clone_par(BODY_MODEL, '2. 底部固定操作栏包含“重置 / 提交”按钮，提交过程中按钮显示“提交中…”并禁用，避免重复提交；提交成功后跳转“我的发布”并提示“已提交，等待管理员审核”。'),
    clone_par(BODY_MODEL, '3. 字段失焦即校验并即时提示，错误提示以红色文字显示在字段下方，页面自动滚动到第一个错误字段。'),
    clone_par(H3_MODEL, '输入项'),
    clone_par(BODY_MODEL, '物品类型（LOST / FOUND）、标题、分类编号、详细描述、丢失或拾取时间、地点、隐藏特征、联系人、联系电话、图片文件（≤ 3 张）、发布者 JWT 令牌'),
    clone_par(H3_MODEL, '输出项'),
    clone_par(BODY_MODEL, '物品记录编号、审核状态（PENDING）、匹配候选列表、统一响应结果（code / message / data）、我的发布列表新增记录'),
    clone_par(H3_MODEL, '程序流程'),
]
img_p = copy.deepcopy(kids[PLAIN_MODEL])
pp = Paragraph(img_p, doc)
set_text(pp, '')
put_picture(pp, FIG2 + r'\fig_flow_publish.png', 5.0)
seq.append(img_p)
seq.append(center_caption('图 3-2  物品发布模块程序流程图'))
seq.append(clone_par(H2_MODEL, '接口数据结构设计'))
seq.append(clone_par(BODY_MODEL, '系统前后端以 RESTful 接口通信，报文统一为 JSON，响应统一封装为 Result{code, message, data}；分页查询统一使用 PageQuery{page, pageSize}，分页结果统一为 PageResult{total, records}。主要接口及其关键字段如表 3-1 所示，完整字段以接口文档为准。'))
seq.append(iface._tbl)
seq.append(clone_par(BODY_MODEL, '状态类字段一律使用大写英文常量：物品状态 PENDING / ACTIVE / PROCESSING / COMPLETED / CLOSED，认领状态 PENDING / APPROVED / REJECTED，消息类型 SYSTEM / CLAIM / CHAT，避免前后端混用中文枚举值；`images` 字段以逗号分隔的 URL 串传递，前端拆分为数组渲染。'))
insert_after(kids[163], seq)
print('detail design done')

# ------------------------------------------------ 11. 数据库设计
set_text(par(167, '数据库系统'), '数据库系统：MySQL 8.0.36（InnoDB 引擎，字符集 utf8mb4，排序规则 utf8mb4_general_ci）')
set_text(par(168, '设计工具'), '设计工具：Navicat Premium 16 / MySQL Workbench 8.0')
set_text(par(169, '编程工具'), '编程工具：IntelliJ IDEA 2023.2（后端）+ Visual Studio Code（前端）')
set_text(par(171, '为了统一和规范数据库命名'),
         '为统一起见，数据库与字段命名遵循以下规则：表名使用小写单数名词，多词以下划线分隔；字段名使用小写下划线（snake_case），主键统一命名为 id（BIGINT 自增）；'
         '外键命名为“关联表名_id”（如 user_id、item_id、category_id）；时间字段统一为 create_time / update_time / xxx_time；'
         '状态类字段使用 VARCHAR 存放大写英文常量（如 PENDING / ACTIVE）；索引以 idx_ 为前缀、唯一索引以 uk_ 为前缀；'
         '字符集统一 utf8mb4，描述类字段使用 TEXT，图片等多值字段以逗号分隔的字符串存储。')
set_text(par(174, '数据库表名清单，如表'), '数据库表名清单，如表 4-1 所示')

fill_table(tbl(175, '序号'), [
    ['1', '用户表', 'user', '记录注册用户与管理员账号、实名与认证信息'],
    ['2', '分类表', 'category', '记录物品分类的名称、图标与排序'],
    ['3', '物品表', 'item', '记录失物 / 招领信息、图片、隐藏特征与审核状态'],
    ['4', '认领记录表', 'claim', '记录认领申请、凭证描述与审核结果'],
    ['5', '消息表', 'message', '记录系统通知、认领通知与站内留言'],
    ['6', '收藏表', 'favorite', '记录用户对物品的收藏关系（用户 + 物品唯一）'],
])

set_text(par(178, '读者信息表'), '用户表(user)：')
fill_table(tbl(179, '字段名'), [
    ['id', '主键', 'BIGINT', '', '否', 'PK，自增'],
    ['username', '登录账号', 'VARCHAR', '50', '否', '唯一索引 uk_username'],
    ['password', '加密密码', 'VARCHAR', '100', '否', 'BCrypt 加密后存储'],
    ['real_name', '真实姓名', 'VARCHAR', '50', '是', ''],
    ['student_no', '学号', 'VARCHAR', '20', '是', '与实名认证配合使用'],
    ['college', '学院', 'VARCHAR', '100', '是', ''],
    ['phone', '手机号', 'VARCHAR', '20', '是', '对外响应中脱敏'],
    ['email', '邮箱', 'VARCHAR', '100', '是', ''],
    ['avatar', '头像地址', 'VARCHAR', '255', '是', 'OSS 返回的 URL'],
    ['verify_status', '认证状态', 'TINYINT', '', '是', '0 未认证 / 1 已认证'],
    ['role', '角色', 'VARCHAR', '20', '是', 'USER / ADMIN，默认 USER'],
    ['status', '账号状态', 'TINYINT', '', '是', '0 正常 / 1 封禁'],
    ['create_time', '创建时间', 'DATETIME', '', '是', '注册时间'],
    ['update_time', '更新时间', 'DATETIME', '', '是', '资料修改时间'],
])

set_text(par(180, '图书信息表'), '分类表(category)：')
fill_table(tbl(181, '字段名'), [
    ['id', '主键', 'BIGINT', '', '否', 'PK，自增'],
    ['name', '分类名称', 'VARCHAR', '50', '否', '同一名称不可重复'],
    ['icon', '图标标识', 'VARCHAR', '255', '是', '对应前端图标名'],
    ['sort', '排序值', 'INT', '', '是', '升序排列，默认 0'],
])

set_text(par(183, '图书财产明细表'), '物品表(item)：')
fill_table(tbl(184, '字段名'), [
    ['id', '主键', 'BIGINT', '', '否', 'PK，自增'],
    ['type', '物品类型', 'VARCHAR', '10', '否', 'LOST 失物 / FOUND 招领'],
    ['title', '物品标题', 'VARCHAR', '100', '否', ''],
    ['category_id', '分类编号', 'BIGINT', '', '是', '外键 → category.id'],
    ['description', '详细描述', 'TEXT', '', '是', '外观、内部物品等描述'],
    ['images', '图片地址', 'VARCHAR', '1000', '是', '多个 URL 逗号分隔，最多 3 张'],
    ['event_time', '丢失 / 拾取时间', 'DATETIME', '', '是', '精确到分钟'],
    ['location', '地点', 'VARCHAR', '100', '是', ''],
    ['secret_feature', '隐藏特征', 'VARCHAR', '255', '是', '仅审核人可见，不对外返回'],
    ['contact_name', '联系人', 'VARCHAR', '50', '是', ''],
    ['contact_phone', '联系电话', 'VARCHAR', '20', '是', ''],
    ['status', '物品状态', 'VARCHAR', '20', '是', 'PENDING / ACTIVE / PROCESSING / COMPLETED / CLOSED'],
    ['audit_remark', '审核备注', 'VARCHAR', '255', '是', '驳回原因'],
    ['user_id', '发布者编号', 'BIGINT', '', '是', '外键 → user.id'],
    ['create_time', '发布时间', 'DATETIME', '', '是', ''],
    ['update_time', '更新时间', 'DATETIME', '', '是', ''],
])

set_text(par(186, '借还书信息表'), '认领记录表(claim)：')
fill_table(tbl(187, '字段名'), [
    ['id', '主键', 'BIGINT', '', '否', 'PK，自增'],
    ['item_id', '物品编号', 'BIGINT', '', '否', '外键 → item.id'],
    ['applicant_id', '申请人编号', 'BIGINT', '', '否', '外键 → user.id'],
    ['claim_desc', '认领凭证描述', 'VARCHAR', '500', '否', '用于核验失主身份'],
    ['status', '认领状态', 'VARCHAR', '20', '是', 'PENDING / APPROVED / REJECTED'],
    ['review_remark', '审核备注', 'VARCHAR', '255', '是', '驳回原因'],
    ['reviewer_id', '审核人编号', 'BIGINT', '', '是', '外键 → user.id'],
    ['create_time', '申请时间', 'DATETIME', '', '是', ''],
    ['review_time', '审核时间', 'DATETIME', '', '是', ''],
])

set_text(par(188, '操作日志表'), '消息表(message)：')
fill_table(tbl(189, '字段名'), [
    ['id', '主键', 'BIGINT', '', '否', 'PK，自增'],
    ['from_user_id', '发送者编号', 'BIGINT', '', '是', '系统消息固定为 0'],
    ['to_user_id', '接收者编号', 'BIGINT', '', '否', '外键 → user.id'],
    ['item_id', '关联物品编号', 'BIGINT', '', '是', '外键 → item.id'],
    ['type', '消息类型', 'VARCHAR', '20', '是', 'SYSTEM / CLAIM / CHAT'],
    ['content', '消息内容', 'VARCHAR', '500', '否', ''],
    ['is_read', '是否已读', 'TINYINT', '', '是', '0 未读 / 1 已读'],
    ['create_time', '发送时间', 'DATETIME', '', '是', ''],
])

set_text(par(190, '借阅证信息表'), '收藏表(favorite)：')
fill_table(tbl(191, '字段名'), [
    ['id', '主键', 'BIGINT', '', '否', 'PK，自增'],
    ['user_id', '用户编号', 'BIGINT', '', '否', '外键 → user.id'],
    ['item_id', '物品编号', 'BIGINT', '', '否', '外键 → item.id'],
    ['create_time', '收藏时间', 'DATETIME', '', '是', '与 user_id 组成唯一索引 uk_user_item'],
])

drop(193)
drop(194)

put_picture(par(198), FIG + r'\fig6_er.png', 5.9)
insert_after(kids[198], [center_caption('图 4-1  表关系图（E-R 图）')])
print('database done')

# ------------------------------------------------ 12. 安全性设计
set_text(par(200, '有些安全通过数据库管理'),
         '系统安全从认证授权、数据安全、传输部署、业务风控四个层面保障：认证授权采用 JWT 令牌 + 拦截器校验，按 USER / ADMIN 两类角色区分接口权限，退出登录后令牌进入黑名单立即失效；'
         '数据安全方面，用户密码使用 BCrypt 加密存储，招领信息的“隐藏特征”字段只在审核接口中返回，不进入列表与详情响应，手机号等敏感字段对外统一脱敏；'
         '传输与部署方面，生产环境启用 HTTPS，数据库账号遵循最小权限且仅允许内网访问，Nginx 限制上传文件的类型与大小；'
         '业务风控方面，对发布与认领接口做频率限制与参数校验，所有管理操作通过日志切面记录操作人、时间与操作对象，便于事后审计。')
set_text(par(201, '数据库设计上的安全管理'),
         '数据库层面通过账号权限分离（应用账号只具备增删改查权限，不授予 DDL 权限）、外键与唯一索引约束（如 uk_username、uk_user_item）保证数据一致性；'
         '应用层面由系统管理员统一管理分类、审核与用户封禁等基础数据权限，普通用户只能操作本人发布的信息和本人发起的认领申请，越权访问由拦截器与业务校验双重拦截。')

# ------------------------------------------------ 13. 开发环境 / 测试环境
set_text(par(203, '开发环境：Microsoft'), '开发环境：IntelliJ IDEA 2023.2（后端）+ Visual Studio Code（前端）')
set_text(par(204, '开发语言'), '开发语言：Java 17 + Vue 3（JavaScript），构建工具 Maven 3.9 与 Vite 4')
set_text(par(205, '系统后台数据库'), '系统后台数据库：MySQL 8.0，持久层使用 MyBatis-Plus 3.5.8')
set_text(par(206, '开发环境运行平台'), '开发环境运行平台：Windows 11 / macOS，Node.js 18 运行前端开发服务器')

set_text(par(208, '部署测试用服务器'),
         '测试在开发机与测试服务器两套环境进行：测试服务器操作系统 Ubuntu 22.04 LTS，安装 JDK 17、MySQL 8.0 与 Nginx 1.24；'
         '接口测试使用 Apifox / Postman，性能测试使用 JMeter 5.6；测试数据由 sql/data.sql 初始化，测试完成后清库重建，保证每次测试的初始状态一致。')
set_text(par(211, '操作系统'), '操作系统：Ubuntu 22.04 LTS')
set_text(par(212, 'Web 服务器'), 'Web 服务器：Nginx 1.24')
set_text(par(213, '数据库服务器'), '数据库服务器：MySQL 8.0（独立实例，测试库 lost_found_test）')
set_text(par(214, '浏览器'), '应用服务：Spring Boot 3.5.6（JDK 17 运行时，端口 8080）')
set_text(par(215, '系统服务器运行环境'), '浏览器：Chrome 120 / Edge 120')
set_text(par(217, '浏览器'), '浏览器：Chrome、Edge、Firefox 近两年主流版本，移动端 Safari / Chrome')
set_text(par(218, '分辨率'), '分辨率：1440×900、1366×768，移动端 390×844')

doc.save(OUT)
print('saved', OUT)
