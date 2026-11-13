"""Gera os SVGs animados do README (identidade: preto, vermelho #D71F2D, branco).

Uso: python scripts/generate.py   -> escreve tudo em assets/
"""
import random
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
RED = "#D71F2D"
MONO = "'JetBrains Mono','Fira Code','Cascadia Code',Consolas,'Courier New',monospace"
CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789$#@%&*<>[]{}()/\\|;:!?^~+=_-"

random.seed(42)

# Raposa original (viewBox 1080) – recortada na região x 271..767, y 186..787
FOX = [
    ("body", "white", "M472.968 333.038L619.955 333.038L766.943 333.038V697.652C766.943 747.227 726.755 787.415 677.18 787.415H472.968V333.038Z"),
    ("tail", RED, "M271 495.684V495.684C382.544 495.684 472.968 586.108 472.968 697.651V787.415V787.415C361.424 787.415 271 696.991 271 585.447V495.684Z"),
    ("tailtip", "white", "M294.686 530.724C293.044 525.476 298.045 520.58 303.257 522.332L364.738 543.004C366.5 543.596 367.938 544.89 368.713 546.58L419.458 657.296C422.274 663.44 415.292 669.438 409.643 665.729L320.141 606.965C318.84 606.111 317.875 604.833 317.41 603.348L294.686 530.724Z"),
    ("head", RED, "M472.968 295.959V384.602L619.955 485.586L766.943 384.602V295.959L619.961 295.96L766.943 186.003V186L619.955 295.96L472.968 186V186.003L619.95 295.96L472.968 295.959Z"),
    ("earR", RED, "M760.07 307.92C763.788 307.92 766.802 304.906 766.802 301.188L766.802 250.87C766.802 245.282 760.387 242.126 755.961 245.537L690.647 295.855C685.557 299.776 688.33 307.92 694.756 307.92L760.07 307.92Z"),
    ("earL", RED, "M479.754 306.103C476.036 306.103 473.022 303.089 473.022 299.371L473.022 249.053C473.022 243.465 479.437 240.31 483.863 243.72L549.177 294.038C554.268 297.96 551.494 306.104 545.069 306.104L479.754 306.103Z"),
    ("nose", "white", "M615.055 463.553C617.713 466.374 622.198 466.374 624.856 463.553L639.388 448.125C643.435 443.829 640.389 436.777 634.488 436.777H605.423C599.521 436.777 596.476 443.829 600.522 448.125L615.055 463.553Z"),
]


def fox_group(x, y, size, delay=0.0, cls="fox"):
    """Raposa montada peça por peça. size = altura em px."""
    s = size / 602
    parts = []
    for i, (name, fill, d) in enumerate(FOX):
        parts.append(
            f'<path class="{cls}-p" style="animation-delay:{delay + i * 0.12:.2f}s" fill="{fill}" d="{d}"/>'
        )
    return (
        f'<g transform="translate({x} {y}) scale({s:.4f}) translate(-271 -186)">'
        f'<g class="{cls}-bob">{"".join(parts)}</g></g>'
    )


def matrix(w, h, cols, size=16, opacity=0.35, seed=1, trail=10):
    """Chuva matrix leve: cada coluna é um único <text> com um rastro curto que
    desce em passos discretos (steps) — poucos glifos e repintura só a cada passo."""
    rnd = random.Random(seed)
    out = []
    step = w / cols
    n = int(h / size) + trail
    for c in range(cols):
        x = c * step + rnd.uniform(0, step * 0.4)
        dur = rnd.uniform(5, 12)
        delay = -rnd.uniform(0, dur)
        hot = rnd.random() < 0.2
        spans = []
        for r in range(trail):
            fo = opacity * (0.15 + 0.85 * (r + 1) / trail)
            fill = ' fill="#ff6b75"' if hot and r == trail - 1 else ""
            spans.append(f'<tspan x="{x:.0f}" y="{r * size}" fill-opacity="{fo:.2f}"{fill}>{escape(rnd.choice(CHARS))}</tspan>')
        out.append(
            f'<text class="rain" style="animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s;'
            f'animation-timing-function:steps({n})">{"".join(spans)}</text>'
        )
    return (
        f'<g font-family="{MONO}" font-size="{size - 2}" fill="{RED}" '
        f'style="--s:{-trail * size}px;--h:{h}px">{"".join(out)}</g>'
    )


