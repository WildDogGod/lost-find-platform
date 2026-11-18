# -*- coding: utf-8 -*-
"""生成 6 张配图（SVG -> HTML -> Edge headless 截图 PNG）。"""
import os, subprocess

OUT = r"D:\code\lost-found-platform\.scratch\figs"
os.makedirs(OUT, exist_ok=True)

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
FONT = "Microsoft YaHei, SimHei, sans-serif"
BLUE = "#2F6FA8"
DARK = "#1F3B57"
GRAY = "#5A6472"
LIGHT = "#EAF1F9"
GREEN = "#2E7D5B"
ORANGE = "#B4611E"

warnings = []


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def head(w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<defs><marker id="ah" markerWidth="11" markerHeight="9" refX="10" refY="4.5" orient="auto">'
            f'<path d="M0,0 L11,4.5 L0,9 z" fill="{GRAY}"/></marker></defs>'
            f'<rect width="{w}" height="{h}" fill="#FFFFFF"/>')


def text(x, y, s, fs=20, color=GRAY, anchor="start", weight="normal"):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{fs}" fill="{color}" '
            f'text-anchor="{anchor}" font-weight="{weight}">{esc(s)}</text>')


def box(x, y, w, h, lines, fs=20, fill="#FFFFFF", stroke=BLUE, rx=8, lc=None,
        weight=None, color=None, first_bold=True):
    if isinstance(lines, str):
        lines = [lines]
    lh = lc or fs * 1.45
    total = lh * (len(lines) - 1)
    y0 = y + (h - total) / 2 + fs * 0.36
    longest = max(len(l) for l in lines)
    if longest * fs * 0.95 + 24 > w:
        warnings.append(f"BOX TEXT TIGHT w={w} fs={fs} len={longest}: {lines[0][:26]}")
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>']
    for i, ln in enumerate(lines):
        bold = weight or ("bold" if (i == 0 and len(lines) > 1 and first_bold) else "normal")
        col = color or (BLUE if (i == 0 and len(lines) > 1 and first_bold) else DARK)
        out.append(f'<text x="{x + w / 2}" y="{y0 + i * lh:.1f}" font-family="{FONT}" font-size="{fs}" '
                   f'font-weight="{bold}" fill="{col}" text-anchor="middle">{esc(ln)}</text>')
    return "".join(out)


def store(x, y, w, h, lines, fs=18):
    if isinstance(lines, str):
        lines = [lines]
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#FBFCFE" stroke="{BLUE}" stroke-width="2"/>',
           f'<line x1="{x + 46}" y1="{y}" x2="{x + 46}" y2="{y + h}" stroke="{BLUE}" stroke-width="2"/>']
    lh = fs * 1.32
    y0 = y + (h - lh * (len(lines) - 1)) / 2 + fs * 0.36
    for i, ln in enumerate(lines):
        if len(ln) * fs * 0.95 + 56 > w:
            warnings.append(f"STORE TEXT TIGHT w={w}: {ln}")
        out.append(text(x + 56, y0 + i * lh, ln, fs=fs, color=DARK, anchor="start"))
    return "".join(out)


def line(pts, color=GRAY, w=2, arrow=True, dash=None, label=None, lx=0, ly=0,
         fs=18, lcolor=None, lanchor="middle", weight="normal"):
    d = " ".join(f"{p[0]},{p[1]}" for p in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    ar = ' marker-end="url(#ah)"' if arrow else ""
    out = [f'<polyline points="{d}" fill="none" stroke="{color}" stroke-width="{w}"{da}{ar}/>']
    if label:
        out.append(f'<text x="{lx}" y="{ly}" font-family="{FONT}" font-size="{fs}" fill="{lcolor or color}" '
                   f'text-anchor="{lanchor}" font-weight="{weight}" paint-order="stroke" stroke="#FFFFFF" '
                   f'stroke-width="5">{esc(label)}</text>')
    return "".join(out)


def ellipse(cx, cy, rx, ry, s, fs=19):
    if len(s) * fs * 0.95 + 26 > rx * 1.8:
        warnings.append(f"ELLIPSE TIGHT rx={rx} len={len(s)}: {s}")
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#FFFFFF" stroke="{BLUE}" stroke-width="2"/>'
            + text(cx, cy + fs * 0.36, s, fs=fs, color=DARK, anchor="middle"))


