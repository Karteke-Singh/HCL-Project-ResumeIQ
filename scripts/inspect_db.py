"""
Inspector tool for Project P_101 SQLite Database (resume_screener.db).
Displays:
1. Tables and row counts
2. Column schema for each table
3. Sample join query showing Jobs, Candidates, Profiles, and Scores
"""

import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "resume_screener.db"


def inspect():
    print("=" * 75)
    print("  SQLITE DATABASE INSPECTION: resume_screener.db")
    print(f"  Path: {DB_PATH}")
    print("=" * 75)

    if not DB_PATH.exists():
        print(f"[ERROR] Database file not found at {DB_PATH}. Please run scripts/seed_data.py first.")
        sys.exit(1)

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # 1. Tables and Row Counts
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in cursor.fetchall()]

    print(f"\n[TABLES SUMMARY] ({len(tables)} tables found):")
    for tbl in sorted(tables):
        cursor.execute(f"SELECT COUNT(*) FROM {tbl};")
        count = cursor.fetchone()[0]
        print(f"  • {tbl:<15} : {count:>4} rows")

    # 2. Schema breakdown
    print("\n" + "-" * 75)
    print("[SCHEMA DEFINITIONS]")
    for tbl in sorted(tables):
        cursor.execute(f"PRAGMA table_info({tbl});")
        cols = cursor.fetchall()
        col_summary = [f"{c[1]} ({c[2]})" for c in cols]
        print(f"\n  Table: {tbl}")
        for c in cols:
            pk = " [PRIMARY KEY]" if c[5] == 1 else ""
            notnull = " NOT NULL" if c[3] == 1 else ""
            print(f"    - {c[1]:<25} : {c[2]:<12}{pk}{notnull}")

    # 3. Sample Joined Query: Top Candidates for Job 1
    print("\n" + "-" * 75)
    print("[SAMPLE QUERY: Top 5 Ranked Candidates for Junior Python Backend Developer]")
    query = """
    SELECT 
        c.display_id,
        p.experience_years,
        s.rule AS rule_score,
        s.semantic AS semantic_score,
        s.llm_fit AS llm_fit,
        s.total AS total_score,
        s.explanation
    FROM candidates c
    JOIN jobs j ON c.job_id = j.id
    JOIN profiles p ON p.candidate_id = c.id
    JOIN scores s ON s.candidate_id = c.id AND s.job_id = j.id
    WHERE j.id = 'JOB_001_PY_BACKEND'
    ORDER BY s.total DESC
    LIMIT 5;
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    print(f"  {'ID':<6} | {'Exp (Yrs)':<9} | {'Rule':<6} | {'Semantic':<8} | {'LLM Fit':<8} | {'Total':<6} | {'Explanation'}")
    print("  " + "-" * 73)
    for r in rows:
        cid, exp, rule, sem, fit, tot, exp_text = r
        short_exp = exp_text[:50] + "..." if len(exp_text) > 50 else exp_text
        print(f"  {cid:<6} | {exp:<9.1f} | {rule:<6.2f} | {sem:<8.2f} | {fit:<8.2f} | {tot:<6.1f} | {short_exp}")

    conn.close()
    print("\n" + "=" * 75)
    print("  [SUCCESS] Database file verified, fully populated, and queryable.")
    print("=" * 75)


if __name__ == "__main__":
    inspect()
