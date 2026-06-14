import os, json, datetime, time
from urllib.request import urlopen, Request

TOKEN      = os.environ["GH_TOKEN"]
USER       = os.environ["GH_USER"]
GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json",
    "User-Agent": "awesome-stars-bot"
}

def gh(url):
    req = Request(url, headers=HEADERS)
    with urlopen(req) as r:
        return json.loads(r.read())

# ── Tüm yıldızları çek ──────────────────────────────────────────────
repos, page = [], 1
while True:
    data = gh(f"https://api.github.com/users/{USER}/starred?per_page=100&page={page}")
    if not data:
        break
    repos.extend(data)
    page += 1
print(f"✅ {len(repos)} repo çekildi.")

# ── Önbellek yükle ──────────────────────────────────────────────────
CACHE_FILE = "meta_cache.json"
try:
    with open(CACHE_FILE, encoding="utf-8") as f:
        cache = json.load(f)
except:
    cache = {}

# ── Gemini API ───────────────────────────────────────────────────────
def gemini_meta(repo):
    if not GEMINI_KEY:
        return None
    prompt = f"""GitHub reposu hakkında bilgi:
- Repo: {repo["full_name"]}
- Açıklama (EN): {repo.get("description") or ""}
- Dil: {repo.get("language") or ""}
- Konular: {", ".join(repo.get("topics") or [])}

YALNIZCA şu JSON formatında yanıt ver, başka hiçbir şey yazma:
{{"tr": "<1-2 cümle Türkçe açıklama>", "tools": ["<araçlar>"]}}

tools için SADECE şu listeden seç: Claude Code, Cursor, Windsurf, VS Code, Gemini CLI, Codex, Terminal, Google Colab, Copilot, MCP, Tauri, Electron, Flutter, Docker, Ollama, LM Studio, API, macOS, Windows, Xcode, Standalone, Genel Referans, VLC, Kodi, Chrome, Firefox, Visual Studio"""

    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 200}
    }).encode()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
    req = Request(url, data=body, headers={"Content-Type": "application/json"})
    try:
        with urlopen(req, timeout=15) as r:
            resp = json.loads(r.read())
        text = resp["candidates"][0]["content"]["parts"][0]["text"].strip()
        start, end = text.find("{"), text.rfind("}") + 1
        return json.loads(text[start:end])
    except Exception as e:
        print(f"  ⚠️  Gemini hatası ({repo['full_name']}): {e}")
        return None

# ── Tüm repolar için meta al (önbellek öncelikli) ────────────────────
new_count = 0
for i, r in enumerate(repos):
    key = r["full_name"]
    if key not in cache:
        print(f"  [{i+1}/{len(repos)}] 🤖 {key}")
        meta = gemini_meta(r)
        cache[key] = meta if meta else {
            "tr": (r.get("description") or "—"),
            "tools": []
        }
        new_count += 1
        time.sleep(0.4)

if new_count:
    print(f"✅ {new_count} repo Gemini ile işlendi.")

with open(CACHE_FILE, "w", encoding="utf-8") as f:
    json.dump(cache, f, ensure_ascii=False, indent=2)
print(f"✅ Önbellek kaydedildi ({len(cache)} repo).")

# ── Kategori eşleştirme ──────────────────────────────────────────────
CATEGORIES = [
    ("🤖 AI & Agents", [
        "goose","ownpilot","wrongstack","openjarvis","vibevoice","agent-reach",
        "career-ops","agency-agents","ai-agent-team","bmad","ai-website-cloner",
        "vibe-kanban","gpt-oss","baguette","project-bootstrap","open-jarvis",
        "google/skills","microsoft/vibevoice","moneyprinterturbo","oh-my-openagent",
        "skillspector","gstack","tolaria","codexqb",
    ]),
    ("🎯 Skills & Prompts", [
        "agents.md","karpathy-skills","frontend-design-toolkit","lenny-skills",
        "gemini-skills","ui-ux-pro-max","gsap-skills","design.md","marketingskills",
        "callstackincubator/agent-skills","addyosmani/agent-skills","graphify",
    ]),
    ("🔧 Dev Tools & CLI", [
        "claudecodeui","warpdotdev","open-design","opentokenusage","openusage",
        "fluidflow","witr","syncthing","ublock","free-for-dev","microsoft/coreutils",
    ]),
    ("📱 Mobile & Cross-Platform", [
        "localsend","telegram-drive","dev-manager-desktop","opennow","openwa",
        "pear-desktop","mobile-system-design",
    ]),
    ("🎵 Medya, Ses & Video", [
        "voxcpm","voicebox","voice-pro","gpt-sovits","vidbee",
        "ytdownloader","free-tv","iptv-org",
    ]),
    ("📋 Prodüktivite & Self-Hosted", [
        "lifeforge","paperless-ngx","taxhacker","twitter-archive",
        "x-bookmark","marktext","recordly","openscreen","opendataloader-pdf",
    ]),
    ("🖥️ macOS & Desktop Apps", [
        "tw93/mole","blankie","dodopulse","awesome-native-macosx",
        "clicklight","microsoft-ui-reactor",
    ]),
    ("⚙️ Yazılım Geliştirme & Güvenlik", [
        "sherlock","vscode-dark-islands","dfmc","open-pdf-studio","claw-code",
    ]),
    ("🇹🇷 Türkçe Projeler", [
        "bakiyedefter","kurtarma-plani","yargi-mcp","turkish-apis",
        "zikiro","ai-arastirma","geo-seo-claude","metroflow",
    ]),
]

