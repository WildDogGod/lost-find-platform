# -*- coding: utf-8 -*-
"""生成实验2设计文档所需配图：系统部署结构图 / 物品发布模块流程图 / 认领审核模块流程图。"""
import os, subprocess

OUT = r"D:\code\lost-found-platform\.scratch\figs2"
os.makedirs(OUT, exist_ok=True)

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
FONT = "Microsoft YaHei, SimHei, sans-serif"
BLUE = "#2F6FA8"
DARK = "#1F3B57"
GRAY = "#5A6472"
LIGHT = "#EAF1F9"
GREEN = "#2E7D5B"
GREENL = "#EAF5EF"
ORANGE = "#B4611E"
RED = "#9A3B33"
REDL = "#FBEFEE"


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


def box(x, y, w, h, lines, fs=19, fill="#FFFFFF", stroke=BLUE, rx=8, color=None,
        dashed=False, weight="normal", lh=None, align="middle"):
    if isinstance(lines, str):
        lines = [lines]
    step = lh or fs * 1.55
    total = step * (len(lines) - 1)
    y0 = y + (h - total) / 2 + fs * 0.36
    da = ' stroke-dasharray="6 4"' if dashed else ''
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" '
           f'stroke-width="2"{da}/>']
    for i, ln in enumerate(lines):
        first = i == 0 and len(lines) > 1 and weight == "bold"
        out.append(text(x + w / 2 if align == "middle" else x + 14, y0 + i * step, ln, fs=fs,
                        color=(color or (BLUE if first else DARK)), anchor=align,
                        weight=("bold" if first else "normal")))
    return "".join(out)


