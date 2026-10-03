from pathlib import Path
import html, re

OUT = Path(__file__).resolve().parent
VIEW_W, VIEW_H = 1280, 720

THEMES = {
    "light": dict(
        paper="#F4F4F5", surface="#FFFFFF", surface2="#E4E4E7",
        ink="#18181B", muted="#52525B", soft="#71717A", rule="#D4D4D8",
        accent="#F43F5E", accent_tint="rgba(244,63,94,0.08)",
        link="#0284C7", wash="rgba(24,24,27,0.025)",
        line="rgba(24,24,27,0.18)", activation="rgba(24,24,27,0.06)"
    ),
    "dark": dict(
        paper="#0D1117", surface="#161B22", surface2="#21262D",
        ink="#F0F6FC", muted="#8B949E", soft="#6E7681", rule="#30363D",
        accent="#FB7185", accent_tint="rgba(251,113,133,0.10)",
        link="#38BDF8", wash="rgba(240,246,252,0.025)",
        line="rgba(240,246,252,0.18)", activation="rgba(240,246,252,0.06)"
    ),
}

def E(s): return html.escape(str(s), quote=True)
def txt(x,y,s,c,size=12,weight=400,anchor="middle",family="sans",italic=False,tracking=None):
    fam = {"sans":"'Geist',system-ui,sans-serif","mono":"'Geist Mono',ui-monospace,monospace","serif":"'Instrument Serif',serif"}[family]
    attrs = f' x="{x}" y="{y}" fill="{c}" font-family="{fam}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}"'
    if italic: attrs += ' font-style="italic"'
    if tracking: attrs += f' letter-spacing="{tracking}"'
    return f'<text data-role="text"{attrs}>{E(s)}</text>'

def node(x,y,w,h,title,sub,tag,c,kind="normal"):
    fill, stroke, sw, dash = c["surface"], c["rule"], 1, ""
    if kind=="focal": fill,stroke,sw = c["accent_tint"],c["accent"],1.4
    elif kind=="external": fill,stroke = c["wash"],c["soft"]
    elif kind=="store": fill,stroke = c["surface2"],c["muted"]
    elif kind=="optional": fill,stroke,dash = c["wash"],c["soft"],' stroke-dasharray="4,3"'
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{c["paper"]}"/>',
           f'<rect data-role="node" x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash}/>']
    out += [f'<rect x="{x+10}" y="{y+8}" width="36" height="14" rx="2" fill="none" stroke="{stroke}" stroke-opacity=".45" stroke-width=".8"/>',
            txt(x+28,y+18,tag,stroke,8,600,family="mono",tracking=".08em"),
            txt(x+w/2,y+48,title,c["ink"],16,600),
            txt(x+w/2,y+69,sub,c["muted"],11,400,family="mono")]
    return "".join(out)

def zone(x,y,w,h,label,c):
    return (f'<rect data-role="zone" x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{c["wash"]}" stroke="{c["line"]}" stroke-width=".8"/>'
            + f'<rect x="{x+16}" y="{y+8}" width="{max(84,len(label)*8)}" height="16" rx="2" fill="{c["paper"]}"/>'
            + txt(x+24,y+20,label,c["soft"],8,600,"start","mono",tracking=".14em"))

def h_arrow(x1,y,x2,label,c,style="muted",dash=False):
    color = c["accent"] if style=="accent" else c["link"] if style=="link" else c["muted"]
    marker = "arr-accent" if style=="accent" else "arr-link" if style=="link" else "arr"
    line = f'<line data-role="connector" x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="{1.4 if style=="accent" else 1.2}"'
    if dash: line += ' stroke-dasharray="5,4"'
    line += f' marker-end="url(#{marker})"/>'
    if label:
        w=max(68,len(label)*7); mx=(x1+x2)/2
        line += f'<rect data-role="label-mask" x="{mx-w/2}" y="{y-25}" width="{w}" height="14" rx="2" fill="{c["paper"]}"/>'
        line += txt(mx,y-15,label.upper(),color,8,500,family="mono",tracking=".06em")
    return line

