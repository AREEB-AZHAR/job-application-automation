import json
import re
from typing import Dict, Any, Tuple, Optional

def load_profile(profile_path: str) -> Dict[str, Any]:
    with open(profile_path, "r", encoding="utf-8") as f:
        return json.load(f)

def evaluate_job(job: Dict[str, Any], profile: Dict[str, Any]) -> Tuple[bool, str, Optional[str], Optional[str]]:
    """
    Evaluates whether a job matches Areeb Azhar's criteria:
    - Must require <= 1 year experience (or entry level/fresh graduate/junior).
    - Must match one of the target tech domains.
    Returns:
    (is_match, reason, matched_domain, cv_path)
    """
    title = job.get("title", "").lower()
    description = job.get("description", "").lower()
    full_text = f"{title} {description}"

    # 1. Experience check
    # Check for senior / lead / principal keywords
    disqualifying_titles = ["senior", "lead", "principal", "staff", "director", "architect", "head of", "vp", "manager"]
    for keyword in disqualifying_titles:
        if keyword in title:
            return False, f"Disqualified: Title contains senior keyword '{keyword}'", None, None

    # Check for experience years requirement (e.g. "3+ years", "2-4 years", "5 years")
    exp_matches = re.findall(r"(\d+)\+?\s*(?:-\s*(\d+))?\s*(?:years?|yrs?)\s*(?:of)?\s*experience", full_text)
    for min_exp, max_exp in exp_matches:
        min_years = int(min_exp)
        if min_years > 1:
            return False, f"Disqualified: Requires {min_years}+ years of experience (criteria is <= 1 year)", None, None

    # Check for acceptable levels
    entry_indicators = [
        "junior", "entry level", "fresh", "graduate", "associate", "intern", 
        "0-1", "0 to 1", "less than 1", "1 year", "1+ year", "no experience required"
    ]
    is_entry_level = any(indicator in full_text for indicator in entry_indicators)

    # 2. Domain matching
    mappings = profile.get("cv_mappings", {})
    if any(re.search(r"\b" + re.escape(k) + r"\b", full_text) for k in ["react", "node", "typescript", "frontend", "web developer", "full stack", "fullstack"]):
        domain = "full_stack"
        cv_path = mappings.get("full_stack")
    elif any(re.search(r"\b" + re.escape(k) + r"\b", full_text) for k in ["rust", "blockchain", "solidity", "hyperledger", "web3", "smart contract"]):
        domain = "rust_blockchain"
        cv_path = mappings.get("rust_blockchain")
    elif any(re.search(r"\b" + re.escape(k) + r"\b", full_text) for k in ["flutter", "dart", "mobile developer", "android", "ios"]):
        domain = "flutter"
        cv_path = mappings.get("flutter")
    elif any(re.search(r"\b" + re.escape(k) + r"\b", full_text) for k in ["unity", "game developer", "c#", "unreal", "game programmer"]):
        domain = "game_dev"
        cv_path = mappings.get("game_dev")
    elif any(re.search(r"\b" + re.escape(k) + r"\b", full_text) for k in ["machine learning", "ai", "artificial intelligence", "deep learning", "nlp", "llm", "data science"]):
        domain = "ai_ml"
        cv_path = mappings.get("ai_ml")
    elif any(re.search(r"\b" + re.escape(k) + r"\b", full_text) for k in ["software engineer", "software developer", "programmer", "trainee"]):
        # Default software engineering maps to full-stack
        domain = "full_stack"
        cv_path = mappings.get("full_stack")
    else:
        return False, "Disqualified: Tech stack does not match software engineering domains", None, None

    match_reason = "Accepted: Matches domain and experience criteria (< 1 year)"
    return True, match_reason, domain, cv_path

def generate_cover_letter(job: Dict[str, Any], domain: str, profile: Dict[str, Any]) -> str:
    """
    Generates an authentic, developer-written cover letter highlighting real engineering projects.
    """
    company = job.get("company", "the engineering team")
    title = job.get("title", "Software Engineer")
    
    project_highlights = {
        "full_stack": (
            "Recently, I built CryptoTrader—a full-stack market analytics dashboard and simulator using React 19, TypeScript, Vite, and Zustand. "
            "I also built IqraDegreeChain, an academic credentials verification service combining an Express/TypeScript API gateway with Hyperledger Fabric."
        ),
        "ai_ml": (
            "My focus centers on practical machine learning pipelines and Python backend services. "
            "I've implemented data ingestion workflows, model inference APIs, and evaluation harnesses with clean, maintainable architecture."
        ),
        "flutter": (
            "I build production-ready mobile apps with Flutter and Dart, with a strong focus on clean architecture, "
            "responsive UI performance, and reliable REST API synchronization."
        ),
        "game_dev": (
            "I develop gameplay systems and interactive mechanics in Unity with C#, focusing on deterministic physics, "
            "state machines, and optimized UI rendering."
        ),
        "rust_blockchain": (
            "I completed a 9-week intensive internship in Rust & Blockchain Technology (Rockstable x Hazara University), "
            "and implemented custom chaincode and verification services for IqraDegreeChain with Hyperledger Fabric."
        )
    }

    highlight = project_highlights.get(domain, project_highlights["full_stack"])

    cover_letter = f"""Hi {company} team,

I'm applying for the {title} opening. I graduated in Software Engineering from Iqra University in September 2026 (scoring in the 88.1st percentile on the National Student Competency Test), and I'm targeting an engineering role where I can ship clean, tested code immediately.

{highlight}

I write readable, modular code, move fast with high engineering standards, and collaborate comfortably across remote, hybrid, or on-site setups. My public code and projects are available at github.com/AREEB-AZHAR.

I would appreciate the chance to discuss your engineering roadmap and how I can help your team ship.

Best regards,

Areeb Azhar
+92 301 2343423
areebazhar3@gmail.com
github.com/AREEB-AZHAR
"""
    return cover_letter