def actor(cx, top, label, fs=22):
    return "".join([
        f'<circle cx="{cx}" cy="{top + 30}" r="24" fill="#FFFFFF" stroke="{DARK}" stroke-width="2.5"/>',
        f'<line x1="{cx}" y1="{top + 54}" x2="{cx}" y2="{top + 140}" stroke="{DARK}" stroke-width="2.5"/>',
        f'<line x1="{cx - 40}" y1="{top + 82}" x2="{cx + 40}" y2="{top + 82}" stroke="{DARK}" stroke-width="2.5"/>',
        f'<line x1="{cx}" y1="{top + 140}" x2="{cx - 36}" y2="{top + 200}" stroke="{DARK}" stroke-width="2.5"/>',
        f'<line x1="{cx}" y1="{top + 140}" x2="{cx + 36}" y2="{top + 200}" stroke="{DARK}" stroke-width="2.5"/>',
        text(cx, top + 236, label, fs=fs, color=DARK, anchor="middle", weight="bold")])


def diamond(cx, cy, hw, hh, lines, fs=19):
    if isinstance(lines, str):
        lines = [lines]
    out = [f'<polygon points="{cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh} {cx - hw},{cy}" '
           f'fill="{LIGHT}" stroke="{ORANGE}" stroke-width="2"/>']
    lh = fs * 1.3
    y0 = cy - lh * (len(lines) - 1) / 2 + fs * 0.36
    for i, ln in enumerate(lines):
        out.append(text(cx, y0 + i * lh, ln, fs=fs, color=DARK, anchor="middle"))
    return "".join(out)


# ---------------------------------------------------------------- 图1 系统结构图
def fig1():
    W, H = 1600, 971
    s = [head(W, H)]
    s.append(box(560, 30, 480, 76, "校园失物招领平台", fs=30, fill=BLUE, stroke=BLUE,
                 color="#FFFFFF", weight="bold", first_bold=False))
    cols = [
        ("账号与权限模块", ["用户注册", "登录 / 退出（令牌失效）", "个人资料管理", "头像上传与修改密码"]),
        ("物品信息模块", ["发布失物 / 招领信息", "图片上传（OSS）", "浏览、检索与筛选", "物品详情展示",
                     "我的发布（编辑 / 下架 / 删除）", "智能匹配推荐"]),
        ("认领管理模块", ["提交认领申请", "我的认领进度", "收到申请的审核", "状态流转与消息通知"]),
        ("收藏与消息模块", ["收藏 / 取消收藏", "我的收藏列表", "系统与认领通知", "站内留言", "未读消息提醒"]),
        ("后台管理模块", ["物品信息审核", "用户管理（封禁 / 解封）", "物品分类管理", "平台数据统计"]),
        ("公共支撑", ["JWT 鉴权与角色控制", "统一响应与异常处理", "MySQL 数据存储", "配置外置与日志"]),
    ]
    n = len(cols)
    cw, gap = 240, 20
    x0 = (W - (n * cw + (n - 1) * gap)) / 2
    s.append(line([(800, 106), (800, 132)], arrow=False))
    s.append(line([(x0 + cw / 2, 132), (x0 + (n - 1) * (cw + gap) + cw / 2, 132)], arrow=False))
    for i, (title, subs) in enumerate(cols):
        cx = x0 + i * (cw + gap)
        s.append(line([(cx + cw / 2, 132), (cx + cw / 2, 176)], arrow=True))
        s.append(box(cx, 176, cw, 58, title, fs=20, fill=LIGHT))
        s.append(line([(cx + cw / 2, 234), (cx + cw / 2, 268)], arrow=True))
        step = 62
        ch = 46 + len(subs) * step
        s.append(f'<rect x="{cx}" y="268" width="{cw}" height="{ch}" rx="8" fill="#FBFCFE" '
                 f'stroke="{GRAY}" stroke-width="1.5" stroke-dasharray="5 4"/>')
        for j, sub in enumerate(subs):
            s.append(text(cx + cw / 2, 268 + 42 + j * step, sub, fs=16, color=DARK, anchor="middle"))
    s.append("</svg>")
    return "fig1_structure", W, H, "".join(s)


# ---------------------------------------------------------------- 图2 普通用户用例图
def fig2():
    W, H = 1000, 1044
    s = [head(W, H)]
    s.append(f'<rect x="280" y="40" width="690" height="964" rx="14" fill="#FCFDFF" stroke="{BLUE}" stroke-width="2.5"/>')
    s.append(text(625, 92, "校园失物招领平台（前台）", fs=26, color=BLUE, anchor="middle", weight="bold"))
    s.append(actor(140, 400, "普通用户"))
    cases = [
        (520, 150, "注册 / 登录"), (800, 150, "提交认领申请"),
        (520, 290, "浏览与检索物品"), (800, 290, "审核收到的认领申请"),
        (520, 430, "查看物品详情"), (800, 430, "收藏 / 取消收藏"),
        (520, 570, "发布失物 / 招领信息"), (800, 570, "收发站内消息"),
        (520, 710, "上传图片至 OSS"), (800, 710, "维护个人资料"),
        (520, 850, "管理我的发布"), (800, 850, "修改密码"),
    ]
    for cx, cy, name in cases:
        s.append(ellipse(cx, cy, 140, 40, name, fs=18))
        s.append(line([(172, 482), (cx - 140, cy)], color="#9AA7B4", w=1.6))
    s.append("</svg>")
    return "fig2_user_usecase", W, H, "".join(s)