def elbow(x1,y1,x2,y2,label,c,style="muted",mid=None,dash=False):
    color = c["accent"] if style=="accent" else c["link"] if style=="link" else c["muted"]
    marker = "arr-accent" if style=="accent" else "arr-link" if style=="link" else "arr"
    m = mid if mid is not None else (x1+x2)//2
    sy = 8 if y2>y1 else -8
    d=f'M {x1},{y1} H {m-8} Q {m},{y1} {m},{y1+sy} V {y2-sy} Q {m},{y2} {m+8},{y2} H {x2}'
    out=f'<path data-role="connector" d="{d}" fill="none" stroke="{color}" stroke-width="{1.4 if style=="accent" else 1.2}"'
    if dash: out += ' stroke-dasharray="5,4"'
    out += f' marker-end="url(#{marker})"/>'
    if label:
        w=max(68,len(label)*7); ly=(y1+y2)/2
        out += f'<rect data-role="label-mask" x="{m+10}" y="{ly-10}" width="{w}" height="14" rx="2" fill="{c["paper"]}"/>'
        out += txt(m+14,ly,label.upper(),color,8,500,"start","mono",tracking=".06em")
    return out

def v_arrow(x,y1,y2,label,c,style="muted",dash=False,label_side="right"):
    color = c["accent"] if style=="accent" else c["link"] if style=="link" else c["muted"]
    marker = "arr-accent" if style=="accent" else "arr-link" if style=="link" else "arr"
    out=f'<line data-role="connector" x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{color}" stroke-width="{1.4 if style=="accent" else 1.2}"'
    if dash: out += ' stroke-dasharray="5,4"'
    out += f' marker-end="url(#{marker})"/>'
    if label:
        w=max(68,len(label)*7); lx=x+12 if label_side=="right" else x-w-12; ly=(y1+y2)/2
        out += f'<rect data-role="label-mask" x="{lx}" y="{ly-10}" width="{w}" height="14" rx="2" fill="{c["paper"]}"/>'
        out += txt(lx+4,ly,label.upper(),color,8,500,"start","mono",tracking=".06em")
    return out

def defs(c):
    return f'''<defs>
<marker id="arr" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="{c["muted"]}"/></marker>
<marker id="arr-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="{c["accent"]}"/></marker>
<marker id="arr-link" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="{c["link"]}"/></marker>
</defs>'''

def legend(c, items):
    y=588; out=[f'<line x1="40" y1="{y}" x2="1240" y2="{y}" stroke="{c["line"]}" stroke-width=".8"/>',
                txt(40,y+24,"LEGEND",c["muted"],8,600,"start","mono",tracking=".18em")]
    x=140
    for kind,label in items:
        if kind=="focal": out.append(f'<rect x="{x}" y="{y+14}" width="18" height="12" rx="2" fill="{c["accent_tint"]}" stroke="{c["accent"]}"/>')
        elif kind=="external": out.append(f'<rect x="{x}" y="{y+14}" width="18" height="12" rx="2" fill="{c["wash"]}" stroke="{c["soft"]}"/>')
        elif kind=="link": out.append(f'<line x1="{x}" y1="{y+20}" x2="{x+24}" y2="{y+20}" stroke="{c["link"]}" stroke-width="1.2" marker-end="url(#arr-link)"/>')
        else: out.append(f'<line x1="{x}" y1="{y+20}" x2="{x+24}" y2="{y+20}" stroke="{c["muted"]}" stroke-width="1.2" marker-end="url(#arr)"/>')
        out.append(txt(x+32,y+23,label,c["muted"],9,400,"start"))
        x += max(164, len(label)*8+64)
    return "".join(out)

def dfd_entity(x,y,w,h,title,sub,c):
    out=[f'<rect data-role="node" x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{c["surface"]}" stroke="{c["muted"]}" stroke-width="1.2"/>']
    out += [txt(x+w/2,y+32,title,c["ink"],14,600),txt(x+w/2,y+52,sub,c["muted"],9,400,family="mono")]
    return "".join(out)

def dfd_process(x,y,w,h,num,title,sub,c,focal=False):
    stroke=c["accent"] if focal else c["muted"]; fill=c["accent_tint"] if focal else c["surface"]
    out=[f'<rect data-role="node" x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}" stroke="{stroke}" stroke-width="{1.4 if focal else 1.1}"/>',
         f'<rect x="{x+12}" y="{y+10}" width="42" height="18" rx="2" fill="{c["paper"]}" stroke="{stroke}" stroke-opacity=".5" stroke-width=".8"/>',
         txt(x+33,y+23,num,stroke,8,600,family="mono"),
         txt(x+w/2,y+43,title,c["ink"],13,600),
         txt(x+w/2,y+61,sub,c["muted"],8,400,family="mono")]
    return "".join(out)

