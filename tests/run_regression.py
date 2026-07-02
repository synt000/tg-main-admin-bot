import os
import subprocess
import sys

def execute_comprehensive_regression():
    print("======================================================================")
    print("🧪 [Phase 3 — Grand Regression Active]: Commencing Sprint 1-5 Final Audit...")
    print("======================================================================\n")
    
    # 🎯 Step 2 Registry Mappings: Structured checklist sequences paths executions
    test_scripts = [
        "tests/dashboard/test_analytics.py",
        "tests/automation/test_notifications.py",
        "tests/automation/test_backup.py",
        "tests/automation/test_cron_jobs.py"
    ]
    
    all_passed = True
    
    for script in test_scripts:
        print(f"🔄 Executing Security Boundaries Audit: {script} ...")
        # Execute sub-processes natively and match explicitly against the environment parameters
        res = subprocess.run([sys.executable, script], env=dict(os.environ, PYTHONPATH="."))
        
        # 🚀 🔒 [FIX APPLIED]: return_code အစား Python standard Property အမှန်ဖြစ်သော returncode သို့ ပြောင်းလဲခြင်း
        if res.returncode != 0:
            all_passed = False
            print(f"❌ REGRESSION BREACH DETECTED AT: {script}\n")
        else:
            print(f"✅ MODULE CONTRACT SAFE: {script} passed integration validations.\n")
            
    print("----------------------------------------------------------------------")
    if all_passed:
        print("🚀 [REGRESSION RESULTS]: ALL SPRINT 1-5 MATRIX TESTS VERIFIED PASS! ⭐⭐⭐⭐⭐")
        print("🎉 STATUS: BUSINESSOS CORE v1.2.0 IS STABLE AND READY FOR RC RELEASE CANDIDATE!")
    else:
        print("❌ [REGRESSION FAILURE]: CORE DEFICITS CAPTURED! RELEASE CANDIDATE REJECTED!")
    print("----------------------------------------------------------------------")

if __name__ == "__main__":
    execute_comprehensive_regression()
