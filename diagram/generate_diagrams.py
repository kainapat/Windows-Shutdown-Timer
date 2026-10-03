from pathlib import Path
import html, re

OUT = Path(__file__).resolve().parent
VIEW_W, VIEW_H = 1280, 820

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
    return f'<text{attrs}>{E(s)}</text>'

def node(x,y,w,h,title,sub,tag,c,kind="normal"):
    fill, stroke, sw, dash = c["surface"], c["rule"], 1, ""
    if kind=="focal": fill,stroke,sw = c["accent_tint"],c["accent"],1.4
    elif kind=="external": fill,stroke = c["wash"],c["soft"]
    elif kind=="store": fill,stroke = c["surface2"],c["muted"]
    elif kind=="optional": fill,stroke,dash = c["wash"],c["soft"],' stroke-dasharray="4,3"'
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{c["paper"]}"/>',
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash}/>']
    out += [f'<rect x="{x+10}" y="{y+8}" width="36" height="14" rx="2" fill="none" stroke="{stroke}" stroke-opacity=".45" stroke-width=".8"/>',
            txt(x+28,y+18,tag,stroke,8,600,family="mono",tracking=".08em"),
            txt(x+w/2,y+48,title,c["ink"],16,600),
            txt(x+w/2,y+69,sub,c["muted"],11,400,family="mono")]
    return "".join(out)

def zone(x,y,w,h,label,c):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{c["wash"]}" stroke="{c["line"]}" stroke-width=".8"/>'
            + f'<rect x="{x+16}" y="{y+8}" width="{max(84,len(label)*8)}" height="16" rx="2" fill="{c["paper"]}"/>'
            + txt(x+24,y+20,label,c["soft"],8,600,"start","mono",tracking=".14em"))

def h_arrow(x1,y,x2,label,c,style="muted",dash=False):
    color = c["accent"] if style=="accent" else c["link"] if style=="link" else c["muted"]
    marker = "arr-accent" if style=="accent" else "arr-link" if style=="link" else "arr"
    line = f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="{1.4 if style=="accent" else 1.2}"'
    if dash: line += ' stroke-dasharray="5,4"'
    line += f' marker-end="url(#{marker})"/>'
    if label:
        w=max(68,len(label)*7); mx=(x1+x2)/2
        line += f'<rect x="{mx-w/2}" y="{y-25}" width="{w}" height="14" rx="2" fill="{c["paper"]}"/>'
        line += txt(mx,y-15,label.upper(),color,8,500,family="mono",tracking=".06em")
    return line

def elbow(x1,y1,x2,y2,label,c,style="muted",mid=None,dash=False):
    color = c["accent"] if style=="accent" else c["link"] if style=="link" else c["muted"]
    marker = "arr-accent" if style=="accent" else "arr-link" if style=="link" else "arr"
    m = mid if mid is not None else (x1+x2)//2
    sy = 8 if y2>y1 else -8
    d=f'M {x1},{y1} H {m-8} Q {m},{y1} {m},{y1+sy} V {y2-sy} Q {m},{y2} {m+8},{y2} H {x2}'
    out=f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{1.4 if style=="accent" else 1.2}"'
    if dash: out += ' stroke-dasharray="5,4"'
    out += f' marker-end="url(#{marker})"/>'
    if label:
        w=max(68,len(label)*7); ly=(y1+y2)/2
        out += f'<rect x="{m+10}" y="{ly-10}" width="{w}" height="14" rx="2" fill="{c["paper"]}"/>'
        out += txt(m+14,ly,label.upper(),color,8,500,"start","mono",tracking=".06em")
    return out

def v_arrow(x,y1,y2,label,c,style="muted",dash=False,label_side="right"):
    color = c["accent"] if style=="accent" else c["link"] if style=="link" else c["muted"]
    marker = "arr-accent" if style=="accent" else "arr-link" if style=="link" else "arr"
    out=f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{color}" stroke-width="{1.4 if style=="accent" else 1.2}"'
    if dash: out += ' stroke-dasharray="5,4"'
    out += f' marker-end="url(#{marker})"/>'
    if label:
        w=max(68,len(label)*7); lx=x+12 if label_side=="right" else x-w-12; ly=(y1+y2)/2
        out += f'<rect x="{lx}" y="{ly-10}" width="{w}" height="14" rx="2" fill="{c["paper"]}"/>'
        out += txt(lx+4,ly,label.upper(),color,8,500,"start","mono",tracking=".06em")
    return out