def dfd_store(x,y,w,h,code,title,sub,c):
    out=[f'<path data-role="node" d="M {x+14},{y} H {x+w} V {y+h} H {x+14} M {x+14},{y} V {y+h}" fill="{c["surface2"]}" stroke="{c["muted"]}" stroke-width="1.1"/>',
         f'<rect x="{x}" y="{y}" width="36" height="{h}" fill="{c["paper"]}" stroke="{c["muted"]}" stroke-width="1.1"/>',
         txt(x+18,y+h/2+3,code,c["muted"],8,600,family="mono"),
         txt(x+48,y+24,title,c["ink"],12,600,"start"),
         txt(x+48,y+42,sub,c["muted"],8,400,"start","mono")]
    return "".join(out)

def seq_message(x1,x2,y,label,c,kind="call",style="muted"):
    color=c["accent"] if style=="accent" else c["link"] if style=="link" else c["muted"]
    dash=' stroke-dasharray="5,4"' if kind=="return" else ""
    out=f'<line data-role="connector" x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="{1.4 if style=="accent" else 1.1}"{dash} marker-end="url(#{"arr-accent" if style=="accent" else "arr-link" if style=="link" else "arr"})"/>'
    w=max(72,len(label)*6.2); mx=(x1+x2)/2
    out += f'<rect data-role="label-mask" x="{mx-w/2}" y="{y-20}" width="{w}" height="12" rx="2" fill="{c["paper"]}"/>'
    out += txt(mx,y-11,label.upper(),color,8,500,family="mono",tracking=".04em")
    return out

def seq_self(x,y,label,c,style="muted"):
    color=c["accent"] if style=="accent" else c["muted"]
    out=f'<path data-role="connector" d="M {x},{y} H {x+54} V {y+18} H {x+8}" fill="none" stroke="{color}" stroke-width="1.1" marker-end="url(#{"arr-accent" if style=="accent" else "arr"})"/>'
    w=max(76,len(label)*6.2)
    out += f'<rect data-role="label-mask" x="{x+62}" y="{y+1}" width="{w}" height="12" rx="2" fill="{c["paper"]}"/>'
    out += txt(x+66,y+10,label.upper(),color,8,500,"start","mono",tracking=".04em")
    return out

def architecture_body(c):
    # Zones own runtime responsibilities; external actor and platform stay outside the app.
    out=[zone(236,48,252,420,"PRESENTATION",c),
         zone(508,48,484,420,"APPLICATION / INFRASTRUCTURE",c),
         zone(1012,48,228,420,"EXTERNAL PLATFORM",c)]

    # Connectors first so nodes mask their endpoints cleanly.
    out += [h_arrow(200,194,272,"USE",c,"link"),
            h_arrow(452,194,548,"START / CANCEL",c),
            v_arrow(362,242,334,"SELECTION",c),
            elbow(452,382,548,238,"SELECTED INPUT",c,mid=500),
            v_arrow(648,242,334,"COUNTDOWN",c),
            elbow(748,194,816,382,"SAVE SETTINGS",c,mid=782),
            h_arrow(748,194,816,"POWER",c,"accent"),
            h_arrow(956,194,1050,"NATIVE CALL",c,"link")]

    out += [node(40,146,160,96,"Desktop User","mouse · keyboard","PERSON",c,"external"),
            node(272,146,180,96,"PySide6 UI","widgets · dialogs","UI",c),
            node(272,334,180,96,"Timer / Clock State","action · mode · target","STATE",c,"store"),
            node(548,146,200,96,"Scheduler Controller","start · validate · cancel","CORE",c,"focal"),
            node(548,334,200,96,"Countdown Engine","QTimer · remaining time","TIMER",c),
            node(816,146,140,96,"Power Gateway","subprocess.run","GATE",c),
            node(816,334,140,96,"Settings Repository","atomic JSON","REPO",c,"store"),
            node(1050,146,160,96,"Microsoft Windows","shutdown · powrprof","SYSTEM",c,"external")]

    out.append(txt(750,444,"Logical runtime responsibilities; all internal components execute in one desktop process.",c["soft"],12,400,family="serif",italic=True))
    out.append(legend(c,[("focal","Core scheduling"),("link","External boundary"),("external","External actor/system")]))
    return "".join(out)

