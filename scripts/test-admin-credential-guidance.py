"""Check that deployment guidance does not prescribe published admin passwords."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HAPROXY = (ROOT / "best-practices/haproxy-best-practices.md").read_text()
GRAFANA = (ROOT / "deploy-monitoring-services.md").read_text()

assert "stats auth admin:pingcap123" not in HAPROXY
assert "bind <management-ip>:8080" in HAPROXY
assert "stats auth <admin-user>:<strong-password>" in HAPROXY
assert "Do not expose the HAProxy Stats page directly to the internet" in HAPROXY
assert "stats admin if TRUE" in HAPROXY
assert "If you only need to view monitoring information" in HAPROXY

assert "admin_password = admin" not in GRAFANA
assert "admin_user = <grafana-admin-user>" in GRAFANA
assert "admin_password = <grafana-strong-password>" in GRAFANA
assert "Do not use `admin` as the password" in GRAFANA
assert "you can choose **Skip**" not in GRAFANA
assert "Do not choose **Skip**" in GRAFANA

print("admin credential guidance checks passed")