# ---------------------------------------------------------------- 图3 管理员用例图
def fig3():
    W, H = 1300, 1114
    s = [head(W, H)]
    s.append(f'<rect x="330" y="40" width="930" height="1034" rx="14" fill="#FCFDFF" stroke="{BLUE}" stroke-width="2.5"/>')
    s.append(text(795, 94, "校园失物招领平台（管理后台）", fs=28, color=BLUE, anchor="middle", weight="bold"))
    s.append(actor(160, 430, "管理员"))
    cases = [
        (640, 200, "登录后台"), (990, 200, "查询用户信息"),
        (640, 370, "查询物品列表"), (990, 370, "封禁 / 解封用户"),
        (640, 540, "审核物品信息（通过 / 驳回）"), (990, 540, "管理物品分类"),
        (640, 710, "处理违规信息"), (990, 710, "查看数据统计"),
        (640, 880, "填写审核备注并通知发布者"), (990, 880, "导出统计结果"),
    ]
    for cx, cy, name in cases:
        s.append(ellipse(cx, cy, 175, 46, name, fs=19))
        s.append(line([(204, 512), (cx - 175, cy)], color="#9AA7B4", w=1.6))
    s.append("</svg>")
    return "fig3_admin_usecase", W, H, "".join(s)


# ---------------------------------------------------------------- 图4 业务流程图
def fig4():
    W, H = 1600, 1149
    s = [head(W, H)]
    lx, lw = 60, 600
    rows = [
        (30, "开始", GREEN, "#EAF4EF"),
        (128, "用户注册 / 登录，获取 JWT 令牌", BLUE, "#FFFFFF"),
        (226, "发布失物 / 招领信息（填写表单、上传图片至 OSS）", BLUE, "#FFFFFF"),
        (324, "物品状态：待审核 PENDING", BLUE, "#FFFFFF"),
        (560, "物品状态：已通过 ACTIVE，前台列表与详情展示", BLUE, "#FFFFFF"),
        (658, "失主浏览 / 检索物品，查看详情并核验物品特征", BLUE, "#FFFFFF"),
        (756, "提交认领申请（填写认领凭证描述）→ 待审核 PENDING", BLUE, "#FFFFFF"),
        (968, "认领通过 APPROVED：物品状态置为已完成 COMPLETED", GREEN, "#EAF4EF"),
    ]
    for y, label, col, fill in rows:
        s.append(box(lx, y, lw, 64, label, fs=21, fill=fill, stroke=col))
    # 主干箭头
    for a, b in [(94, 128), (192, 226), (290, 324), (388, 420), (528, 560),
                 (624, 658), (722, 756), (820, 830), (938, 968)]:
        s.append(line([(360, a), (360, b)], arrow=True))
    s.append(text(374, 556, "通过", fs=19, color=GREEN, anchor="start", weight="bold"))
    s.append(text(374, 962, "通过", fs=19, color=GREEN, anchor="start", weight="bold"))
    # 判断菱形
    s.append(diamond(360, 474, 170, 54, ["管理员审核", "（通过 / 驳回）"], fs=20))
    s.append(diamond(360, 884, 170, 54, ["发布者 / 管理员", "审核认领申请"], fs=19))
    # 右侧分支
    rx, rw = 900, 640
    s.append(line([(530, 474), (rx, 474)], arrow=True))
    s.append(box(rx, 424, rw, 100, ["驳回：物品状态置为已关闭 CLOSED",
                                    "系统消息通知发布者，修改后可重新提交"], fs=20,
                 fill="#FDF4EC", stroke=ORANGE))
    s.append(line([(rx + rw / 2, 524), (rx + rw / 2, 570), (760, 570), (760, 356), (666, 356)], arrow=True))
    s.append(text(772, 424, "修改后重新提交", fs=18, color=GRAY, anchor="start"))
    s.append(line([(530, 884), (rx, 884)], arrow=True))
    s.append(box(rx, 836, rw, 96, ["驳回：认领状态置为 REJECTED",
                                   "消息通知申请人，物品回到可认领状态"], fs=20,
                 fill="#FDF4EC", stroke=ORANGE))
    s.append(line([(660, 1000), (rx, 1000)], arrow=True))
    s.append(box(rx, 964, rw, 72, "同一物品的其他待审核申请自动驳回并通知", fs=20,
                 fill="#FBF3F3", stroke="#A33A3A"))
    s.append(line([(rx + rw / 2, 1036), (rx + rw / 2, 1064)], arrow=True))
    s.append(box(rx, 1064, rw, 62, "结束：物品归还失主，平台记录完成", fs=21, fill="#EAF4EF",
                 stroke=GREEN, rx=31, weight="bold", color=GREEN, first_bold=False))
    s.append("</svg>")
    return "fig4_flow", W, H, "".join(s)