def defs(c):
    return f'''<defs>
<marker id="arr" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="{c["muted"]}"/></marker>
<marker id="arr-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="{c["accent"]}"/></marker>
<marker id="arr-link" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="{c["link"]}"/></marker>
</defs>'''

def legend(c, items):
    y=660; out=[f'<line x1="40" y1="{y}" x2="1240" y2="{y}" stroke="{c["line"]}" stroke-width=".8"/>',
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

def architecture_body(c):
    out=[zone(36,52,428,520,"PRESENTATION",c),zone(484,52,292,520,"APPLICATION CORE",c),zone(796,52,448,520,"WINDOWS PLATFORM",c)]
    out += [h_arrow(224,208,264,"UI EVENTS",c),h_arrow(444,208,520,"REQUEST",c),
            h_arrow(720,208,836,"POWER CMD",c,"accent"),h_arrow(1016,208,1060,"NATIVE",c,"link"),
            v_arrow(354,256,360,"SELECTION",c),v_arrow(620,256,360,"TICK",c),
            h_arrow(444,408,520,"TARGET",c),h_arrow(720,408,836,"SAVE",c)]
    out += [node(64,160,160,96,"Desktop User","mouse · keyboard","EXT",c,"external"),
            node(264,160,180,96,"PySide6 UI","widgets · dialogs","UI",c),
            node(264,360,180,96,"Timer / Clock State","mode · action · time","STATE",c,"store"),
            node(520,160,200,96,"Scheduler Controller","start_timer()","CORE",c,"focal"),
            node(520,360,200,96,"Countdown Engine","QTimer · target time","TIMER",c),
            node(836,160,180,96,"Windows Adapter","subprocess.run","OS",c),
            node(836,360,180,96,"Config Store","atomic JSON","FILE",c,"store"),
            node(1060,160,160,96,"Windows OS","shutdown · powrprof","EXT",c,"external")]
    out.append(legend(c,[("focal","Scheduling decision"),("link","OS boundary"),("external","External actor/system")]))
    return "".join(out)

def context_body(c):
    out=[zone(356,88,568,472,"SYSTEM BOUNDARY",c)]
    out += [h_arrow(244,260,436,"CONFIGURE",c,"link"),
            h_arrow(844,260,1040,"POWER ACTION",c,"accent"),
            v_arrow(640,356,468,"READ / WRITE",c),
            h_arrow(844,420,1040,"STATUS",c,dash=True)]
    out += [node(64,212,180,96,"Desktop User","select · start · cancel","EXT",c,"external"),
            node(436,196,408,160,"Windows Shutdown Timer","local PySide6 desktop utility","SYS",c,"focal"),
            node(540,468,200,96,"Local Config","timer / window JSON","FILE",c,"store"),
            node(1040,196,180,96,"Windows OS","shutdown.exe · powrprof","EXT",c,"external"),
            node(1040,372,180,96,"System State","shutdown · restart · sleep","STATE",c,"external")]
    out.append(txt(640,392,"No service, driver, web backend, or network dependency.",c["soft"],12,400,family="serif",italic=True))
    out.append(legend(c,[("focal","System under review"),("link","User interaction"),("external","External dependency")]))
    return "".join(out)

def component_body(c):
    out=[zone(64,72,1152,508,"SHUTDOWN_TIMER.PY · MONOLITHIC MODULE",c)]
    out += [h_arrow(300,196,388,"SIGNALS",c),h_arrow(588,196,684,"CALL",c),
            h_arrow(884,196,980,"SUBPROCESS",c,"accent"),
            v_arrow(488,244,360,"STYLE / TEXT",c,dash=True),
            v_arrow(784,244,360,"COUNTDOWN",c),
            h_arrow(588,408,684,"STATE",c),h_arrow(884,408,980,"JSON",c)]
    out += [node(100,148,200,96,"Main Window","ShutdownTimerApp","UI",c),
            node(388,148,200,96,"Input & Mode Adapters","SpinBoxProxy · DateTimeProxy","ADAPT",c),
            node(684,148,200,96,"Scheduling Logic","validate · route · cancel","CORE",c,"focal"),
            node(980,148,200,96,"Windows Power Adapter","shutdown.exe · rundll32","OS",c),
            node(388,360,200,96,"Theme & Localization","QSS · EN / TH · SVG","UI",c),
            node(684,360,200,96,"Countdown State","QTimer · remaining time","STATE",c,"store"),
            node(980,360,200,96,"Persistence","timer + window config","FILE",c,"store")]
    out.append(txt(640,520,"Logical components are currently co-located in one 2,022-line Python module.",c["soft"],12,400,family="serif",italic=True))
    out.append(legend(c,[("focal","Core orchestration"),("muted","Internal dependency"),("external","Platform boundary")]))
    return "".join(out)

def system_context_body(c):
    out=[zone(332,76,616,492,"WINDOWS DESKTOP ENVIRONMENT",c)]
    out += [h_arrow(244,244,416,"USE",c,"link"),
            h_arrow(816,244,1036,"POWER",c,"accent"),
            v_arrow(616,340,452,"SETTINGS",c)]
    out += [node(64,196,180,96,"Desktop User","runs local utility","PERSON",c,"external"),
            node(416,180,400,160,"Windows Shutdown Timer","standalone PySide6 application","SYSTEM",c,"focal"),
            node(516,452,200,96,"Local File System","JSON preferences","FILE",c,"store"),
            node(1036,196,180,96,"Microsoft Windows","power management","EXT",c,"external"),
            node(64,436,240,96,"GitHub Release","packaged application","DIST",c,"external")]
    out.append(elbow(304,484,416,292,"PACKAGE",c,"link",mid=360,dash=True))
    out.append(txt(640,388,"Distribution is separate from runtime: the installed app needs no network service.",c["soft"],12,400,family="serif",italic=True))
    out.append(legend(c,[("focal","System of interest"),("link","Distribution / interaction"),("external","External system")]))
    return "".join(out)

def data_flow_body(c):
    out=[]
    lanes=[("USER",100),("UI",220),("APP",340),("PLATFORM",460)]
    steps=[("01","SELECT",260),("02","CAPTURE",460),("03","VALIDATE",660),("04","ROUTE",860),("05","EXECUTE",1060)]
    for i,(name,y) in enumerate(lanes):
        if i%2==0: out.append(f'<rect x="40" y="{y}" width="1200" height="120" fill="{c["wash"]}"/>')
        out.append(f'<line x1="40" y1="{y}" x2="1240" y2="{y}" stroke="{c["line"]}" stroke-width=".8"/>')
        out.append(txt(88,y+64,name,c["muted"],9,600,family="mono",tracking=".14em"))
    out.append(f'<line x1="148" y1="100" x2="148" y2="580" stroke="{c["line"]}" stroke-width=".8"/>')
    for num,label,x in steps:
        focal = label=="VALIDATE"; fill=c["accent_tint"] if focal else c["surface2"]; col=c["accent"] if focal else c["muted"]
        out.append(f'<rect x="{x-18}" y="60" width="36" height="18" rx="6" fill="{fill}"/>')
        out.append(txt(x,73,num,col,8,600,family="mono"))
        out.append(txt(x,92,label,col,8,600,family="mono",tracking=".12em"))

    out += [elbow(340,160,380,280,"",c,mid=360),
            elbow(540,280,580,400,"request",c,"accent",mid=560),
            h_arrow(740,400,780,"",c),
            v_arrow(860,440,480,"",c),
            elbow(940,400,980,520,"",c,"link",mid=960),
            v_arrow(1060,480,320,"result",c,"link",label_side="right")]
    out += [node(180,120,160,80,"Action + Time","shutdown · mode · target","USR",c,"external"),
            node(380,240,160,80,"UI Selection","combo / date picker","UI",c),
            node(580,360,160,80,"Validate Request","future · nonzero · ≤72h","VAL",c,"focal"),
            node(780,360,160,80,"Execution Router","scheduled vs immediate","ROUTE",c),
            node(780,480,160,80,"Config Snapshot","atomic JSON","FILE",c,"store"),
            node(980,480,160,80,"Windows Command","shutdown / rundll32","OS",c),
            node(980,240,160,80,"UI Feedback","status · toast · progress","UI",c)]
    out.append(txt(860,590,"Sleep / Hibernate follows the immediate branch; Shutdown / Restart follows the scheduled branch.",c["soft"],12,400,family="serif",italic=True))
    out.append(legend(c,[("focal","Validated schedule request"),("link","Platform handoff"),("muted","Internal state flow")]))
    return "".join(out)

def sequence_body(c):
    xs=[120,360,640,920,1160]
    out=[]
    for x in xs: out.append(f'<line x1="{x}" y1="116" x2="{x}" y2="604" stroke="{c["line"]}" stroke-width="1" stroke-dasharray="3,3"/>')
    out += [f'<rect x="636" y="212" width="8" height="320" fill="{c["activation"]}" stroke="{c["muted"]}" stroke-width=".8"/>',
            f'<rect x="916" y="300" width="8" height="180" fill="{c["activation"]}" stroke="{c["muted"]}" stroke-width=".8"/>',
            f'<rect x="316" y="240" width="888" height="300" rx="6" fill="none" stroke="{c["rule"]}" stroke-width="1"/>',
            f'<path d="M316,240 H368 V262 H316 Z" fill="{c["surface2"]}" stroke="{c["rule"]}" stroke-width="1"/>',
            txt(342,255,"ALT",c["muted"],8,600,family="mono",tracking=".12em"),
            txt(336,282,"[ SHUTDOWN / RESTART ]",c["soft"],9,500,"start","mono"),
            f'<line x1="316" y1="392" x2="1204" y2="392" stroke="{c["rule"]}" stroke-width=".8"/>',
            txt(336,418,"[ SLEEP / HIBERNATE ]",c["soft"],9,500,"start","mono")]
    out += [h_arrow(120,160,360,"configure action/time",c,"link"),
            h_arrow(360,212,640,"start_timer()",c),
            h_arrow(640,312,920,"shutdown /s|/r /t",c,"accent"),
            h_arrow(640,352,1160,"save_settings()",c),
            h_arrow(640,376,360,"countdown active",c,dash=True),
            h_arrow(640,456,920,"rundll32 SetSuspendState",c,"link"),
            h_arrow(640,504,360,"executing now",c,dash=True)]

    actors=[
        (40,"Desktop User","mouse / keyboard","EXT","external"),
        (280,"PySide6 UI","widgets + dialogs","UI","normal"),
        (560,"ShutdownTimerApp","controller","CORE","focal"),
        (840,"Windows CLI","shutdown / rundll32","OS","external"),
        (1080,"Config Store","JSON files","FILE","store"),
    ]
    for x,title,sub,tag,kind in actors:
        out.append(node(x,36,160,80,title,sub,tag,c,kind))
    out.append(txt(640,580,"The two branches diverge at the controller: scheduled actions persist a countdown; sleep/hibernate executes immediately.",c["soft"],12,400,family="serif",italic=True))
    out.append(legend(c,[("focal","Scheduled power command"),("link","Immediate power command"),("muted","Return / UI update")]))
    return "".join(out)

DIAGRAMS = {
    "architecture-diagram": ("Architecture","Runtime architecture and Windows platform boundary.",architecture_body),
    "data-flow-diagram": ("Data Flow","Scheduling request lifecycle from selection to operating-system effect.",data_flow_body),
    "sequence-diagram": ("Sequence","Start action sequence, including scheduled and immediate branches.",sequence_body),
    "context-diagram": ("Context","Level-0 runtime context for the local desktop utility.",context_body),
    "component-diagram": ("Component","Logical components currently co-located in shutdown_timer.py.",component_body),
    "system-context-diagram": ("System Context","Product context spanning distribution and the Windows runtime.",system_context_body),
}

FONT_URL="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500;600&display=swap"

def svg_doc(slug,theme,title,desc,body):
    c=THEMES[theme]; sid=f"{slug}-{theme}"
    return f'''<svg viewBox="0 0 {VIEW_W} {VIEW_H}" width="{VIEW_W}" height="{VIEW_H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{sid}-title {sid}-desc">
<title id="{sid}-title">{E(title)}</title>
<desc id="{sid}-desc">{E(desc)}</desc>
{defs(c)}
<rect width="100%" height="100%" fill="{c["paper"]}"/>
{txt(48,40,title.upper()+" · DIAGRAM DESIGN",c["muted"],10,500,"start","mono",tracking=".18em")}
{txt(48,76,"Windows Shutdown Timer",c["ink"],32,600,"start","sans")}
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
