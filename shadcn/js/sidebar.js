// scroll to the active link in the sidebar on page load
const sidebar = document.querySelector('[data-sidebar="content"]');
const activeLinks = sidebar
	? [...sidebar.querySelectorAll('[data-active="true"]')]
	: [];
const activeLink = activeLinks.at(-1);
if (sidebar) {
	const saved = sessionStorage.getItem("sidebar-scroll");
	if (saved !== null) {
		sidebar.scrollTop = parseInt(saved, 10);
	}

	if (activeLink) {
		const sidebarRect = sidebar.getBoundingClientRect();
		const activeRect = activeLink.getBoundingClientRect();
		const isVisible =
			activeRect.top >= sidebarRect.top &&
			activeRect.bottom <= sidebarRect.bottom;

		if (!isVisible) {
			activeLink.scrollIntoView({ block: "nearest" });
		}
	}

	const persistSidebarScroll = () => {
		sessionStorage.setItem("sidebar-scroll", sidebar.scrollTop);
	};

	sidebar.querySelectorAll("a[href]").forEach((link) => {
		link.addEventListener("click", persistSidebarScroll, { capture: true });
	});
	window.addEventListener("pagehide", persistSidebarScroll);
}