RAIN_CSS = "@keyframes fall{from{transform:translateY(var(--s))}to{transform:translateY(var(--h))}}.rain{animation-name:fall;animation-iteration-count:infinite}"


def typed(text, x, y, start, speed=0.06, size=22, fill="white", weight="400", cls="ch"):
    """Texto 'digitado' caractere por caractere (largura monoespaçada = 0.6em)."""
    cw = size * 0.6
    out = []
    for i, ch in enumerate(text):
        if ch == " ":
            continue
        out.append(
            f'<text class="{cls}" x="{x + i * cw:.1f}" y="{y}" style="animation-delay:{start + i * speed:.2f}s">{escape(ch)}</text>'
        )
    end = start + len(text) * speed
    return (
        f'<g font-family="{MONO}" font-size="{size}" fill="{fill}" font-weight="{weight}">{"".join(out)}</g>',
        end,
        x + len(text) * cw,
    )


# Fonte pixel 5x7 para o nome (imita a fonte pixelada do banner)
PIX = {
    "J": ["..###", "...#.", "...#.", "...#.", "#..#.", "#..#.", ".##.."],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "Ã": [".#.#.", "#.#..", ".###.", "#...#", "#####", "#...#", "#...#"],
    "V": ["#...#", "#...#", "#...#", "#...#", ".#.#.", ".#.#.", "..#.."],
    "I": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "C": [".####", "#....", "#....", "#....", "#....", "#....", ".####"],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    " ": [".....", ".....", ".....", ".....", ".....", ".....", "....."],
}


def pixel_text(text, x, y, px, start, fill="white"):
    out = []
    cx = x
    rnd = random.Random(7)
    for ch in text:
        glyph = PIX[ch]
        for r, row in enumerate(glyph):
            for c, v in enumerate(row):
                if v == "#":
                    d = start + rnd.uniform(0, 0.9)
                    out.append(
                        f'<rect class="px" x="{cx + c * px:.1f}" y="{y + r * px:.1f}" width="{px - 0.6:.1f}" height="{px - 0.6:.1f}" style="animation-delay:{d:.2f}s"/>'
                    )
        cx += 6 * px
    return f'<g fill="{fill}">{"".join(out)}</g>', cx - x - px


def write(name, body):
    OUT.mkdir(exist_ok=True)
    (OUT / name).write_text(body, encoding="utf-8")
    print(f"{name}: {len(body) / 1024:.1f} KB")