def categorize(repo):
    full   = repo["full_name"].lower()
    topics = " ".join(repo.get("topics") or []).lower()
    desc   = (repo.get("description") or "").lower()
    for cat_name, keywords in CATEGORIES:
        if any(kw.lower() in full for kw in keywords):
            return cat_name
    if any(k in topics for k in ["agent","llm","ai","gpt","claude","gemini","copilot","mcp"]):
        return "🤖 AI & Agents"
    if any(k in topics for k in ["prompt","skill","template"]):
        return "🎯 Skills & Prompts"
    if any(k in topics for k in ["cli","terminal","devtool"]):
        return "🔧 Dev Tools & CLI"
    if any(k in topics for k in ["macos","swiftui","mac-app","menubar"]):
        return "🖥️ macOS & Desktop Apps"
    if any(k in topics for k in ["flutter","react-native","mobile","ios","android"]):
        return "📱 Mobile & Cross-Platform"
    if any(k in topics for k in ["tts","voice","speech","audio","video","iptv"]):
        return "🎵 Medya, Ses & Video"
    if any(k in topics for k in ["self-hosted","homelab","docker","productivity"]):
        return "📋 Prodüktivite & Self-Hosted"
    if any(k in topics for k in ["security","osint","pentest","ctf"]):
        return "⚙️ Yazılım Geliştirme & Güvenlik"
    if any(k in desc for k in ["türk","turkish","türkçe"]):
        return "🇹🇷 Türkçe Projeler"
    return "🗂️ Diğer"

order = [c[0] for c in CATEGORIES] + ["🗂️ Diğer"]
buckets = {c: [] for c in order}
for r in repos:
    buckets[categorize(r)].append(r)

# ── Badge üretici ────────────────────────────────────────────────────
COLORS = {
    "Claude Code":"5C4EFF","Cursor":"000000","Windsurf":"0099FF",
    "VS Code":"007ACC","Gemini CLI":"4285F4","Codex":"412991",
    "Terminal":"4EAA25","Google Colab":"F9AB00","Copilot":"555555",
    "MCP":"7C3AED","Tauri":"FFC131","Electron":"47848F",
    "Flutter":"02569B","Docker":"2496ED","Ollama":"222222",
    "LM Studio":"8B5CF6","API":"6C757D","macOS":"222222",
    "Windows":"0078D4","Xcode":"147EFB","Standalone":"6B7280",
    "Genel Referans":"6B7280","Chrome":"4285F4","Firefox":"FF7139",
    "VLC":"FF8800","Kodi":"17B2E7","Visual Studio":"5C2D91",
}

def badges(tools):
    out = []
    for t in tools:
        c = COLORS.get(t, "6B7280")
        l = t.replace(" ", "%20").replace("-","--")
        out.append(f"![{t}](https://img.shields.io/badge/{l}-{c}?style=flat-square&logoColor=white)")
    return " ".join(out) if out else "—"

# ── README oluştur ───────────────────────────────────────────────────
today     = datetime.date.today().strftime("%d %B %Y")
total     = len(repos)
cat_count = len([b for b in buckets.values() if b])

lines = [
    "# ⭐ awesome-stars",
    "",
    "> **batuhanarici** tarafından yıldızlanan GitHub repoları — kategorilere göre otomatik düzenlenmiş",
    f"> 🕐 Son güncelleme: **{today}** &nbsp;|&nbsp; 📦 Toplam: **{total} repo** &nbsp;|&nbsp; 🗂️ Kategori: **{cat_count}**",
    "",
    "## İçindekiler", "",
]
for cat in order:
    if buckets[cat]:
        lines.append(f"- [{cat}](#) — {len(buckets[cat])} repo")
lines += ["", "---", ""]

for cat in order:
    rlist = buckets[cat]
    if not rlist:
        continue
    lines += [f"## {cat}", "", "| Repo | Açıklama | Dil | Araçlar |", "|------|----------|-----|---------|"]
    for r in sorted(rlist, key=lambda x: x["full_name"].lower()):
        key  = r["full_name"]
        meta = cache.get(key, {})
        desc = (meta.get("tr") or r.get("description") or "—").replace("|","\\|")
        tools = meta.get("tools", [])
        lang  = r.get("language") or "N/A"
        lines.append(f"| [{key}]({r['html_url']}) | {desc} | `{lang}` | {badges(tools)} |")
    lines += ["", "---", ""]

lines.append("*🤖 Bu dosya [GitHub Actions](.github/workflows/update.yml) tarafından her gece otomatik güncellenmektedir.*")

with open("README.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ README güncellendi: {total} repo, {cat_count} kategori")
