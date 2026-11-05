"""Check that deployment guidance keeps monitoring administration restricted."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HAPROXY = (ROOT / "best-practices/haproxy-best-practices.md").read_text(
    encoding="utf-8"
)
GRAFANA = (ROOT / "deploy-monitoring-services.md").read_text(encoding="utf-8")
FIREWALL = (ROOT / "check-before-deployment.md").read_text(encoding="utf-8")
DEFAULT_ADMIN_PASSWORD = re.compile(
    r"^\s*admin_password\s*=\s*(?:\"{1,3}|'{1,3})?admin"
    r"(?:\"{1,3}|'{1,3})?\s*(?:[;#].*)?$",
    re.IGNORECASE | re.MULTILINE,
)
DEFAULT_ADMIN_PASSWORD_EXAMPLES = (
    "admin_password=admin",
    ' admin_password = "admin"',
    "admin_password = '''admin''' # comment",
)

assert "stats auth admin:pingcap123" not in HAPROXY
assert "bind <management-ip>:8080" in HAPROXY
assert "stats auth <admin-user>:<strong-password>" in HAPROXY
assert "Do not expose the HAProxy Stats page directly to the internet" in HAPROXY
assert not re.search(r"^\s*stats\s+admin\b", HAPROXY, re.MULTILINE)
assert "keeps the Stats page read-only" in HAPROXY

assert all(
    DEFAULT_ADMIN_PASSWORD.search(assignment)
    for assignment in DEFAULT_ADMIN_PASSWORD_EXAMPLES
)
assert not DEFAULT_ADMIN_PASSWORD.search(GRAFANA)
assert "admin_user = <grafana-admin-user>" in GRAFANA
assert 'admin_password = """<grafana-strong-password>"""' in GRAFANA
assert "Do not use `admin` as the password" in GRAFANA
assert "For an existing instance, use its current administrator account" in GRAFANA
assert "you can choose **Skip**" not in GRAFANA
assert "Do not choose **Skip**" in GRAFANA
assert '--web.listen-address="127.0.0.1:9090"' in GRAFANA
assert "--web.enable-admin-api" not in GRAFANA
assert "leaves the Prometheus admin API disabled" in GRAFANA

assert "systemctl stop firewalld" not in FIREWALL
assert "systemctl disable firewalld" not in FIREWALL
assert "--set-default-zone trusted" not in FIREWALL
assert "allow only trusted sources to access the required ports" in FIREWALL

print("admin credential guidance checks passed")
