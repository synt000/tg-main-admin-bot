import sys, os, traceback
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from modules.automation.backup import DatabaseBackupEngine

def run_sprint5_task2_dynamic_summary_runner():
    print("======================================================================")
    print("🧪 [Sprint 5 - Task 2 GREEN Phase]: PostgreSQL Backup Engine Assertions")
    print("======================================================================\n")
    
    mock_db_url = "postgresql://admin:7m1NJ4OnRufr@localhost/tg_saas"
    
    # 🎯 ပြင်ဆင်ချက် ၁: အစ်ကို ညွှန်ကြားထားသည့်အတိုင်း Termux Permission Denial ကျော်လွှားရန် Local Directory သို့ ပြောင်းလဲခြင်း
    mock_storage = os.path.join(os.getcwd(), "backups")
    
    all_tests_passed = True

    # 🧪 TEST 1: pg_dump Command Generation Contract
    try:
        cmd = DatabaseBackupEngine.build_backup_command(mock_db_url, f"{mock_storage}/test.sql")
        assert "pg_dump " in cmd
        assert "-f " in cmd
        print("tests/automation/test_backup.py::test_pg_dump_command                  ✅ PASSED")
    except Exception:
        all_tests_passed = False
        print("❌ TEST 1 (pg_dump Command Builder): FAILED")
        traceback.print_exc()

    # 🧪 TEST 2: Backup Filename Format Contract
    try:
        filename = DatabaseBackupEngine.generate_backup_filename()
        assert filename.startswith("backup_")
        assert filename.endswith(".sql")
        assert len(filename) == 26
        print("tests/automation/test_backup.py::test_backup_filename                  ✅ PASSED")
    except Exception:
        all_tests_passed = False
        print("❌ TEST 2 (Backup Filename Format): FAILED")
        traceback.print_exc()

    # 🧪 TEST 3: Backup Directory Creation Contract (FIXED ENVIRONMENT PATH)
    try:
        dir_ok = DatabaseBackupEngine.ensure_backup_directory(mock_storage)
        assert dir_ok is True
        print("tests/automation/test_backup.py::test_directory_auto_create            ✅ PASSED")
    except Exception:
        all_tests_passed = False
        print("❌ TEST 3 (Backup Directory Creation): FAILED")
        traceback.print_exc()

    # 🧪 TEST 4: Backup Failure Handling Contract (FIXED ENVIRONMENT PATH)
    try:
        res_ok = DatabaseBackupEngine.run_backup(mock_db_url, mock_storage)
        assert res_ok["status"] == "success"
        assert "file" in res_ok
        
        res_fail = DatabaseBackupEngine.run_backup("", mock_storage)
        assert res_fail["status"] == "failed"
        assert "error" in res_fail
        print("tests/automation/test_backup.py::test_backup_failure_recovery          ✅ PASSED")
    except Exception:
        all_tests_passed = False
        print("❌ TEST 4 (Backup Failure Handling Contract): FAILED")
        traceback.print_exc()

    print("\n----------------------------------------------------------------------")
    if all_tests_passed:
        print("🚀 [TDD TASK 2 STATUS]: POSTGRESQL BACKUP ENGINE GREEN WAVE VERIFIED PASS! ⭐⭐⭐⭐⭐")
    else:
        print("❌ [TDD TASK 2 STATUS]: GREEN PHASE FAILED - CORE BOUNDARY DEFICITS UNRESOLVED!")
    print("----------------------------------------------------------------------")

if __name__ == "__main__":
    run_sprint5_task2_dynamic_summary_runner()
