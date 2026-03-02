// TOC scroll fix: wait for video metadata before scrolling
(function() {
    const SCROLL_OFFSET = 32; // 2rem in pixels

    function getOffsetTop(element) {
        let top = 0;
        while (element) {
            top += element.offsetTop;
            element = element.offsetParent;
        }
        return top;
    }

    function scrollToElement(element, behavior) {
        const top = getOffsetTop(element) - SCROLL_OFFSET;
        window.scrollTo({ top: top, behavior: behavior });
    }

    // Promise that resolves when all video metadata is loaded (or timeout)
    function waitForVideos(timeout) {
        return new Promise(resolve => {
            const videos = document.querySelectorAll('video');
            if (videos.length === 0) return resolve();

            let loaded = 0;
            const total = videos.length;
            const timer = setTimeout(resolve, timeout);

            const checkDone = () => {
                loaded++;
                if (loaded >= total) {
                    clearTimeout(timer);
                    resolve();
                }
            };

            videos.forEach(video => {
                if (video.readyState >= 1) {
                    checkDone();
                } else {
                    video.addEventListener('loadedmetadata', checkDone, { once: true });
                    video.addEventListener('error', checkDone, { once: true });
                }
            });
        });
    }

    // Handle TOC link clicks (works with both static and dynamically generated TOCs)
    document.addEventListener('click', function(e) {
        const link = e.target.closest('.toc-link');
        if (!link) return;

        const href = link.getAttribute('href');
        if (!href || href === '#') return;

        const target = document.querySelector(href);
        if (!target) return;

        e.preventDefault();
        history.pushState(null, '', href);
        scrollToElement(target, 'smooth');
    });

    // Scrollspy: highlight the active TOC link based on scroll position
    (function() {
        const headings = Array.from(document.querySelectorAll('.heading-anchor'));
        if (headings.length === 0) return;

        function setActive(id) {
            document.querySelectorAll('.toc-link').forEach(function(link) {
                const href = link.getAttribute('href');
                const isActive = href === '#' + id || (id === null && href === '#');
                link.classList.toggle('toc-link--active', isActive);
            });
        }

        // Use IntersectionObserver to track which heading is at the top of the viewport
        const visibleHeadings = new Set();

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    visibleHeadings.add(entry.target);
                } else {
                    visibleHeadings.delete(entry.target);
                }
            });

            // Activate the topmost visible heading; if none visible, the last one above viewport
            if (visibleHeadings.size > 0) {
                const topmost = headings.filter(h => visibleHeadings.has(h))[0];
                if (topmost) setActive(topmost.id);
            } else {
                // Find the last heading above the viewport
                const scrollTop = window.scrollY || document.documentElement.scrollTop;
                let active = null;
                headings.forEach(function(h) {
                    if (getOffsetTop(h) - SCROLL_OFFSET <= scrollTop + 1) active = h;
                });
                setActive(active ? active.id : null);
            }
        }, { rootMargin: '-32px 0px -60% 0px', threshold: 0 });

        headings.forEach(function(h) { observer.observe(h); });
    })();

    // Handle initial page load with hash in URL
    if (window.location.hash) {
        const target = document.querySelector(window.location.hash);
        if (target) {
            // Wait for video metadata, then wait for layout, then scroll
            waitForVideos(3000).then(() => {
                // Double RAF ensures layout is fully complete
                requestAnimationFrame(() => {
                    requestAnimationFrame(() => {
                        scrollToElement(target, 'instant');
                    });
                });
            });
        }
    }
})();
