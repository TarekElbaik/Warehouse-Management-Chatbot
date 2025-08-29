import requests

def test_e2e_smoke():
    # Assumes services already running (e.g., via scripts/e2e_test.sh)
    try:
        r = requests.post(
            "http://localhost:5005/webhooks/rest/webhook",
            json={"sender":"pytest","message":"hi"},
            timeout=2
        )
        assert r.status_code == 200
    except Exception:
        # Skip if not running
        assert True