def context_body(c):
    # DFD Context / Level 0: one process, external entities only, no internal store.
    out=[]

    # Distinct ports keep bidirectional flows visually separate.
    out += [h_arrow(220,206,430,"CONTROL REQUEST",c,"link"),
            h_arrow(430,314,220,"UI FEEDBACK",c,dash=True),
            h_arrow(850,206,1060,"POWER COMMAND",c,"accent"),
            h_arrow(1060,314,850,"COMMAND RESULT",c,dash=True)]

    out += [dfd_entity(40,180,180,160,"Desktop User","external entity",c),
            dfd_process(430,154,420,200,"0","Windows Shutdown Timer","single system process",c,True),
            dfd_entity(1060,180,180,160,"Microsoft Windows","external system",c)]

    out.append(txt(640,396,"Control request = action/time/start/cancel · UI feedback = confirmation/status/countdown/error.",c["soft"],12,400,family="serif",italic=True))
    out.append(txt(640,418,"DFD Context / Level 0 · internal components and data stores intentionally omitted.",c["soft"],12,400,family="serif",italic=True))
    out.append(legend(c,[("focal","Process 0"),("link","External input"),("muted","External output / result")]))
    return "".join(out)

def component_body(c):
    # C4-style logical component view inside one PySide6 desktop application container.
    out=[zone(36,44,996,430,"WINDOWS SHUTDOWN TIMER · PYSIDE6 DESKTOP APPLICATION",c)]

    # Primary top-row dependencies.
    out += [h_arrow(250,178,430,"START / CANCEL",c),
            h_arrow(630,178,760,"POWER REQUEST",c,"accent"),
            h_arrow(940,178,1080,"NATIVE COMMAND",c,"link")]

    # Focused internal dependencies with dedicated corridors.
    out += [v_arrow(160,226,334,"THEME / TEXT",c,dash=True),
            elbow(250,206,300,382,"LEGACY ACCESS",c,mid=274,dash=True),
            v_arrow(630,226,334,"START / STOP",c),
            elbow(630,206,780,382,"SAVE TIMER",c,mid=744)]

    # Main Window also owns window-preference load/save; route below the component row.
    window_cfg = (
        f'<path data-role="connector" d="M 250,206 H 262 Q 270,206 270,214 V 454 Q 270,462 278,462 '
        f'H 862 Q 870,462 870,454 V 430" fill="none" stroke="{c["muted"]}" '
        f'stroke-width="1" stroke-dasharray="5,4" marker-end="url(#arr)"/>'
        f'<rect data-role="label-mask" x="510" y="438" width="122" height="14" rx="2" fill="{c["paper"]}"/>'
        + txt(571,448,"LOAD / SAVE WINDOW",c["muted"],8,500,family="mono",tracking=".04em")
    )
    out.append(window_cfg)

    out += [node(70,130,180,96,"Main Window","ShutdownTimerApp","UI",c),
            node(430,130,200,96,"Scheduler Controller","validate · route · cancel","CORE",c,"focal"),
            node(760,130,180,96,"Power Gateway","shutdown · rundll32","GATE",c),
            node(70,334,180,96,"Theme & Localization","QSS · EN / TH · SVG","I18N",c),
            node(300,334,180,96,"Compatibility Adapters","SpinBoxProxy · DateTimeProxy","ADAPT",c),
            node(530,334,200,96,"Countdown Engine","QTimer · update_countdown","TIMER",c),
            node(780,334,180,96,"Settings Repository","timer + window JSON","REPO",c,"store"),
            node(1080,130,160,96,"Microsoft Windows","power management","SYSTEM",c,"external")]

    out.append(txt(534,492,"Logical components only — currently co-located in shutdown_timer.py, not separately deployed.",c["soft"],12,400,family="serif",italic=True))
    out.append(legend(c,[("focal","Core orchestration"),("muted","Internal dependency"),("external","External system")]))
    return "".join(out)

