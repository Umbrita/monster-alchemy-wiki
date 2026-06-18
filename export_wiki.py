import os
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# ----------------------------
# CONFIGURATION
# ----------------------------
CREDENTIALS_FILE = "credentials.json"
SPREADSHEET_URL_OR_NAME = "MonsterTable" # Replace with your sheet's exact name

OUTPUT_BASE_DIR = "./content"
FOLDERS = ["monsters", "active_skills", "passive_skills", "resources"]

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]

def get_client():
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    return gspread.authorize(creds)

def clean_filename(name):
    return "".join([c if c.isalnum() or c in " _-" else "" for c in str(name)]).strip()

def create_md_file(folder, filename, frontmatter_dict, body=""):
    """Helper to write markdown files with YAML frontmatter."""
    os.makedirs(os.path.join(OUTPUT_BASE_DIR, folder), exist_ok=True)
    filepath = os.path.join(OUTPUT_BASE_DIR, folder, f"{filename}.md")
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("---\n")
        for k, v in frontmatter_dict.items():
            # Clean up the value to avoid YAML breaks
            clean_val = str(v).replace('"', "'") 
            f.write(f'{k}: "{clean_val}"\n')
        f.write("---\n\n")
        f.write(body)

# ----------------------------
# MAIN EXPORT LOGIC
# ----------------------------
def main():
    gc = get_client()
    # You can open by URL if you prefer: gc.open_by_url("YOUR_URL")
    sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1XM4GWAg83_4Sc6OylbDRciPxqfdAUCCUkvtrehe7Ynk/edit")

    print("Fetching data from Google Sheets...")
    
    # 1. Load tabs into Pandas DataFrames
    # We use empty dictionaries to catch missing tabs gracefully
    try: df_monsters = pd.DataFrame(sheet.worksheet("monsters").get_all_records())
    except: df_monsters = pd.DataFrame()
    
    try: df_active = pd.DataFrame(sheet.worksheet("active skills").get_all_records())
    except: df_active = pd.DataFrame()
    
    try: df_passive = pd.DataFrame(sheet.worksheet("passive skills").get_all_records())
    except: df_passive = pd.DataFrame()
    
    try: df_resources = pd.DataFrame(sheet.worksheet("resource data").get_all_records())
    except: df_resources = pd.DataFrame()
    
    try: df_skill_levels = pd.DataFrame(sheet.worksheet("monsterskillslevels").get_all_records())
    except: df_skill_levels = pd.DataFrame()

    print("Exporting Resources, Active Skills, and Passive Skills...")
    
    # 2. Export basic entities (Skills & Resources)
    for index, row in df_active.iterrows():
        name = row.get("Name", f"ActiveSkill_{index}")
        create_md_file("active_skills", clean_filename(name), row.to_dict())

    for index, row in df_passive.iterrows():
        name = row.get("Name", f"PassiveSkill_{index}")
        create_md_file("passive_skills", clean_filename(name), row.to_dict())
        
    for index, row in df_resources.iterrows():
        name = row.get("Name", f"Resource_{index}")
        create_md_file("resources", clean_filename(name), row.to_dict())

    print("Processing Monsters and linking abilities...")

    # 3. Group Active Skills by Monster
    # Assuming columns in 'monsterskillslevels' are something like 'Monster', 'Skill', 'Level'
    monster_skills_dict = {}
    if not df_skill_levels.empty:
        # Standardize column names to lowercase for easier matching if needed, 
        # but here we assume the exact names are 'Monster', 'Skill', 'Level'
        for _, row in df_skill_levels.iterrows():
            m_name = str(row.get("Monster", "")).strip()
            skill_name = str(row.get("Skill", "")).strip()
            level = str(row.get("Level", "1")).strip()
            
            if m_name not in monster_skills_dict:
                monster_skills_dict[m_name] = []
            
            # Create an Obsidian link: [[Skill Name]] (Level X)
            if level in ["1", 1, "0", 0, ""]:
                monster_skills_dict[m_name].append(f"- [[{skill_name}]] (Innate/Unlocked)")
            else:
                monster_skills_dict[m_name].append(f"- [[{skill_name}]] (Unlocks at Lv. {level})")

    # 4. Export Monsters
    for index, row in df_monsters.iterrows():
        name = str(row.get("Name", "")).strip()
        if not name:
            continue
            
        # Extract attributes exactly as you requested
        tier = row.get("Tier", "")
        m_type = row.get("Type", "")
        attack_type = row.get("AttackType", "")
        health = row.get("health", "")
        strength = row.get("strenght", "") # Intentionally matching your spelling
        defense = row.get("defense", "")
        mind = row.get("mind", "")
        soul = row.get("soul", "")
        agility = row.get("agility", "")
        total_stats = row.get("total stats", "")
        description = row.get("description", "")
        
        # Link Passive Skill (Obsidian format)
        passive_raw = str(row.get("passive", "")).strip()
        passive_link = f"[[{passive_raw}]]" if passive_raw else "None"
        
        # Get Active Skills for this specific monster
        active_skills_list = monster_skills_dict.get(name, ["- No active skills listed."])
        active_skills_formatted = "\n".join(active_skills_list)
        
        # Build the Markdown body exactly to your specifications
        body = f"""# {name}

*{description}*

## Combat Profile
- **Tier:** {tier}
- **Elemental Type:** {m_type}
- **Technique Type:** {attack_type}

## Stats
| Stat | Value |
| ---- | ----- |
| **Health** | {health} |
| **Strength** | {strength} |
| **Defense** | {defense} |
| **Mind** | {mind} |
| **Soul** | {soul} |
| **Agility** | {agility} |
| **Total Stats** | **{total_stats}** |

## Abilities

### Passive Ability
{passive_link}

### Active Skills
{active_skills_formatted}
"""
        # Create the frontmatter (YAML) for Quartz tagging/filtering
        frontmatter = {
            "title": name,
            "tier": tier,
            "type": m_type,
            "tags": "monster"
        }
        
        create_md_file("monsters", clean_filename(name), frontmatter, body)

    print("Wiki generation complete! Check the './content' folder.")

if __name__ == "__main__":
    main()