# ---------------------------------------------------------------- header
def header():
    W, H = 1280, 420
    css = f"""
    
    .orb{{animation:float ease-in-out infinite alternate}}
    @keyframes float{{from{{transform:translate(0,0) scale(1)}}to{{transform:translate(var(--dx),var(--dy)) scale(1.08)}}}}
    .ch{{opacity:0;animation:on .01s forwards}}
    @keyframes on{{to{{opacity:1}}}}
    .cur{{animation:blink 1s steps(1) infinite}}
    @keyframes blink{{50%{{opacity:0}}}}
    .fox-p{{opacity:0;transform-box:fill-box;transform-origin:center;animation:pop .6s cubic-bezier(.2,1.6,.4,1) forwards}}
    @keyframes pop{{from{{opacity:0;transform:scale(.3) rotate(-12deg)}}to{{opacity:1;transform:none}}}}
    .fox-bob{{animation:bob 4s ease-in-out 3.5s infinite}}
    @keyframes bob{{50%{{transform:translateY(-14px)}}}}
    .frame{{stroke-dasharray:1400;stroke-dashoffset:1400;animation:draw 1.4s ease-out 1.6s forwards}}
    @keyframes draw{{to{{stroke-dashoffset:0}}}}
    .px{{opacity:0;animation:pxin .35s ease-out forwards}}
    @keyframes pxin{{from{{opacity:0;transform:translateY(-30px)}}to{{opacity:1;transform:none}}}}
    .fade{{opacity:0;animation:fade .8s ease-out forwards}}
    @keyframes fade{{from{{opacity:0;transform:translateX(30px)}}to{{opacity:1;transform:none}}}}
    .scan{{animation:scan 6s linear infinite}}
    @keyframes scan{{from{{transform:translateY(-40px)}}to{{transform:translateY({H}px)}}}}
    .glitch{{animation:glitch 5s steps(1) 4s infinite}}
    @keyframes glitch{{0%,92%,100%{{transform:none}}93%{{transform:translate(-4px,1px)}}95%{{transform:translate(3px,-2px)}}97%{{transform:translate(-2px,0)}}}}
    """
    orbs = [
        (150, 40, 130, 0, 0, "20px", "25px", 9),
        (90, 250, 70, 0, 0, "15px", "-20px", 7),
        (300, 360, 52, 0, 0, "-18px", "-12px", 8),
        (1300, 40, 90, 6, 0, "-25px", "15px", 10),
        (1060, 400, 38, 10, 0, "12px", "-25px", 6),
    ]
    orb_svg = "".join(
        f'<circle class="orb" cx="{x}" cy="{y}" r="{r}" fill="{"url(#soft)" if b else RED}" '
        f'style="--dx:{dx};--dy:{dy};animation-duration:{d}s;transform-box:fill-box;transform-origin:center"/>'
        for x, y, r, b, _, dx, dy, d in orbs
    )
    l1, e1, _ = typed("github@victor:", 470, 92, 0.3, size=26)
    l2, e2, x2 = typed("~$ sudo whoami", 470, 128, e1 + 0.2, size=26)
    fox = fox_group(555, 162, 210, delay=e2 + 0.1)
    name, nw = pixel_text("JOÃO VICTOR", 0, 0, 6, e2 + 0.8)
    nx = 1210 - nw
    t_role = e2 + 1.9
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>{css}{RAIN_CSS}</style>
<defs>
<linearGradient id="bg" x1="0" x2="1"><stop stop-color="#232121"/><stop offset=".625" stop-color="#000"/></linearGradient>
<radialGradient id="soft"><stop offset=".82" stop-color="{RED}"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>
<linearGradient id="scanG" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{RED}" stop-opacity="0"/><stop offset=".5" stop-color="{RED}" stop-opacity=".12"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></linearGradient>
<clipPath id="clip"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#clip)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
{matrix(W, H, 34, size=18, opacity=0.45, trail=12)}
{orb_svg}
<rect class="scan" width="{W}" height="40" fill="url(#scanG)"/>
{l1}{l2}
<rect class="cur" x="{x2 + 6:.0f}" y="106" width="14" height="28" fill="{RED}"/>
<rect class="frame" x="470" y="150" width="300" height="236" fill="#000" fill-opacity=".55" stroke="white" stroke-width="2"/>
<rect class="frame" x="476" y="156" width="288" height="224" fill="none" stroke="white" stroke-width="1" style="animation-delay:1.9s"/>
{fox}
<g transform="translate({nx:.0f} 150)"><g class="glitch">{name}</g></g>
<g class="fade" style="animation-delay:{t_role:.2f}s" font-family="{MONO}" text-anchor="end">
<text x="1210" y="240" fill="white" font-size="26" font-weight="700">Químico &amp; Full Stack Dev</text>
<text x="1210" y="276" fill="{RED}" font-size="18">&lt; química + código /&gt;</text>
</g>
<g class="fade" style="animation-delay:{t_role + 0.4:.2f}s" font-family="{MONO}" text-anchor="end" fill="#bbb" font-size="17">
<text x="1210" y="330">j.victorccrisostomo@gmail.com</text>
<text x="1210" y="358">@faladaivictor</text>
</g>
</g>
<rect width="{W - 2}" height="{H - 2}" x="1" y="1" rx="18" fill="none" stroke="{RED}" stroke-opacity=".5" stroke-width="2"/>
</svg>"""


# ---------------------------------------------------------------- terminal "sobre mim"
def about():
    W = 1280
    lines = [
        ("cmd", "cat sobre_mim.txt"),
        ("out", "> Químico de formação, desenvolvedor por paixão."),
        ("out", "> Uno a teoria da Química com a inovação da Tecnologia"),
        ("out", "  para criar soluções eficientes."),
        ("out", "> Hoje: agentes de IA, dashboards de dados e"),
        ("out", "  controle de sistemas embarcados para reatores."),
        ("cmd", "echo $STATUS"),
        ("hl", "> aprendendo algo novo todo dia  ▮▮▮▮▮▮▮▯▯▯ 70%"),
    ]
    H = 110 + len(lines) * 38 + 20
    css = """
    .ch{opacity:0;animation:on .01s forwards}
    @keyframes on{to{opacity:1}}
    .cur{animation:blink 1s steps(1) infinite}
    @keyframes blink{50%{opacity:0}}
    .dot{animation:pulse 2s ease-in-out infinite}
    @keyframes pulse{50%{opacity:.35}}
    .glow{animation:glow 3s ease-in-out infinite}
    @keyframes glow{50%{stroke-opacity:.9}}
    """
    out = []
    t = 0.4
    y = 105
    lx = 0
    for kind, text in lines:
        if kind == "cmd":
            p, _, px = typed("victor@lab:~$ ", 40, y, t, speed=0, size=20, fill=RED, weight="700")
            out.append(p)
            s, t, lx = typed(text, px, y, t + 0.2, speed=0.05, size=20)
            t += 0.3
        else:
            s, t, lx = typed(text, 40, y, t, speed=0.018, size=20, fill="#ff6b75" if kind == "hl" else "#d8d8d8")
            t += 0.1
        out.append(s)
        y += 38
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>{css}{RAIN_CSS}</style>
<rect class="glow" x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="#0b0b0b" stroke="{RED}" stroke-opacity=".35" stroke-width="2"/>
<path d="M1 15a14 14 0 0 1 14-14h{W - 30}a14 14 0 0 1 14 14v31H1z" fill="#1a1818"/>
<circle class="dot" cx="32" cy="24" r="7" fill="{RED}"/><circle cx="56" cy="24" r="7" fill="#555"/><circle cx="80" cy="24" r="7" fill="#555"/>
<text x="{W / 2}" y="30" text-anchor="middle" font-family="{MONO}" font-size="15" fill="#888">victor@lab: ~/sobre</text>
{"".join(out)}
<rect class="cur" x="{lx + 8:.0f}" y="{y - 38 - 18}" width="12" height="22" fill="{RED}" style="opacity:0;animation:blink 1s steps(1) {t:.1f}s infinite"/>
</svg>"""


