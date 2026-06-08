import os, json, datetime
from urllib.request import urlopen, Request

TOKEN = os.environ["GH_TOKEN"]
USER  = os.environ["GH_USER"]

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json",
    "User-Agent": "awesome-stars-bot"
}

def gh(url):
    req = Request(url, headers=HEADERS)
    with urlopen(req) as r:
        return json.loads(r.read())

# Tüm yıldızları çek
repos, page = [], 1
while True:
    data = gh(f"https://api.github.com/users/{USER}/starred?per_page=100&page={page}")
    if not data:
        break
    repos.extend(data)
    page += 1

print(f"Toplam {len(repos)} repo çekildi.")

# Kategori eşleştirme — repo adı veya owner içinde geçen anahtar kelimeler
CATEGORIES = [
    ("🤖 AI & Agents", [
        "goose", "ownpilot", "wrongstack", "openjarvis", "viбevoice",
        "vibevoice", "agent-reach", "career-ops", "agency-agents",
        "ai-agent-team", "bmad", "ai-website-cloner", "vibe-kanban",
        "gpt-oss", "baguette", "project-bootstrap", "open-jarvis",
        "google/skills", "microsoft/vibevoice"
    ]),
    ("🎯 Skills & Prompts", [
        "agents.md", "karpathy-skills", "frontend-design-toolkit",
        "callstackincubator/agent-skills", "lenny-skills", "gemini-skills",
        "ui-ux-pro-max", "gsap-skills", "design.md", "marketingskills"
    ]),
    ("🔧 Dev Tools & CLI", [
        "claudecodeui", "warpdotdev", "open-design", "opentokenusage",
        "openusage", "fluidflow", "witr", "syncthing", "ublock",
        "free-for-dev", "microsoft/coreutils"
    ]),
    ("📱 Mobile & Cross-Platform", [
        "localsend", "telegram-drive", "dev-manager-desktop", "opennow",
        "openwa", "pear-desktop"
    ]),
    ("🎵 Medya, Ses & Video", [
        "voxcpm", "voicebox", "voice-pro", "gpt-sovits", "vidbee",
        "ytdownloader", "free-tv", "iptv-org"
    ]),
    ("📋 Prodüktivite & Self-Hosted", [
        "lifeforge", "paperless-ngx", "taxhacker", "twitter-archive",
        "x-bookmark", "marktext", "recordly", "openscreen",
        "opendataloader-pdf"
    ]),
    ("🖥️ macOS & Desktop Apps", [
        "tw93/mole", "blankie", "dodopulse", "awesome-native-macosx",
        "clicklight", "microsoft-ui-reactor"
    ]),
    ("⚙️ Yazılım Geliştirme & Güvenlik", [
        "sherlock", "vscode-dark-islands", "dfmc", "open-pdf-studio",
        "claw-code"
    ]),
    ("🇹🇷 Türkçe Projeler", [
        "bakiyedefter", "kurtarma-plani", "yargi-mcp", "turkish-apis",
        "zikiro", "ai-arastirma", "geo-seo-claude", "metroflow"
    ]),
]

def categorize(repo):
    full = repo["full_name"].lower()
    for cat_name, keywords in CATEGORIES:
        if any(kw.lower() in full for kw in keywords):
            return cat_name
    # topics ile de dene
    topics = " ".join(repo.get("topics") or []).lower()
    if any(k in topics for k in ["agent","llm","ai","gpt","claude","gemini"]):
        return "🤖 AI & Agents"
    if any(k in topics for k in ["macos","swiftui","mac-app"]):
        return "🖥️ macOS & Desktop Apps"
    if any(k in topics for k in ["flutter","react-native","mobile"]):
        return "📱 Mobile & Cross-Platform"
    if any(k in topics for k in ["tts","voice","speech","audio"]):
        return "🎵 Medya, Ses & Video"
    return "🗂️ Diğer"

# Kategorilere ayır
order = [c[0] for c in CATEGORIES] + ["🗂️ Diğer"]
buckets = {c: [] for c in order}
for r in repos:
    buckets[categorize(r)].append(r)

# README oluştur
today = datetime.date.today().strftime("%d %B %Y")
lines = [
    "# ⭐ awesome-stars",
    "",
    "> **batuhanarici** tarafından yıldızlanan GitHub repoları — kategorilere göre otomatik düzenlenmiş  ",
    f"> 🕐 Son güncelleme: {today} &nbsp;|&nbsp; 📦 Toplam: {len(repos)} repo",
    "",
    "## İçindekiler",
    "",
]

for cat in order:
    rlist = buckets[cat]
    if not rlist:
        continue
    emoji = cat.split()[0]
    label = " ".join(cat.split()[1:])
    lines.append(f"- [{cat}](#) — {len(rlist)} repo")

lines += ["", "---", ""]

for cat in order:
    rlist = buckets[cat]
    if not rlist:
        continue
    lines += [
        f"## {cat}",
        "",
        "| Repo | Açıklama | Dil |",
        "|------|----------|-----|",
    ]
    for r in sorted(rlist, key=lambda x: x["full_name"].lower()):
        desc = (r.get("description") or "—").replace("|", "\\|")[:90]
        lang = r.get("language") or "N/A"
        lines.append(f"| [{r['full_name']}]({r['html_url']}) | {desc} | `{lang}` |")
    lines += ["", "---", ""]

lines.append(f"*🤖 Bu dosya [GitHub Actions](.github/workflows/update.yml) tarafından her gece otomatik güncellenmektedir.*")

with open("README.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ README güncellendi: {len(repos)} repo, {len([b for b in buckets.values() if b])} kategori")
