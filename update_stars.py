import os, json, base64
from urllib.request import urlopen, Request
from urllib.error import URLError

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

# Kategori kuralları
CATEGORIES = [
    ("🤖 AI & Agents", [
        "goose","OwnPilot","WrongStack","OpenJarvis","skills","VibeVoice",
        "Agent-Reach","career-ops","agency-agents","ai-agent-team","BMAD",
        "ai-website-cloner","vibe-kanban","gpt-oss","baguette","project-bootstrap"
    ]),
    ("🎯 Skills & Prompts", [
        "agents.md","karpathy-skills","Frontend-Design-Toolkit","agent-skills",
        "lenny-skills","gemini-skills","ui-ux-pro-max","gsap-skills","design.md","marketingskills"
    ]),
    ("🔧 Dev Tools & CLI", [
        "claudecodeui","warp","open-design","OpenTokenUsage","openusage",
        "FluidFlow","witr","syncthing","uBlock","free-for-dev","coreutils"
    ]),
    ("📱 Mobile & Cross-Platform", [
        "localsend","Telegram-Drive","dev-manager-desktop","OpenNOW","OpenWA","pear-desktop"
    ]),
    ("🎵 Medya, Ses & Video", [
        "VoxCPM","voicebox","voice-pro","GPT-SoVITS","VidBee","ytDownloader",
        "IPTV","iptv"
    ]),
    ("📋 Prodüktivite & Self-Hosted", [
        "lifeforge","paperless-ngx","TaxHacker","twitter-archive","x-bookmark",
        "marktext","Recordly","openscreen","opendataloader-pdf"
    ]),
    ("🖥️ macOS & Desktop Apps", [
        "Mole","Blankie","dodopulse","awesome-native-macosx","clicklight","microsoft-ui-reactor"
    ]),
    ("⚙️ Yazılım Geliştirme & Güvenlik", [
        "sherlock","vscode-dark-islands","dfmc","open-pdf-studio","claw-code"
    ]),
    ("🇹🇷 Türkçe Projeler", [
        "bakiyedefter","kurtarma-plani","yargi-mcp","turkish-apis","zikiro",
        "Ai-Arastirma","geo-seo","MetroFlow"
    ]),
]

def categorize(repo):
    name = repo["full_name"].lower()
    for cat_name, keywords in CATEGORIES:
        if any(kw.lower() in name for kw in keywords):
            return cat_name
    return "🗂️ Diğer"

# Kategorilere ayır
buckets = {c[0]: [] for c in CATEGORIES}
buckets["🗂️ Diğer"] = []
for r in repos:
    buckets[categorize(r)].append(r)

# README oluştur
lines = [
    "# ⭐ awesome-stars",
    "",
    "> Yıldızladığım GitHub repoları — kategorilere göre otomatik düzenlenmiş",
    f"> Son güncelleme: {__import__(\"datetime\").date.today()}",
    "",
    "## İçindekiler", ""
]

for cat, rlist in buckets.items():
    if rlist:
        anchor = cat.lower().replace(" ", "-").replace("&","").replace("/","").replace("ı","i").replace("ü","u").replace("ö","o").replace("ğ","g").replace("ş","s").replace("ç","c").replace("️","").replace("🤖","").replace("🎯","").replace("🔧","").replace("📱","").replace("🎵","").replace("📋","").replace("🖥","").replace("⚙","").replace("🇹🇷","").replace("🗂","").strip("-")
        lines.append(f"- [{cat} ({len(rlist)})](#{.join(c for c in anchor if c.isalnum() or c == \"-\")})")

lines += ["", "---", ""]

for cat, rlist in buckets.items():
    if not rlist:
        continue
    lines += [f"## {cat}", "", "| Repo | Açıklama | Dil |", "|------|----------|-----|"]
    for r in sorted(rlist, key=lambda x: x["full_name"].lower()):
        desc = (r.get("description") or "").replace("|","\\|")[:80]
        lang = r.get("language") or "N/A"
        lines.append(f"| [{r[\"full_name\"]}]({r[\"html_url\"]}) | {desc} | {lang} |")
    lines += ["", "---", ""]

lines.append(f"*Toplam: {len(repos)} repo · {len([b for b in buckets.values() if b])} kategori*")

with open("README.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ {len(repos)} repo, {len([b for b in buckets.values() if b])} kategori")