# ---------------------------------------------------------------- tabela periódica de tecnologias
STACK = [
    # (num, símbolo, nome, categoria)
    (1, "Py", "Python", "linguagem"),
    (2, "Js", "JavaScript", "linguagem"),
    (3, "Ts", "TypeScript", "linguagem"),
    (4, "Ht", "HTML5", "web"),
    (5, "Cs", "CSS3", "web"),
    (6, "Re", "React", "web"),
    (7, "Nx", "Next.js", "web"),
    (8, "Ph", "PHP", "web"),
    (9, "Sq", "MySQL", "dados"),
    (10, "Pd", "Pandas", "dados"),
    (11, "Jp", "Jupyter", "dados"),
    (12, "Bi", "Power BI", "dados"),
    (13, "Ai", "Agentes IA", "dados"),
    (14, "Lx", "Linux", "ferramenta"),
    (15, "Gt", "Git", "ferramenta"),
    (16, "Dk", "Docker", "ferramenta"),
]
CAT = {"linguagem": RED, "web": "#ffffff", "dados": "#ff7a84", "ferramenta": "#8a8a8a"}


def stack():
    cols, cw, ch, gap = 8, 140, 150, 16
    rows = (len(STACK) + cols - 1) // cols
    W = cols * cw + (cols - 1) * gap + 80
    H = 90 + rows * (ch + gap) + 60
    css = """
    .el{opacity:0;transform-box:fill-box;transform-origin:center;animation:drop .7s cubic-bezier(.2,1.4,.4,1) forwards}
    @keyframes drop{from{opacity:0;transform:translateY(-40px) scale(.6)}to{opacity:1;transform:none}}
    .shine{animation:shine 7s ease-in-out infinite}
    @keyframes shine{0%,70%,100%{opacity:0}80%{opacity:.9}}
    .react{animation:spin 8s linear infinite;transform-box:fill-box;transform-origin:center}
    @keyframes spin{to{transform:rotate(360deg)}}
    .bubble{animation:rise linear infinite}
    @keyframes rise{from{transform:translateY(0);opacity:0}15%{opacity:.8}to{transform:translateY(-120px);opacity:0}}
    """
    tiles = []
    for i, (n, sym, name, cat) in enumerate(STACK):
        r, c = divmod(i, cols)
        x = 40 + c * (cw + gap)
        y = 90 + r * (ch + gap)
        col = CAT[cat]
        d = 0.15 + (r + c) * 0.09
        tiles.append(
            f"""<g class="el" style="animation-delay:{d:.2f}s">
<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="10" fill="#0f0f0f" stroke="{col}" stroke-width="2"/>
<rect class="shine" x="{x}" y="{y}" width="{cw}" height="{ch}" rx="10" fill="none" stroke="{col}" stroke-width="5" style="animation-delay:{i * 0.43:.2f}s"/>
<text x="{x + 12}" y="{y + 26}" font-size="16" fill="#888">{n}</text>
<text x="{x + cw / 2}" y="{y + 92}" font-size="54" font-weight="700" text-anchor="middle" fill="{col}">{sym}</text>
<text x="{x + cw / 2}" y="{y + 128}" font-size="15" text-anchor="middle" fill="#ccc">{escape(name)}</text>
</g>"""
        )
    # bolhas de "reação" subindo
    rnd = random.Random(3)
    bubbles = "".join(
        f'<circle class="bubble" cx="{rnd.uniform(40, W - 40):.0f}" cy="{H - 10}" r="{rnd.uniform(2, 6):.1f}" fill="{RED}" '
        f'style="animation-duration:{rnd.uniform(4, 9):.1f}s;animation-delay:-{rnd.uniform(0, 9):.1f}s"/>'
        for _ in range(12)
    )
    legend = []
    lx = 40
    for cat, col in CAT.items():
        legend.append(f'<rect x="{lx}" y="{H - 42}" width="14" height="14" rx="3" fill="{col}"/>'
                      f'<text x="{lx + 22}" y="{H - 30}" font-size="15" fill="#aaa">{cat}</text>')
        lx += 170
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{MONO}">
<style>{css}{RAIN_CSS}</style>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="#060606" stroke="#222" stroke-width="2"/>
{bubbles}
<g transform="translate({W - 70} 45)"><g class="react">
<ellipse rx="26" ry="9" fill="none" stroke="{RED}" stroke-width="2"/>
<ellipse rx="26" ry="9" fill="none" stroke="{RED}" stroke-width="2" transform="rotate(60)"/>
<ellipse rx="26" ry="9" fill="none" stroke="{RED}" stroke-width="2" transform="rotate(120)"/></g>
<circle r="5" fill="white"/></g>
<text x="40" y="54" font-size="26" font-weight="700" fill="white">Tabela Periódica <tspan fill="{RED}">do Dev</tspan></text>
{"".join(tiles)}
{"".join(legend)}
</svg>"""


# ---------------------------------------------------------------- cards de projeto
PROJECTS = [
    ("hermes", "project-hermes", "Hermes", "Agente de IA que ajuda a criar, preencher", "e organizar documentos.", ["Python", "IA", "Agentes"]),
    ("poseidon", "project-poseidon", "Poseidon", "Visualização, EDA e controle de sistemas", "embarcados para reatores químicos.", ["Python", "Dados", "IoT"]),
    ("orion", "Orion-py", "Orion", "Bot em Python com API, banco de dados", "e deploy com Docker.", ["Python", "API", "Docker"]),
    ("chemquiz", "chemquiz", "ChemQuiz", "Quiz de Química no terminal com banco", "de questões e POO.", ["Python", "POO", "Química"]),
]


def card(slug, repo, title, d1, d2, tags, idx):
    W, H = 620, 230
    css = f"""
    
    .bar{{animation:bar 3s ease-in-out infinite}}
    @keyframes bar{{0%,100%{{transform:scaleX(.15)}}50%{{transform:scaleX(1)}}}}
    .orb{{animation:orb 6s ease-in-out infinite alternate}}
    @keyframes orb{{to{{transform:translate(-30px,20px)}}}}
    .arrow{{animation:nudge 1.6s ease-in-out infinite}}
    @keyframes nudge{{50%{{transform:translateX(6px)}}}}
    """
    tag_svg = []
    tx = 28
    for t in tags:
        w = len(t) * 9 + 22
        tag_svg.append(f'<rect x="{tx}" y="172" width="{w}" height="28" rx="14" fill="none" stroke="{RED}"/>'
                       f'<text x="{tx + w / 2}" y="191" font-size="14" text-anchor="middle" fill="#eee">{t}</text>')
        tx += w + 10
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{MONO}">
<style>{css}{RAIN_CSS}</style>
<defs><clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath>
<radialGradient id="soft"><stop offset=".35" stop-color="{RED}"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>
<linearGradient id="g" x1="0" x2="1"><stop stop-color="#1d1b1b"/><stop offset=".7" stop-color="#050505"/></linearGradient></defs>
<g clip-path="url(#c)">
<rect width="{W}" height="{H}" fill="url(#g)"/>
<circle class="orb" cx="{W - 20}" cy="30" r="90" fill="url(#soft)" opacity=".55"/>
<g>
<text x="28" y="52" font-size="15" fill="{RED}">~/projetos/{escape(repo)}</text>
<text x="28" y="94" font-size="34" font-weight="700" fill="white">{escape(title)}</text>
<text x="28" y="128" font-size="16" fill="#cfcfcf">{escape(d1)}</text>
<text x="28" y="150" font-size="16" fill="#cfcfcf">{escape(d2)}</text>
{"".join(tag_svg)}
<g class="arrow"><text x="{W - 30}" y="194" font-size="16" text-anchor="end" fill="white">ver repo →</text></g>
</g>
<rect class="bar" x="0" y="{H - 5}" width="{W}" height="5" fill="{RED}" style="transform-origin:0 0"/>
</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="#2a2a2a" stroke-width="2"/>
</svg>"""