def system_context_body(c):
    # C4 System Context / Level 1: person, system of interest, external software system.
    out=[]

    out += [h_arrow(240,226,430,"CONFIGURE / CONTROL POWER",c,"link"),
            h_arrow(430,330,240,"CONFIRMATION / STATUS",c,dash=True),
            h_arrow(850,226,1040,"SCHEDULE / CANCEL / EXECUTE",c,"accent")]

    out += [node(60,178,180,144,"Desktop User","uses the local utility","PERSON",c,"external"),
            node(430,154,420,200,"Windows Shutdown Timer","PySide6 desktop application","SYSTEM",c,"focal"),
            node(1040,178,180,144,"Microsoft Windows","power management services","SYSTEM",c,"external")]

    out.append(txt(640,410,"C4 System Context · internal files, components, and distribution concerns are intentionally omitted.",c["soft"],12,400,family="serif",italic=True))
    out.append(legend(c,[("focal","System of interest"),("link","User relationship"),("external","External person/system")]))
    return "".join(out)

def data_flow_body(c):
    # DFD Level 1 balanced with the Level 0 Context Diagram.
    out=[]

    # External input and main processing chain.
    out += [h_arrow(180,214,260,"REQUEST",c,"link"),
            h_arrow(420,214,520,"INPUT",c),
            h_arrow(680,214,780,"ACTION",c,"accent"),
            h_arrow(960,202,1080,"POWER CMD",c,"accent"),
            h_arrow(1080,246,960,"RESULT",c,dash=True)]

    # Internal status and routing flows use distinct attach points.
    out += [v_arrow(870,250,360,"EXECUTION STATUS",c,label_side="right"),
            elbow(680,230,780,402,"VALIDATION / ROUTE",c,mid=730,dash=True),
            v_arrow(330,250,360,"PREFERENCE UPDATE",c,label_side="left"),
            v_arrow(370,360,250,"RESTORED PREFS",c,dash=True,label_side="right")]

    # D1/D2 sit beside P5 so read/write flows remain short, horizontal, and separate.
    store_flows = [
        f'<line data-role="connector" x1="260" y1="382" x2="200" y2="382" stroke="{c["muted"]}" stroke-width="1.1" marker-end="url(#arr)"/>',
        f'<rect data-role="label-mask" x="208" y="360" width="44" height="12" rx="2" fill="{c["paper"]}"/>',
        txt(230,369,"WRITE",c["muted"],8,500,family="mono"),
        f'<line data-role="connector" x1="200" y1="406" x2="260" y2="406" stroke="{c["muted"]}" stroke-width="1" stroke-dasharray="5,4" marker-end="url(#arr)"/>',
        f'<rect data-role="label-mask" x="208" y="412" width="44" height="12" rx="2" fill="{c["paper"]}"/>',
        txt(230,421,"READ",c["muted"],8,500,family="mono"),
        f'<line data-role="connector" x1="440" y1="382" x2="500" y2="382" stroke="{c["muted"]}" stroke-width="1.1" marker-end="url(#arr)"/>',
        f'<rect data-role="label-mask" x="448" y="360" width="44" height="12" rx="2" fill="{c["paper"]}"/>',
        txt(470,369,"WRITE",c["muted"],8,500,family="mono"),
        f'<line data-role="connector" x1="500" y1="406" x2="440" y2="406" stroke="{c["muted"]}" stroke-width="1" stroke-dasharray="5,4" marker-end="url(#arr)"/>',
        f'<rect data-role="label-mask" x="448" y="412" width="44" height="12" rx="2" fill="{c["paper"]}"/>',
        txt(470,421,"READ",c["muted"],8,500,family="mono"),
    ]
    out += store_flows

    # Feedback runs through the empty bottom corridor and the gap between User and P1.
    feedback = (
        f'<path data-role="connector" d="M 870,456 V 476 Q 870,484 862,484 H 228 Q 220,484 220,476 '
        f'V 246 Q 220,238 212,238 H 180" fill="none" stroke="{c["link"]}" '
        f'stroke-width="1.1" stroke-dasharray="5,4" marker-end="url(#arr-link)"/>'
        f'<rect data-role="label-mask" x="484" y="460" width="160" height="14" rx="2" fill="{c["paper"]}"/>'
        + txt(564,470,"CONFIRM · STATUS · ERROR",c["link"],8,500,family="mono",tracking=".04em")
    )
    out.append(feedback)

    out += [dfd_entity(40,154,140,124,"Desktop User","external entity",c),
            dfd_process(260,154,160,96,"1.0","Capture Request","action · mode · target",c),
            dfd_process(520,154,160,96,"2.0","Validate & Route","rules · branch · cancel",c,True),
            dfd_process(780,154,180,96,"3.0","Execute / Schedule","shutdown · suspend",c),
            dfd_entity(1080,154,160,124,"Microsoft Windows","external system",c),
            dfd_process(780,360,180,96,"4.0","Update UI State","toast · status · progress",c),
            dfd_process(260,360,180,96,"5.0","Persist Preferences","save · restore JSON",c),
            dfd_store(40,350,160,64,"D1","Timer Settings","timer_config.json",c),
            dfd_store(500,350,160,64,"D2","Window Preferences","window_config.json",c)]

    out.append(txt(640,500,"Shutdown / Restart uses validated scheduling; Sleep / Hibernate branches to immediate execution.",c["soft"],12,400,family="serif",italic=True))
    out.append(legend(c,[("focal","Validation / routing"),("link","External flow"),("muted","Internal data flow")]))
    return "".join(out)