# ---------------------------------------------------------------- 图5 0层数据流图
def fig5():
    W, H = 1600, 915
    s = [head(W, H)]
    s.append(box(40, 120, 220, 90, "普通用户", fs=22, fill=LIGHT))
    s.append(box(40, 650, 220, 90, "管理员", fs=22, fill=LIGHT))
    s.append(box(1340, 60, 220, 100, ["阿里云 OSS", "（图片存储）"], fs=20, fill=LIGHT))
    procs = [
        (60, "P1 用户与权限管理", "注册、登录、资料、密码"),
        (220, "P2 物品信息管理", "发布、编辑、检索、图片"),
        (380, "P3 认领审核管理", "申请、审核、状态流转"),
        (540, "P4 消息与收藏服务", "消息、已读、收藏"),
        (700, "P5 后台审核与统计", "审核、用户管理、统计"),
    ]
    px, pw = 420, 300
    for y, t, sub in procs:
        s.append(box(px, y, pw, 90, [t, sub], fs=20, fill="#F7FAFD"))
    stores = [(60, ["D1  用户信息表", "user"]), (220, ["D2  物品信息表", "item"]),
              (380, ["D3  认领记录表", "claim"]), (540, ["D4  消息 / 收藏表", "message、favorite"]),
              (700, ["D5  分类表", "category"])]
    sx, sw = 880, 320
    for y, t in stores:
        s.append(store(sx, y + 13, sw, 64, t, fs=18))
    for y, lbl in [(60, "注册 / 登录 / 资料"), (220, "发布 / 编辑 / 检索"),
                   (380, "认领申请 / 审核"), (540, "收藏 / 消息")]:
        s.append(line([(260, 165), (350, 165), (350, y + 45), (px, y + 45)], arrow=True, w=1.8))
        s.append(text(345, y + 38, lbl, fs=16, color=GRAY, anchor="end"))
    s.append(line([(260, 695), (360, 695), (360, 745), (px, 745)], arrow=True, w=1.8))
    s.append(text(272, 688, "审核 / 用户管理 / 统计", fs=16, color=GRAY, anchor="start"))
    for y, lbl in [(60, "读写"), (220, "读写"), (380, "读写"), (540, "读写"), (700, "读写")]:
        s.append(line([(px + pw, y + 45), (sx, y + 45)], arrow=True, w=1.8))
        s.append(text((px + pw + sx) / 2, y + 38, lbl, fs=16, color=GRAY, anchor="middle"))
    s.append(line([(700, 470), (1000, 470), (1000, 297)], arrow=True, w=1.8, dash="6 5"))
    s.append(text(742, 460, "更新物品状态", fs=16, color=GRAY, anchor="start"))
    s.append(line([(720, 745), (780, 745), (780, 880), (1290, 880), (1290, 105), (1200, 105)],
                  arrow=True, w=1.8, dash="6 5"))
    s.append(text(1000, 872, "读取用户与物品数据生成统计", fs=16, color=GRAY, anchor="middle"))
    s.append(line([(700, 220), (700, 180), (1440, 180), (1440, 160)], arrow=True, w=1.8))
    s.append(text(900, 172, "上传图片 / 返回可访问 URL", fs=17, color=GRAY, anchor="middle"))
    s.append("</svg>")
    return "fig5_dfd", W, H, "".join(s)