# ---------------------------------------------------------------- divisória e rodapé
def divider():
    W, H = 1280, 40
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
.run{{animation:run 4s ease-in-out infinite alternate}}
@keyframes run{{to{{transform:translateX({W - 80}px)}}}}
.l{{stroke-dasharray:6 10;animation:dash 1.5s linear infinite}}
@keyframes dash{{to{{stroke-dashoffset:-32}}}}
</style>
<defs><radialGradient id="g"><stop offset=".3" stop-color="{RED}"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient></defs>
<line class="l" x1="20" y1="20" x2="{W - 20}" y2="20" stroke="{RED}" stroke-opacity=".6" stroke-width="2"/>
<g class="run"><circle cx="40" cy="20" r="13" fill="url(#g)"/><circle cx="40" cy="20" r="5" fill="white"/></g>
</svg>"""


def footer():
    W, H = 1280, 200
    prompt = "victor@lab:~$ "
    s, _, x = typed("exit 0  # valeu pela visita!", 400 + len(prompt) * 15.6, 112, 0.5, speed=0.05, size=26)
    css = """
    
    .ch{opacity:0;animation:on .01s forwards}
    @keyframes on{to{opacity:1}}
    .fox-bob{animation:bob 3s ease-in-out infinite}
    @keyframes bob{50%{transform:translateY(-30px)}}
    .cur{opacity:0;animation:blink 1s steps(1) 2.2s infinite}
    @keyframes blink{50%{opacity:1}}
    """
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>{css}{RAIN_CSS}</style>
<defs><clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath></defs>
<g clip-path="url(#c)">
<rect width="{W}" height="{H}" fill="#060606"/>
{matrix(W, H, 26, size=16, opacity=0.3, seed=99, trail=7)}
{fox_group(250, 30, 140)}
<text x="400" y="112" font-family="{MONO}" font-size="26" font-weight="700" fill="{RED}">{prompt}</text>
{s}
<rect class="cur" x="{x + 6:.0f}" y="90" width="14" height="28" fill="{RED}"/>
</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="#222" stroke-width="2"/>
</svg>"""


if __name__ == "__main__":
    write("header.svg", header())
    write("about.svg", about())
    write("stack.svg", stack())
    for i, p in enumerate(PROJECTS):
        write(f"card-{p[0]}.svg", card(*p, i))
    write("divider.svg", divider())
    write("footer.svg", footer())