def sequence_body(c):
    xs=[100,330,620,920,1160]
    out=[]

    # Lifelines and activation bars. Windows is active only while a native call is executing.
    for x in xs:
        out.append(f'<line x1="{x}" y1="92" x2="{x}" y2="578" stroke="{c["line"]}" stroke-width="1" stroke-dasharray="3,3"/>')
    out += [f'<rect x="326" y="110" width="8" height="468" fill="{c["activation"]}" stroke="{c["muted"]}" stroke-width=".8"/>',
            f'<rect x="616" y="136" width="8" height="442" fill="{c["activation"]}" stroke="{c["muted"]}" stroke-width=".8"/>',
            f'<rect x="916" y="316" width="8" height="58" fill="{c["activation"]}" stroke="{c["muted"]}" stroke-width=".8"/>',
            f'<rect x="916" y="536" width="8" height="36" fill="{c["activation"]}" stroke="{c["muted"]}" stroke-width=".8"/>']

    # One UML alt combined fragment; confirmation is branch-specific in the real code.
    out += [f'<rect x="286" y="164" width="934" height="414" rx="6" fill="none" stroke="{c["rule"]}" stroke-width="1"/>',
            f'<path d="M286,164 H344 V186 H286 Z" fill="{c["surface2"]}" stroke="{c["rule"]}" stroke-width="1"/>',
            txt(315,179,"ALT",c["muted"],8,600,family="mono",tracking=".12em"),
            txt(306,190,"[ SHUTDOWN / RESTART ]",c["soft"],9,500,"start","mono"),
            f'<line x1="286" y1="446" x2="1220" y2="446" stroke="{c["rule"]}" stroke-width=".8"/>',
            txt(306,456,"[ SLEEP / HIBERNATE ]",c["soft"],9,500,"start","mono")]

    # Common entry.
    out += [seq_message(100,330,110,"choose action/time + Start",c,style="link"),
            seq_message(330,620,138,"start_timer()",c)]

    # Scheduled branch: start_timer() owns confirmation, validation, scheduling, countdown, persistence.
    out += [seq_message(620,330,218,"show schedule confirmation",c),
            seq_message(100,330,242,"confirm Yes",c,style="link"),
            seq_message(330,620,266,"confirmed",c,kind="return"),
            seq_self(620,284,"validate target",c,"accent"),
            seq_message(620,920,318,"shutdown /a",c),
            seq_message(620,920,344,"shutdown /s|/r /t",c,style="accent"),
            seq_message(920,620,370,"command result",c,kind="return"),
            seq_self(620,386,"start 1s QTimer",c),
            seq_message(620,1160,420,"save_settings()",c),
            seq_message(620,330,438,"scheduled status",c,kind="return")]

    # Immediate branch: _execute_sleep_hibernate() asks its own confirmation before the native call.
    out += [seq_message(620,330,480,"show immediate confirmation",c),
            seq_message(100,330,500,"confirm Yes",c,style="link"),
            seq_message(330,620,520,"confirmed",c,kind="return"),
            seq_message(620,920,540,"rundll32 SetSuspendState",c,style="link"),
            seq_message(920,620,558,"command result",c,kind="return"),
            seq_message(620,330,574,"executing status",c,kind="return")]

    actors=[
        (20,"Desktop User","mouse / keyboard","PERSON","external"),
        (250,"PySide6 UI","widgets · dialogs","UI","normal"),
        (540,"ShutdownTimerApp","controller","CORE","focal"),
        (840,"Windows Power API","shutdown · rundll32","SYSTEM","external"),
        (1080,"Settings Store","timer JSON","REPO","store"),
    ]
    for x,title,sub,tag,kind in actors:
        out.append(node(x,10,160,80,title,sub,tag,c,kind))

    out.append(legend(c,[("focal","Scheduled command"),("link","External / immediate call"),("muted","Return / UI update")]))
    return "".join(out)