def diamond(cx, cy, hw, hh, lines, fs=19, fill=LIGHT, stroke=ORANGE):
    if isinstance(lines, str):
        lines = [lines]
    out = [f'<polygon points="{cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh} {cx - hw},{cy}" '
           f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>']
    lh = fs * 1.32
    y0 = cy - lh * (len(lines) - 1) / 2 + fs * 0.34
    for i, ln in enumerate(lines):
        out.append(text(cx, y0 + i * lh, ln, fs=fs, color=DARK, anchor="middle"))
    return "".join(out)


def line(pts, color=GRAY, w=2, arrow=True, dash=None, label=None, lx=0, ly=0,
         fs=18, lcolor=None, lanchor="middle", weight="bold"):
    d = " ".join(f"{p[0]},{p[1]}" for p in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    ar = ' marker-end="url(#ah)"' if arrow else ""
    out = [f'<polyline points="{d}" fill="none" stroke="{color}" stroke-width="{w}"{da}{ar}/>']
    if label:
        out.append(f'<text x="{lx}" y="{ly}" font-family="{FONT}" font-size="{fs}" fill="{lcolor or color}" '
                   f'text-anchor="{lanchor}" font-weight="{weight}" paint-order="stroke" stroke="#FFFFFF" '
                   f'stroke-width="6">{esc(label)}</text>')
    return "".join(out)


# --------------------------------------------------------------- 系统部署结构图
def fig_deploy():
    W, H = 1440, 960
    s = [head(W, H)]
    lx = 46

    # 用户层
    s.append(text(lx, 96, "用户层", fs=20, color=BLUE, weight="bold"))
    s.append(box(300, 60, 470, 84, ["PC 浏览器（Chrome / Edge / Firefox）", "学生、教师、管理员访问"], fs=18, fill=LIGHT))
    s.append(box(830, 60, 470, 84, ["移动端浏览器", "手机 / 平板自适应访问"], fs=18, fill=LIGHT))

    # 接入层
    s.append(text(lx, 292, "接入层", fs=20, color=BLUE, weight="bold"))
    s.append(box(300, 230, 1000, 100, ["Nginx 1.24（HTTPS，443 / 80）",
                                       "托管 Vue3 打包后的静态资源　｜　/api 反向代理至应用服务"], fs=18))

    # 应用层
    s.append(text(lx, 470, "应用层", fs=20, color=BLUE, weight="bold"))
    s.append(box(300, 386, 1000, 46, ["Spring Boot 3.5.6 应用服务（内嵌 Tomcat，端口 8080）"],
                 fs=19, fill=LIGHT, weight="bold", rx=8))
    inner = [
        ("控制层 Controller", "RESTful 接口、参数校验"),
        ("业务层 Service", "业务规则、事务控制"),
        ("持久层 Mapper", "MyBatis-Plus 读写数据库"),
        ("公共支撑", "JWT 拦截器、全局异常、日志切面"),
    ]
    bw, gap = 478, 24
    for i, (t1, t2) in enumerate(inner):
        x = 300 + (i % 2) * (bw + gap)
        y = 446 + (i // 2) * 88
        s.append(box(x, y, bw, 78, [t1, t2], fs=16, fill="#FFFFFF"))

    # 数据层
    s.append(text(lx, 720, "数据层", fs=20, color=BLUE, weight="bold"))
    s.append(box(300, 660, 470, 116, ["MySQL 8.0（lost_found 库）", "InnoDB / utf8mb4 / 6 张业务表"], fs=18))
    s.append(box(830, 660, 470, 116, ["阿里云 OSS 对象存储", "物品图片、用户头像（URL 访问）"], fs=18))

    # 连线
    s.append(line([(535, 144), (535, 230)], label="HTTPS", lx=548, ly=196, lanchor="start"))
    s.append(line([(1065, 144), (1065, 230)], label="HTTPS", lx=1078, ly=196, lanchor="start"))
    s.append(line([(800, 330), (800, 386)], label="HTTP /api", lx=814, ly=366, lanchor="start"))
    s.append(line([(470, 612), (470, 660)], label="JDBC", lx=484, ly=644, lanchor="start"))
    s.append(line([(1130, 612), (1130, 660)], label="SDK 上传", lx=1144, ly=644, lanchor="start"))
    s.append(text(720, 810, "说明：前后端分离部署，前端静态资源与应用服务可同机部署，也可分机部署；图片默认存本地 upload 目录，生产环境切阿里云 OSS。",
                  fs=16, color=GRAY, anchor="middle"))
    s.append("</svg>")
    return "fig_deploy", W, H, "".join(s)


# --------------------------------------------------------------- 物品发布模块流程图
def fig_publish():
    W, H = 1220, 1260
    s = [head(W, H)]
    cx, hw = 450, 330
    bw = 560

    def node(y, lines, h=78, fill="#FFFFFF", stroke=BLUE, color=None):
        s.append(box(cx - bw / 2, y, bw, h, lines, fs=18, fill=fill, stroke=stroke, color=color))

    s.append(box(cx - 90, 24, 180, 56, "开始", fs=20, fill=GREENL, stroke=GREEN, color=GREEN))
    s.append(line([(cx, 80), (cx, 108)]))
    node(108, "用户点击“发布失物 / 招领”，进入发布页面", 62)
    s.append(line([(cx, 170), (cx, 198)]))
    node(198, ["填写发布表单：类型（失物 / 招领）、标题、分类、描述、", "发生时间、地点、隐藏特征、联系人及电话"], 84)
    s.append(line([(cx, 282), (cx, 310)]))
    node(310, ["选择本地图片，前端校验格式（jpg / png / webp）", "与单张大小（≤ 5MB）、最多 3 张"], 84)
    s.append(line([(cx, 394), (cx, 422)]))
    node(422, "调用上传接口，图片写入 OSS 并返回访问 URL", 62)
    s.append(line([(cx, 484), (cx, 512)]))
    s.append(diamond(cx, 570, 150, 56, ["表单校验通过？"], fs=19))
    s.append(line([(cx, 626), (cx, 660)]))
    node(660, "提交 POST /api/items，请求头携带 JWT 令牌", 62)
    s.append(line([(cx, 722), (cx, 750)]))
    node(750, ["后端校验登录态与角色、必填项与长度、图片 URL 合法性与", "发布频率，并按“类型 + 分类 + 关键词”生成匹配候选"], 84)
    s.append(line([(cx, 834), (cx, 862)]))
    s.append(diamond(cx, 920, 150, 56, ["校验通过？"], fs=19))
    s.append(line([(cx, 976), (cx, 1010)]))
    node(1010, ["写入 item 表：status = PENDING、user_id = 发布者、", "create_time = 当前时间，返回统一 Result 结果"], 84)
    s.append(line([(cx, 1094), (cx, 1122)]))
    node(1122, "页面提示“提交成功，等待管理员审核”，跳转“我的发布”", 62)
    s.append(line([(cx, 1184), (cx, 1204)]))
    s.append(box(cx - 120, 1204, 240, 52, "结束（待审核）", fs=18, fill=GREENL, stroke=GREEN, color=GREEN))

    # 失败分支
    s.append(line([(620, 570), (750, 570)], label="否", lx=634, ly=556, lanchor="start"))
    s.append(box(775, 512, 400, 116, ["前端提示错误并高亮对应字段", "（如“请选择物品分类”）",
                                      "返回表单修改后重新提交"], fs=15, fill=REDL, stroke=RED, color=RED))

    s.append(line([(620, 920), (750, 920)], label="否", lx=634, ly=906, lanchor="start"))
    s.append(box(775, 862, 400, 116, ["返回 Result(code≠200) 与错误描述", "已填内容保留在表单中",
                                      "修改后重新提交"], fs=15, fill=REDL, stroke=RED, color=RED))
    s.append("</svg>")
    return "fig_flow_publish", W, H, "".join(s)


# --------------------------------------------------------------- 认领审核模块流程图
def fig_claim():
    W, H = 1400, 1320
    s = [head(W, H)]
    cx, bw = 420, 600

    def node(y, lines, h=78, fill="#FFFFFF", stroke=BLUE, color=None):
        s.append(box(cx - bw / 2, y, bw, h, lines, fs=18, fill=fill, stroke=stroke, color=color))

    s.append(box(cx - 90, 24, 180, 56, "开始", fs=20, fill=GREENL, stroke=GREEN, color=GREEN))
    s.append(line([(cx, 80), (cx, 106)]))
    node(106, "申请人在物品详情页点击“我要认领”，填写认领凭证描述", 68)
    s.append(line([(cx, 174), (cx, 200)]))
    node(200, ["校验：已登录且账号正常；物品状态为 ACTIVE；申请人不是发布者；", "该物品下无本人待审申请"], 84)
    s.append(line([(cx, 284), (cx, 310)]))
    s.append(diamond(cx, 372, 152, 58, ["满足认领条件？"], fs=19))
    s.append(line([(cx, 430), (cx, 462)]))
    node(462, ["创建 claim 记录（status = PENDING，claim_desc = 凭证描述），", "item 状态由 ACTIVE 置为 PROCESSING"], 84)
    s.append(line([(cx, 546), (cx, 574)]))
    node(574, "写入 message 表，通知发布者“收到新的认领申请”", 62)
    s.append(line([(cx, 636), (cx, 664)]))
    node(664, ["发布者（或管理员）在“收到的申请”中查看凭证，核对隐藏特征，", "作出审核结论：通过 / 驳回，并填写审核备注"], 84)
    s.append(line([(cx, 748), (cx, 776)]))
    s.append(diamond(cx, 838, 150, 56, ["审核通过？"], fs=19))
    s.append(line([(cx, 894), (cx, 926)]))
    node(926, ["claim 置为 APPROVED、review_time = 当前时间；", "item 置为 COMPLETED；同一物品其他待审申请自动 REJECTED"], 88)
    s.append(line([(cx, 1014), (cx, 1042)]))
    node(1042, ["写入 message 表通知申请人认领成功及其他申请人申请已关闭，", "物品从列表“可认领”集合中移除"], 84)
    s.append(line([(cx, 1126), (cx, 1154)]))
    s.append(box(cx - 150, 1154, 300, 56, "结束（物品归还失主）", fs=18, fill=GREENL, stroke=GREEN, color=GREEN))

    # 否分支一：条件不满足
    s.append(line([(572, 372), (700, 372)], label="否", lx=586, ly=358, lanchor="start"))
    s.append(box(710, 320, 620, 110, ["直接拒绝并返回原因：物品已被认领 / 不可认领、", "不能认领自己发布的信息、已有待审申请",
                                      "流程返回物品详情页，本次申请不落库"], fs=16, fill=REDL, stroke=RED, color=RED))

    # 否分支二：审核驳回
    s.append(line([(570, 838), (700, 838)], label="否", lx=584, ly=824, lanchor="start"))
    s.append(box(710, 772, 620, 136, ["claim 置为 REJECTED，review_remark 记录驳回原因；", "item 恢复为 ACTIVE 可重新被认领；",
                                      "通知申请人驳回结果，等待其他申请人发起"], fs=16, fill=REDL, stroke=RED, color=RED))
    s.append("</svg>")
    return "fig_flow_claim", W, H, "".join(s)


FIGS = [fig_deploy(), fig_publish(), fig_claim()]

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
