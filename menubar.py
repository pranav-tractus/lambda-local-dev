import webbrowser
import requests
import rumps

API_BASE = "http://localhost:9000"


def fetch_services():
    try:
        return requests.get(f"{API_BASE}/api/services", timeout=2).json()
    except Exception:
        return []


class DevOrchestratorApp(rumps.App):
    def __init__(self):
        super().__init__("⚡", quit_button=None)
        self.menu = []
        self._service_items: dict[str, rumps.MenuItem] = {}
        self._rebuild_menu(fetch_services())

    def _rebuild_menu(self, services: list[dict]) -> None:
        self.menu.clear()
        self._service_items.clear()

        for svc in services:
            label = self._label(svc)
            item = rumps.MenuItem(label, callback=self._toggle(svc["name"]))
            self._service_items[svc["name"]] = item
            self.menu.add(item)

        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("Start All", callback=self._start_all))
        self.menu.add(rumps.MenuItem("Stop All", callback=self._stop_all))
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("Open Dashboard", callback=self._open_dashboard))
        self.menu.add(rumps.MenuItem("Quit", callback=rumps.quit_application))

    def _label(self, svc: dict) -> str:
        prefix = "✓" if svc["status"] == "running" else "○"
        return f"{prefix} {svc['name']}"

    def _toggle(self, name: str):
        def handler(_):
            services = fetch_services()
            svc = next((s for s in services if s["name"] == name), None)
            if not svc:
                return
            endpoint = "stop" if svc["status"] == "running" else "start"
            try:
                requests.post(f"{API_BASE}/api/services/{name}/{endpoint}", timeout=5)
            except Exception:
                pass
        return handler

    def _start_all(self, _):
        for svc in fetch_services():
            try:
                requests.post(f"{API_BASE}/api/services/{svc['name']}/start", timeout=5)
            except Exception:
                pass

    def _stop_all(self, _):
        for svc in fetch_services():
            try:
                requests.post(f"{API_BASE}/api/services/{svc['name']}/stop", timeout=5)
            except Exception:
                pass

    def _open_dashboard(self, _):
        webbrowser.open("http://localhost:9000")

    @rumps.timer(5)
    def refresh(self, _):
        services = fetch_services()
        if not services:
            return
        # update labels in place (avoid full menu rebuild on every tick)
        for svc in services:
            name = svc["name"]
            if name in self._service_items:
                self._service_items[name].title = self._label(svc)
            else:
                # new service appeared — rebuild
                self._rebuild_menu(services)
                return


if __name__ == "__main__":
    DevOrchestratorApp().run()