# ---------------------------------------------------------------- 图6 E-R 图
def fig6():
    W, H = 1500, 1125
    s = [head(W, H)]

    def entity(x, y, w, title, attrs, fs=19):
        h = 52 + len(attrs) * 29 + 16
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#FFFFFF" stroke="{BLUE}" stroke-width="2"/>')
        s.append(f'<path d="M{x+8},{y} H{x+w-8} A8,8 0 0 1 {x+w},{y+8} V{y+42} H{x} V{y+8} A8,8 0 0 1 {x+8},{y} Z" '
                 f'fill="{LIGHT}" stroke="{BLUE}" stroke-width="2"/>')
        s.append(text(x + w / 2, y + 29, title, fs=21, color=BLUE, anchor="middle", weight="bold"))
        for i, a in enumerate(attrs):
            s.append(text(x + 16, y + 70 + i * 29, a, fs=fs, color=DARK, anchor="start"))
        return h

    entity(40, 60, 400, "用户 User", [
        "id  BIGINT  PK", "username  登录账号（唯一）", "password  密码密文（BCrypt）",
        "real_name / student_no", "college / phone / email", "avatar  头像 URL",
        "verify_status  认证状态", "role  角色 USER / ADMIN", "status  账号状态",
        "create_time / update_time"])
    entity(560, 60, 400, "物品 Item", [
        "id  BIGINT  PK", "type  LOST 失物 / FOUND 招领", "title / description",
        "category_id  FK → 分类", "images  图片 URL（逗号分隔）", "event_time / location",
        "secret_feature  隐藏特征", "contact_name / contact_phone", "status  PENDING / ACTIVE /",
        "          PROCESSING / COMPLETED / CLOSED", "user_id  FK → 发布者", "audit_remark  审核备注"])
    entity(1060, 60, 400, "分类 Category", ["id  BIGINT  PK", "name  分类名称", "icon  图标", "sort  排序"])
    entity(40, 640, 400, "收藏 Favorite", [
        "id  BIGINT  PK", "user_id  FK → 用户", "item_id  FK → 物品", "create_time  收藏时间"])
    entity(560, 640, 400, "认领 Claim", [
        "id  BIGINT  PK", "item_id  FK → 物品", "applicant_id  FK → 申请人",
        "claim_desc  认领凭证描述", "status  PENDING / APPROVED / REJECTED",
        "review_remark  审核备注", "reviewer_id  FK → 审核人", "create_time / review_time"])
    entity(1060, 640, 400, "消息 Message", [
        "id  BIGINT  PK", "from_user_id  FK → 发送者", "to_user_id  FK → 接收者",
        "item_id  FK → 关联物品", "type  SYSTEM / CLAIM / CHAT", "content  消息内容",
        "is_read  是否已读", "create_time  发送时间"])

    orl = lambda pts, lbl, lx, ly, anchor="middle": (
        line(pts, color=GRAY, w=2, arrow=True) + text(lx, ly, lbl, fs=18, color=ORANGE, anchor=anchor, weight="bold"))
    s.append(orl([(440, 220), (560, 220)], "发布 1:N", 500, 205))
    s.append(orl([(960, 220), (1060, 220)], "属于 N:1", 1010, 205))
    s.append(orl([(800, 476), (800, 640)], "对应 1:N", 812, 566, "start"))
    s.append(orl([(200, 418), (200, 640)], "收藏 M:N", 212, 540, "start"))
    s.append(orl([(380, 418), (380, 578), (620, 578), (620, 640)], "申请 / 审核 1:N", 480, 566))
    s.append(orl([(600, 476), (600, 618), (400, 618), (400, 640)], "被收藏 M:N", 500, 606))
    s.append(orl([(940, 380), (1000, 380), (1000, 590), (1260, 590), (1260, 640)], "关联 N:1", 1012, 470, "start"))
    s.append(orl([(40, 120), (16, 120), (16, 1060), (1260, 1060), (1260, 940)],
                 "接收 / 发送 1:N（from_user_id、to_user_id）", 700, 1092))
    s.append("</svg>")
    return "fig6_er", W, H, "".join(s)


FIGS = [fig1(), fig2(), fig3(), fig4(), fig5(), fig6()]

for name, w, h, svg in FIGS:
    html = ('<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;padding:0;'
            'overflow:hidden;background:#fff}</style></head><body>' + svg + '</body></html>')
    hp = os.path.join(OUT, name + ".html")
    with open(hp, "w", encoding="utf-8") as f:
        f.write(html)
    png = os.path.join(OUT, name + ".png")
    cmd = [EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
           f"--window-size={w},{h}", f"--screenshot={png}",
           f"--user-data-dir={os.path.join(OUT, '_edgeprofile')}", "file:///" + hp.replace("\\", "/")]
    r = subprocess.run(cmd, capture_output=True)
    print(name, "rc=", r.returncode, "png=", os.path.exists(png))

print("WARNINGS:", len(warnings))
for x in warnings:
    print("  ", x)