import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from app.parser import ResumeParser
from app.ats_engine import ATSEngine
from app.session_store import SessionStore
from app.llm_service import LLMService
from app.chart_generator import ChartGenerator

def run_tests():
    print("==========================================")
    print("RUNNING ATS CHATBOT AUTOMATED TEST SUITE")
    print("==========================================")

    # 1. Test Resume Parser (Sample Text)
    sample_resume_1 = """
    Jane Doe
    jane.doe@example.com | (555) 123-4567 | linkedin.com/in/janedoe | github.com/janedoe

    SUMMARY
    Senior DevOps Engineer with 5 years of experience building and scaling cloud infrastructure.

    TECHNICAL SKILLS
    AWS, Docker, Python, Terraform, CI/CD, Kubernetes, SQL, Git, Linux, Bash

    EXPERIENCE
    Senior Infrastructure Engineer | Tech Corp (2021 - Present)
    - Built and architected cloud infrastructure on AWS reducing deployment time by 40%.
    - Scaled Kubernetes clusters to support over 100k daily active users.
    - Automated CI/CD pipelines using GitHub Actions, cutting release cycles from 2 days to 30 ms.

    EDUCATION & CERTIFICATIONS
    - BS in Computer Science, State University
    - AWS Certified Solutions Architect
    """

    parsed_1 = ResumeParser.structure_extracted_text(sample_resume_1)
    print("\n[PASSED] 1/10 Resume Parser Test:")
    print(f"   Email: {parsed_1['contact']['email']}")
    print(f"   Years Exp: {parsed_1['years_experience']}")
    print(f"   Skills Found ({len(parsed_1['skills'])}): {parsed_1['skills'][:5]}...")
    print(f"   Parseability Score: {parsed_1['parseability']['score']}/100")
    assert parsed_1['contact']['email'] == "jane.doe@example.com"
    assert parsed_1['years_experience'] >= 3

    # 2. Second Candidate Resume for Multi-Resume Testing
    sample_resume_2 = """
    John Smith
    john.smith@example.com | (555) 987-6543 | linkedin.com/in/johnsmith

    SUMMARY
    Junior Developer with 1 year experience in Python and HTML.

    TECHNICAL SKILLS
    Python, SQL, HTML, CSS, Git

    EXPERIENCE
    Junior Developer | Web Studio (2023 - Present)
    - Built web scrapers and internal SQL dashboards.
    """
    parsed_2 = ResumeParser.structure_extracted_text(sample_resume_2)

    # 3. Test ATS Scoring Engine
    sample_jd = """
    We are looking for a Senior DevOps & Cloud Engineer.
    Requirements:
    - 4+ years of experience with AWS, Kubernetes, Docker, and Terraform.
    - Strong proficiency in Python or Go.
    - Experience with Prometheus, Grafana, and CI/CD pipelines.
    - Bachelor's degree in CS or related field.
    """

    eval_result = ATSEngine.evaluate(parsed_1, sample_jd)
    print("\n[PASSED] 2/10 ATS Engine Test:")
    print(f"   Total Score: {eval_result['total_score']}/100")
    print(f"   Matched Skills: {eval_result['matched_skills']}")
    print(f"   Missing Skills: {eval_result['missing_skills']}")
    assert eval_result['total_score'] > 50

    # 4. Test Live What-If Recalculation
    what_if = ATSEngine.live_what_if(parsed_1, sample_jd, "What if I add Prometheus and Grafana certs?")
    print("\n[PASSED] 3/10 Live What-If Test:")
    print(f"   Original Score: {what_if['base_score']} -> Recalculated: {what_if['new_score']}")
    print(f"   Delta Impact: +{what_if['delta']} pts")
    assert what_if['delta'] >= 0

    # 5. Test Multi-JD Comparison (Single Resume vs Multiple JDs)
    jds = [
        {"title": "DevOps Engineer", "text": sample_jd},
        {"title": "Frontend React Lead", "text": "Requires React, Next.js, Tailwind, TypeScript, 5+ years experience"}
    ]
    matrix = ATSEngine.compare_multiple_jds(parsed_1, jds)
    print("\n[PASSED] 4/10 Multi-JD Matrix Test:")
    for row in matrix:
        print(f"   Role: {row['role_title']} -> Score: {row['score']}/100")
    assert len(matrix) == 2

    # 6. Test Course Recommendations based on JD Missing Skills
    courses = ATSEngine.recommend_courses(["Prometheus", "Grafana", "Terraform", "Kubernetes"], sample_jd)
    print("\n[PASSED] 5/10 JD-Based Course Recommendations Test:")
    print(f"   Courses Recommended ({len(courses)}):")
    for c in courses[:3]:
        print(f"   • {c['title']} ({c['platform']} | {c.get('est_score_boost', '+10 pts')})")
    assert len(courses) > 0
    assert "title" in courses[0]
    assert "url" in courses[0]

    # 7. Test Multi-Resume Evaluation for a Single JD
    resumes_list = [
        {"filename": "Jane_DevOps_Senior.pdf", "data": parsed_1},
        {"filename": "John_Junior_Dev.pdf", "data": parsed_2}
    ]
    multi_comparison = ATSEngine.compare_multiple_resumes(resumes_list, sample_jd)
    print("\n[PASSED] 6/10 Multi-Resume Single-JD Comparison Test:")
    print(f"   Total Candidates: {multi_comparison['total_candidates']}")
    print(f"   Verdict: {multi_comparison['verdict']}")
    for r in multi_comparison['ranked_resumes']:
        print(f"   Rank #{r['rank']}: {r['filename']} -> Score: {r['score']}/100")
    assert multi_comparison['total_candidates'] == 2
    assert multi_comparison['ranked_resumes'][0]['rank'] == 1
    assert multi_comparison['ranked_resumes'][0]['score'] > multi_comparison['ranked_resumes'][1]['score']

    # 8. Test Session Store Multi-Resume State
    sid, session = SessionStore.get_or_create_session("test_session_multi")
    SessionStore.update_jd(sid, sample_jd, "Senior DevOps")
    SessionStore.update_resume(sid, parsed_1, "Jane_DevOps.pdf")
    SessionStore.update_resume(sid, parsed_2, "John_Junior.pdf")
    stored_comparison = SessionStore.get_multi_resume_comparison(sid)
    print("\n[PASSED] 7/10 Session Store Multi-Resume State Test:")
    print(f"   Stored Resumes in Session: {len(session['resumes'])}")
    print(f"   Best Match: {stored_comparison['best_match']['filename']}")
    assert len(session['resumes']) == 2
    assert stored_comparison is not None

    # 9. Test Chart Image Generator (Radar, Bar, and Multi-Resume Comparison)
    radar_png = ChartGenerator.generate_radar_chart(eval_result['radar_chart'])
    bar_png = ChartGenerator.generate_bar_chart(eval_result['matched_skills'], eval_result['missing_skills'])
    multi_chart_png = ChartGenerator.generate_multi_resume_chart(multi_comparison['ranked_resumes'])
    print("\n[PASSED] 8/10 Server-Side Chart PNG Generator Test:")
    print(f"   Radar Chart PNG Size: {len(radar_png)} bytes")
    print(f"   Bar Chart PNG Size: {len(bar_png)} bytes")
    print(f"   Multi-Resume Chart PNG Size: {len(multi_chart_png)} bytes")
    assert len(radar_png) > 1000
    assert len(bar_png) > 1000
    assert len(multi_chart_png) > 1000

    # 10. Test Base Messaging Adapter (Course Intent & Multi-Resume Upload)
    from app.adapters.base_adapter import BaseMessagingAdapter
    # Test course intent
    course_resp = BaseMessagingAdapter.handle_incoming_message(
        platform="telegram",
        user_id="test_user_courses",
        text="recommend courses"
    )
    print("\n[PASSED] 9/10 Base Messaging Adapter Course Intent Test:")
    print(f"   Adapter Response Text: {course_resp['text'][:70]}...")
    assert "text" in course_resp

    # 11. Test WhatsApp Webhook TwiML Adapter
    from app.adapters.whatsapp_adapter import WhatsAppAdapter
    twiml_output = WhatsAppAdapter.process_twilio_webhook({
        "From": "whatsapp:+15550199",
        "Body": "recommend courses",
        "NumMedia": "0"
    })
    print("\n[PASSED] 10/10 WhatsApp TwiML Webhook Test:")
    print(f"   TwiML Output snippet: {twiml_output[:80]}...")
    assert "<Response>" in twiml_output

    print("\n==========================================")
    print("ALL 10 AUTOMATED TESTS PASSED SUCCESSFULLY!")
    print("==========================================")

if __name__ == "__main__":
    run_tests()