DIAGRAMS = {
    "architecture-diagram": ("Architecture","Layered runtime architecture separating the desktop actor, application responsibilities, and Microsoft Windows.",architecture_body),
    "data-flow-diagram": ("Data Flow","DFD Level 1 showing balanced external flows, numbered processes, and local preference data stores.",data_flow_body),
    "sequence-diagram": ("Sequence","UML interaction for Start, including scheduled Shutdown/Restart and immediate Sleep/Hibernate branches.",sequence_body),
    "context-diagram": ("Context","DFD Context / Level 0 showing the application as one process with only external entities and boundary flows.",context_body),
    "component-diagram": ("Component","C4-style logical component view inside the PySide6 desktop application container.",component_body),
    "system-context-diagram": ("System Context","C4 System Context / Level 1 showing the user, system of interest, and Microsoft Windows.",system_context_body),
}

FONT_URL="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500;600&display=swap"

def svg_doc(slug,theme,title,desc,body):
    c=THEMES[theme]; sid=f"{slug}-{theme}"
    return f'''<svg viewBox="0 0 {VIEW_W} {VIEW_H}" width="{VIEW_W}" height="{VIEW_H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{sid}-title {sid}-desc">
<title id="{sid}-title">{E(title)}</title>
<desc id="{sid}-desc">{E(desc)}</desc>
{defs(c)}
<rect width="100%" height="100%" fill="{c["paper"]}"/>
{txt(48,40,title.upper()+" · DIAGRAM DESIGN",c["muted"],8,500,"start","mono",tracking=".18em")}
{txt(48,76,"Windows Shutdown Timer",c["ink"],28,400,"start","serif")}
<g transform="translate(0 100)">
{body}
</g>
</svg>'''

def html_doc(slug,theme,title,desc,body):
    c=THEMES[theme]
    svg=svg_doc(slug,theme,title,desc,body)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} · Windows Shutdown Timer</title>
<link href="{FONT_URL}" rel="stylesheet">
<style>
*{{box-sizing:border-box}} html,body{{margin:0;background:{c["paper"]};min-height:100%}}
body{{display:flex;align-items:flex-start;justify-content:center}}
svg{{display:block;width:min(100vw,1280px);height:auto}}
</style></head><body>
{svg}
</body></html>'''

def standalone_svg(html_text):
    m=re.search(r'(<svg\b.*?</svg>)',html_text,re.S)
    if not m: raise ValueError("No SVG found")
    svg=m.group(1)

    font_css="@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&amp;family=Geist:wght@400;500;600&amp;family=Geist+Mono:wght@400;500;600&amp;display=swap');"
    svg=svg.replace("<defs>","<defs><style>"+font_css+"</style>",1)
    def rgba(m):
        attr,r,g,b,a=m.groups()
        return f'{attr}="#{int(r):02x}{int(g):02x}{int(b):02x}" {attr}-opacity="{a}"'
    svg=re.sub(r'(fill|stroke)="rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d*\.?\d+)\s*\)"',rgba,svg)
    svg=re.sub(r'(fill|stroke)="transparent"',r'\1="none"',svg)
    return '<?xml version="1.0" encoding="UTF-8"?>\n'+svg

def main():
    for slug,(kind,desc,fn) in DIAGRAMS.items():
        for theme in ("light","dark"):
            title=f"{kind} Diagram"
            html_text=html_doc(slug,theme,title,desc,fn(THEMES[theme]))
            hp=OUT/f"{slug}-{theme}.html"
            sp=OUT/f"{slug}-{theme}.svg"
            hp.write_text(html_text,encoding="utf-8")
            sp.write_text(standalone_svg(html_text),encoding="utf-8")
            print(hp.name,"->",sp.name)

if __name__=="__main__":
    main()
